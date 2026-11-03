#!/usr/bin/env python3
"""Read-only, bounded learning-vault checks. Python standard library only."""
import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit


DEFAULT_CONFIG = {
    "protected_prefixes": ["Paper"],
    "skip_names": [".git", ".obsidian", ".vscode", ".agents", ".agent-review",
                   ".claude", ".claudian", ".codex", ".word-memo", ".venv", "venv",
                   "node_modules", "__pycache__", "__MACOSX", ".pytest_cache",
                   "data", "datasets", "checkpoints", "checkpoints-meta", "weights",
                   "results", "server_resume"],
    "max_markdown_bytes": 2 * 1024 * 1024,
    "large_file_bytes": 50 * 1024 * 1024,
    "duplicate_max_bytes": 2 * 1024 * 1024,
    "frontmatter_roots": ["Concepts"],
    "frontmatter_fields": ["title", "note_type"],
    "navigation_roots": ["README.md", "学习导航.md"],
    "inbox_days": 30,
}


def _beneath(path, prefix):
    return path == prefix or path.startswith(prefix.rstrip("/") + "/")


def _special(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) &
                                   getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 1024))


def _has_reparse_ancestor(path):
    # Walk from the drive down: never inspect a child through a directory link.
    for ancestor in [*reversed(path.parents), path]:
        try:
            if _special(ancestor):
                return True
        except FileNotFoundError:
            break
    return False


def _protected_root(path, config):
    parts = [part.casefold() for part in path.parts]
    for prefix in config["protected_prefixes"]:
        protected = [part.casefold() for part in Path(prefix).parts]
        if any(parts[start:start + len(protected)] == protected
               for start in range(len(parts) - len(protected) + 1)):
            return True
    return False


def _excluded_target(root, path, config):
    relative = path.relative_to(root)
    return (any(_beneath(relative.as_posix().casefold(), prefix.casefold())
                for prefix in config["protected_prefixes"]) or
            any(part.casefold() in {name.casefold() for name in config["skip_names"]}
                for part in relative.parts) or _has_reparse_ancestor(path))


def _inventory(root, config):
    files, skipped, errors, repos = {}, [], [], [root] if (root / ".git").exists() else []
    def onerror(error):
        errors.append(str(error))
    for current, dirs, names in os.walk(root, topdown=True, followlinks=False, onerror=onerror):
        folder = Path(current)
        if folder != root and (folder / ".git").exists():
            repos.append(folder)
        kept = []
        for name in sorted(dirs):
            path = folder / name
            rel = path.relative_to(root).as_posix()
            try:
                exclude = (name.casefold() in {n.casefold() for n in config["skip_names"]} or name.startswith("._") or
                           any(_beneath(rel.casefold(), p.casefold()) for p in config["protected_prefixes"]) or _special(path))
                if exclude:
                    skipped.append(rel)
                else:
                    kept.append(name)
            except OSError as error:
                errors.append(f"{rel}: {error}")
        dirs[:] = kept
        for name in sorted(names):
            path = folder / name
            rel = path.relative_to(root).as_posix()
            try:
                if name.startswith("._") or name == ".DS_Store" or _special(path):
                    continue
                files[rel] = path.stat()
            except OSError as error:
                errors.append(f"{rel}: {error}")
    return files, sorted(skipped), errors, repos


def _mask_code(text):
    # Preserve newlines so every finding points back to the original source line.
    mask = lambda match: re.sub(r"[^\n]", " ", match.group())
    text = re.sub(r"<!--[\s\S]*?-->|%%[\s\S]*?%%", mask, text)
    output, fence = [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(?:>\s*)*(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            output.append(re.sub(r"[^\n]", " ", line))
        elif fence or line.startswith(("    ", "\t")):
            output.append(re.sub(r"[^\n]", " ", line))
        else:
            output.append(line)
    return re.sub(r"(`+)([^`\n]*?)\1", mask, "".join(output))


def extract_links(text):
    """Extract common wiki, inline/reference Markdown and HTML local targets."""
    clean, found = _mask_code(text), []
    def add(kind, target, offset):
        value = target.strip()
        value = (html.unescape(value) if kind == "html" else
                 re.sub(r"&(?:#[0-9]+|#x[0-9a-fA-F]+|[A-Za-z][A-Za-z0-9]+);", lambda m: html.unescape(m.group()), value))
        found.append({"kind": kind, "target": value,
                      "line": clean.count("\n", 0, offset) + 1})
    for match in re.finditer(r"(?<!\\)\[\[([^\]\n]+)\]\]", clean):
        add("wiki", match.group(1).split("|", 1)[0].removesuffix("\\"), match.start())
    for match in re.finditer(r"(?<!\\)\[[^\]\n]*\]\(", clean):
        start, position, depth, angle = match.end(), match.end(), 1, False
        while position < len(clean) and depth:
            char = clean[position]
            if char == "\\":
                position += 2
                continue
            if char == "<" and position == start:
                angle = True
            elif char == ">" and angle:
                angle = False
            elif not angle:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
            position += 1
        if depth == 0:
            value = clean[start:position - 1].strip()
            if value.startswith("<") and ">" in value:
                value = value[1:value.index(">")]
            else:
                value = re.sub(r'\s+[\"\'][^\n]*[\"\']\s*$', "", value)
            add("markdown", value, match.start())
    for match in re.finditer(r"(?m)^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)", clean):
        add("reference", match.group(1).strip("<>"), match.start())
    for match in re.finditer(r"<(?:img|a|audio|video|source)\b[^>]*?\b(?:src|href)=[\"']([^\"']+)[\"']", clean, re.I):
        add("html", match.group(1), match.start())
    return sorted(found, key=lambda item: item["line"])


def _resolve(root, source, link, files, folded, basenames, config):
    target = re.sub(r"\\([ ()\[\]#])", r"\1", link["target"])
    if not target or target.startswith("#") or urlsplit(target).scheme or target.startswith("//"):
        return "external_or_anchor", []
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return "external_or_anchor", []
    candidates = []
    bases = [root / Path(source).parent, root] if link["kind"] == "wiki" else [root / Path(source).parent]
    if target.startswith("/"):
        bases = [root]
        target = target.lstrip("/")
    for base in bases:
        path = Path(os.path.abspath(base / target))
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            return "outside_vault", []
        if _excluded_target(root, path, config):
            return "excluded_target", [rel]
        options = [rel] + ([rel + ".md"] if link["kind"] == "wiki" and not rel.endswith(".md") else [])
        for option in options:
            if option in files:
                return "ok", [option]
        candidates.extend(options)
        if path.is_dir():
            return "folder", [rel]
    if link["kind"] == "wiki":
        options = [target] + ([target + ".md"] if not target.endswith(".md") else [])
        matches = sorted({p for option in options for p in basenames.get(option, [])})
        if not matches and "/" in target:
            matches = sorted(p for p in files if any(p.endswith("/" + option) for option in options))
        if len(matches) == 1:
            return "ok", matches
        if len(matches) > 1:
            return "ambiguous", matches
    case_matches = sorted({p for candidate in candidates for p in folded.get(candidate.casefold(), [])})
    if case_matches:
        return "case_mismatch", case_matches
    # Files inside deliberately excluded directories are outside this audit's scope.
    for candidate in candidates:
        path = root / candidate
        if _excluded_target(root, path, config):
            return "excluded_target", [candidate]
        if path.exists():
            return "excluded_target", [candidate]
    return "missing", []


def _git(root, *args):
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false", *args],
                                cwd=root, capture_output=True, timeout=20)
        return result.returncode, result.stdout.decode("utf-8", "replace").rstrip("\r\n"), result.stderr.decode("utf-8", "replace").strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        return -1, "", str(error)


def git_snapshot(root, check_remote=False):
    code, top, error = _git(root, "rev-parse", "--show-toplevel")
    if code or Path(top).resolve() != root.resolve():
        return {"path": str(root), "available": False, "remote_verified": False,
                "error": error or "Not the root of an independent Git worktree"}
    code, status, error = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if code:
        return {"path": str(root), "available": True, "remote_verified": False, "error": error}
    records, index = status.split("\0"), 0
    counts = Counter()
    while index < len(records):
        record = records[index]
        index += 1
        if len(record) < 3:
            continue
        flag = record[:2]
        if flag == "??":
            counts["untracked"] += 1
        else:
            counts["staged"] += flag[0] != " "
            counts["unstaged"] += flag[1] != " "
            if "R" in flag or "C" in flag:
                index += 1
    branch = _git(root, "branch", "--show-current")[1]
    head = _git(root, "rev-parse", "--verify", "HEAD")[1]
    upstream_code, upstream, _ = _git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    result = {"path": str(root), "available": True, "branch": branch, "head": head if len(head) == 40 else None,
              "staged": counts["staged"], "unstaged": counts["unstaged"], "untracked": counts["untracked"],
              "remote_verified": False, "upstream": upstream if upstream_code == 0 else None,
              "upstream_comparison": "local cached references only"}
    if upstream_code == 0:
        code, difference, _ = _git(root, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        if code == 0:
            result["ahead"], result["behind"] = map(int, difference.split())
    if check_remote:
        code, remote, error = _git(root, "ls-remote", "--symref", "origin", "HEAD")
        result["remote_verified"] = code == 0 and bool(remote)
        result["remote_head"] = next((line.split()[0] for line in remote.splitlines()
                                     if line.endswith("\tHEAD") and not line.startswith("ref:")), None)
        if code:
            result["remote_error"] = error
    return result


def audit(root, config, *, hash_duplicates=False, check_remote=False):
    root = Path(os.path.abspath(root))
    if _protected_root(root, config):
        raise ValueError(f"Cannot scan a protected directory or its descendants: {root}")
    if _has_reparse_ancestor(root):
        raise ValueError(f"Reparse points are outside the audit scope: {root}")
    if not root.is_dir():
        raise ValueError(f"Vault directory does not exist: {root}")
    files, skipped, errors, repos = _inventory(root, config)
    folded, basenames = defaultdict(list), defaultdict(list)
    for path in files:
        folded[path.casefold()].append(path)
        basenames[Path(path).name].append(path)
    notes = sorted(p for p, info in files.items() if p.lower().endswith(".md") and
                   info.st_size <= config["max_markdown_bytes"])
    issues, frontmatter, graph, folder_edges = [], [], defaultdict(set), defaultdict(set)
    link_counts, excluded_links, progress_mentions = Counter(), [], []
    for source in notes:
        try:
            text = (root / source).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as error:
            errors.append(f"{source}: {error}")
            continue
        if any(_beneath(source, prefix) for prefix in config["frontmatter_roots"]):
            match = re.match(r"\A---\s*\n([\s\S]*?)\n---(?:\s*\n|$)", text)
            keys = set(re.findall(r"(?m)^([\w-]+):", match.group(1))) if match else set()
            if "type" in keys:
                keys.add("note_type")
            missing = [field for field in config["frontmatter_fields"] if field not in keys]
            if missing:
                frontmatter.append({"source": source, "missing": missing})
        for link in extract_links(text):
            link_counts[link["kind"]] += 1
            issue, matches = _resolve(root, source, link, files, folded, basenames, config)
            if issue == "ok" and matches[0] in notes:
                graph[source].add(matches[0])
            elif issue == "folder":
                folder_edges[source].add(matches[0])
            elif issue == "excluded_target":
                excluded_links.append({"source": source, **link})
            elif issue not in {"ok", "external_or_anchor"}:
                issues.append({"source": source, **link, "issue": issue, "candidates": matches})
        if Path(source).name.lower() == "readme.md":
            for number, line in enumerate(text.splitlines(), 1):
                if re.search(r"已学完|已完成|暂缓|尚未学完|仅学习", line):
                    progress_mentions.append({"source": source, "line": number, "text": line.strip()})
    reachable, queue = set(), deque(p for p in config["navigation_roots"] if p in notes)
    while queue:
        source = queue.popleft()
        if source in reachable:
            continue
        reachable.add(source)
        queue.extend(graph[source] - reachable)
        for folder in folder_edges[source]:
            queue.extend(p for p in notes if _beneath(p, folder) and p not in reachable)
    duplicates = []
    if hash_duplicates:
        groups = defaultdict(list)
        for path, info in files.items():
            if 0 < info.st_size <= config["duplicate_max_bytes"] and Path(path).suffix.lower() in {".md", ".pdf"}:
                groups[(Path(path).suffix.lower(), info.st_size)].append(path)
        for paths in groups.values():
            if len(paths) < 2:
                continue
            hashes = defaultdict(list)
            for path in paths:
                try:
                    hashes[hashlib.sha256((root / path).read_bytes()).hexdigest()].append(path)
                except OSError as error:
                    errors.append(f"{path}: {error}")
            duplicates.extend(sorted(group) for group in hashes.values() if len(group) > 1)
    now = datetime.now(timezone.utc).timestamp()
    return {
        "root": str(root), "checked_at": datetime.now(timezone.utc).isoformat(), "read_only": True,
        "summary": {"files": len(files), "bytes": sum(i.st_size for i in files.values()),
                    "markdown_files": len(notes), "types": dict(Counter(Path(p).suffix.lower() or "[none]" for p in files)),
                    "links": dict(link_counts)},
        "protected_prefixes": config["protected_prefixes"], "skipped_directories": skipped,
        "read_errors": errors, "link_issues": issues, "excluded_links": excluded_links,
        "navigation_candidates": sorted(set(notes) - reachable - {"AGENTS.md"}),
        "frontmatter_candidates": frontmatter,
        "large_files": [{"path": p, "bytes": info.st_size} for p, info in files.items()
                        if info.st_size >= config["large_file_bytes"]],
        "duplicate_groups": sorted(duplicates), "duplicate_hashing_enabled": hash_duplicates,
        "stale_inbox": sorted(p for p, info in files.items() if _beneath(p, "Inbox") and
                              Path(p).name != "README.md" and now - info.st_mtime > config["inbox_days"] * 86400),
        "recent_files": sorted(files, key=lambda p: files[p].st_mtime, reverse=True)[:20],
        "progress_mentions": progress_mentions,
        "git": [git_snapshot(repo, check_remote=check_remote) for repo in repos],
        "limitations": ["Static local-target checks only; anchors and remote web pages are not validated.",
                        "Navigation candidates and progress mentions are advisory; no learning state is inferred.",
                        "Protected Paper content, skipped folders and oversized Markdown are outside the content scan."],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout; no report file is created")
    parser.add_argument("--hash-duplicates", action="store_true", help="Hash same-size Markdown/PDF up to 2 MiB")
    parser.add_argument("--check-remote", action="store_true", help="Read live origin HEAD with ls-remote; never fetch")
    parser.add_argument("--strict", action="store_true", help="Nonzero exit for read errors or definite path issues")
    args = parser.parse_args(argv)
    try:
        report = audit(args.root, DEFAULT_CONFIG, hash_duplicates=args.hash_duplicates, check_remote=args.check_remote)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Audit failed: {error}\n")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"只读检查：{report['root']}")
        print(f"范围内文件 {report['summary']['files']}，Markdown {report['summary']['markdown_files']}")
        print("Paper 全部排除；跳过环境、数据、权重和个人配置；不创建报告或修改 Git 引用。")
        print(f"链接候选 {len(report['link_issues'])}；导航候选 {len(report['navigation_candidates'])}；读取错误 {len(report['read_errors'])}")
        for issue in report["link_issues"][:20]:
            print(f"  {issue['source']}:{issue['line']} [{issue['issue']}] {issue['target']}")
        for repo in report["git"]:
            print(f"Git {repo['path']}: {json.dumps(repo, ensure_ascii=False)}")
        print("详细结果：添加 --json；导航候选不是错误，完成状态不会自动推断或改写。")
    definite = {"missing", "case_mismatch", "outside_vault"}
    return int(args.strict and (bool(report["read_errors"]) or any(i["issue"] in definite for i in report["link_issues"])))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
