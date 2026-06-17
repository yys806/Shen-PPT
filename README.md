<h1 align="center">Shen-PPT</h1>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">简体中文</a>
</p>

<p align="center">
  <strong>A Codex skill for generating editable academic and defense PowerPoint decks.</strong>
</p>

<p align="center">
  <a href="https://github.com/yys806/Shen-PPT/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/yys806/Shen-PPT/validate.yml?branch=main&style=for-the-badge&logo=github&label=CI" alt="CI status" /></a>
  <a href="https://github.com/yys806/Shen-PPT/tree/main"><img src="https://img.shields.io/badge/version-main-blue?style=for-the-badge" alt="main branch" /></a>
  <a href="references/style-samples-v2-20260606/sample-decks"><img src="https://img.shields.io/badge/templates-15%20editable-7c3aed?style=for-the-badge" alt="15 editable templates" /></a>
  <a href="references/highest-references/orangepi-defense-final-v9-20260607"><img src="https://img.shields.io/badge/reference-highest%20quality-f97316?style=for-the-badge" alt="highest reference" /></a>
  <a href="SKILL.md"><img src="https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge" alt="Codex Skill" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT license" /></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> |
  <a href="#preview">Preview</a> |
  <a href="#fixed-pipeline">Pipeline</a> |
  <a href="#validation">Validation</a>
</p>

Shen-PPT is a Codex skill for Chinese academic presentations, course defenses, thesis defenses, and engineering project reports. It reads user-provided reports, code folders, screenshots, charts, experiment results, and reference materials, then generates editable PowerPoint decks through a fixed production pipeline.

Its goal is not to create slide-looking images. Its goal is to produce real PPTX files where text, icons, shapes, flowcharts, tables, screenshots, and images remain editable or independently replaceable whenever practical.

## Use Cases

- Group meeting reports
- Course defenses
- Thesis defenses
- Academic presentations
- Project and code walkthroughs
- Experiment result presentations
- Tongji University blue-white and logo-based decks

## Preview

### General Style Samples

[![General style samples](references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)](references/style-samples-v2-20260606/sample-decks)

### Tongji Style Samples

[![Tongji style samples](references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)](references/style-samples-v2-20260606/sample-decks)

### Highest Quality Reference

The OrangePi defense deck is kept only as a quality reference. It is not a reusable template.

[![Highest reference contact sheet](references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)](references/highest-references/orangepi-defense-final-v9-20260607)

## What Shen-PPT Fixes

- Ignoring the requested template
- Random fonts and drifting page styles
- Flattening whole slides into non-editable screenshots
- Sparse pages with tiny evidence images
- Fake square icons or decorative icon noise
- Skipping outline approval and four-page sample approval
- Showing long English execution dumps to Chinese users
- Delivering only the PPTX while forgetting speaker scripts and likely Q&A

## Final Deliverables

Every complete Shen-PPT run should deliver three files:

| File | Required | Description |
|---|---:|---|
| `{deck-title}.pptx` | yes | editable PowerPoint deck |
| `{deck-title}_讲稿.md` | yes | compact speaker script based on the final deck and source materials |
| `{deck-title}_问答.md` | yes | likely defense questions and direct answers |

## Fixed Pipeline

Shen-PPT must run like an assembly line. Stages should not be skipped, merged, or silently replaced.

| Stage | Name | Output |
|---:|---|---|
| 0 | Activation | load rules, parameter spec, and references |
| 1 | Intake | theme, materials, output path, audience |
| 2 | Material Reading | read reports, code, figures, tables, and results |
| 3 | Outline Only | page-level outline and asset plan for user approval |
| 4 | Template/Style Lock | lock the requested template or sample deck |
| 5 | Design Lock | fonts, navigation, icons, density, and QA rules |
| 6 | Four Sample Pages | cover, directory, section divider, and body page for approval |
| 7 | Full Deck Production | complete editable PPTX |
| 8 | QA And Repair | render previews and check overlap, cropping, fonts, density |
| 9 | Final Documents | generate speaker script and likely Q&A |
| 10 | Delivery | PPTX + speaker script + likely Q&A |

## Core Visual Rules

- Chinese large titles: `Microsoft YaHei` bold
- Chinese subtitles, body text, presenter/team text, and module labels: `FangZheng XiaoBiaoSong JianTi`
- English letters and numbers: `Times New Roman`
- Each body page has one large section title and one formal subtitle
- Right-top navigation uses two fixed lines: `01/02` above and a four-character Chinese label below
- Real screenshots, charts, result tables, terminal outputs, and device photos take priority
- Real images must be shown complete with contain/fit placement, not arbitrarily cropped
- AI images are local/partial assets only, never full-slide reference pages
- No animations or slide transitions by default
- Icons must be real semantic line icons or omitted; filled square pseudo-icons are forbidden

## Template Library

All PPT samples, reference images, parameter specs, and highest references live under `references/`.

| Type | Count | Location |
|---|---:|---|
| General editable samples | 8 | `references/style-samples-v2-20260606/sample-decks/` |
| Tongji editable samples | 7 | `references/style-samples-v2-20260606/sample-decks/` |
| Highest quality reference | 1 | `references/highest-references/orangepi-defense-final-v9-20260607/` |
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
  README_CN.md
  LICENSE
  references/
    parameter-spec.md
    highest-references/
    orangepi-defense-final-v9-20260607/
    style-samples-v2-20260606/
      sample-deck-map.json
      style-manifest.json
      sample-decks/
  scripts/
    validate-repo.ps1
```

The repository root is intentionally clean. PPTX files, previews, reference decks, contact sheets, and parameter files should live under `references/`.

## Installation

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/yys806/Shen-PPT.git C:\Users\Lenovo\.codex\skills\shen-ppt
```

If it is already installed:

```powershell
cd C:\Users\Lenovo\.codex\skills\shen-ppt
git pull
```

## Usage

Invoke `$shen-ppt` in Codex and provide the theme, material paths, and output path.

Example:

```text
[$shen-ppt](C:\Users\Lenovo\.codex\skills\shen-ppt\SKILL.md)
Please create a course defense PPT.
Materials: D:\project\report and D:\project\code
Output: D:\project\ppt
Style: tongji-blue-clean
```

Expected behavior: Shen-PPT first reads the materials and generates only the outline. After outline approval, it locks the template or visual style, then creates four sample pages. Only after the four sample pages are approved does it generate the full deck.

## Validation

Run before publishing changes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate-repo.ps1
```

The checker verifies:

- no top-level PPTX/PNG reference files are accidentally placed outside `references/`
- `references/` exists
- all 15 editable sample PPTX decks exist
- general and Tongji overview images exist
- highest reference PPTX, contact sheet, and parameter spec exist
- `sample-deck-map.json` resolves to real sample deck files

## License

MIT License.
