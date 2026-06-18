# Shen-PPT Parameter Spec

Use this file as the default production parameter table for Shen-PPT decks unless the user explicitly approves a different visual system. Values are based on a `1280 x 720` 16:9 canvas. For another 16:9 canvas, scale all coordinates, sizes, and line widths proportionally.

The highest-quality reference is the OrangePi v9 productized reference in `highest-references/orangepi-defense-final-v9-20260607`. Treat that deck as the quality bar for density, evidence visibility, icon discipline, navigation consistency, copywriting, no-animation, and final delivery. It is not a reusable template: do not copy its OrangePi-specific content, slide sequence, metrics, screenshots, or page compositions into unrelated decks. Other styles may change palette, background, structure, and image mood, but they must still meet the highest-reference quality bar unless the user explicitly approves a different system.

Fixed builder chain: use `presentations:Presentations` when available. If it is unavailable, use Windows PowerPoint COM as the official Shen-PPT fallback when PowerPoint is installed and controllable. If neither builder is available, stop. Do not use `python-pptx`, HTML, SVG export, full-slide screenshots, or other PPT skills as Shen-PPT-compliant builders. PowerPoint COM fallback must follow the same Stage 0-10 pipeline, parameter table, editability standard, preview/QA checks, no-animation rule, and final PPTX + two Markdown document package.

User constraint authority: latest explicit user instructions override Shen-PPT defaults. If the user specifies a PPT/PPTX template, use that PPTX as the working base deck and fill/extend it instead of recommending unrelated styles or recreating a lookalike deck. If the user selects a Shen-PPT sample style, the selected sample PPTX becomes the working base deck. If the user specifies fonts, enforce those fonts on visible editable text instead of keeping PowerPoint defaults or conflicting template fonts. User-facing approval output must be concise Chinese by default; do not ask the user to approve a long English status dump.

Template fill lock: a locked template or selected sample deck is the base deck to fill, not inspiration and not something to recreate from scratch. Open/copy the real PPTX, duplicate the closest existing template slide/layout for each new page, then replace text, images, tables, charts, diagrams, and only content-specific objects. Preserve the template's actual slides, masters, layouts, slide size, logo placement, line rules, color tokens, navigation style, spacing rhythm, and component proportions. If a user template is specified, Stage 4 becomes a short template fill lock confirmation and must not show candidate styles unless the user asks for alternatives. If a sample style is selected, Stage 4 must record the exact sample PPTX path and state that the sample deck will be filled/extended directly.

Template traceability QA: every produced slide must map to one copied source slide/layout family from the locked base deck, or to a synthesized page type built only from actual base-deck components. A deck that merely imitates the template colors, logo, lines, navigation, or typography is a QA failure.

## 1. Canvas

| Token | Value |
|---|---:|
| `SLIDE_W` | `1280` |
| `SLIDE_H` | `720` |
| `SAFE_X` | `54` |
| `SAFE_RIGHT` | `1226` |
| `SAFE_W` | `1172` |
| `TOP_RULE_Y` | `100` |
| `BODY_START_Y` | `112` |
| `BODY_BOTTOM_Y` | `660` |
| `BOTTOM_RULE_Y` | `670` |
| `FOOTER_Y` | `684` |
| `PAGE_NUM_X` | `1182` |
| `PAGE_NUM_Y` | `676` |

Body content should normally occupy `BODY_START_Y..BODY_BOTTOM_Y`. A normal body slide that ends much above `y=620` is considered sparse unless it is intentionally a breathing slide.

Highest-reference density lock:

- normal body slides should place proof objects, flow rows, image cards, tables, or conclusion boxes down to `y=640-660`
- `BOTTOM_RULE_Y=670` is a visible editable horizontal rule and the main content target is about `10px` above it
- when a slide feels sparse, expand the actual evidence and body blocks; do not fill the page with decorative shapes
- run the density check deck-wide, not only on the slide named by the user

## 2. Color Tokens

| Token | Hex | Use |
|---|---|---|
| `base` | `#07100F` | main background |
| `base2` | `#0A1513` | background overlay |
| `grid` | `#0D1A17` | background grid lines |
| `panel` | `#0E1E1A` | default panels |
| `panelDark` | `#0C1D19` | dense cards/tables |
| `imagePanel` | `#081411` | image card fill |
| `panel2` | `#132A24` | secondary panels |
| `line` | `#24443B` | separators and card borders |
| `imageLine` | `#1D3A33` | image card border |
| `text` | `#EAF4EF` | primary text |
| `muted` | `#A4B7B0` | subtitles/body secondary text |
| `amber` | `#F2B84B` | active state/accent/section line |
| `blue` | `#58C4D8` | step and section numbers |
| `green` | `#5EE6A8` | positive status only |
| `red` | `#FF6B5F` | warning/error only |

Do not randomly introduce extra accent colors. Peer elements use the same color unless the active state, status, or comparison winner is explicitly meaningful.

## 3. Fonts

| Role | Typeface | Default Size |
|---|---|---:|
| Chinese title | `微软雅黑` | page dependent |
| Chinese subtitle/body | `方正小标宋简体` | page dependent |
| English/numbers | `Times New Roman` | page dependent |
| Body header section title | `微软雅黑` bold | `30` |
| Body page subtitle | `方正小标宋简体` muted | `21` |
| Footer text | `Times New Roman` muted | `10` |
| Page number | `Times New Roman` amber | `14` |

If mixed Chinese and English/number typography must be exact, split into separate editable text boxes.

Role-level font lock:

- cover title, directory title, section-divider number/title, and body big section title use `微软雅黑` bold
- body subtitle, presenter name, team members, body copy, card titles, module labels, Chinese table text, and Chinese diagram labels use `方正小标宋简体`
- English letters, code identifiers, formulas, page numbers, module numbers, chart axis numbers, table numbers, and Arabic numerals use `Times New Roman`
- visible editable text must not retain `Aptos`, `Calibri`, `DengXian`, or any other unintended PowerPoint default font
- template fonts are allowed only when the user explicitly prioritizes the template font over Shen-PPT font lock
- when content needs to be richer, reduce body/table/formula text by `1-2pt` before deleting source-grounded details; keep slide titles readable and stable
- dense paper-explanation slides normally use body text `12-16pt`, compact table text `10-12pt`, formula display text `11-13pt`, and captions `10-12pt`

## 4. Background And Chrome

Background:

- draw `base` full slide
- draw `base2` full slide overlay
- vertical grid lines every `80px`, starting at `x=40`
- horizontal grid lines every `80px`, starting at `y=40`
- top amber strip: `x=0, y=0, w=1280, h=4`

Body chrome:

| Element | Geometry |
|---|---|
| body section title | `x=54, y=22, w=520, h=38`, size `30`, `微软雅黑` bold |
| body subtitle | `x=56, y=69, w=760, h=28`, size `21`, `方正小标宋简体`, muted |
| top body rule | `x=54, y=100, w=1172, h=2`, line color |
| bottom footer rule | `x=54, y=670, w=1172, h=2`, line color |
| footer text | `x=54, y=684, w=720, h=18`, size `10` |
| page number | `x=1182, y=676, w=44, h=24`, size `14`, right aligned |

## 5. Right-Top Module Navigation

Default six-section navigation:

| Token | Value |
|---|---:|
| `NAV_START_X` | `590` |
| `NAV_Y` | `24` |
| `NAV_W` | `98` |
| `NAV_H` | `52` |
| `NAV_GAP` | `8` |
| number text box | `x=buttonX, y=30, w=98, h=18` |
| number size/font | `16`, `Times New Roman` |
| label text box | `x=buttonX, y=51, w=98, h=16` |
| label size/font | `12`, `方正小标宋简体` |

Rules:

- first line is section number only, for example `01`
- second line is exactly a concise four-character Chinese label when possible
- active button fill `amber`, active text `base`, active border transparent
- inactive button fill `panel`, inactive text `muted`, border `line`
- all buttons keep identical width, height, y-position, border, and text positions
- if section count differs, recompute `NAV_W` and `NAV_GAP` to keep all modules inside `x=590..1226`; do not wrap to a second row

Tongji logo lock:

| Token | Value |
|---|---:|
| asset | `references/style-samples-v2-20260606/assets/tongji-logo.jpg` |
| `TONGJI_LOGO_X` | `1030` |
| `TONGJI_LOGO_Y` | `24` |
| `TONGJI_LOGO_W` | `184` |
| `TONGJI_LOGO_H` | `52` |
| fit | `contain` |

For Tongji-specific decks, use this logo asset and geometry consistently on all pages that show the upper-right logo. The logo height is locked to the navigation-button height. Do not use per-template logo media, hand-drawn substitutes, recolored variants, or uneven slide-by-slide placement unless the user explicitly changes the Tongji logo lock.

## 6. Default Page Types

### Cover

Use a large editable title on the left and an independent source visual on the right. The right visual is mandatory: paper decks use a real paper figure/table/chart when available; project decks use a real screenshot/chart/photo from the project/report folders when available. If no real source asset exists, use a local partial AI/editorial visual, but never leave the cover as icon-only decoration or a blank panel.

| Element | Geometry |
|---|---|
| right visual | `x=650, y=76, w=570, h=360`, no label, no frame if cover illustration |
| accent bar | `x=54, y=82, w=84, h=6`, amber |
| course/theme text | `x=54, y=104, w=420, h=30`, size `22`, amber |
| title line 1 | `x=54, y=150, w=590, h=64`, size `56` |
| title line 2 | `x=54, y=220, w=480, h=66`, size `58` |
| title line 3 | `x=54, y=288, w=520, h=66`, size `58` |

Presenter on cover uses `方正小标宋简体`, not title font. Title text remains editable even if the cover visual is AI-generated. If the cover uses a real paper/project image, insert it with contain/fit-complete placement and a concise caption.

### Directory

| Element | Geometry |
|---|---|
| `目录` | `x=58, y=44, w=220, h=78`, size `66`, `微软雅黑` bold |
| `CONTENTS` | `x=64, y=136, w=130, h=18`, size `11`, amber |
| vertical divider | `x=284, y=64, w=2, h=596`, line color |

Directory entries use descriptive chapter titles. Do not force them into four characters.

### Section Divider

| Element | Geometry |
|---|---|
| nav | standard body navigation |
| section number | `x=58, y=76, w=132, h=100`, size `82`, amber, vertically middle |
| section title icon | `x=204, y=95, w=56, h=56`, amber Lucide badge |
| section title | `x=278, y=76, w=606, h=100`, size `64`, `微软雅黑` bold, vertically middle |
| summary | `x=64, y=188, w=1060, h=42`, size `28`, `微软雅黑` bold |
| rule | `x=62, y=248, w=1120, h=2` |
| talking points | start around `y=292`, row gap about `130` |

The section number, title icon, and title must read as one aligned header row. Use concise points; do not force card grids unless the material needs grouped cards. If talking-point icons are used, place them directly to the left of the point title, not below the number or in an isolated lane.

### Body

Every body page has exactly:

- one section/chapter title in the upper left
- one formal page subtitle below it
- standard right-top navigation
- standard top rule and bottom rule

No second explanatory subtitle line is allowed. Put explanations in the body content.

Default accepted body-page layout families:

- evidence split: large real/source image or chart on one side, dense table/callout/process evidence on the other
- process flow: visible arrows, enough arrow lanes, no hidden or clipped connectors
- results page: one dominant chart/table plus compact interpretation block
- implementation page: code/module table plus ordered process rows
- summary page: two real evidence images or one evidence table plus conclusion panel

Do not reuse a generic empty card grid when the slide should explain implementation order, evidence, or results.

### Thank-You

| Element | Geometry |
|---|---|
| accent bar | `x=520, y=94, w=240, h=6`, amber |
| topic title | `x=150, y=138, w=980, h=56`, size `36`, centered |
| rule | `x=54, y=220, w=1172, h=2` |
| thanks text | `x=90, y=286, w=1100, h=96`, size `72`, centered |
| presenter | `x=420, y=408, w=440, h=40`, size `28`, centered |
| closing text | `x=390, y=472, w=500, h=44`, size `32`, centered muted |
| course/topic label | `x=430, y=548, w=420, h=34`, size `24`, centered amber |

No card or frame around presenter/closing information.

## 7. Components

### Icon System

Default academic/engineering decks should include a restrained icon system. Use one coherent line-icon family across the whole deck. The default Shen-PPT icon family is the built-in Apple-style pure rounded SVG set at `references/icons/apple-svg/`; use Lucide only when a required semantic icon is missing from the built-in set or when the user explicitly selects Lucide. Icons are governed components, not decoration.

Built-in Apple-style SVG icon lock:

| Token | Value |
|---|---|
| asset root | `references/icons/apple-svg/` |
| generator | `scripts/generate-apple-svg-icons.py` |
| manifest | `references/icons/apple-svg/manifest.json` |
| preview | `references/icons/apple-svg/contact-sheet.png` |
| generated SVGs | `references/icons/apple-svg/generated/*.svg` |
| default style | pure rounded line SVG, no background fill |
| default color | `shen-blue` / `#58C4D8` |
| default SVG size | `64x64` viewBox |
| default stroke | `3.4` |
| default PPT insertion | independent SVG image/vector object, not a full-slide raster |

To regenerate the icon batch in another deck color, run:

```powershell
python scripts/generate-apple-svg-icons.py --color "#005BAC" --color-name tongji-blue
```

The generator intentionally writes stable filenames such as `target.svg`, `code.svg`, and `chart.svg`. Do not create per-slide random filenames; stable names make PPT generation deterministic.

Built-in icon semantic map:

| Icon | Use For |
|---|---|
| `target` | target, detection, tracking |
| `code` | code, implementation, module |
| `cpu` | hardware, compute, embedded device |
| `database` | data, storage, dataset |
| `network` | network, connection, communication |
| `chart` | result, metric, statistics |
| `camera` | vision, image, camera |
| `experiment` | experiment, validation, testing |
| `route` | process, path, steps |
| `shield` | safety, stability, protection |
| `terminal` | terminal, command, runtime |
| `document` | report, document, material |
| `presentation` | presentation, defense, display |
| `team` | team, members, collaboration |
| `cloud` | cloud, service, deployment |
| `robot` | robot, intelligence, automation |
| `device` | device, physical object, hardware |
| `layers` | architecture, layers, modules |
| `algorithm` | algorithm, model, inference |
| `spark` | highlight, innovation, key point |

| Role | Default |
|---|---|
| icon family | Shen-PPT Apple-style pure rounded SVG |
| fallback family | Lucide line icons only when built-in semantic icon is missing |
| stroke width | `3.4` for source SVG; scale visually by size in PPT |
| primary icon color | `blue` |
| emphasis icon color | `amber` |
| neutral icon color | `muted` |
| normal inline icon size | `20px` |
| icon-to-text gap | `8-10px` |
| section divider badge | `56px` outer badge, `44px` icon area, amber |
| evidence/image label icon | `20px`, blue, placed before the label text |
| step/card icon | `20px`, blue, left of the card title |
| process-card icon | `22px`, blue, left of the process title |
| horizontal-flow icon | `24px`, blue, immediately before row title |
| metric-card icon | `18px`, blue, left of the metric label |
| status/conclusion icon | `20px`, amber only for real emphasis or status |

Allowed icon roles:

| Role | Allowed | Default Geometry |
|---|---|---|
| section-divider title badge | yes | badge `56x56`, icon centered/inset `6px`, placed before section title |
| evidence/image label | yes | `x=labelX, y=labelY+8, size=20`, text starts `36px` after label left |
| process/step row | yes | icon immediately before title, gap `8-10px`, vertically centered with title |
| metric label | yes | icon `18px`, label starts `26px` after icon left |
| architecture/module label | yes | icon `20px`, left-attached to module title |
| conclusion/status cue | conditional | icon `20px`, amber only when the cue is a true status/result |
| directory entry | no | no icon by default |
| ordinary paragraph/body bullet | no | no icon |
| plain subtitle/header text | no | no icon |
| thank-you page | no | no icon |
| decorative empty space | no | no icon |

Rules:

- icons must be semantic identifiers, not decoration or filler
- use icons only for the allowed roles above
- directory pages use no icons by default; keep the directory clean with numbers, titles, and descriptions
- icon placement is constrained: prefer left of the related title/text, tightly attached; right-attached or below-centered placement is allowed only when it is repeated by the whole component family
- same-role icons must keep the same exact size, color token, x/y offset, text gap, and alignment across the whole deck
- batch consistency is mandatory: if one item in a same-role group has an icon, every peer item in that group must have an icon; if icons are unnecessary, remove them from the whole group
- avoid isolated one-off icons on body slides, summary panels, thank-you pages, and ordinary text blocks
- do not mix multiple icon styles in one deck
- do not use unofficial brand/logo-like icons, mascot marks, app icons, or school logos as generic decoration
- do not add icon backgrounds, rounded-square fills, color blocks, or button-like containers unless the locked template already uses that component family and the user approves it
- prefer the built-in Apple-style SVG set for Shen-PPT-generated decks; use stable manifest names and semantic tags to select icons
- when using a non-default color, regenerate the built-in SVG batch once for the deck color and record the color name/hex in the design lock and asset manifest
- if downloading icons from iconfont.cn or another site, record source package, license/provenance, local asset path, color, size, and slide usage in an icon manifest
- if no built-in, verified external, or Lucide icon fits the meaning, omit the icon instead of inventing a pseudo-icon
- keep icons independently selectable as separate image/vector-like objects when practical; never bake them into full-slide screenshots
- if an icon makes a dense slide crowded, remove the icon before shrinking proof images or source text
- if an icon has no clear semantic label or cannot be applied consistently to the whole peer group, omit it

### Panel

Default panel:

- geometry: `roundRect`
- radius follows the presentation engine default; keep visual radius small
- fill `panel`
- border `line`, width `1`

Dense panel:

- fill `panelDark`
- border `line`, width `1.2`

### Image Card

| Token | Value |
|---|---:|
| fill | `imagePanel` |
| border | `imageLine`, width `0.8` |
| pad | `6` |
| label height | `36` |
| label icon | `x + pad + 8`, `y + 8`, size `20`, blue |
| label text | `x + pad + 36`, `y + 4`, `w - pad*2 - 40`, `30` |
| label size | `20` |
| label color | `amber` |

Real screenshots, charts, wiring photos, and tables use contain/fit-complete placement. Never use cover/crop for real evidence unless the user explicitly requests it.

Image caption lock:

- every inserted figure, screenshot, chart, table image, AI local insert, or representative image needs a visible caption
- caption text size is normally `10-12px` for compact evidence captions and `11-13px` for dominant figures
- captions are placed directly under the image region inside the same visual block and use muted text
- visible captions should be concise; long source captions belong in the asset manifest or slide card
- a slide with an image but no visible caption is a QA failure unless the user explicitly asks for caption-free images

### Data Table

- outer panel fill `panelDark`
- header text color `amber`, bold
- default header size `12-13`
- default body size `10-12`
- row height should be large enough that all text has visible vertical padding
- columns should use fixed widths; do not let columns auto-drift page by page
- paper/project experiment pages should use editable tables for core experiment summaries rather than explaining all results as bullets
- core experiment tables should include source-grounded fields such as scenario, metric, method/result, and interpretation/notes
- if a paper has multiple experiment settings, create one compact summary table and pair it with the real figure/chart; do not leave the figure without a table when the conclusion depends on experimental comparison

### Step Card

| Element | Default |
|---|---|
| fill | `panelDark` |
| number | `x+16`, title lane, size `22`, `Times New Roman`, blue |
| title | `x+72`, title lane, size `21`, `方正小标宋简体` |
| detail | `x+16`, below title, size `15`, muted, vertically middle |

Cards with the same role must use the same fill, border, number color, title color, and sizing.

Icon placement override: when step cards use icons, place the icon on the left side of the title, tightly attached to the text. Default geometry is `icon x+68, titleY+3, size=20`, then title at `x+96`. Do not place step-card icons as loose top-right badges. If one step card in a peer batch has an icon, every peer step card in that batch must have one; otherwise remove icons from the whole batch.

### Metric Card

| Element | Default |
|---|---|
| value | `x+14, y+8, w-28, h=28`, size `25`, `Times New Roman`, amber |
| icon | `x+14, y+43, size=18`, blue |
| label | `x+40, y+40, w-50, h=22`, size `13`, muted |

Metric-card icons are allowed only as a complete batch. Put each icon directly to the left of its label; do not place metric icons as loose corner badges.

### Process Card

| Element | Default |
|---|---|
| fill | `panelDark`, border `line` width `1.2` |
| number | `x+16, y+18, w=42, h=28`, size `25`, blue |
| title | `x+66, y+16, w=w-88, h=34`, size `28`, `方正小标宋简体` |
| module name | `x+18, y+68, w=w-36, h=24`, size `17`, `Times New Roman` |
| detail | `x+18, y+102, w=w-36, h=h-126`, size `16`, muted |

Icon placement override: when process cards use icons, place the icon on the left side of the process title, tightly attached to the title. Default geometry is `icon x+66, y+23, size=22`, then title at `x+96`. Do not place process-card icons as loose top-right marks.

### Horizontal Flow Row

| Element | Default |
|---|---|
| number | `x+20, cy-15, w=46, h=30`, size `25`, blue |
| title | `x+76, cy-18, w=150, h=36`, size `27`, `方正小标宋简体` |
| separator | `x+236, y+16, w=1.4, h=h-32`, line color |
| detail | `x+258, y+16, w=w-284, h=h-36`, size `16`, muted |

Use this for horizontal process explanations. Keep text vertically centered.

Icon placement override: when horizontal flow rows use icons, place the icon immediately before the row title. Default geometry is `icon x+76, cy-12, size=24`, then title at `x+110`. Every row in the same flow must either use an icon or omit icons together.

### Arrows

- horizontal arrow: geometry `rightArrow`, default `w=34, h=22`, fill `amber`, no border
- vertical arrow: geometry `downArrow`, default `w=22, h=24`, fill `amber`, no border
- stacked vertical flows reserve `30-40px` lane between boxes for the arrow
- arrows must remain visible and not collide with card borders

## 8. Density Rules

| Rule | Threshold |
|---|---|
| normal body content bottom | should reach `y=640-660` |
| standard content bottom target | `y=660` |
| bottom rule | `y=670` |
| sparse warning | main content ends above `y=620` without intentional reason |
| card fill warning | large card has text pinned to top with empty lower half |
| image scale warning | evidence image is readable only as decoration |
| text overflow error | text touches/crosses card boundary or overlaps another object |

When a slide feels sparse, enlarge real evidence images, increase card height, add source-grounded detail, or simplify layout. Do not add decorative filler.

## 9. Style Sample Production

The style sample library is a parameterized skin system. The OrangePi v9 highest reference is separate and must not be treated as a sample template. Each style sample deck has exactly four editable PPT pages:

1. cover page
2. directory page
3. section divider page
4. body/evidence page

This four-page order is mandatory for every Shen-PPT visual sample deck. A cover plus three topic/content pages is not a valid sample deck, even if the topic text is useful or the palette looks acceptable.

All style sample decks must keep these shared parameters:

- 1280x720 design coordinates
- top rule around `y=100`, body start around `y=112`, content bottom near `y=660`, bottom rule at `y=670`
- directory entries use descriptive titles, not forced four-character labels
- right-top navigation uses two lines: number plus four-character label
- body slide has one section title and one formal subtitle
- section divider has large aligned section number/title and concise talking points
- image areas contain real/example images or template assets, never blank placeholders
- image placement uses contain/fit-complete
- icons are semantic, batched, left-attached where practical, and omitted from directory pages
- body page includes visible arrows for process relationships
- peer cards/rows have uniform fill and color unless an active navigation state is being shown

Style sample script paths must be self-contained under `references/style-samples-v2-20260606/`. Do not hard-code a temporary thread output directory as the source of assets, slides, previews, layouts, or final sample decks.

Tongji sample lock:

| Style slug | Published editable sample deck |
|---|---|
| `tongji-blue-clean` | `references/style-samples-v2-20260606/sample-decks/Shen-PPT同济样板_tongji-blue-clean.pptx` |

For any Tongji deck, the execution lock must name the selected Tongji style slug and the published sample deck path inside this skill. A generic blue-white style or a manually placed Tongji logo is not enough to satisfy the Tongji style rule.

The complete slug-to-PPTX mapping is in `references/style-samples-v2-20260606/sample-deck-map.json`. When a style slug is used, resolve the sample PPTX from that map instead of guessing filenames or trusting any legacy encoded filename display.

Runtime sample-deck path lock:

- Runtime references must resolve from this skill directory, especially `references/style-samples-v2-20260606/sample-decks/`.
- `D:\shen\test\skill-manage\shen-ppt` is a management mirror/backup workspace only. Do not use it as the runtime source of style sample PPTX decks unless the user explicitly asks to operate on the management mirror.
- If a sample PPTX is missing from `references/style-samples-v2-20260606/sample-decks/`, stop and report the missing skill reference instead of silently falling back to the management mirror.

## 10. Productized Production Parameters

Every generated deck should be driven by structured slide cards, a locked style kit, and a QA scorecard.

Skill runtime lock:

- Shen-PPT is used from a Codex conversation through the `shen-ppt` skill.
- The skill must use the shared engine scripts and parameter rules whenever practical.
- The skill expresses gates as Chinese chat confirmations and must preserve the required approvals: outline approved, template/style locked, four-sample pages approved, final deck generated, QA passed or repaired, final documents generated.

Code engine lock:

- Default deterministic helper: `scripts/shen_ppt_engine.py`
- Default PowerPoint COM renderer: `scripts/build_shen_ppt_com.ps1`
- Engine test file: `tests/test_shen_ppt_engine.py`
- Shen-PPT should treat the slide-card JSON as the stable boundary between material understanding and PPT rendering.
- Shen-PPT should treat preview PNGs, QA reports, speaker scripts, and likely-Q&A Markdown as standard artifacts, not optional side effects.
- For Markdown/text/PDF sources, the engine should create `{deck-title}_slide_cards.json` before deck construction whenever practical.
- The COM renderer consumes slide cards and must generate editable PowerPoint objects using the locked parameter table.
- The COM renderer must accept `-PreviewDir` and export slide PNG previews for QA whenever practical.
- The COM renderer must set `EntryEffect = none`, remove object animation sequences, disable timed advance, and leave click advance only.
- The COM renderer must set visible text fonts by role: `Microsoft YaHei`, `方正小标宋简体`, and `Times New Roman`; no visible text should remain in Aptos, Calibri, DengXian, or accidental fallback fonts after QA.
- The COM renderer must stay UTF-8 BOM safe for Windows PowerShell and avoid fragile unescaped Chinese literals in parser-sensitive places.
- The code engine is a deterministic assistant, not a gate bypass. It may generate slide cards, previews, and Markdown drafts, but it cannot skip Stage 3, Stage 4, or Stage 6 approvals in normal Shen-PPT runs.

PDF and paper extraction lock:

- Remove or ignore PDF front matter from visible content: journal headers, page headers, page numbers, author lists, affiliations, `Senior Member IEEE`, `Fellow IEEE`, references, and repeated paper title strings.
- Do not paste broken double-column extraction fragments into visible slide text or final Markdown, for example merged words, interrupted hyphenation, or cross-column sentence splices.
- If a raw sentence is needed for traceability, store it as slide-card source evidence or notes, then rewrite the visible slide copy in concise formal Chinese.
- For paper explanation decks, extract the real paper structure when available: abstract/problem, key definitions/modeling, problem formulation, method/module design, experiments/setup/metrics, conclusion/limitations.
- For paper explanation decks, extract real paper figures/tables/charts from the PDF and assign them to relevant slide cards before deck construction. Cover, evidence, method, and results pages should use those real assets when available.
- The visible PPT should teach the paper, not display raw extracted paragraphs. Use Chinese claims, process diagrams, architecture maps, matrices, and metric cards to explain the structure.

Project asset extraction lock:

- For project/report/code decks, recursively scan the supplied folders for real screenshots, charts, terminal captures, device photos, UI screenshots, wiring photos, result tables, and exported images.
- Do not skip common asset folders such as `assets`, `images`, `figures`, `screenshots`, `results`, or `report` when looking for source visuals.
- Use project visuals before generic icons, AI visuals, or placeholder diagrams.
- The source/asset manifest or slide cards must identify which real images were used on which pages.

LaTeX and formula lock:

- Default local LaTeX-PPT root is `D:\shen\test\latex-ppt`; the COM renderer may load `latex.ppam` from that folder when PowerPoint allows it.
- The original LaTeX/source formula must be preserved in slide cards or notes for traceability.
- Visible slide content must show either a converted editable PowerPoint equation or a clean readable display formula/summary.
- PowerPoint COM equation insertion must select the current slide and then select the seed textbox's `TextFrame.TextRange` before `EquationInsertNew`. Selecting the shape itself is a known failure mode.
- The COM renderer should enable LaTeX mode on the same slide that receives the first equation, using a temporary tiny textbox; do not use a pre-inserted scratch slide to enable LaTeX mode in long decks.
- Converted equations must carry a `ShenPPT_LatexSource` tag containing the original source expression. Formula-heavy deck QA should reopen the PPTX and count these tags against the slide-card `latex` count.
- Formula-heavy paper decks should include multiple formulas or formula summaries where they clarify the paper: objective/modeling, method/sampling, and metric/risk/evaluation are the default minimum roles.
- If automated equation insertion fails because PowerPoint rejects the formula state or the local macro requires interactive input, do not show raw broken LaTeX with long backslash/braces syntax on the slide; use the clean display formula, record the fallback in QA, and do not call the deck final until the fallback is accepted or repaired.

Mandatory Startup Contract:

- load `SKILL.md`
- load `references/parameter-spec.md`
- load `references/highest-references/orangepi-defense-final-v9-20260607/accepted-standard.md`
- when a style or Tongji deck is requested, load `references/style-samples-v2-20260606/style-manifest.json`, `references/style-samples-v2-20260606/sample-deck-map.json`, and the matching published editable sample deck
- create a Shen-PPT execution lock before outline writing, sample generation, or full PPT production
- do not approximate a requested sample style from memory if the sample deck path cannot be found

Fixed production pipeline:

| Stage | Required Output | Confirmation |
|---|---|---|
| 0 activation | Shen-PPT execution lock with loaded references | show only |
| 1 intake | theme/material/output/style summary | ask if required fields missing |
| 2 material reading | material findings and asset/evidence list | ask if critical facts missing |
| 3 outline only | page-by-page outline and asset/content plan only | **required user approval** |
| 4 visual style or template lock | if user template is specified, lock that PPTX as the base deck; otherwise show visual options, recommend one, and lock the chosen sample PPTX as the base deck | **required approval or recorded explicit template lock** |
| 5 design lock | parameterized design lock, copied layout mapping, and QA checklist | show only |
| 6 four sample pages | cover, directory, section divider, body | **required user approval** |
| 7 full deck | editable PPTX | no skip allowed before Stage 6 approval |
| 8 QA and repair | preview/contact sheet and QA result | repair before delivery |
| 9 final documents | speaker-script Markdown and likely-Q&A Markdown | after final PPTX only |
| 10 delivery | PPTX + two Markdown files | complete |

Gate isolation lock:

- Stage 3 is outline only. It must not include visual palette, typography, style recommendation, sample deck path, template choice, web preflight, design lock, sample pages, or full-deck promises.
- Stage 4 is visual style/template selection only. It must not restate the full outline, generate sample pages, or build the full deck.
- If a template is already specified by the user, Stage 4 must lock that template and must not output candidate styles. Use the wording `不再推荐其他风格`.
- If no user template is specified and the user chooses a Shen-PPT style, Stage 4 must lock the exact sample PPTX as the base deck. The selected sample deck must be filled/extended directly, not recreated visually.
- Required gates are independent: Stage 3 outline approval, Stage 4 visual/template lock, and Stage 6 four sample pages approval.
- If a response combines material findings, outline, visual style, web research/preflight, and later-stage promises into one approval block, it fails Shen-PPT and must be regenerated at the current gate.

Forbidden jumps:

- Stage 0 -> Stage 7 is forbidden
- Stage 1 -> Stage 7 is forbidden
- Stage 2 -> Stage 7 is forbidden
- Stage 3 -> Stage 5 is forbidden without Stage 4 visual/template lock
- Stage 3 -> Stage 6 is forbidden without Stage 4 visual/template lock and Stage 5 design lock
- Stage 4 -> Stage 7 is forbidden without Stage 6 four-page sample approval
- do not generate full deck before Stage 3 outline approval, Stage 4 visual/template lock, and Stage 6 sample approval
- Stage 3 outline approval is mandatory
- Stage 4 visual/template lock is mandatory; it can be either explicit user approval of a style choice or a recorded lock of a template the user already specified
- Stage 6 sample approval is mandatory
- do not treat `继续`, `直接做`, `你看着办`, material paths, execution lock, or design lock as approval for a skipped gate
- the execution lock is not approval
- material paths are not approval
- do not generate final Markdown documents before the final PPTX has been QA-checked
- do not replace `presentations:Presentations` with `python-pptx`, HTML, SVG, full-slide screenshots, or another PPT construction path while still claiming Shen-PPT compliance
- PowerPoint COM is the only official fixed fallback when `presentations:Presentations` is unavailable; record it as `PowerPoint COM official fallback` and keep the same Stage 0-10 process, parameters, editability, previews, QA, no-animation rule, and final package
- do not ask the user to approve routine PowerPoint COM fallback; ask only if both standard builders are unavailable or the user wants an explicitly nonstandard path
- do not produce a deck that only imitates the locked template/sample style; each produced slide needs a source template/sample layout trace

Material boundary lock:

- use user-provided materials as the source of truth
- do not search the web, add outside papers, add outside claims, or expand the evidence base unless the user explicitly approves external research for that deck
- if external research is approved, record it in the execution lock and evidence plan
- web research never replaces reading the user's files

Canonical output format:

| Stage | Required Header | Required Status |
|---|---|---|
| 0 | `## Shen-PPT Execution Lock` | `Pipeline Stage: 0 / Activation` |
| 3 | `## Shen-PPT Outline` | `Pipeline Stage: 3 / Awaiting User Approval` |
| 4 | `## Shen-PPT Visual Style Selection` | `Pipeline Stage: 4 / Awaiting User Approval` |
| 5 | `## Shen-PPT Design Lock` | `Pipeline Stage: 5 / Design Locked` |
| 6 | `## Shen-PPT Four Sample Pages` | `Pipeline Stage: 6 / Awaiting User Approval` |
| 8 | `## Shen-PPT QA Result` | `Pipeline Stage: 8 / QA` |
| 10 | `## Shen-PPT Final Delivery` | `Pipeline Stage: 10 / Complete` |

Canonical file naming:

| Artifact | Filename |
|---|---|
| PPTX | `{deck-title}.pptx` |
| speaker script | `{deck-title}_讲稿.md` |
| likely Q&A | `{deck-title}_问答.md` |
| review folder | `{deck-title}_review` |
| contact sheet | `{deck-title}_contact_sheet.png` |
| design lock | `{deck-title}_design_lock.md` |
| slide cards | `{deck-title}_slide_cards.json` |
| asset manifest | `{deck-title}_asset_manifest.json` |
| QA report | `{deck-title}_qa.md` |

Canonical Markdown formats:

- speaker script uses one `#` title, then `## 第 01 页：标题` sections
- likely Q&A uses one `#` title, then `## Q1：问题` and `A：答案`
- no repeated blank lines
- no boilerplate preface
- no generated-document explanation

Every conversation must use these same headers, field names, artifact names, and confirmation messages. Do not invent alternate wording, merge headers, or omit stage/status fields.

Chinese approval format:

- Keep fixed markdown headers for machine recognition, but use Chinese field labels in chat approval blocks.
- Do not expose long English field dumps to the user. Put detailed slide cards, QA tables, and manifests in files when needed.
- Stage 3 approval block ends with `请先确认 PPT 大纲，确认后我才会进入模板和视觉锁定`.
- Stage 4 template-lock block ends with `请确认是否按这个模板扩充，确认后我再生成四页样板`.
- Stage 4 no-template style-selection block ends with `请确认视觉风格和模板方向，确认后我才会进入设计锁和四页样板制作`.

Slide-card fields:

| Field | Required Content |
|---|---|
| `purpose` | why this slide exists in the defense |
| `claim` | one audience-facing statement the slide proves or explains |
| `sourceEvidence` | report/code/image/table/screenshot/metric used as evidence |
| `layoutFamily` | one finite layout type, not freehand placement |
| `visualAsset` | real image/table/chart/code/AI local insert or `none` |
| `latex` | optional list of original formula source plus clean display expression |
| `tables` | optional list of editable table data with kind, title, headers, and rows |
| `speakerNote` | optional private presenter note, never visible on slide |
| `qaRisk` | likely failure: sparse, crowded, weak evidence, tiny image, overflow, alignment, font, or asset provenance |

Default layout families:

- `cover`
- `directory`
- `section divider`
- `evidence split`
- `process flow`
- `results dominant`
- `architecture map`
- `comparison matrix`
- `code/module walkthrough`
- `timeline`
- `summary`
- `thanks`

Style-kit fields:

- palette tokens and accent roles
- font roles and fallback policy
- navigation geometry and active state
- chrome constants: top rule, bottom rule, footer, page number
- image-card treatment and contain/fit-complete rule
- icon family, size, color, placement, and batch policy
- logo/template asset policy
- no-animation rule

Execution-lock required fields:

| Field | Required Content |
|---|---|
| `theme` | one of `组会汇报`, `课程答辩`, `论文答辩` |
| `materialPaths` | concrete files/folders provided by the user |
| `loadedReferences` | `SKILL.md`, `references/parameter-spec.md`, highest reference `accepted-standard.md`, plus any style manifest/sample |
| `styleSlug` | selected style slug or `default` |
| `sampleDeckPath` | exact published editable sample deck path when a style sample is requested |
| `samplePageTypes` | fixed order `cover`, `directory`, `section divider`, `body` |
| `finalPackage` | PPTX, speaker-script Markdown, likely-Q&A Markdown |
| `pipelineStage` | current stage number and next required confirmation gate |

QA scorecard dimensions:

| Dimension | Pass Standard |
|---|---|
| content grounding | every key claim ties to source material or is marked as an assumption |
| hierarchy | title, subtitle, evidence, and conclusion are visually ordered |
| density | normal body content reaches the locked lower target without decorative filler |
| alignment | repeated chrome, navigation, cards, and image labels align across pages |
| evidence visibility | screenshots, charts, tables, and photos are large enough to inspect |
| image completeness | real assets use contain/fit-complete and are not unintentionally cropped |
| editability | text, shapes, connectors, tables, and icons are independently editable where practical |
| typography | Chinese/English/number font roles follow the lock |
| user font authority | user-specified fonts override template/default fonts; visible text does not retain unintended PowerPoint defaults such as Aptos or Calibri |
| icon role whitelist | icons appear only in approved semantic roles, never as decoration |
| icon geometry | same-role icons use the same locked size, color, gap, x/y offset, and alignment |
| icon consistency | same-role icon batches are complete or omitted together |
| no-animation | no object build effects, automatic reveal timings, or slide transitions |
| audience-facing copy | visible text contains no presenter reminders or internal process notes |

## 11. Copy Parameters

- remove Chinese full stops `。` from formal Chinese slide copy
- use short formal subtitles with no comma
- body text should usually be `1-3` compact sentences or `2-4` source-grounded bullets per content block
- no internal presenter notes or process reminders on slides
- no generic filler terms such as `形成`, `赋能`, `闭环`, `支撑`, `可量化`, `可复现`, `体系化`, `场景化`, `全流程`, `落地`

## 12. No-Animation Parameters

Shen-PPT standard output is a static editable defense deck. Do not add animations, object build effects, automatic reveal timings, or slide-transition effects by default.

Static presentation lock:

- one presenter click advances to the slide
- the next slide appears complete immediately
- no slide should require repeated manual clicks to reveal bullets, cards, figures, arrows, tables, charts, or conclusions
- no slide should rely on automatic effects to become complete
- every slide must remain correct when exported to PDF, printed, or opened in a viewer that ignores animations

Forbidden by default:

- click-by-click bullet reveal inside one slide
- automatic reveal sequence inside one slide
- fly-in, bounce, spin, flip, random transition, long zoom, per-letter animation
- motion paths for evidence screenshots, result charts, tables, or real photos
- `Fade`, `Morph`, or any other slide transition as a standard deck feature
- using animation to hide incomplete content, weak hierarchy, or overloaded slides

## 13. Final Deliverable Package Parameters

Every completed Shen-PPT deck must finish as a compact core package:

| Deliverable | Required | Format | Placement |
|---|---|---|---|
| editable deck | yes | `.pptx` | final output folder |
| speaker script | yes | `.md` | next to PPTX |
| likely Q&A | yes | `.md` | next to PPTX |

Speaker-script Markdown rules:

- generate after the final PPTX is complete, using the final slide order, visible slide content, private PowerPoint notes when present, and original materials
- organize by slide number/title
- write presenter-ready language that can be spoken aloud
- keep each slide entry compact and source-grounded
- no preface, no generation explanation, no repeated blank lines, no design commentary

Likely-Q&A Markdown rules:

- generate from source materials, final slide claims, metrics, methods, implementation details, limitations, and expected reviewer concerns
- include direct compact answers
- distinguish facts from assumptions or future work
- no invented metrics, no generic confidence language, no unrelated questions
- no preface, no generation explanation, no repeated blank lines

Final package naming defaults:

| Token | Default |
|---|---|
| PPTX | `{deck-title}.pptx` |
| speaker script | `{deck-title}_讲稿.md` |
| likely Q&A | `{deck-title}_问答.md` |

Review artifacts such as contact sheets, slide-card JSON, preview PNGs, asset manifests, and QA records may be stored in a review folder, but they do not replace the two required Markdown files.

## 14. QA Gates

Before delivery, run or manually confirm:

- slide count equals approved outline
- PPTX is non-empty and opens as editable content
- final speaker-script Markdown exists next to the PPTX
- final likely-Q&A Markdown exists next to the PPTX
- Markdown files are compact: no boilerplate preface, no generation explanation, and no repeated blank lines
- Markdown content is grounded in the final PPT and source materials
- execution lock exists and lists loaded references
- pipeline stages were followed in order, with no forbidden jump
- user approval for Stage 3 outline-only gate is recorded before template/style lock
- Stage 4 visual/template lock is recorded before design lock and sample pages
- user approval for Stage 6 four sample pages is recorded before full deck production
- if a style or Tongji sample is requested, execution lock lists the selected style slug and exact sample deck path
- four visual sample pages use fixed page types: cover, directory, section divider, body
- sample deck page 2 contains `目录`
- sample deck page 3 is a section divider rather than a body/content page
- sample deck page 4 contains right-top module navigation
- every normal content slide has a slide card with `purpose`, `claim`, `sourceEvidence`, `layoutFamily`, `visualAsset`, and `qaRisk`
- style kit fields were locked before full production
- no full-slide screenshot or full-slide AI page is used
- all navigation buttons follow the fixed two-line format
- repeated elements align and use the same geometry
- icons appear only in approved roles: section-divider title badge, evidence/image label, process/step row, metric label, architecture/module label, or true conclusion/status cue
- no icons appear on directory pages, thank-you pages, plain subtitles, ordinary paragraphs, or decorative empty space by default
- same-role icons keep the same exact size, color token, gap, offset, and alignment across the deck
- same-role icon batches are either complete or omitted together
- no Chinese full stops in formal Chinese slide copy
- no text overlap or text overflow
- no visible raw broken LaTeX strings on slides; formulas are converted equations or clean display formulas
- formula-heavy decks have `ShenPPT_LatexSource` tags for converted equations; the tag count should match the expected slide-card formula count unless a recorded fallback was accepted
- formula-heavy paper decks include objective/modeling, method/sampling, and metric/risk/evaluation formulas when the source contains or implies them
- core experiment comparisons are represented as editable table objects where relevant, not only prose bullets
- cover page has a right-side visual asset
- every inserted image/figure/chart/table/local AI visual has a visible caption
- paper decks use extracted real PDF figures/tables/charts when available
- project decks use real local screenshots/charts/photos from supplied folders when available
- real images/charts/tables are complete, not cropped
- evidence images are large enough to inspect
- process arrows are present, visible, and correctly shaped
- peer groups use uniform color unless a real active state is intended
- final previews/contact sheet meet the highest-reference density and polish level without copying its OrangePi-specific content or page composition
- style sample decks regenerate from the local style-sample scripts and local style-sample assets
- style sample overview images are refreshed after rebuilding the sample PPTX files
- no object build animations, automatic reveal timings, or slide transitions are present unless the user explicitly cancels the no-animation rule for a special one-off deck
- source/asset manifest records real source images, downloaded icons, logos, template assets, and AI local inserts
- speaker notes, if present, are private PowerPoint notes and do not appear on the visible slide
