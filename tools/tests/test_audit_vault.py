"""Maintenance-tool tests; fixtures are created outside the learning vault."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).resolve().parents[1] / "audit_vault.py"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TOOL.is_file(), "The read-only audit tool has not been implemented yet")
        spec = importlib.util.spec_from_file_location("audit_vault", TOOL)
        self.audit = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = self.audit
        spec.loader.exec_module(self.audit)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_audit(self, **options):
        return self.audit.audit(self.root, self.audit.DEFAULT_CONFIG, **options)

    def test_skips_fenced_inline_indented_and_commented_examples(self):
        text = """```bash
[[missing1]]
```
> ```sh
> [[missing2]]
> ```
`if [[ n -eq 42 ]]; then`
    sed '[[:space:]]'
<!-- [[missing3]] -->
%% [[missing4]] %%
[[real]]
"""
        self.assertEqual([x["target"] for x in self.audit.extract_links(text)], ["real"])

    def test_resolves_dot_in_note_name_and_global_code_embed(self):
        self.put("README.md", "[[1. 命题逻辑]]\n![[Hailstone sequence.cpp]]")
        self.put("Math/1. 命题逻辑.md")
        self.put("CS/Code/Hailstone sequence.cpp", "int main() {}")
        self.assertEqual(self.run_audit()["link_issues"], [])

    def test_ampersand_in_code_filename_is_not_an_unterminated_html_entity(self):
        self.put("README.md", "![[Max2-recursion&divide-conquer.cpp]]\n[code](Code/Max2-recursion&divide-conquer.cpp)")
        self.put("Code/Max2-recursion&divide-conquer.cpp", "int main() {}")
        self.assertEqual(self.run_audit()["link_issues"], [])

    def test_git_output_preserves_leading_status_space(self):
        from unittest.mock import patch
        raw = subprocess.CompletedProcess([], 0, b" M note.md\0", b"")
        with patch.object(self.audit.subprocess, "run", return_value=raw):
            self.assertEqual(self.audit._git(self.root, "status")[1], " M note.md\0")

    def test_decodes_relative_spaces_and_balanced_parentheses(self):
        self.put("README.md", "[note](<CS/a b.md>)\n[pdf](Math/test%20(1).pdf)")
        self.put("CS/a b.md")
        self.put("Math/test (1).pdf")
        self.assertEqual(self.run_audit()["link_issues"], [])

    def test_detects_missing_target_with_source_line(self):
        self.put("README.md", "# Home\n\n[missing](missing.md)")
        issue = self.run_audit()["link_issues"][0]
        self.assertEqual((issue["issue"], issue["source"], issue["line"]), ("missing", "README.md", 3))

    def test_warns_ambiguous_wiki_target(self):
        self.put("README.md", "[[Note]]")
        self.put("A/Note.md")
        self.put("B/Note.md")
        self.assertEqual(self.run_audit()["link_issues"][0]["issue"], "ambiguous")

    def test_reports_case_difference_on_every_platform(self):
        self.put("README.md", "[note](notes/example.md)")
        self.put("Notes/Example.md")
        self.assertEqual(self.run_audit()["link_issues"][0]["issue"], "case_mismatch")

    def test_detects_link_outside_vault(self):
        self.put("README.md", "[outside](../outside.md)")
        self.assertEqual(self.run_audit()["link_issues"][0]["issue"], "outside_vault")

    def test_ignores_external_and_same_note_anchors(self):
        self.put("README.md", "[web](https://example.com/x)\n[[#Heading]]\n[local](#heading)")
        self.assertEqual(self.run_audit()["link_issues"], [])

    def test_recognizes_reference_links_and_html_attachments(self):
        self.put("README.md", '[item][target]\n[target]: notes.md\n<img src="image.png">')
        self.put("notes.md")
        self.put("image.png")
        self.assertEqual(self.run_audit()["link_issues"], [])

    def test_paper_and_heavy_directories_are_not_parsed(self):
        self.put("README.md", "[paper](Paper/note.md)")
        self.put("Paper/note.md", "[[missing]]")
        self.put("AI/data/bad.md", "[[missing]]")
        self.put("AI/.venv/bad.md", "[[missing]]")
        report = self.run_audit()
        self.assertEqual(report["summary"]["markdown_files"], 1)
        self.assertEqual(report["link_issues"], [])
        self.assertIn("Paper", report["skipped_directories"])

    def test_custom_root_cannot_enter_protected_paper(self):
        protected = self.put("Paper/experiment/note.md", "[[missing]]").parent
        with self.assertRaisesRegex(ValueError, "protected"):
            self.audit.audit(protected, self.audit.DEFAULT_CONFIG)

    def test_root_with_reparse_ancestor_is_rejected_before_scanning(self):
        from unittest.mock import patch
        portal = self.root / "portal"
        child = self.put("portal/child/note.md").parent
        with patch.object(self.audit, "_special", side_effect=lambda p: Path(p) == portal):
            with self.assertRaisesRegex(ValueError, "[Rr]eparse"):
                self.audit.audit(child, self.audit.DEFAULT_CONFIG)

    def test_protected_folder_link_is_outside_verified_scope(self):
        self.put("README.md", "[paper](Paper/existing/)")
        self.put("Paper/existing/note.md")
        result = self.run_audit()
        self.assertEqual(len(result["excluded_links"]), 1)
        self.assertEqual(result["link_issues"], [])

    def test_target_with_reparse_ancestor_is_not_followed(self):
        from unittest.mock import patch
        portal = self.root / "portal"
        link = {"kind": "markdown", "target": "portal/file.md", "line": 1}
        with patch.object(self.audit, "_special", side_effect=lambda p: Path(p) == portal):
            with patch.object(Path, "is_dir", return_value=False) as directory_check:
                with patch.object(Path, "exists", return_value=False) as existence_check:
                    state, _ = self.audit._resolve(self.root, "README.md", link, {}, {}, {}, self.audit.DEFAULT_CONFIG)
                    self.assertEqual(state, "excluded_target")
                    directory_check.assert_not_called()
                    existence_check.assert_not_called()

    def test_reachable_folder_entry_is_not_an_orphan(self):
        self.put("README.md", "[homework](Math/Homework/)")
        self.put("Math/Homework/problem.md")
        self.put("lonely.md")
        self.assertEqual(self.run_audit()["navigation_candidates"], ["lonely.md"])

    def test_frontmatter_checks_new_concepts_only_and_accepts_legacy_type(self):
        self.put("README.md")
        self.put("old.md")
        self.put("Concepts/good.md", "---\ntitle: Good\ntype: concept\n---\n")
        self.put("Concepts/bad.md", "# Missing metadata")
        issues = self.run_audit()["frontmatter_candidates"]
        self.assertEqual([x["source"] for x in issues], ["Concepts/bad.md"])

    def test_duplicates_require_explicit_hash_option(self):
        self.put("a.md", "same")
        self.put("b.md", "same")
        self.assertEqual(self.run_audit()["duplicate_groups"], [])
        self.assertEqual(self.run_audit(hash_duplicates=True)["duplicate_groups"], [["a.md", "b.md"]])

    def test_audit_does_not_change_files_or_create_reports(self):
        self.put("README.md", "[[missing]]")
        self.put("Paper/experiment/config.json", '{"keep": true}')
        before = {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob("*") if p.is_file()}
        self.run_audit()
        after = {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_git_snapshot_separates_untracked_files_and_never_fetches(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.put("new.md")
        result = self.audit.git_snapshot(self.root)
        self.assertEqual(result["untracked"], 1)
        self.assertFalse(result["remote_verified"])
        self.assertFalse((self.root / ".git/FETCH_HEAD").exists())

    def test_cli_is_read_only_and_outputs_json(self):
        self.put("README.md", "# Home")
        result = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.root), "--json"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["summary"]["markdown_files"], 1)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["README.md"])


if __name__ == "__main__":
    unittest.main()
