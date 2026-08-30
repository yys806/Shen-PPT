<h1 align="center">Shen-PPT</h1>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">简体中文</a>
</p>

<p align="center">
  <strong>An agent skill for generating editable academic, defense and shareable PowerPoint decks — with S1-S4 scenario routing.</strong>
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
  <a href="#scenario-routing">Scenario Routing</a> |
  <a href="#installation">Installation</a> |
  <a href="#usage">Usage</a> |
  <a href="#preview">Preview</a> |
  <a href="#fixed-pipeline">Pipeline</a> |
  <a href="#validation">Validation</a>
</p>

Shen-PPT v4.1 is an agent skill for Chinese academic presentations, course defenses, thesis defenses, engineering project reports and daily shareable decks. It routes every request to one of four production pipelines (S1-S4), reads user-provided reports, code folders, screenshots, charts, experiment results, and reference materials, then generates **real editable PPTX files** (or HTML decks for sharing) through deterministic engines.

> **v4.1.0 (2026-08-30)** — Quality gates absorbed from ppt-master upstream v6.1.0: content-fidelity review (absence needs a reason), image upscale warning at ≥2x (engine-enforced), text-width calibration, single page-semantics ownership, and a final review checkpoint. See [`references/quality-gates.md`](references/quality-gates.md).

Its goal is not to create slide-looking images. Its goal is to produce real PPTX files where text, icons, shapes, flowcharts, tables, screenshots, and images remain editable or independently replaceable whenever practical.

## Scenario Routing

| Scenario | Trigger words | Discipline | Output |
|---|---|---|---|
| **S1 Group meeting** | 北大组会 / 组会汇报 | 🔒 Locked template (pku-report), zero divergence | PPTX |
| **S2 Course defense** | 课程作业 / 大作业 / 课设答辩 | 🔓 Full structure, style varies (ppt-master official pipeline) | PPTX |
| **S3 Thesis defense** | 论文答辩 / 毕设 / 学位论文 | 🔒 Formal fixed layout (thesis-formal) | PPTX |
| **S4 Daily / self-media / science pop** | 介绍一下 / 科普 / 自媒体 / 分享 | 🎨 Free narrative (guizang / frontend-slides) | HTML |
| **S5 Formal defense / summer camp** | 夏令营 / 正式答辩 | 🔒 Three-school variants (PKU/Tsinghua/Tongji) | PPTX |

One brain (scenario routing + single-source `deck-spec.json`) + two arms (PPTX pipeline S1/S2/S3 via `render_pptx.py`, HTML pipeline S4 via guizang/frontend-slides). Styles are defined once in the style asset library and shared by both pipelines.

## Preview

### General Style Samples

[![General style samples](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)](/yys806/Shen-PPT/blob/main/references/style-samples-v2-20260606/sample-decks)

![General style samples](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png)

### Tongji Style Samples

[![Tongji style samples](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)](/yys806/Shen-PPT/blob/main/references/style-samples-v2-20260606/sample-decks)

![Tongji style samples](/yys806/Shen-PPT/raw/main/references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png)

### Highest Quality Reference

The OrangePi defense deck is kept only as a quality reference. It is not a reusable template.

[![Highest reference contact sheet](/yys806/Shen-PPT/raw/main/references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)](/yys806/Shen-PPT/blob/main/references/highest-references/orangepi-defense-final-v9-20260607)

![Highest reference contact sheet](/yys806/Shen-PPT/raw/main/references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png)

## Final Deliverables

Every complete Shen-PPT run should deliver three files:

| File | Required | Description |
| --- | --- | --- |
| `{deck-title}.pptx` | yes | editable PowerPoint deck |
| `{deck-title}_讲稿.md` | yes | compact speaker script based on the final deck and source materials |
| `{deck-title}_问答.md` | yes | likely defense questions and direct answers |

## Code Engines

Shen-PPT includes deterministic engines so runs do not rely on freehand prompting:

| File | Role |
| --- | --- |
| `scripts/render_pptx.py` | S1/S2/S3 PPTX engine — renders deck-spec.json + style-spec + layout skeleton into editable PPTX |
| `scripts/export_preview.py` | exports per-slide PNG previews for visual QA |
| `scripts/shen_ppt_engine.py` | legacy engine — reads Markdown/text/PDF sources and creates structured slide cards plus compact Markdown drafts |
| `scripts/build_shen_ppt_com.ps1` | official PowerPoint COM fallback renderer for editable PPTX generation from slide cards |
| `tests/test_shen_ppt_engine.py` | regression tests for slide-card generation, compact docs, and PDF front-matter cleanup |

## Fixed Pipeline

Shen-PPT must run like an assembly line. Stages should not be skipped, merged, or silently replaced.

| Stage | Name | Output |
| --- | --- | --- |
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

## Template Library

All PPT samples, reference images, parameter specs, and highest references live under `references/`.

| Type | Count | Location |
| --- | --- | --- |
| General editable samples | 8 | `references/style-samples-v2-20260606/sample-decks/` |
| Tongji editable samples | 7 | `references/style-samples-v2-20260606/sample-decks/` |
| Highest quality reference | 1 | `references/highest-references/orangepi-defense-final-v9-20260607/` |
| Parameter spec | 1 | `references/parameter-spec.md` |

Available style slugs:

`academic-minimal
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
tongji-study-space`

## Repository Layout

```
shen-ppt/
SKILL.md
README.md
README_CN.md
LICENSE
references/
parameter-spec.md
deck-spec.md
layout-skeletons.md
style-library.md
template-specs.md
formal-defense.md
html-pipeline.md
highest-references/
orangepi-defense-final-v9-20260607/
style-samples-v2-20260606/
sample-decks/
icons/
apple-svg/
layouts/
skeleton-report.json
skeleton-defense.json
styles/
index.json
pku-report/
thesis-formal/
...
assets/
pku/
schools/
templates/
deck-spec.example.json
scripts/
render_pptx.py
export_preview.py
make_school_logos.py
shen_ppt_engine.py
build_shen_ppt_com.ps1
validate-repo.ps1
tests/
test_shen_ppt_engine.py
```

## Installation

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/yys806/Shen-PPT.git ~/.codex/skills/shen-ppt
```

External pipelines (S2 ppt-master, S4 guizang/frontend-slides) are cloned separately:

```bash
mkdir -p ~/ppt-refs && cd ~/ppt-refs
git clone <ppt-master-upstream>
git clone <guizang-ppt-skill-upstream>
git clone <frontend-slides-upstream>
```

## Usage

Invoke `$shen-ppt` in Codex and provide the theme, material paths, and output path.

`$shen-ppt`

Example:

`[$shen-ppt](C:\Users\Lenovo\.codex\skills\shen-ppt\SKILL.md)
Please create a course defense PPT.
Materials: D:\project\report and D:\project\code
Output: D:\project\ppt
Style: tongji-blue-clean`

Expected behavior: Shen-PPT first identifies the scenario (S1-S5), reads the materials and generates only the outline. After outline approval, it locks the template or visual style, then creates four sample pages. Only after the four sample pages are approved does it generate the full deck.

## Validation

Run before publishing changes: `./scripts/validate-repo.ps1` (Windows PowerShell) — checks repository layout, references structure, sample decks, icon generation and tests.

## License

MIT License.

## About

神了PPT-固定风格，指定输出高质量可编辑PPT文件（S1-S4 场景路由）
