# Obsidian 插件同步清单

> 记录时间：2026-09-11
>
> 来源 vault：`D:\\Learning\\CS Learning`
>
> 当前插件数量：16 个

## 使用说明

这份清单记录当前 vault 中实际安装并启用的插件。Obsidian 社区插件本质上按 vault 保存，不存在官方意义上的“全局插件目录”。迁移到另一台电脑时，需要把插件目录复制到目标 vault 的 `.obsidian/plugins`，再复制启用清单。

官方说明：[Obsidian 社区插件](https://obsidian.md/help/community-plugins)

## 插件列表

| 插件 ID | 名称 | 版本 | 用途与基本用法 | 官方文档 |
|---|---|---:|---|---|
| `calendar` | Calendar | 1.5.10 | 打开日历视图，点击日期创建或打开每日笔记。建议配合核心插件 Daily notes。 | [GitHub](https://github.com/liamcain/obsidian-calendar-plugin) |
| `dataview` | Dataview | 0.5.68 | 用 `dataview` 或 `dataviewjs` 查询文件、标签、属性和任务，生成动态表格。 | [文档](https://blacksmithgu.github.io/obsidian-dataview/) |
| `editing-toolbar` | Editing Toolbar | 4.1.3 | 提供顶部编辑工具栏，可快速执行标题、粗体、列表、表格、公式和文本处理命令。 | [GitHub](https://github.com/cumany/obsidian-editing-toolbar) |
| `obsidian-excalidraw-plugin` | Excalidraw | 2.27.3 | 创建手绘图、流程图和思维导图；`.excalidraw` 文件可以直接嵌入笔记。 | [GitHub](https://github.com/zsviczian/obsidian-excalidraw-plugin) |
| `excalidraw-extras` | Excalidraw Extras | 0.1.0 | Excalidraw 的伴侣插件，为 LaTeX、Mermaid 转图和 PDF 导出提供额外组件。 | [社区页面](https://community.obsidian.md/plugins/excalidraw-extras) |
| `obsidian-git` | Git | 2.39.0 | 对 vault 进行 Git 提交、备份、拉取和推送；首次使用需要配置 Git 仓库和自动备份策略。 | [GitHub](https://github.com/Vinzent03/obsidian-git) |
| `obsidian-icon-folder` | Iconize | 2.14.7 | 为文件夹、文件和笔记内容添加图标；可通过右键菜单或命令面板操作。 | [GitHub](https://github.com/FlorianWoelki/obsidian-icon-folder) |
| `obsidian-kanban` | Kanban | 2.0.51 | 创建 Markdown 看板，拖动卡片管理任务；看板内容仍保存在 Markdown 文件中。 | [文档](https://publish.obsidian.md/kanban/Obsidian+Kanban+Plugin) |
| `obsidian-style-settings` | Style Settings | 1.0.9 | 调整主题和插件暴露的 CSS 变量；可用选项取决于当前主题和插件。 | [GitHub](https://github.com/mgmeyers/obsidian-style-settings) |
| `obsidian-tasks-plugin` | Tasks | 8.4.0 | 管理截止日期、优先级、重复任务和完成日期，并用 Tasks 查询块汇总任务。 | [文档](https://publish.obsidian.md/tasks/) |
| `omnisearch` | Omnisearch | 1.31.0 | 提供全文搜索。当前 PDF、Office 和图片索引默认关闭，可按需开启。 | [GitHub](https://github.com/scambier/obsidian-omnisearch) |
| `quickadd` | QuickAdd | 2.25.0 | 配置 Choice、Capture、Template 和 Macro，通过命令面板快速创建笔记和执行自动化。当前 Choices 为空，需要重新配置。 | [文档](https://quickadd.obsidian.guide/docs/) |
| `realclaudian` | Claudian | 2.2.6 | 在 Obsidian 侧栏中使用 Coding Agent，支持文件读取、搜索、编辑、命令和多步工作流。当前已改为 Codex。 | [GitHub](https://github.com/YishenTu/claudian) |
| `remotely-save` | Remotely Save | 0.5.25 | 将笔记同步到远程存储服务。每台电脑、每个 vault 都应单独配置凭据。 | [GitHub](https://github.com/remotely-save/remotely-save) |
| `table-editor-obsidian` | Advanced Tables | 0.23.2 | 编辑 Markdown 表格时使用 Tab 移动单元格、Enter 创建新行，并自动调整表格格式。 | [GitHub](https://github.com/tgrosinger/advanced-tables-obsidian) |
| `templater-obsidian` | Templater | 2.25.0 | 使用模板变量和脚本自动生成笔记标题、日期、属性和内容。 | [文档](https://silentvoid13.github.io/Templater/) |

## 常用示例

### Dataview

````markdown
```dataview
TABLE file.mtime AS "修改时间"
FROM ""
SORT file.mtime DESC
LIMIT 20
```
````

### Tasks

```markdown
- [ ] 复习 Transformer 📅 2026-09-12 ⏫
```

### Templater

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
---
```

## 前置依赖检查

| 依赖项 | 类型 | 状态 | 说明 |
|---|---|---|---|
| Daily notes | Obsidian 核心插件 | 已满足 | Calendar 使用它来创建和打开每日笔记。 |
| Templates | Obsidian 核心插件 | 已满足 | Templater 和部分模板工作流可以配合它使用。 |
| Dataview | 社区插件 | 已安装 | ExcalidrawAutomate 的 Dataview 集成可直接使用。 |
| Templater | 社区插件 | 已安装 | QuickAdd、ExcalidrawAutomate 的高级模板/脚本集成可直接使用。 |
| QuickAdd | 社区插件 | 已安装 | ExcalidrawAutomate 的脚本工作流集成可直接使用。 |
| Excalidraw Extras | 社区伴侣插件 | 已补全 | Excalidraw 的 LaTeX、Mermaid 和 PDF 导出等高级功能需要；版本 0.1.0。 |
| Git for Windows | 外部程序 | 已满足 | Git 插件检测到 `git version 2.45.1.windows.1`。仍需在目标 vault 中初始化或连接 Git 仓库。 |
| Codex CLI | 外部程序 | 已满足 | Claudian 检测到 `codex-cli 0.153.4`；另一台电脑需要重新安装并登录。 |
| Remotely Save 远程服务 | 外部服务 | 待配置 | 不是插件依赖；每台电脑需要单独填写远程服务和凭据。 |

说明：除 Excalidraw Extras 外，没有发现必须额外安装的社区插件。QuickAdd、Templater、Dataview 和 Excalidraw 之间的关系主要是可选集成，不是启动依赖。

## Claudian → Codex 配置

本 vault 已创建：`.claudian/claudian-settings.json`

```json
{
  "settingsProvider": "codex",
  "permissionMode": "yolo",
  "model": "gpt-5.6-luna",
  "effortLevel": "high",
  "providerConfigs": {
    "codex": {
      "enabled": true,
      "safeMode": "workspace-write",
      "cliPath": ""
    },
    "claude": {
      "enabled": false
    }
  },
  "lastSelectedChatModel": null,
  "savedProviderModel": {
    "codex": "gpt-5.6-luna"
  }
}
```

Claudian 的默认提供商已经从 Claude 改为 Codex，并关闭 Claude 回退。当前 vault 的活动标签页已绑定 `draftModel: "gpt-5.6-luna"`；本机配置另外指向 Windows 原生 `codex.exe`，没有使用 npm 的 `.ps1/.cmd` wrapper。另一台电脑还需要：

1. 安装 Obsidian 桌面版。
2. 安装 Codex CLI，并确保 `codex` 可以在终端运行。
3. 登录 Codex CLI：`codex login`。
4. 把本文件中的 Claudian 配置复制到目标 vault 的 `.claudian/claudian-settings.json`；如果 Codex 不在 GUI 的 PATH 中，在 Claudian 的 Codex 设置里填写该电脑的原生 `codex.exe` 路径。
5. 重启 Obsidian，然后在 `设置 → Claudian → Providers → Codex` 检查 Codex 是否启用。

Claudian 使用 Codex CLI，而不是直接调用本网页 ChatGPT 会话。Codex CLI 的模型和登录状态由本机 Codex 配置决定。

## 迁移方法一：复制插件文件

在 Windows PowerShell 中，将下面的路径替换为另一台电脑上的实际路径：

```powershell
$source = "<源 vault>\.obsidian\plugins"
$target = "<目标 vault>\.obsidian\plugins"

New-Item -ItemType Directory -Force -Path $target | Out-Null
robocopy $source $target /E /XF data.json
Copy-Item "<源 vault>\.obsidian\community-plugins.json" `
          "<目标 vault>\.obsidian\community-plugins.json" -Force
```

`data.json` 没有复制，因为它可能包含远程同步凭据、API 密钥、本地路径或其他 vault 私有状态。Remotely Save 尤其需要在新电脑上重新填写配置。

复制 Claudian 配置：

```powershell
New-Item -ItemType Directory -Force -Path "<目标 vault>\.claudian" | Out-Null
Copy-Item "<源 vault>\.claudian\claudian-settings.json" `
          "<目标 vault>\.claudian\claudian-settings.json" -Force
```

复制完成后重启 Obsidian，在 `设置 → 社区插件` 中确认 16 个插件均已启用。

## 迁移方法二：逐个安装

如果不想复制插件文件，可以在另一台电脑的 Obsidian 中打开社区插件，按本表的“插件名称”逐个安装。安装完成后，在插件设置中重新配置：

- Templater：模板文件夹。
- QuickAdd：Choices、Capture 和 Macro。
- Git：仓库、提交和自动备份策略。
- Remotely Save：远程服务和凭据。
- Claudian：Codex provider 和 Codex CLI。
- Excalidraw、Iconize、Omnisearch：按需要恢复各自的个性化设置。

## 当前启用清单

```json
[
  "templater-obsidian",
  "obsidian-excalidraw-plugin",
  "excalidraw-extras",
  "obsidian-icon-folder",
  "dataview",
  "obsidian-tasks-plugin",
  "table-editor-obsidian",
  "obsidian-git",
  "calendar",
  "obsidian-style-settings",
  "obsidian-kanban",
  "remotely-save",
  "quickadd",
  "realclaudian",
  "editing-toolbar",
  "omnisearch"
]
```
