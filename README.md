# Shen-PPT

<p align="center">
  <img src="https://img.shields.io/badge/CI-passing-brightgreen?style=for-the-badge&logo=github" alt="CI passing" />
  <img src="https://img.shields.io/badge/release-v0.1.0-blue?style=for-the-badge" alt="release v0.1.0" />
  <img src="https://img.shields.io/badge/templates-15%20editable-7c3aed?style=for-the-badge" alt="15 editable templates" />
  <img src="https://img.shields.io/badge/PPTX-editable-f97316?style=for-the-badge" alt="editable PPTX" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT license" />
  <img src="https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87%20%7C%20English-2563eb?style=for-the-badge" alt="Chinese and English" />
</p>

<p align="center">
  <strong>A deterministic Codex skill for generating editable academic and defense PowerPoint decks.</strong>
</p>

Shen-PPT is a Codex skill for Chinese academic PPT production. It turns user-provided reports, code folders, figures, screenshots, tables, and project materials into a structured editable PPTX package through a fixed approval pipeline.

It is designed for:

- 组会汇报
- 课程答辩
- 论文答辩
- 学术汇报
- 项目/代码/实验结果展示
- 同济大学蓝白/校徽风格 PPT

## Preview

### General Style Samples

![General style samples](references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)

### Tongji Style Samples

![Tongji style samples](references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)

### Highest Reference Quality Bar

The OrangePi defense deck is kept as a quality reference only. It is not a reusable template.

![Highest reference contact sheet](references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)

## What Shen-PPT Fixes

Shen-PPT is built to avoid the common failure modes of AI-generated PPT:

- not following the requested template
- random fonts and drifting page styles
- full-slide screenshots that cannot be edited
- sparse pages with tiny evidence images
- fake or decorative icons
- long English execution dumps shown to Chinese users
- skipping outline/sample approval and directly generating the whole deck
- forgetting speaker script and likely Q&A documents

## Fixed Output Package

Every completed Shen-PPT run should produce:

| File | Required | Notes |
|---|---:|---|
| `{deck-title}.pptx` | yes | editable PPTX, not full-slide screenshots |
| `{deck-title}_讲稿.md` | yes | compact speaker script generated from final PPT and source materials |
| `{deck-title}_问答.md` | yes | compact likely defense questions and direct answers |

## Fixed Pipeline

Shen-PPT works like an assembly line. The stages should not be skipped or merged.

| Stage | Name | Output |
|---:|---|---|
| 0 | Activation | execution lock with loaded references |
| 1 | Intake | theme, materials, output path, audience |
| 2 | Material Reading | source findings and asset list |
| 3 | Outline Only | page-by-page outline for user approval |
| 4 | Template/Style Lock | selected template or sample deck lock |
| 5 | Design Lock | parameters, fonts, navigation, density, QA checklist |
| 6 | Four Sample Pages | cover, directory, section divider, body for approval |
| 7 | Full Deck Production | complete editable PPTX |
| 8 | QA And Repair | previews/contact sheet and fixes |
| 9 | Final Documents | 讲稿.md and 问答.md |
| 10 | Delivery | final package |

## Core Visual Rules

- Chinese large titles: `微软雅黑` bold
- Chinese subtitles, body, presenter/team text, module labels: `方正小标宋简体`
- English letters and numbers: `Times New Roman`
- Body page header: one large section title plus one formal subtitle only
- Right-top navigation: fixed two-line module buttons, number on top and four-character label below
- Real screenshots, charts, tables, terminal outputs, and device photos are used first
- Real images must be shown complete with contain/fit placement, not cropped
- AI images are allowed only as local/partial assets, not full-slide reference pages
- No animations or slide transitions by default
- Icons must be real semantic line icons or omitted, never filled square pseudo-icons

## Template Library

All PPTX templates and preview images live under `references/`.

| Group | Count | Location |
|---|---:|---|
| General editable samples | 8 | `references/style-samples-v2-20260606/sample-decks/` |
| Tongji editable samples | 7 | `references/style-samples-v2-20260606/sample-decks/` |
| Highest reference deck | 1 | `references/highest-references/orangepi-defense-final-v9-20260607/` |
| Parameter spec | 1 | `references/parameter-spec.md` |

Available style slugs:

```text
academic-minimal
business-roadshow
chinese-academic
dark-engineering
data-analytics
education-clean
research-blue
tech-launch
tongji-blue-clean
tongji-green-academic
tongji-green-vitality
tongji-guangying
tongji-guangying-jiyi
tongji-sakura
tongji-study-space
```

## Repository Layout

```text
shen-ppt/
  SKILL.md
  README.md
  LICENSE
  references/
    parameter-spec.md
    highest-references/
    orangepi-defense-final-v9-20260607/
    style-samples-v2-20260606/
      sample-deck-map.json
      sample-decks/
  scripts/
    validate-repo.ps1
```

The repository root intentionally stays clean. PPTX files, previews, reference decks, contact sheets, and parameter files belong inside `references/`.

## Installation

Clone the repository into your Codex skills directory:

```powershell
git clone https://github.com/yys806/Shen-PPT.git C:\Users\Lenovo\.codex\skills\shen-ppt
```

If the directory already exists, update it:

```powershell
cd C:\Users\Lenovo\.codex\skills\shen-ppt
git pull
```

## Usage

Invoke the skill in Codex with `$shen-ppt`, then provide:

- theme: `组会汇报`, `课程答辩`, or `论文答辩`
- material paths: report files, code folders, image folders, result tables, screenshots
- output folder
- optional style slug or user-provided PPTX template
- presenter/team information if it should appear on the cover

Example:

```text
[$shen-ppt](C:\Users\Lenovo\.codex\skills\shen-ppt\SKILL.md)
请帮我做课程答辩 PPT。
材料路径：D:\project\report 和 D:\project\code
输出路径：D:\project\ppt
风格：tongji-blue-clean
```

Expected behavior:

1. Shen-PPT reads `SKILL.md`, `references/parameter-spec.md`, and required reference assets.
2. It shows a concise Chinese execution lock.
3. It reads the user's materials and generates only the outline first.
4. After outline approval, it locks the visual/template direction.
5. It generates four editable sample pages.
6. After sample approval, it generates the full editable PPTX.
7. It QA-checks previews and produces the final PPTX plus two Markdown documents.

## Validation

Run the repository checker before publishing changes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-repo.ps1
```

The checker verifies:

- top-level PPTX/PNG reference files were not accidentally placed outside `references/`
- required reference folders exist
- sample overview images exist
- the 15 editable sample PPTX decks are present
- the highest reference deck, contact sheet, and parameter spec exist

## License

MIT License.
