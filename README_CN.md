<h1 align="center">Shen-PPT（神了PPT）</h1>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">简体中文</a>
</p>

<p align="center">
  <strong>Agent 技能：生成可编辑的学术汇报/课程答辩/论文答辩/日常分享 PPT —— S1-S4 场景路由。</strong>
</p>

<p align="center">
  <a href="https://github.com/yys806/Shen-PPT/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/yys806/Shen-PPT/validate.yml?branch=main&style=for-the-badge&logo=github&label=CI" alt="CI status" /></a>
  <a href="https://github.com/yys806/Shen-PPT/tree/main"><img src="https://img.shields.io/badge/version-main-blue?style=for-the-badge" alt="main branch" /></a>
  <a href="references/style-samples-v2-20260606/sample-decks"><img src="https://img.shields.io/badge/templates-15%20editable-7c3aed?style=for-the-badge" alt="15 editable templates" /></a>
  <a href="references/highest-references/orangepi-defense-final-v9-20260607"><img src="https://img.shields.io/badge/reference-highest%20quality-f97316?style=for-the-badge" alt="highest reference" /></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Agent-Skill-111827?style=for-the-badge" alt="Agent Skill" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT license" /></a>
</p>

<p align="center">
  <a href="#场景路由">场景路由</a> |
  <a href="#安装">安装</a> |
  <a href="#使用">使用</a> |
  <a href="#预览">预览</a> |
  <a href="#固定管道">固定管道</a> |
  <a href="#校验">校验</a>
</p>

Shen-PPT v4.1 是面向中文场景的 Agent 技能：学术汇报、课程答辩、论文答辩、工程项目报告与日常分享 PPT。它把每次请求路由到四条生产管道之一（S1-S4），读取用户提供的报告、代码目录、截图、图表、实验结果和参考资料，通过确定性引擎生成**真正可编辑的 PPTX 文件**（分享场景输出 HTML）。

> **v4.1.0（2026-08-30）** —— 吸收 ppt-master 上游 v6.1.0 质量机制：内容保真核对（缺失必须有理由）、图片放大 ≥2x 引擎级警告、文本宽度校准、每页语义唯一归属、最终复查检查点。详见 [`references/quality-gates.md`](references/quality-gates.md)。

目标不是做出"像 PPT 的图片"，而是产出文本、图标、形状、流程图、表格、截图、图片都**可编辑或可独立替换**的真实 PPTX。

## 场景路由

| 场景 | 识别词 | 纪律 | 产出 |
|---|---|---|---|
| **S1 组会汇报** | 北大组会/组会汇报 | 🔒 锁定北大模板（pku-report）零发散 | PPTX |
| **S2 课程大作业答辩** | 课程作业/大作业/课设答辩 | 🔓 结构完整风格可变（ppt-master 官方管线） | PPTX |
| **S3 论文答辩** | 论文答辩/毕设/学位论文 | 🔒 正式固定版式（thesis-formal） | PPTX |
| **S4 日常/自媒体/科普** | 介绍一下/科普/自媒体/分享 | 🎨 自由叙事（guizang/frontend-slides） | HTML |
| **S5 正式答辩/夏令营** | 夏令营/正式答辩/自我介绍 | 🔒 三校变体（北大红/清华紫/同济蓝） | PPTX |

架构一句话：**一个大脑（场景路由 + 内容单源 deck-spec.json）+ 两条手臂（PPTX 管道 S1/S2/S3 走 `render_pptx.py`，HTML 管道 S4 走 guizang/frontend-slides）**。风格只在风格资产库定义一次，两管道共享。

## 预览

### 通用风格样例

[![通用风格样例](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)](/yys806/Shen-PPT/blob/main/references/style-samples-v2-20260606/sample-decks)

![通用风格样例](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)

### 同济风格样例

[![同济风格样例](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)](/yys806/Shen-PPT/blob/main/references/style-samples-v2-20260606/sample-decks)

![同济风格样例](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)

### 最高质量参考

OrangePi 答辩 PPT 仅作为质量参考保留，不是可复用模板。

[![最高质量参考联系表](/yys806/Shen-PPT/raw/main/references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)](/yys806/Shen-PPT/blob/main/references/highest-references/orangepi-defense-final-v9-20260607)

![最高质量参考联系表](/yys806/Shen-PPT/raw/main/references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)

## 最终交付物

每次完整运行交付三件套：

| 文件 | 必需 | 说明 |
| --- | --- | --- |
| `{deck-title}.pptx` | 是 | 可编辑 PPT |
| `{deck-title}_讲稿.md` | 是 | 基于最终 PPT 与素材的紧凑讲稿 |
| `{deck-title}_问答.md` | 是 | 可能的答辩提问与直接回答 |

## 代码引擎

| 文件 | 角色 |
| --- | --- |
| `scripts/render_pptx.py` | S1/S2/S3 PPTX 引擎——deck-spec.json + style-spec + 版式骨架 → 可编辑 PPTX |
| `scripts/export_preview.py` | 导出每页 PNG 预览供视觉 QA |
| `scripts/shen_ppt_engine.py` | 原版引擎——读 Markdown/text/PDF 源 → 结构化 slide cards + 压缩草稿 |
| `scripts/build_shen_ppt_com.ps1` | 官方 PowerPoint COM 回退渲染器（无 python-pptx 时从 slide cards 生成可编辑 PPTX） |
| `tests/test_shen_ppt_engine.py` | slide-card 生成、压缩文档、PDF 前页清理的回归测试 |

## 固定管道

Shen-PPT 必须像流水线一样运行。阶段不可跳过、合并或静默替换。

| 阶段 | 名称 | 输出 |
| --- | --- | --- |
| 0 | 激活 | 加载规则、参数规格、参考 |
| 1 | 输入 | 主题、素材、输出路径、受众 |
| 2 | 素材阅读 | 读报告、代码、图表、表格、结果 |
| 3 | 仅大纲 | 页面级大纲与素材计划，等用户确认 |
| 4 | 模板/风格锁定 | 锁定指定模板或样例 |
| 5 | 设计锁定 | 字体、导航、图标、密度、QA 规则 |
| 6 | 四页样板 | 封面/目录/章节页/正文页，等确认 |
| 7 | 完整制作 | 完整可编辑 PPTX |
| 8 | QA 与修复 | 渲染预览检查重叠、裁切、字体、密度 |
| 9 | 最终文档 | 生成讲稿与可能的问答 |
| 10 | 交付 | PPTX + 讲稿 + 问答 |

## 模板库

所有 PPT 样例、参考图、参数规格、最高质量参考都在 `references/`。

| 类型 | 数量 | 位置 |
| --- | --- | --- |
| 通用可编辑样例 | 8 | `references/style-samples-v2-20260606/sample-decks/` |
| 同济可编辑样例 | 7 | `references/style-samples-v2-20260606/sample-decks/` |
| 最高质量参考 | 1 | `references/highest-references/orangepi-defense-final-v9-20260607/` |
| 参数规格 | 1 | `references/parameter-spec.md` |

可用风格 slug：

`academic-minimal business-roadshow chinese-academic dark-engineering data-analytics education-clean research-blue tech-launch tongji-blue-clean tongji-green-academic tongji-green-vitality tongji-guangying tongji-guangying-jiyi tongji-sakura tongji-study-space`

## 仓库布局

```
shen-ppt/
SKILL.md
README.md
README_CN.md
LICENSE
references/            # 模板库 + 规格文档（deck-spec/layout-skeletons/style-library/template-specs/formal-defense/html-pipeline/parameter-spec + 15 样例 + 最高参考 + 图标）
layouts/               # 版式骨架（skeleton-report/skeleton-defense）
styles/                # 风格资产（index.json + 9 风格 style-spec）
assets/                # 校徽（pku/tsinghua/tongji）+ 北大 LOGO
templates/             # deck-spec.example.json
scripts/               # 渲染引擎 + 原版引擎
tests/                 # 回归测试
```

## 安装

Clone 到 Codex skills 目录：

```bash
git clone https://github.com/yys806/Shen-PPT.git ~/.codex/skills/shen-ppt
```

S2/S4 外部管线按需 clone：
```bash
mkdir -p ~/ppt-refs && cd ~/ppt-refs
git clone <ppt-master 上游>
git clone <guizang-ppt-skill 上游>
git clone <frontend-slides 上游>
```

## 使用

在 Codex 中调用 `$shen-ppt`，提供主题、素材路径与输出路径。

`$shen-ppt`

示例：

`[$shen-ppt](C:\Users\Lenovo\.codex\skills\shen-ppt\SKILL.md)
请制作课程答辩 PPT。
素材：D:\project\report 与 D:\project\code
输出：D:\project\ppt
风格：tongji-blue-clean`

预期行为：Shen-PPT 先识别场景（S1-S5），读素材后只生成大纲。大纲确认后锁定模板/视觉风格，再制作四页样板。四页样板确认后才生成完整 PPT。

## 校验

发布前运行 `./scripts/validate-repo.ps1`（Windows PowerShell）——检查仓库布局、references 结构、样例 decks、图标生成与测试。

## License

MIT License.

## 关于

神了PPT-固定风格，指定输出高质量可编辑PPT文件（S1-S4 场景路由）
