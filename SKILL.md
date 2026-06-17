---
name: shen-ppt
description: Use when creating editable academic PowerPoint/PPTX decks from user-provided reference materials for group meeting reports, course defenses, thesis defenses, research talks, paper presentations, code/project reports, or Chinese PPT tasks involving 组会汇报, 课程答辩, 论文答辩, 学术汇报, PPT制作, or 答辩PPT.
---

# Shen-PPT

## Overview

Create material-first academic PPTX decks through a gated workflow: read the user's sources, design the content outline and visual system, build four editable PPT sample pages for approval, then generate the full deck as editable PowerPoint elements.

The core principle is **editable PPT first**. Do not use full-slide screenshots or full-slide AI images as the final deck. AI image generation is allowed only for local/partial assets when it improves a slide and no better real source asset exists.

## Highest Reference Baseline

The highest-quality reference is stored at `references/highest-references/orangepi-defense-final-v9-20260607/`.

Load `references/highest-references/orangepi-defense-final-v9-20260607/accepted-standard.md` when judging whether a draft reaches the accepted Shen-PPT quality level, when calibrating density and evidence polish, or when building a course-defense or engineering project deck without a new visual preference.

The OrangePi v9 deck is **not a reusable template**. It is the top reference and quality benchmark only. Use it to calibrate productized evidence handling, density, navigation discipline, icon consistency, no-animation behavior, copy quality, and final-package completeness. Never clone its slide sequence, OrangePi-specific structure, screenshots, metrics, names, conclusions, or visual composition as a template for unrelated decks.

`references/orangepi-defense-final-v9-20260607/` is kept as a compatibility mirror. `references/orangepi-defense-accepted-20260606/` is a historical V7 calibration pack. The highest-reference path above is the active quality benchmark.

For default production, also load `references/parameter-spec.md`. It is the machine-style parameter table for canvas size, colors, fonts, grid, header chrome, navigation buttons, page types, component geometry, density thresholds, copy rules, and QA gates. Unless the user explicitly approves different parameters, treat `parameter-spec.md` as binding, not advisory.

Reference files:

- `references/parameter-spec.md`: default production parameters and QA thresholds
- `reference.pptx`: final accepted editable v9 reference deck, not a template
- `contact-sheet.png`: all-slide visual overview
- representative previews: `slide-01.png`, `slide-02.png`, `slide-03.png`, `slide-04.png`, `slide-08.png`, `slide-12.png`, `slide-17.png`, `slide-21.png`, `slide-22.png`

Style sample library:

- `references/style-samples-v2-20260606/`: parameterized style sample source library for Shen-PPT visual selection and future batch production; every sample is an accepted-skeleton skin, not an independent layout system
- `references/style-samples-v2-20260606/sample-decks/`: canonical runtime sample-deck directory inside this skill. It contains fifteen editable four-page sample PPTX decks and two overview PNGs. Use this directory, not the management mirror, as the active sample-deck reference path.
- `references/style-samples-v2-20260606/sample-decks/Shen-PPT风格样板_*.pptx`: eight general editable sample decks: `academic-minimal`, `business-roadshow`, `chinese-academic`, `dark-engineering`, `data-analytics`, `education-clean`, `research-blue`, and `tech-launch`
- `references/style-samples-v2-20260606/sample-decks/Shen-PPT同济样板_*.pptx`: seven Tongji-specific editable sample decks: `tongji-blue-clean`, `tongji-green-academic`, `tongji-green-vitality`, `tongji-guangying`, `tongji-guangying-jiyi`, `tongji-sakura`, and `tongji-study-space`
- `references/style-samples-v2-20260606/sample-decks/style-samples-v2-general-overview.png`: overview of the eight general styles
- `references/style-samples-v2-20260606/sample-decks/style-samples-v2-tongji-overview.png`: overview of the seven Tongji template-adapted styles
- `references/style-samples-v2-20260606/style-manifest.json`: style names, slugs, groups, and template mapping
- `references/style-samples-v2-20260606/sample-deck-map.json`: canonical mapping from style slug to skill-internal sample PPTX and overview PNG paths
- `references/style-samples-v2-20260606/qa-layout-summary.json`: layout QA record for the sample library
- `references/style-samples-v2-20260606/assets/`: bundled representative images for general samples
- `references/style-samples-v2-20260606/template-media-inspect/`: bundled Tongji template media used by Tongji sample skins

Runtime sample-deck path lock:

- Runtime style/sample references must resolve from this skill directory, especially `references/style-samples-v2-20260606/sample-decks/`.
- `D:\shen\test\skill-manage\shen-ppt` is only a management mirror and backup workspace. Do not use it as the runtime source of sample decks unless the user explicitly asks to operate on that management mirror.
- If a required sample PPTX or overview image is missing from `references/style-samples-v2-20260606/sample-decks/`, stop and report the missing skill reference instead of silently falling back to the management mirror.

Load the v2 style sample library when the user asks for multiple occasions, multiple visual styles, random style matching, style sample PPTs, Tongji-specific styles, or a visual direction beyond the default accepted engineering baseline. Read the roster, sample-deck map, and QA metadata from `references/style-samples-v2-20260606/`, then use the published sample decks and overview PNGs in `references/style-samples-v2-20260606/sample-decks/` as editable style references and parameter examples. Do not copy their sample topic or dummy text into a real deck. When adapting any sample style to a real deck, use the style sample as the skin source and the highest reference as the quality bar: dense evidence-led pages, fixed two-line navigation, formal subtitle discipline, complete image placement, semantic batched icons, bottom-baseline density, and final PPTX plus two Markdown documents.

Default accepted visual baseline unless the user chooses another direction:

- 16:9 editable PPTX, typically 1280x720 design coordinates
- dark green/black academic engineering background with restrained grid texture
- amber accent line and active state, cyan section/step numbers, muted gray subtitles, light main text
- dense but readable layout: content should use the vertical canvas and avoid large empty lower bands
- real evidence first: screenshots, charts, result tables, wiring photos, terminal outputs, and report figures are shown complete and enlarged safely
- right-top module navigation is fixed, two-line, and consistent across body pages
- section divider pages use large aligned section number/title and concise chapter talking points
- one coherent semantic line-icon system is used for section identity, evidence labels, process steps, metrics, and summary cues when it improves readability
- style variants change only visual skin parameters such as palette, background treatment, accent color, image mood, and Tongji/template assets; they do not relax the highest-reference quality bar for density, image handling, icon discipline, copy, no-animation, or delivery-package rules
- final thank-you page is centered with no presenter card/frame

## Required Sub-Skills

- **PRIMARY PPT BUILDER:** Use `presentations:Presentations` when it is available. It is the preferred standard builder for the four editable sample pages and the final editable PPTX.
- **OFFICIAL FIXED FALLBACK:** If `presentations:Presentations` is not available in the current session, use Windows PowerPoint COM as the only Shen-PPT-compliant fixed fallback, provided PowerPoint is installed and controllable. PowerPoint COM is compliant only when it follows the exact Stage 0-10 pipeline, uses the locked parameters, creates editable/selectable PPT elements, renders previews/contact sheets when practical, passes QA, and records the fallback in the execution lock and QA result.
- **CONDITIONAL:** Use `imagegen` only for local/partial assets such as abstract illustrations, scenario visuals, polished object cutouts, or conceptual inserts. Do not use `imagegen` to generate full-slide PPT reference pages.
- **EXCLUSIVE PPT SKILL RULE:** When `shen-ppt` is active, do not use other PPT-making skills such as `html-ppt`, `ppt-master`, `pptx`, or other deck-generation workflows. Shen-PPT owns the PPT workflow; use only `presentations:Presentations` or the official PowerPoint COM fixed fallback for PPTX construction, plus `imagegen` for local/partial image assets when allowed.
- **REFERENCE-ONLY BORROWING:** It is allowed to inspect other PPT skills for planning ideas only when the user explicitly asks, but do not execute their workflows, scripts, templates, conversion tools, or generation logic while Shen-PPT is active.

Tool availability rule: choose the PPT construction tool in this fixed order and do not ask the user to approve routine fallback:

1. Use `presentations:Presentations` if available.
2. If it is unavailable, test Windows PowerPoint COM. If COM is available, record `Tool Status: PowerPoint COM official fallback` and continue as standard Shen-PPT.
3. If both are unavailable, stop and report `Tool Status: blocked`. Do not use `python-pptx`, HTML conversion, SVG export, screenshots, or another PPT construction path as Shen-PPT.

PowerPoint COM is not a shortcut. It must produce the same editable, dense, parameterized, no-animation, evidence-first result as the accepted final reference. The user should not be asked whether to allow COM fallback each time; it is now part of the standard Shen-PPT tool chain. Any other fallback is one-off nonstandard work and must be explicitly requested by the user after cancelling Shen-PPT compliance.

No-rationalization rule: phrases such as `为了不拖你来回确认`, `我直接生成完整 PPT`, `虽然没有 presentations 但可以用 python-pptx`, `先做出来再说`, or similar convenience arguments are not valid reasons to skip Shen-PPT gates. If a gate requires user approval, wait for approval.

## User Constraint Authority Lock

Explicit user constraints are binding. Do not treat Shen-PPT defaults, sample styles, the OrangePi highest reference, or the style library as equal choices when the user has already specified a template, font, school template, logo, palette, or visual style.

Precedence order:

1. Latest explicit user instruction in the current conversation.
2. User-specified PPT/PPTX template or sample deck.
3. User-specified fonts, logos, colors, output path, page count, and required content.
4. `references/parameter-spec.md` geometry, density, image, icon, copy, and QA rules.
5. Shen-PPT style sample library and default highest-reference quality bar.

If these conflict, follow the higher-priority item and record the deviation briefly in the design lock. Do not ask the user to choose again when their instruction is already explicit.

Template fill lock:

- A locked template is a **working base deck**, not inspiration. This applies to user-provided PPT/PPTX files and Shen-PPT sample decks selected from `sample-deck-map.json`.
- Template use means direct fill/extension: open/copy the real PPTX, duplicate the closest existing slide/layout for each new page, then replace text, images, tables, charts, diagrams, and only the content-specific objects required by the new material.
- Do not "recreate", "imitate", "redraw", "visually replicate", or "复刻" the template from scratch. Do not build a lookalike deck by manually drawing similar lines, logos, footers, colors, navigation, or background chrome.
- Preserve the template's masters, layouts, slide size, page chrome, line rules, logo placement, color system, navigation style, spacing rhythm, component proportions, and repeated object positions unless the user explicitly asks to change them.
- New slides must be expanded from the closest existing template page/layout whenever practical. For long decks, map every slide card to a finite copied layout family (`cover`, `directory`, `section divider`, `body/evidence`, `process`, `results`, `summary`, `thanks`) before production.
- If the template lacks a required page type, synthesize that page only from real components already present in the template or locked sample deck; then compare it visually against the template preview before continuing.
- Do not redraw school logos, top rules, footers, navigation blocks, or template marks by memory. Reuse real template assets or user-provided assets.
- When the user has already specified a template, Stage 4 is only a short template fill lock. If the user's wording already clearly confirms the template, record it as locked and proceed after Stage 3 outline approval; do not show 2-4 alternate styles.
- When no user template is specified and a Shen-PPT sample style is selected, the selected sample PPTX becomes the locked base deck. Use it directly by copying/extending its four editable page types; do not merely use its palette as inspiration.
- QA failure: if the output deck cannot trace each produced slide to a copied template/sample layout or a template-derived synthesized page type, the deck is not Shen-PPT-compliant.

Font lock:

- If the user specifies fonts, set every editable text object by role. Do not rely on PowerPoint defaults such as Aptos/Calibri, and do not silently keep template fonts that conflict with the user's font instruction.
- Default user-approved Shen-PPT fonts are: Chinese large titles `微软雅黑`; Chinese subtitles/body/presenter/module labels `方正小标宋简体`; English and numbers `Times New Roman`.
- Role details are fixed unless the user overrides them: cover title, directory title, section-divider number/title, and body big section title use `微软雅黑` bold; body subtitle, presenter name, team members, body copy, card titles, module labels, and Chinese table text use `方正小标宋简体`; all English letters, code identifiers, formulas, page numbers, module numbers, and Arabic numerals use `Times New Roman`.
- If a text box mixes Chinese with English or numbers and exact font fidelity matters, split it into separate editable text boxes or text runs so each part uses the correct font.
- When practical, check the generated PPTX text styles or PowerPoint object fonts before delivery. Any leftover default font in visible text is a QA failure unless the user explicitly allowed it.

Chinese interaction lock:

- User-facing stage outputs and approval prompts must be in Chinese by default.
- Do not make the user approve a long English status dump. Use short Chinese labels, concise bullets, and plain confirmation wording.
- Keep detailed internal fields, slide cards, QA checklists, and manifests in files when needed; the chat approval block should show only the current gate's decision points.
- Each approval request must end with one clear Chinese sentence, for example `请确认这个大纲，确认后我再进入模板和视觉锁定` or `请确认是否按这个模板扩充，确认后我再生成四页样板`.

## Mandatory Startup Contract

When Shen-PPT is invoked, do not start writing an outline, creating sample pages, or building a PPT until these reference checks are complete:

1. Load this `SKILL.md`.
2. Load `references/parameter-spec.md`.
3. Load `references/highest-references/orangepi-defense-final-v9-20260607/accepted-standard.md`.
4. If the user requests a style, style library, Tongji version, blue-white Tongji deck, or a named sample style, load `references/style-samples-v2-20260606/style-manifest.json`, `references/style-samples-v2-20260606/sample-deck-map.json`, and the matching published editable sample deck or overview from `references/style-samples-v2-20260606/sample-decks/`.
5. If the selected sample style cannot be found or loaded, stop and tell the user which reference is missing instead of approximating the style from memory.

Before presenting the outline or generating the four sample pages, create a short **Shen-PPT execution lock** that states:

- confirmed theme and material paths
- loaded reference files
- selected style slug and sample deck path, or `default highest-reference quality bar`
- page-type contract for the four sample pages: `cover`, `directory`, `section divider`, `body`
- final package contract: PPTX plus compact speaker-script Markdown plus compact likely-Q&A Markdown

The execution lock is not optional. If another conversation has already started without this lock, pause, create the lock, and re-check the workflow before continuing.

The execution lock is not approval. After the execution lock, present only the PPT outline for approval. After outline approval, record the template/style lock: if a template is specified, lock the base PPTX and fill policy; if no template is specified, present visual style options for approval and then lock the selected sample PPTX as the base deck. After the template/style lock, create the design lock, generate the four sample pages, then ask for approval again before the full deck.

## Fixed Production Pipeline

Shen-PPT must run as a fixed assembly-line workflow. Do not skip, merge, reorder, or silently replace stages. Each stage has a required output and a required next-step condition.

| Stage | Name | Required Action | Required Output | User Confirmation | Next Step |
|---|---|---|---|---|---|
| 0 | Activation | Load `SKILL.md`, `parameter-spec.md`, highest reference, and requested style/sample references | Shen-PPT execution lock | no, but must be shown | Stage 1 |
| 1 | Intake | Confirm theme, material paths, output path, audience, style request, presenter/team info | intake summary | if any required input is missing | Stage 2 |
| 2 | Material Reading | Inspect and read materials before writing content | material findings: topic, evidence, assets, missing facts | no, unless critical facts are missing | Stage 3 |
| 3 | Outline Only | Produce only the page-by-page PPT outline and asset/content plan | outline only | **yes, required** | Stage 4 only after approval |
| 4 | Visual Style Or Template Lock | If the user specified a template, lock that PPTX as the base deck; otherwise present 2-4 visual style options, recommend one, and lock the chosen Shen-PPT sample PPTX as the base deck | template fill lock or sample-deck lock | **yes, required unless the user's template instruction was already explicit** | Stage 5 only after approval/recorded lock |
| 5 | Design Lock | Convert approved outline and locked base deck into a contract with copied layout mapping, parameters, slide-card schema, fonts, navigation, density, QA checklist | design lock | no, but must be shown | Stage 6 |
| 6 | Four Sample Pages | Build exactly four editable sample pages in order: cover, directory, section divider, body | sample PPTX or sample preview/contact sheet | **yes, required** | Stage 7 only after approval |
| 7 | Full Deck Production | Build the complete editable PPTX from slide cards and the design lock | full editable PPTX | no intermediate approval unless user requested | Stage 8 |
| 8 | QA And Repair | Render previews/contact sheet and check against QA gates | QA result + repaired PPTX if needed | no, unless QA finds a blocking ambiguity | Stage 9 |
| 9 | Final Documents | Generate compact speaker-script Markdown and likely-Q&A Markdown from final PPT and materials | `{deck-title}_讲稿.md` + `{deck-title}_问答.md` | no | Stage 10 |
| 10 | Delivery | Report final files and any limitations | PPTX + two Markdown files | complete | stop |

Hard confirmation locks:

- Stage 3 outline approval is mandatory. Do not present visual style options until the user approves the outline.
- Stage 4 visual style/template lock is mandatory. If the user explicitly specified the template, record that template as locked instead of asking them to choose from candidate styles. If the user chooses a Shen-PPT style, record the exact sample PPTX as the base deck. Do not create the design lock or sample pages until the base deck is locked.
- Stage 6 four-sample-page approval is mandatory. Do not build the full deck until the user approves the four editable sample pages.
- The execution lock, design lock, or a user-provided material path is not approval.
- A user saying `继续`, `直接做`, `你看着办`, or providing enough materials is not approval for a skipped earlier stage unless they explicitly approve the current gate after seeing its required output.
- If the user asks to skip a required confirmation, explain that this would leave the Shen-PPT standard and ask whether they want a nonstandard fallback. Do not call that fallback Shen-PPT-compliant.

Forbidden jumps:

- Stage 0 -> Stage 7 is forbidden.
- Stage 1 -> Stage 7 is forbidden.
- Stage 2 -> Stage 7 is forbidden.
- Stage 3 -> Stage 5 is forbidden without Stage 4 visual/template lock.
- Stage 3 -> Stage 6 is forbidden without Stage 4 visual/template lock and Stage 5 design lock.
- Stage 4 -> Stage 7 is forbidden without Stage 6 four-page sample approval.
- Do not generate full deck before Stage 3 outline approval, Stage 4 visual/template lock, and Stage 6 sample approval.
- Full deck production before four sample pages is forbidden.
- Final documents before the final PPTX is QA-checked are forbidden.

If a conversation is interrupted, resumed, or migrated, restart from the last completed stage with evidence. If there is no visible execution lock or approval record, return to the earliest missing gate.

Material boundary lock:

- Use the user-provided materials as the source of truth.
- Do not search the web, add outside papers, add outside claims, or expand the evidence base unless the user explicitly approves external research for that deck.
- If external research is approved, record it in the execution lock and asset/evidence plan, keep citations separate from user-provided materials, and do not let web results replace reading the user's files.
- If the deck is a research-topic discussion and outside references would help, ask at Stage 2 or Stage 3 before using them.

## Canonical Output Format

Every Shen-PPT run must use the same output format, no matter which conversation, directory, topic, or style is used. Do not invent new section names, omit fields, merge stages, or change the order.

Every conversation must use these same headers, field names, artifact names, and confirmation messages. Do not invent alternate wording, merge headers, or omit stage/status fields.

Chat language rule:

- Keep the markdown headers fixed for machine recognition, but use Chinese field labels and Chinese explanations in user-facing chat.
- Do not expose long English labels such as `Candidate Styles`, `Image Treatment`, `Pipeline Stage`, or `Tool Status` as the main user-facing content unless they are inside the fixed execution lock or an artifact file.
- Stage approval messages should normally be under 500 Chinese characters unless the outline itself needs more detail.
- The user-facing approval block should show only the current gate. Do not include Stage 0/1/2/3/4 together in one chat response unless the user explicitly asks for a full audit.

### Stage 0 Output: Shen-PPT Execution Lock

Use this exact structure:

```markdown
## Shen-PPT Execution Lock
- Pipeline Stage: 0 / Activation
- Theme: 组会汇报 | 课程答辩 | 论文答辩
- Materials: [absolute paths]
- Output Folder: [absolute path]
- Loaded References:
  - SKILL.md: [path]
  - Parameter Spec: [path]
  - Highest Reference: [path]
  - Style Manifest: [path or none]
  - Sample Deck: [path or default]
- Style Slug: [slug or default]
- Four Sample Pages: cover, directory, section divider, body
- Required Confirmations:
  - Stage 3 outline-only approval
  - Stage 4 visual/template lock
  - Stage 6 four sample pages approval
- Final Package: PPTX + 讲稿.md + 问答.md
- External Research: not allowed unless user approves
- Tool Status: presentations:Presentations available | PowerPoint COM official fallback | blocked
```

### Stage 3 Output: Outline Only

Use this exact structure. In chat, field values and explanations should be Chinese.

```markdown
## Shen-PPT Outline
- 阶段: 3 / 等待确认大纲
- PPT标题:
- 面向对象:
- 核心表达:
- 章节安排:
- 页面大纲:
  - 01 [page title] | [layout family] | [source evidence] | [visual asset]
- 真实素材:
- 局部AI素材:
- 需要确认: 请先确认 PPT 大纲，确认后我才会进入模板和视觉锁定
```

Stage 3 content lock:

- Stage 3 must output only the outline and asset/content plan.
- Stage 3 must not include visual palette, typography, template recommendation, sample deck path, design lock, sample-page promise, or web-research claims.
- Stage 3 must stop after asking for outline approval.
- If the previous response mixed outline, visual direction, web preflight, and later-stage plans into one section, discard that output and regenerate Stage 3 as outline only.

### Stage 4 Output: Visual Style Or Template Lock

If the user already specified a template, use this concise template-lock structure:

```markdown
## Shen-PPT Visual Style Selection
- 阶段: 4 / 模板已锁定
- 使用模板:
- 模板填充方式: 直接以该 PPTX 为工作底稿；复制最接近的模板页或版式扩充；只替换文字、图片、表格、图表、流程图和必要内容对象
- 字体锁定:
- 版式继承:
- 不再推荐其他风格: 是
- 下一步: 进入设计锁和四页样板制作
- 需要确认: 请确认是否按这个模板扩充，确认后我再生成四页样板
```

If the user did not specify a template, use this visual-selection structure:

```markdown
## Shen-PPT Visual Style Selection
- 阶段: 4 / 等待确认视觉风格
- 已确认大纲:
- 候选风格:
  - A. [style name] | [style slug] | [sample deck path or default reference] | [why it fits]
  - B. [style name] | [style slug] | [sample deck path or default reference] | [why it fits]
- 推荐风格:
- 展示模板:
- 选中后执行方式: 直接以选中的样板 PPTX 为工作底稿扩充，不复刻、不重画
- 预览图:
- 颜色:
- 字体:
- 导航:
- 图片处理:
- 需要确认: 请确认视觉风格和模板方向，确认后我才会进入设计锁和四页样板制作
```

Stage 4 content lock:

- Stage 4 must be shown only after Stage 3 outline approval.
- Stage 4 must show the recommended visual style and the matching template/sample PPT reference or overview preview when available, unless a user template is already specified.
- When a user template is specified, Stage 4 must say `不再推荐其他风格` and must not output candidate styles.
- Stage 4 must not generate sample pages or the full deck.
- If the style uses a sample from the Shen-PPT library, name the exact style slug and sample PPTX path.
- If a sample deck is selected, the sample PPTX is the base deck to fill/extend. Do not recreate its look from scratch.
- If no sample style is chosen, state `default highest-reference quality bar` and show the default visual parameters instead of pretending a sample deck was loaded.

### Stage 5 Output: Design Lock

Use this exact structure:

```markdown
## Shen-PPT Design Lock
- Pipeline Stage: 5 / Design Locked
- Canvas:
- Fonts:
- Palette:
- Style Slug:
- Sample Deck:
- Navigation Geometry:
- Page Density:
- Four Sample Page Contract:
- Asset Policy:
- Icon Policy:
- No-Animation Rule:
- Final Package Rule:
- QA Checklist:
```

### Stage 6 Output: Four Sample Pages Review

Use this exact structure:

```markdown
## Shen-PPT Four Sample Pages
- Pipeline Stage: 6 / Awaiting User Approval
- Sample PPTX:
- Preview / Contact Sheet:
- Page 1: cover
- Page 2: directory
- Page 3: section divider
- Page 4: body
- QA Result:
- Approval Required: 请确认四页样板，确认后我才会生成完整 PPT
```

### Stage 8 Output: QA Result

Use this exact structure:

```markdown
## Shen-PPT QA Result
- Pipeline Stage: 8 / QA
- PPTX:
- Slide Count:
- Preview / Contact Sheet:
- Editability:
- Font Compliance:
- Navigation Compliance:
- Image Completeness:
- Density:
- No Animation:
- Issues Found:
- Repairs Applied:
```

### Stage 10 Output: Final Delivery

Use this exact structure:

```markdown
## Shen-PPT Final Delivery
- Pipeline Stage: 10 / Complete
- PPTX: [absolute path]
- Speaker Script: [absolute path]
- Likely Q&A: [absolute path]
- Preview / Review Folder: [absolute path or none]
- Notes:
```

Canonical filenames:

- PPTX: `{deck-title}.pptx`
- speaker script: `{deck-title}_讲稿.md`
- likely Q&A: `{deck-title}_问答.md`
- optional review folder: `{deck-title}_review`
- optional contact sheet: `{deck-title}_contact_sheet.png`
- optional design lock: `{deck-title}_design_lock.md`
- optional slide cards: `{deck-title}_slide_cards.json`
- optional asset manifest: `{deck-title}_asset_manifest.json`
- optional QA report: `{deck-title}_qa.md`

The two final Markdown documents must also use stable compact formats:

- Speaker script: one `#` title, then slide-by-slide `## 第 01 页：标题` sections, no repeated blank lines
- Likely Q&A: one `#` title, then `## Q1：问题` and `A：答案`, no repeated blank lines

## Hard Gates

Gate isolation lock:

- The approval gates are strictly separated. Stage 3 is outline only. Stage 4 is visual style/template selection only. Stage 6 is four sample pages only.
- Stage 3 must not contain palette, typography, visual direction, sample deck path, template recommendation, web preflight, design lock, or sample-page generation promises.
- Stage 4 must not repeat the full outline, generate sample pages, or build the full deck. If no template was specified, it only shows visual style options, the recommended style, and the template/sample PPT reference or overview preview. If a template was specified, it only shows the template lock.
- A response that combines material findings, outline, visual style, web research/preflight, and later-stage promises into one approval block is invalid. Regenerate the current gate instead of continuing.
- Required gates are independent: Stage 3 outline approval, Stage 4 visual/template lock, and Stage 6 four sample pages approval.
- Use the newest stage definitions in this gate isolation lock if any older wording in this file appears to combine outline and visual direction.

Do not skip these gates:

1. The user must choose one theme: `组会汇报`, `课程答辩`, or `论文答辩`.
2. The user must provide reference material: files, images, charts, tables, PDFs, papers, existing slides, code files, or code folders.
3. Load the mandatory startup references and create the Shen-PPT execution lock before presenting the outline or building any PPT page.
4. After reading materials, present only the PPT outline for user approval before showing visual styles or building sample pages.
5. After outline approval, either lock the user-specified template directly or present visual style/template options for user approval. After style/template lock, lock the approved outline, approved template/style, loaded references, selected style slug, and execution contract in a concise design lock.
6. Build exactly four editable PPT sample pages in this fixed order: page 1 cover, page 2 directory, page 3 section divider, page 4 body page. These are visual-lock page types, not the first four content slides of the eventual deck.
7. Treat the four editable sample pages as the visual lock. Do not proceed to full deck generation until the user approves them or requests specific revisions.
8. The four sample pages fail QA if page 2 is not a real directory page with `目录`, if page 3 is not a section divider, or if page 4 does not contain the fixed right-top module navigation.
9. The final PPTX must be editable. Do not deliver a deck made from full-slide screenshots pasted into PowerPoint.
10. For final delivery, every practical page element must be separately selectable: text boxes, navigation buttons, section numbers, panels, lines, connectors, icon-like marks, chart shapes, and inserted source figures.
11. Complex photos, real screenshots, and AI local illustrations may remain as separate image objects, but never as whole-slide flattened backgrounds.
12. Do not combine Shen-PPT with another PPT skill or deck workflow in the same task. If another PPT skill seems useful, ignore it unless the user explicitly cancels Shen-PPT and switches workflows.
13. Default production must be parameterized from `references/parameter-spec.md`. Do not freehand coordinates, colors, fonts, module geometry, or page chrome after the parameters are locked.
14. Final delivery must include exactly the core deliverable package unless the user asks for more: one editable PPTX, one compact speaker-script Markdown, and one compact likely-Q&A Markdown.
15. Do not bypass user approval to save time. If the user has not approved the current gate, the only valid next action is to ask for approval or revise that gate's artifact.
16. PPT construction follows one fixed standard tool chain: `presentations:Presentations` first, then PowerPoint COM official fallback if presentations is unavailable, then blocked if both are unavailable.
17. Do not ask the user whether to allow PowerPoint COM fallback. It is already part of the Shen-PPT standard when it follows all gates, parameters, editability requirements, preview/QA checks, and no-animation rules.

## Workflow

### 0. Activation And Reference Loading

Complete the mandatory startup contract before any creative production. This means the response should be able to name the actual loaded files and selected style sample, not just say that Shen-PPT will be followed.

For a Tongji or blue-white Tongji request, the execution lock must include:

- selected style slug, usually `tongji-blue-clean` unless the user chooses another Tongji style
- published sample deck path, for example `references/style-samples-v2-20260606/sample-decks/Shen-PPT同济样板_tongji-blue-clean.pptx`
- Tongji logo source path and placement lock from `references/parameter-spec.md`
- highest-reference comparison path

If the user provides an already-generated sample PPT and says it does not follow Shen-PPT, inspect that sample against this startup contract and the four-page sample QA before editing the skill or regenerating.

If the user asks for a full deck in one message, still follow the gates. Do not infer approval from urgency, convenience, or the fact that the user provided enough material. Shen-PPT requires explicit approval of the outline, a recorded template/style lock, and explicit approval of the four sample pages before full production.

### 1. Intake

Ask the user to choose one theme if it is not already clear:

- `组会汇报`: research group meeting, weekly/monthly research progress, experiment update, paper/project discussion.
- `课程答辩`: course project presentation, class report, final course defense.
- `论文答辩`: thesis/dissertation proposal, midterm defense, final defense, graduation defense.

Require concrete materials. Accept files or folders, including:

- papers, PDFs, DOCX, existing PPT/PPTX, Markdown, notes, experiment logs
- figures, screenshots, charts, tables, CSV/XLSX files
- code files, repositories, README files, notebooks, config files

If the user names a folder, inspect the folder structure first, then read the most relevant files. Prefer README, report text, experiment scripts, notebooks, result files, figures, and configuration files before broad code reading.

### 2. Material Read

Extract:

- central topic and intended audience
- background, problem, method, implementation, experiment, result, conclusion, and future work
- key facts, terms, equations, metrics, figures, tables, screenshots, and code snippets
- materials that should be used directly as real assets
- abstract concepts, scenarios, or complex explanations that may need local AI-generated visuals

Do not invent results, metrics, citations, or claims missing from the source material. Mark missing inputs clearly.

### 3. PPT Outline

Before visual sample generation, create a user-facing outline that specifies:

- deck title and subtitle
- directory sections with `01`, `02`, `03` numbering
- what each section explains
- page-by-page title and subtitle
- page-by-page core content, claim, or teaching point
- suggested layout for each page, such as left text/right figure, full-width diagram, comparison layout, process flow, result chart, code walkthrough, timeline, or summary page
- which real figures, charts, screenshots, tables, or code excerpts should be used
- which local/partial AI assets might be useful
- where visual modules, section labels, and repeated navigation elements appear

Ask the user to confirm or revise the outline.

### 4. Visual Direction

Present 2-4 visual directions derived from the materials and theme. Each direction must include:

- mood and audience fit
- background system
- color palette
- typography hierarchy
- figure/chart treatment
- navigation/module-button style
- why the direction matches the user's material

When the user asks for a style library, style randomization, or multiple sample styles, use `references/style-samples-v2-20260606/style-manifest.json` as the current style roster. The current library contains eight general styles: dark engineering, academic minimal, research blue, tech launch, data analytics, business roadshow, Chinese academic, and education clean. It also contains seven Tongji-specific styles adapted from local Tongji/Electrical College template motifs: 光影济忆, 同济光影PPT模板, 学习空间, 樱花济遇, 碧蓝如洗, 绿意生机PPT模板, and 绿意盎然.

Tongji-specific style rule: when the user requests a Tongji version, a Tongji/Electrical College template, or a blue-white Tongji style, use a blue-white base system, add the verified Tongji logo/wordmark in the upper-right, and preserve Shen-PPT page structure: cover, directory, section divider, and body page. The fixed Tongji logo asset is `references/style-samples-v2-20260606/assets/tongji-logo.jpg`. On a `1280 x 720` canvas, place it at `x=1030, y=24, w=184, h=52`, use contain/fit-complete placement, and keep this position/size identical across every Tongji style and Tongji deck unless the user explicitly changes the logo lock. The logo height should visually match the right-top navigation button height. Do not draw, approximate, recolor, or swap the Tongji logo from individual template media.

Tongji sample-load rule: a Tongji visual direction is invalid unless the selected Tongji style slug and its published sample PPTX path are named in the execution lock. For `tongji-blue-clean`, the expected published sample deck is `references/style-samples-v2-20260606/sample-decks/Shen-PPT同济样板_tongji-blue-clean.pptx` inside this skill. A blue palette, a manually placed logo, or generic university styling is not enough to claim the Tongji sample rule was followed.

Sample-image rule: style sample pages must include normal representative images in image areas. Do not leave sample image regions blank, use empty placeholder boxes, or fill them only with abstract placeholder diagrams. For general samples, use appropriate public/example images with source notes; for branded or school-specific samples, prefer user-provided/template assets. Insert every sample image as a separate image object with contain/fit-complete placement.

Style-skin rule: the style sample library is a skin system, while the OrangePi v9 highest reference is a quality benchmark. Cover, directory, section divider, and body page geometry should follow the selected style/sample and project needs, then be checked against the highest reference for density, evidence polish, navigation discipline, and editability. A style may adjust color, background, logo placement, image source, and accent treatment, but it must not become a sparse placeholder deck, a generic card-grid deck, or a different PPT workflow.

Sample-regeneration rule: when updating or adding styles, rebuild every sample deck from the local `references/style-samples-v2-20260606/scripts/` scripts, refresh both overview images, and update `qa-layout-summary.json`. Do not leave stale PPTX or overview images from an older standard.

Ask the user to approve one direction, optionally with edits. This is a separate gate after outline approval. Do not restate the whole outline here except as a one-line reference to the approved outline.

### 4.5 Productized Deck Pipeline

Borrow product discipline from presentation tools and PPT-master-style planning, but do not use their execution workflows. Convert those ideas into Shen-PPT's editable, material-first pipeline:

- Treat the outline as structured slide cards: each slide card has `purpose`, `audience-facing claim`, `source evidence`, `layout family`, `visual asset`, `speaker note`, and `QA risk` fields. Do not start building slides from loose prose.
- Build from a style kit, not one-off styling: every deck locks color tokens, font roles, component geometry, image treatment, icon family, module navigation, and footer/header chrome before full production.
- Use layout candidates before committing difficult pages: for process, result, architecture, comparison, and evidence-heavy slides, decide the layout family first, then place content. Avoid forcing all pages into the same card grid.
- Keep brand/template assets as a governed library: logos, school marks, public/template images, icon sets, and AI local inserts must have a recorded source and fixed usage rule.
- Prefer smart resizing over content deletion: if a slide is crowded, adjust layout family, grid, image scale, or table structure before deleting important source-grounded content.
- Add speaker notes as private presenter support when useful. Speaker notes must not appear as slide body text and must not replace evidence on the slide.
- Produce a delivery package mindset: final PPTX, compact speaker-script Markdown, compact likely-Q&A Markdown, optional PDF preview when requested, contact sheet/preview images when practical, source-asset manifest, and design-lock summary.
- Use a slide-quality scorecard before delivery: content grounding, hierarchy, density, alignment, evidence visibility, editability, font compliance, image completeness, icon consistency, no-animation compliance, and audience-facing wording.

### 5. Design Lock

After the user confirms the outline and the template/style lock is recorded, create a concise design lock before building the four sample pages. This borrows PPT-master's planning discipline, not its SVG/conversion workflow.

The design lock must include:

- canvas ratio and slide size, usually 16:9
- page count and section roster
- audience, use case, and core message
- template fill policy: if a template is locked, list the base PPTX path, the page/layout types to copy, and the objects to replace; explicitly state that the deck will fill/extend the template rather than recreate it
- chosen visual direction or locked template, palette, and shape language
- typography rules and font-size hierarchy
- icon style: choose one consistent icon style for the whole deck; default to the built-in Shen-PPT Apple-style pure rounded SVG set at `references/icons/apple-svg/`; use Lucide only when the built-in set lacks a matching semantic icon or the user explicitly selects Lucide
- icon role whitelist: icons are allowed only for section-divider title badges, evidence/image labels, process/step rows, metric labels, architecture/module labels, and conclusion/status cues. Directory pages, ordinary paragraphs, thank-you pages, plain subtitles, and decorative empty space do not get icons by default.
- icon asset policy: icons must be semantic identifiers for sections, evidence labels, process steps, metrics, or conclusions; do not add random decorative icons just to fill space
- icon placement policy: icons should sit directly to the left of the related title/text by default, tightly attached to that text; right-attached or below-centered icons are allowed only when the whole component family repeats that placement consistently
- icon geometry policy: every icon role must use the fixed size, gap, color, and alignment from `references/parameter-spec.md`; do not resize icons slide-by-slide to "make it look right"
- icon batch policy: within the same role or peer group, either every item has an icon or no item has an icon. Do not add isolated one-off icons to ordinary text blocks, summary panels, directory pages, or thank-you pages
- icon color policy: for the built-in Apple-style SVG set, use the default `shen-blue #58C4D8` unless the locked style requires another single deck color. Regenerate the batch once with `scripts/generate-apple-svg-icons.py --color "#HEX" --color-name name`; do not create random per-slide colors.
- icon provenance policy: if downloading icons from iconfont.cn or another web source, record the package/source, license/provenance, local asset path, color, size, and slide usage in an icon manifest before delivery
- image policy: real assets first, editable diagrams second, local/partial AI assets only when useful
- style reference policy: if a sample style from `references/style-samples-v2-20260606/` is selected, name the exact style slug and list any overrides; if no style sample is selected, state that the highest reference and `parameter-spec.md` govern the quality bar, while the deck's actual structure must come from the user's material and approved outline
- highest-reference policy: the OrangePi v9 deck is a top reference only, not a template. Use it to compare density, polish, evidence visibility, navigation discipline, copy quality, no-animation compliance, and final package completeness. Do not copy its OrangePi topic, slide sequence, screenshot choices, metrics, or page composition into other decks.
- style-skin lock: when a style sample is selected, the selected style controls the skin. The highest-reference quality bar still controls density, right-top navigation discipline, icon batching, complete-image placement, formal copy, and final delivery documents unless the user explicitly overrides those rules.
- section navigation/module-button rules, including size, position, color, active state, and the required two-line module-button text format
- static-deck rule: Shen-PPT decks do not use animations, object build effects, or slide-transition effects by default or as a standard variant. Every slide must be complete and readable immediately when opened, exported to PDF, or advanced during a defense.
- page density and vertical spacing rules: content should visibly use the vertical canvas, avoid large empty top/bottom bands, and stretch lists, matrices, evidence panels, section cards, and image blocks vertically when the slide feels sparse
- density revision rule: if the user says the bottom area is still too empty, enlarge and stretch the main content downward; prefer larger evidence blocks, taller image regions, and fewer unused bands over adding decorative filler
- subtitle and body-copy rules: page subtitles must be formal, concise, declarative academic-defense titles without commas, and body copy must stay grounded in source material rather than generic AI filler
- source-image rule: real source images, screenshots, figures, charts, and tables must be displayed complete by scaling and positioning; do not crop them unless the user explicitly asks for a crop
- sample-image rule: visual sample decks and style sample pages must show real/example images in image frames; image slots cannot be empty, cannot rely only on generic placeholder diagrams, and cannot crop the image unless the user explicitly requests a crop
- slide-card rule: each planned slide should have an explicit purpose, audience-facing claim, source evidence, layout family, visual asset plan, speaker-note intent, and QA risk. If those fields cannot be filled, the slide is not ready for production.
- layout-family rule: select from a finite layout family such as `evidence split`, `process flow`, `results dominant`, `architecture map`, `comparison matrix`, `code/module walkthrough`, `timeline`, `summary`, `section divider`, or `thanks`; do not freehand every page from scratch.
- brand/style-kit rule: record the selected style kit, logo policy, icon family, color tokens, typography roles, component geometry, image treatment, and no-animation rule in the design lock.
- delivery-package rule: when practical, deliver the PPTX with a contact sheet or rendered previews, source/asset manifest, and design-lock summary so the user can audit what was used.
- final-package rule: every finished deck must produce one editable PPTX, one speaker script `.md`, and one likely Q&A `.md`. The Markdown files are not optional after full deck generation.
- speaker-script rule: generate the speaker script from the final PPT and the user's source materials after the PPTX is complete. It should be slide-by-slide, presenter-ready, source-grounded, and concise. Do not add meta explanations, drafting notes, or filler openings.
- likely-QA rule: generate likely teacher/audience questions from the source materials, final slide claims, metrics, methods, limitations, and visible evidence. Answers must be compact, accurate, and grounded; mark uncertainty rather than inventing facts.
- Markdown compactness rule: final `.md` files must have tight formatting with no extra blank lines, no preface such as `以下是`, no boilerplate about how the document was generated, and no repeated empty lines between sections.
- section-divider rule: section divider pages should explain the few points this chapter will cover; do not force card blocks or artificial three-part structures when plain numbered points are clearer
- section-divider typography rule: when section divider pages are requested, use larger type and set the large section number/title in `微软雅黑` bold
- section-divider alignment rule: on section divider pages, the large section number (`01`, `02`) and the chapter title must sit on the same horizontal visual line/baseline. Use one shared header row, set both text boxes to middle vertical alignment, and avoid the number floating higher or lower than the title.
- cover-illustration rule: the cover page may use an AI-generated project overview or realistic object/scene illustration as a local illustration asset, but it must be inserted as an independent image object and the cover text must remain editable
- cover-presenter typography rule: the presenter name on the cover uses the body Chinese font `方正小标宋简体` unless the user explicitly asks otherwise; do not render the presenter name in Microsoft YaHei title styling.
- directory-title rule: directory entries use normal descriptive chapter titles and are not limited to four Chinese characters; the four-character constraint applies only to right-top body-page navigation labels
- body-header rule: each body slide has one left-top section/chapter title and one formal page subtitle only; do not stack two subtitle/explanation lines below the chapter title
- body-subtitle typography rule: the single body-page subtitle must use `方正小标宋简体` and muted/gray text, not Microsoft YaHei bold
- image-scale rule: source images, screenshots, charts, and local cover illustrations should be enlarged as much as the layout safely allows while preserving full contain/fit placement and no overlap
- module-button-scale rule: right-top module buttons should be slightly larger when readability or visual weight is weak, while keeping the same fixed two-line format
- block-ratio rule: fix a visual density target before placing content. Main content should generally occupy about 70-80% of the usable body area; evidence blocks, cards, and text panels should not leave large empty lower halves or crowd text against edges.
- deck-wide density audit rule: when the user reports sparse frames, oversized boxes, undersized boxes, invisible arrows, or overflowing text on one slide, inspect the same layout role across every slide before exporting. Do not only patch the named slide.
- usable-area rule: for normal body slides, after the body header is locked, the upper content-divider may be moved upward when the page feels compressed; on a 1280x720 canvas, prefer an upper divider around `y=113-128` and let the main content begin around `y=125-140`. The main content region should extend to roughly `y=660` unless the slide is intentionally sparse. `y=660` is the standard content-bottom target, leaving `10px` above the bottom baseline at `y=670`. Large blank top or bottom bands are a defect.
- compact-header rule: if the user asks to move the upper line upward, treat it as a deck-wide density change. On a 1280x720 canvas, move the upper divider to roughly `y=98-102`, start the main content around `y=110-116`, and enlarge the actual proof objects, images, tables, and process blocks to use the newly opened space. Do not move one slide only.
- bottom-baseline rule: on a 1280x720 canvas, draw a consistent editable horizontal rule at `y=670` (`50px` from the bottom), matching the upper content-divider rule style. Treat `y=660` as the normal content-bottom target: main content, image regions, tables, process blocks, and evidence panels should extend to within about `10px` above this bottom rule whenever the slide is not intentionally sparse. Footer text and page numbers live below the rule.
- image-label rule: labels inside image cards, screenshot cards, chart cards, and evidence frames must not be tiny after the image is enlarged. Use a readable label size, normally `16-18px` on a 1280x720 canvas, and increase label strip height/padding if needed so labels feel proportional to the frame. If screenshot/chart text looks too small, enlarge the frame or reduce inner padding before accepting a small proof object.
- box-content rule: if a box is visibly too tall for its text, either add source-grounded detail or increase typography until the box feels intentionally filled. If text is cramped, enlarge the box or reduce content; do not accept either sparse boxes or overflowing text.
- text-fit rule: rendered text must stay inside its containing box with visible bottom padding. If a text block touches or crosses the bottom border, reduce font size, increase box height, shorten the sentence, or split the content.
- box-vertical-alignment rule: text inside large cards, process rows, and callout boxes should be optically vertically centered inside its lane or group. If the box has too little copy, either center the existing text vertically, enlarge the text, or add source-grounded detail; do not leave large empty lower halves with text pinned to the top.
- flow-layout rule: if a visual represents a process, use visible directional arrows or connectors. Horizontal process boxes should arrange `number/title` on the left and explanation on the right; vertical process boxes should arrange title above and explanation below. In horizontal flow rows, vertically center the number, title, separator, and detail text within the row instead of pinning them to the top.
- arrow-visibility rule: process arrows need their own visible spacing between boxes. Do not place process boxes so tightly that arrows are hidden, clipped, or visually reduced to a small square; if arrows look cramped, reduce row height slightly, widen the gap between rows, or move the flow area upward/downward as a system.
- stacked-flow-spacing rule: for stacked vertical process rows, reserve a visible `30-40px` lane between neighboring boxes for arrows. The arrow should sit in that lane with a real arrowhead, clear top/bottom breathing room, and no collision with either box.
- arrow-rule: arrows in process diagrams must use a consistent proper arrow shape with a visible arrowhead and clear direction. Do not fake arrows with a plain rectangle plus a triangle if the result looks like a broken or ambiguous mark.
- page rhythm for every slide: `cover`, `directory`, `section`, `dense`, `breathing`, `evidence`, `summary`, or `thanks`
- thank-you-page rule: for course defenses, thesis defenses, and formal academic defenses, add a final editable thank-you page unless the user rejects it. Keep it consistent with the deck's visual system and include the report topic plus audience-facing wording such as `感谢各位老师聆听` and `敬请批评指正`.
- thank-you-center rule: final thank-you pages should use a centered, no-card composition. Center the thank-you text horizontally, place the presenter line directly below it, and do not put presenter or closing information inside a framed box unless the user explicitly asks for a frame.
- page-by-page layout intent
- chart/diagram plan for every slide that needs structured visualization
- asset inventory listing real source assets, AI local assets to generate, page usage, and crop/placement policy
- speaker-note plan: what private presenter note, if any, should be added to each slide. Notes must be concise, evidence-grounded, and not visible on the slide.
- QA scorecard thresholds for content grounding, layout hierarchy, density, editability, source image completeness, and no-animation compliance
- highest-reference comparison: when using the default quality bar, compare the draft against `references/highest-references/orangepi-defense-final-v9-20260607/contact-sheet.png` for density, navigation rhythm, image scale, section divider treatment, productized evidence handling, no-animation behavior, and thank-you composition before delivery. This comparison is an acceptance check, not a template-cloning instruction.
- parameter lock: list every deck-specific override to `references/parameter-spec.md`. If there is no explicit override, use the parameter table exactly for canvas, palette, fonts, page chrome, module buttons, footer, image cards, process arrows, and thank-you page geometry.

Use the design lock as the source of truth during sample-page and full-deck generation. If the full deck is long or the session has drift risk, write a project-local `design-lock.md` near the output PPTX or working artifacts and re-check it before each batch of slides.

### 6. Typography Rules

Apply these font rules unless the user explicitly overrides them:

- Chinese large titles: `微软雅黑`
- Chinese subtitles and body text: `方正小标宋简体`
- English text and numbers: `Times New Roman`

When a text region mixes Chinese with English/numbers and font fidelity matters, split it into separate editable text boxes so the Chinese and English/number parts can use their assigned fonts.

### Accepted General Constraints

Apply these constraints deck-wide unless the user explicitly approves a different standard:

- Use only the Shen-PPT workflow with `presentations:Presentations` or PowerPoint COM official fallback; do not use `html-ppt`, `ppt-master`, `pptx`, or another PPT skill
- Build editable PPT elements directly; never paste full-slide screenshots as final pages
- Use the approved four-page sample lock: cover, directory, section divider, body page
- Keep the accepted dark engineering academic style when no new style is chosen: dark green/black background, amber accents, cyan numbers, muted gray subtitles, restrained lines, no decorative filler
- Keep body pages compact at the top and full through the bottom: upper divider around `y=98-102`, body content begins around `y=110-116`, content normally reaches near `y=660`, bottom rule at `y=670`
- Keep the right-top module buttons fixed in position and size; each button has section number on the first line and a four-character label on the second line
- Use normal descriptive titles in the directory; do not force directory entries to four characters
- Body pages have exactly one section title and one formal subtitle; do not add a second explanatory subtitle line
- Page subtitles are formal declarative phrases, not casual speech, long clauses, or presenter reminders
- Body copy must explain the actual project sequence, implementation, evidence, and result; do not fill space with abstract AI-sounding claims
- Remove Chinese full stops from formal Chinese slide copy unless the user asks to keep them
- Use real project images, screenshots, tables, charts, terminal outputs, and result figures first; scale them to fit complete, never crop them accidentally
- Use AI images only as local/partial assets such as a cover illustration or conceptual insert
- For style samples, fill image areas with appropriate representative sample images and record public image sources when they are downloaded from the web
- For style samples, preserve the accepted four-page skeleton across every template; do not make independent sparse sample layouts per style
- Process pages need real visible arrows; horizontal process boxes place title/number on the left and explanation on the right, vertical process boxes place title above and explanation below
- Peer cards, numbered steps, metric blocks, and summary items use uniform colors; do not randomly highlight one item
- Use a unified semantic icon system by default: section-divider title icons, evidence-label icons, process-step icons, and metric-label icons should share one line style, stroke width, and color grammar
- Use the built-in Shen-PPT Apple-style pure rounded SVG icon set by default. Load `references/icons/apple-svg/manifest.json` when selecting icons, and prefer generated SVG files from `references/icons/apple-svg/generated/`.
- Let the deck generator use icons autonomously only when an icon adds semantic scanning value: section identity, evidence type, process step, architecture module, metric label, status cue, or key highlight. Do not add icons merely because there is empty space.
- Use icons from the approved role whitelist only: section-divider title badge, evidence/image label, process/step row, metric label, architecture/module label, and conclusion/status cue
- Directory pages use no icons by default; keep them to section numbers, titles, and concise descriptions
- Icons should usually be left-attached to the related text. Right-attached or below-centered placement is allowed only when that placement is repeated across the whole component family
- Icons must follow fixed geometry from `references/parameter-spec.md`: same-role icons use the same size, x/y offset, gap to text, color token, and vertical alignment across the whole deck
- Same-role batches must be consistent: if one peer card, image label, process row, metric card, or section divider uses an icon, every peer in that batch uses the same icon treatment; otherwise remove icons from the whole batch
- Avoid isolated decorative icons on summary panels, ordinary text blocks, thank-you pages, and one-off callouts
- Do not mix icon libraries in one deck unless a verified brand/logo asset is required. Generic Shen-PPT icons default to the built-in Apple-style SVG set; Lucide is fallback only.
- Do not use icon backgrounds, colored rounded squares, fake square marks, or button-like icon containers. The approved built-in style is pure colored line SVG with transparent background.
- Icons must remain separate selectable objects when practical and must not be baked into full-slide images
- Section divider pages use large `01`/`02` numbers aligned horizontally with the section title, with concise talking points rather than forced card grids
- Thank-you pages are centered, no-card, no-frame, with the presenter line below the thanks text
- Do not add animations, object build effects, automatic reveals, or slide-transition effects. Shen-PPT output should behave like a clean static defense deck: one click moves to the next fully visible slide.
- Before delivery, render previews/contact sheet and inspect for overlap, excessive whitespace, tiny evidence images, cropped real assets, inconsistent navigation, and punctuation drift

### 7. Copywriting Rules

Apply these writing rules to every sample page and final slide:

- Slide text must be audience-facing. Never put internal planning, speaker coaching, or agent instructions on the slide, including phrases such as `这一页要说明`, `答辩表达重点`, `本章位置`, `本页结论`, `需要讲`, `可以说`, or similar process notes. If a sentence sounds like a reminder to the presenter, rewrite it as teacher-facing evidence or remove it.
- Treat every user complaint about one slide as a deck-wide standard check. If one numbered list, card group, figure treatment, subtitle style, or color role is wrong on one page, inspect and correct the same role across the whole deck before exporting.
- Same-role visual elements must stay uniform. Peer steps, peer command cards, peer summary columns, peer bullets, and peer metric numbers should use the same fill, border, number color, and title color unless the slide has an explicit analytical reason for a highlighted active state.
- Do not arbitrarily recolor one item in a peer group. Active-state highlighting is allowed only for navigation buttons, current process state, or a clearly labeled comparison winner; otherwise keep all peers visually equal.
- Page subtitles must be formal, concise, declarative academic-defense titles. They should look like `当前已经完成的目标`, `系统硬件连接方式`, or `视觉检测处理流程`, not casual spoken phrases.
- Page subtitles should avoid commas and long chained clauses. If a subtitle needs a comma, rewrite it as a shorter formal title.
- Page subtitles should not be口语化. Avoid phrases like `现场能跑`, `先保证能演示`, `结果能被复查`, or other casual summaries.
- Body copy must be grounded in the user's material: use project names, hardware, metrics, source figures, code modules, real screenshots, and actual experiment facts.
- Prefer defense-ready language that the presenter could say aloud. Use concrete verbs and nouns.
- For formal Chinese defense slides, avoid Chinese full stops (`。`) in on-slide copy unless the user explicitly requests sentence punctuation. Use line breaks, semicolons, short clauses, or no terminal punctuation instead.
- Avoid AI-flavored filler and vague polish words, especially repeated uses of `形成`, `赋能`, `闭环`, `支撑`, `可量化`, `可复现`, `体系化`, `场景化`, `全流程`, and `落地`.
- Do not use grand claims when the source only proves a smaller engineering result. Say exactly what was built, tested, observed, or still limited.
- For lists and cards, keep each item to one clear point. Replace abstract slogans with visible evidence, such as a script name, screenshot, chart, metric, or hardware part.

### 8. Four Editable PPT Sample Pages

Build exactly four editable PPT sample pages with the locked PPT builder: `presentations:Presentations` when available, otherwise PowerPoint COM official fallback. These pages replace the old full-slide AI reference-image step. They are real PPT pages, not raster reference images.

Generate these four editable pages:

1. **Cover page**: large title, optional subtitle, presenter name, group members, institution/course/group metadata when available.
2. **Directory page**: the large Chinese word `目录` in the upper left; sections listed top-to-bottom; each section begins with `01`, `02`, `03`.
3. **Section divider page**: one directory section; include section number, section title, and concise summary of what this section covers.
4. **Body page**: top-right horizontal module buttons; all modules share one style; the active module is highlighted or recolored; upper-left section title such as `01 XXXX`; below it, a smaller subtitle for the page's subtopic. The upper-left section title position and wording must stay consistent across all pages in that section.

These pages are a visual-system sample, not four consecutive topic/content pages. A deck with cover plus three ordinary content pages is not a valid Shen-PPT sample deck and must be discarded or rebuilt. A cover plus three topic/content pages is not a valid sample deck.

Directory entries should be normal descriptive chapter titles, not forced four-character labels. The four-character rule applies only to the short labels inside the right-top module buttons.

For final body slides, keep the header hierarchy to exactly two levels: the section/chapter title and one concise formal page subtitle. If an explanatory sentence is useful, place it in the body content rather than as a second subtitle line.

Right-top module buttons are fixed-format UI elements:

- Each module button must use two editable text lines.
- First line: section number only, such as `01`, `02`, `03`.
- Second line: a concise four-character Chinese label (`四字中文标签`) summarizing that section, using the body Chinese font `方正小标宋简体`.
- All module buttons must have the same width, height, alignment, border, fill, and text positions.
- The active button changes fill/color; inactive buttons keep the same neutral style. Do not change shape size or layout by active state.
- Module buttons should be large enough to read clearly at presentation distance; enlarge the block size before reducing the two-line structure.

All four sample pages must share:

- same slide ratio, preferably 16:9
- same color palette
- same typography rules
- same spacing, shape language, module-button style, and visual hierarchy
- consistent section numbering and navigation treatment
- approved page density: do not leave the top or bottom third visually empty unless the page is intentionally a `breathing` page; stretch content vertically with larger panels, row heights, evidence bands, images, and metric blocks when the page looks sparse

Section divider pages should not automatically become card grids. Use a large section number, section title, concise chapter summary, and 3-5 plain numbered talking points unless the material itself has a real comparison, matrix, or grouped structure.

When section divider pages are included, set the large section number and title in `微软雅黑` bold. Use larger type than normal body slides and avoid small card blocks unless the chapter content truly needs grouped cards.

After building the four sample pages, render preview images and show them to the user. If not satisfied, revise the sample pages and visual system until approved.

### 9. AI Image Rules

AI image generation is allowed only for local/partial slide assets.

Priority order:

1. Use real source assets first: real figures, tables, charts, screenshots, device photos, experiment outputs, code excerpts, and report images.
2. Use editable shapes/charts when the concept can be represented cleanly as a diagram, flow, structure map, metric card, or chart.
3. Use `imagegen` for local/partial assets only when no real asset exists or when a scenario, object demonstration, conceptual visual, or polished insert would benefit from AI generation.

Rules:

- Do not use AI to generate a full PPT page or full-slide reference image.
- Do not set an AI image as a full-slide background in the final PPTX.
- Insert AI outputs as independent, replaceable image objects inside a larger editable slide.
- A cover page can use AI image generation for a project overview, realistic device scene, or polished object illustration. It is still a local/partial asset: title, subtitle, presenter, group members, course metadata, metrics, and other cover elements stay editable.
- Clearly distinguish real source assets from AI-generated local inserts when relevant.
- Real source images and charts must use contain/fit-complete placement. Do not use cover/crop behavior for real screenshots, wiring photos, terminal screenshots, charts, or tables.

### 10. Full Editable PPTX Build

After sample-page approval, use the locked PPT builder to build the full deck as editable PowerPoint content: `presentations:Presentations` when available, otherwise PowerPoint COM official fallback.

PowerPoint COM fallback implementation standard:

- use native PowerPoint shapes, text boxes, lines, connectors, tables, picture objects, and optional chart objects
- keep every practical object separately selectable and editable
- set fonts, colors, geometry, navigation, bottom rule, page number, and density from `references/parameter-spec.md`
- save as normal `.pptx`, not exported images or a PDF-like deck
- render previews/contact sheets when practical, then repair visible issues before delivery
- do not use COM to bypass Stage 3 outline approval, Stage 4 visual/template lock, Stage 6 four-page sample approval, or the final package rule
- the visual target remains the accepted final-reference quality level: dense evidence-led pages, clean icon discipline, complete enlarged images, fixed right-top navigation, no animations, and compact final Markdown documents

Required editable treatment:

- text as editable text boxes
- section numbers and module buttons as editable shapes/text
- icons as editable shapes when practical, or separate image assets when necessary
- charts as editable chart objects or editable shape-based charts when practical
- flowcharts, architecture maps, timelines, and diagrams as editable shapes/connectors
- figures, real screenshots, real photos, and local AI assets as separate replaceable image objects
- page backgrounds, lines, containers, and decorations as editable shapes when practical

Do not flatten completed pages into full-slide screenshots. Do not place a full-slide generated image as a background. If a visually complex object cannot be reasonably decomposed, crop it to that object or insert it as its own independently selectable image, not as a full-slide raster.

During generation, keep the approved design lock open as the execution contract. For each slide, check the slide's page rhythm, layout intent, source assets, chart/diagram plan, typography role, and module-button state before constructing it.

For parameterized production, define reusable tokens and component helpers before creating pages: color tokens, font tokens, chrome constants, navigation constants, image-card defaults, table defaults, flow-row defaults, section-divider defaults, and thank-you defaults. Generate slides from those helpers instead of repeating raw coordinates on every page. Raw per-slide coordinates are allowed only for content-specific placement inside the locked body region.

For productized production, generate from slide cards and layout families. Before creating each page, confirm the slide's claim, evidence asset, layout family, component recipe, and QA risks. After creating each page, record any deviation from the style kit or parameter spec.

Speaker notes are allowed and often useful for defenses, but they must stay private in PowerPoint notes. Never put presenter reminders, internal process comments, or "this page should explain" language on the visible slide.

### 10.5 Final Delivery Documents

After the final PPTX is generated and QA-checked, create two Markdown files next to the PPTX:

1. `讲稿.md` or `{deck-title}_讲稿.md`
2. `问答.md` or `{deck-title}_问答.md`

The speaker script must:

- be generated from the final PPT pages, private speaker notes when present, and original source materials
- follow slide order and use clear slide numbers or slide titles
- explain what the presenter should say, not how the slide was designed
- stay specific to the project, data, code, screenshots, charts, and limitations
- avoid excessive blank lines, generic openings, and meta commentary

The likely-Q&A document must:

- focus on questions teachers or reviewers are likely to ask about background, method choice, implementation sequence, evidence, metrics, limitations, and future work
- include short direct answers that can be said aloud in a defense
- distinguish proven facts from assumptions
- avoid invented results, vague assurances, and unrelated generic questions

The final user-facing deliverable package is the PPTX plus these two compact Markdown files. Review artifacts such as contact sheets, preview images, slide-card JSON, and asset manifests can remain in a working/review folder, but they do not replace the two Markdown documents.

### 11. QA

Before delivery, verify:

- final PPTX exists and is non-empty
- final speaker-script Markdown exists next to the PPTX and is compact, source-grounded, and slide-aligned
- final likely-Q&A Markdown exists next to the PPTX and is compact, source-grounded, and defense-ready
- `presentations:Presentations` was used, or PowerPoint COM official fallback was used and recorded in the execution lock, design lock, and QA result
- user approval of the outline-only gate was obtained before template/style lock
- user approval of the visual style/template gate was obtained before design lock and sample-page generation
- user approval of the four sample pages was obtained before full-deck generation
- mandatory startup references were loaded and listed in the execution lock
- if a style or Tongji sample was requested, the selected style slug and sample deck path were listed in the execution lock
- four sample pages were generated in the required page-type order: cover, directory, section divider, body
- sample page 2 contains a real directory page with `目录`
- sample page 3 is a real section divider page, not another body/content slide
- sample page 4 contains fixed right-top module navigation
- slide count matches the approved outline
- design lock matches the delivered deck
- `references/parameter-spec.md` was loaded for default production
- every deviation from `references/parameter-spec.md` is explicitly recorded in the design lock or user-approved revision
- core geometry did not drift: canvas, safe margins, top rule, body start, bottom rule, footer, navigation buttons, and thank-you page follow the locked parameters
- core styling did not drift: palette, fonts, active/inactive states, line colors, and peer-element colors follow the locked parameters
- the deck follows the accepted baseline when no different visual direction was approved
- when using a style from `references/style-samples-v2-20260606/`, the generated deck visibly preserves that style's palette, chrome, typography rhythm, image treatment, and navigation grammar
- Tongji-specific decks include a verified Tongji logo/wordmark in the upper-right without colliding with navigation or body headers
- final previews/contact sheet have been inspected against the accepted reference for overall density, hierarchy, and visual polish
- icon role whitelist has been inspected: icons appear only in approved roles and never as filler decoration
- icon usage has been inspected: one icon family, consistent stroke/color, semantic placement, no directory icons by default, no random decorative filler, no isolated one-off icons, and no unverified logo-like marks
- built-in Apple-style SVG icon usage has been inspected when used: SVGs come from `references/icons/apple-svg/generated/`, use transparent backgrounds, share one deck color, and match semantic tags from `manifest.json`
- icon geometry has been inspected: same-role icons share the exact locked size, gap, color token, alignment, and repeated placement from `references/parameter-spec.md`
- icon placement has been inspected: icons are left-attached to the related title/text by default, or right/below placement is repeated consistently across the whole component family
- icon batch consistency has been inspected: same-role peer groups either all have icons or all omit icons
- if web-downloaded icons are used, an icon manifest records source/provenance, local path, color, size, and slide usage
- title, directory sections, section numbers, and module labels are consistent
- every right-top module button follows the two-line format: number line plus four-character body-font label
- repeated body-page elements align consistently
- font rules are followed where practical
- user-specified fonts override template fonts and defaults; visible editable text must not retain Aptos, Calibri, DengXian, Microsoft YaHei, or other unintended fonts when the user specified a different role font
- if exact mixed-font fidelity is needed, Chinese, English, and numeric fragments are split into separate text boxes/runs using their locked fonts
- Chinese full stops (`。`) are absent from formal Chinese defense slide copy unless explicitly requested
- no slide has object build animations, automatic reveal timings, or slide-transition effects unless the user explicitly cancels this no-animation rule for a special one-off deck
- each slide card has a clear claim, evidence source, layout family, and visual asset plan
- speaker notes, if present, are private notes and do not leak onto the slide canvas
- speaker script and likely-Q&A documents contain no extra boilerplate, no repeated blank lines, and no unsupported claims
- source/asset manifest records real images, AI local inserts, downloaded icons, logos, and template assets used in the deck
- contact sheet or preview set was generated when practical, and the preview was inspected using the slide-quality scorecard
- text does not overlap images, charts, buttons, or page chrome
- vertical spacing follows the approved sample-page density; no accidental oversized empty top/bottom bands
- normal body content reaches close to the bottom baseline where the slide is not intentionally sparse
- page subtitles are formal, concise, declarative academic-defense titles without commas or long chained clauses
- body-page subtitles use `方正小标宋简体` and muted/gray text consistently
- body copy avoids generic AI language and stays specific to the user's source material
- process diagrams have correct directional arrows, and horizontal/vertical process boxes follow their respective left-right or top-bottom text layout rules
- arrows remain visible with enough spacing between neighboring process boxes
- boxes and cards follow the approved density target: large enough to fill the page, but not so large that their lower half is empty
- peer cards, peer steps, summary columns, and list numbers use uniform color treatment unless a real active state or comparison winner is being shown
- page rhythm varies according to content instead of forcing every page into the same card layout
- icon style is consistent across the deck
- every promised chart, diagram, process flow, architecture map, or table is represented with an editable or independently selectable object
- real source assets are used where promised
- real source images and charts are shown complete without unintended cropping
- source screenshots and charts are enlarged enough to be visually useful while remaining complete and non-overlapping
- sample-image areas are filled with normal representative images or real/template images, not blank placeholders
- AI-generated visuals are local/partial inserts only
- no full-slide screenshot or full-slide AI image is used as a fake editable page
- the final thank-you page uses centered no-card/no-frame composition when present
- final deck opens as editable PPTX content
- if PowerPoint COM official fallback was used, the deck still visually matches the locked sample pages and the highest-reference quality bar; COM fallback is not allowed to reduce density, font fidelity, image completeness, editability, navigation consistency, or document-package completeness

Render previews or a contact sheet for the four sample pages and the final deck whenever practical. Inspect the rendered previews for overlap, cropped text, inconsistent navigation, mismatched fonts, and accidental rasterized full-slide pages before delivery.

## Common Mistakes

- Mixing Shen-PPT with `html-ppt`, `ppt-master`, `pptx`, or another PPT workflow.
- Treating the OrangePi v9 highest reference as a reusable template instead of a quality benchmark.
- Copying OrangePi-specific chapter order, metrics, screenshots, hardware narrative, or page compositions into unrelated decks.
- Skipping the mandatory startup contract and starting directly from an outline or PPT generation.
- Treating the execution lock as user approval. It is only a lock; approval must still happen at the outline-only gate, visual style/template gate, and four-sample-page gate.
- Saying `为了不拖你来回确认` or using urgency/convenience as a reason to skip approval gates.
- Generating the full deck directly after reading materials without first getting approval for the outline, recording the template/style lock, and getting approval for the four sample pages.
- Replacing `presentations:Presentations` with `python-pptx`, HTML, SVG, full-slide screenshots, or another construction path while still claiming standard Shen-PPT compliance.
- Treating PowerPoint COM official fallback as permission to skip the fixed pipeline, loosen the style parameters, skip previews, or deliver a lower-quality deck.
- Claiming an arbitrary fallback deck is Shen-PPT-compliant when neither `presentations:Presentations` nor PowerPoint COM official fallback was available.
- Saying that a style or Tongji sample was used without naming and loading the actual style slug and sample PPTX path.
- Building four topic/content pages and calling them the four Shen-PPT sample pages. The required sample order is cover, directory, section divider, body.
- Producing a cover plus three body slides without a directory page and section divider page.
- Treating a cover plus three topic/content pages as a valid sample deck.
- Copying PPT-master's execution pipeline instead of only borrowing its planning gates and design-lock discipline.
- Copying external AI-PPT products' generic output style instead of using their useful production concepts: structured slide cards, governed style kits, template assets, layout families, speaker notes, and QA scorecards.
- Starting sample pages before the outline, template/style lock, and design lock are confirmed.
- Generating full-slide AI reference images instead of editable PPT sample pages.
- Treating a full-slide screenshot as an editable deliverable.
- Using AI images when the user's real figure, table, chart, or screenshot should be used.
- Leaving style sample image areas blank or using only empty placeholder diagrams when normal representative images are available.
- Creating a pseudo Tongji logo or hand-drawn lookalike instead of using a verified user-provided, template-provided, or official asset.
- Adding icons to decorative empty space, directory entries, thank-you pages, plain subtitles, or isolated ordinary text blocks.
- Using different icon sizes, offsets, colors, or placements inside the same component family.
- Adding an icon to only one item in a peer group instead of applying the same icon treatment to all peers or removing the icon batch.
- Flattening slides into screenshots instead of rebuilding editable PPT elements.
- Adding animations, automatic build effects, click-by-click bullet reveals, slide transitions, or live-show variants after the no-animation rule has been locked.
- Delivering only the PPTX and forgetting the required compact speaker script and likely-Q&A Markdown files.
- Writing the Markdown documents as generic advice, process explanation, or a loose summary instead of using the final PPT and source materials.
- Adding extra blank lines, boilerplate prefaces, or generated-document explanations to the final Markdown files.
- Letting long-deck generation drift away from the approved design lock.
- Changing section-title position or wording across pages in the same section.
- Letting module buttons drift in color, size, text structure, or active-state behavior.
- Making right-top module buttons number-only instead of the required number plus four-character label.
- Forcing directory chapter names into four characters; only body-page navigation labels need four-character short names.
- Stacking a page title, a subtitle, and another explanatory subtitle in the body-page header.
- Rendering the single body-page subtitle in the wrong font or color; it should be `方正小标宋简体` with muted/gray text.
- Leaving slides vertically sparse after the approved sample pages established a fuller top-to-bottom density.
- Leaving cover/project visuals, source screenshots, or result charts too small when they could be safely enlarged without overlap.
- Drawing process arrows as broken rectangles/triangles or omitting arrows from process diagrams.
- Using the same empty box height regardless of text amount; every card or evidence block should have a deliberate content-to-box ratio.
- Ignoring the typography rules for Chinese titles, Chinese body text, English, and numbers.
- Writing page subtitles as casual spoken phrases, long compressed summaries with commas, slash-heavy lists, or multiple clauses.
- Filling body text with generic AI-sounding phrases instead of source-grounded defense language.
- Cropping real screenshots, photos, charts, or tables when they should be scaled down and shown complete.
- Making every section divider page a forced three-card layout instead of explaining the chapter's actual talking points.
