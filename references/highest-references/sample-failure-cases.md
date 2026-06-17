# Shen-PPT Sample Failure Cases

Use these cases as negative examples when checking whether a draft actually followed Shen-PPT.

## Case: Four Topic Pages Mistaken For Four Sample Pages

Observed file: `D:\shen\research\shuqi\bishe_topic_replan_2026\ppt\topic_replan_sample_4pages_tongji_blue_v2.pptx`

Why it fails:

- It contains a cover plus three topic/content slides, not the required four sample page types
- Page 2 is an ordinary content slide, not a directory page with `目录`
- Page 3 is an overview/table content slide, not a section divider page
- Page 4 is another body/content slide, not the only required body-page sample
- It does not prove that the selected Tongji sample deck was loaded
- It uses a blue-white/Tongji-like visual treatment but does not satisfy the Shen-PPT startup contract or sample-page QA

Correct behavior:

- Before generating pages, create a Shen-PPT execution lock listing loaded references, selected style slug, sample deck path, material paths, and final package contract
- For Tongji blue, explicitly load and name the skill-internal sample deck path `references/style-samples-v2-20260606/sample-decks/Shen-PPT同济样板_tongji-blue-clean.pptx`
- Generate exactly four editable sample pages in this order: cover, directory, section divider, body
- Ask for user approval of the four-page visual lock before full deck generation

## Case: Stage 3 Mixed Outline And Visual Direction Dump

Observed behavior:

- A response outputs Stage 0 execution lock, Stage 1 intake, Stage 2 material findings, and Stage 3 all at once
- Stage 3 is titled `Shen-PPT Outline And Visual Direction`
- The same approval block includes page plan, real assets, AI assets, palette, typography, navigation, image treatment, and external/web preflight
- The user is asked to approve the outline and visual direction together

Why it fails:

- Stage 3 must be `## Shen-PPT Outline` only
- Stage 3 must not include visual style, palette, typography, template/sample deck recommendation, design lock, web preflight, or sample-page planning
- Visual style/template choice is a separate Stage 4 gate shown only after the user approves the Stage 3 outline
- External research/preflight is not allowed unless the user explicitly approves it for the deck
- Combining several gates makes the workflow non-machine-like and causes later stages to drift from the chosen template and style rules

Correct behavior:

- Stage 0 execution lock may be shown first
- Stage 1 and Stage 2 may be concise, but after material reading the next approval block must be only `## Shen-PPT Outline`
- Stop after asking: `请先确认 PPT 大纲，确认后我才会进入视觉风格和模板选择`
- After the user approves the outline, output `## Shen-PPT Visual Style Selection`
- Show 2-4 visual styles, recommend one, and provide the matching template/sample PPT path or overview preview
- Only after the user approves the visual style may the model create the design lock and four sample pages

## Case: User-Specified Template Ignored

Observed behavior:

- The user specified a PPT/PPTX template or a fixed visual sample
- The response still recommends unrelated visual styles or creates a new default-looking design
- The generated slides use approximate colors, lines, fonts, logos, or navigation instead of expanding from the actual template
- The approval prompt is a long English/status-heavy block that the user cannot quickly confirm

Why it fails:

- Explicit user constraints outrank Shen-PPT defaults and style samples
- A specified template must be treated as the source file, not as loose inspiration
- Stage 4 must become a template lock, not a style marketplace
- User-facing approval prompts must be concise Chinese by default
- Specified fonts must be enforced on visible editable text; default PowerPoint fonts or conflicting template fonts are QA failures

Correct behavior:

- Inspect the user-specified template and reuse its actual slides, masters, layouts, logo placement, color tokens, line rules, spacing rhythm, and component proportions
- Expand new pages from the closest existing template page/layout
- Keep the user's specified fonts by role across visible editable text
- In Stage 4, output only a short template lock block and say `不再推荐其他风格`
- Ask in Chinese: `请确认是否按这个模板扩充，确认后我再生成四页样板`
## Case: Sample Deck Treated As Inspiration Instead Of Base Deck

Observed behavior:

- The user selected a Shen-PPT style sample deck
- The generated PPT uses roughly similar colors or navigation but was rebuilt from blank slides
- Logos, line rules, spacing, module blocks, and page chrome drift from the sample deck
- The agent says it "referenced" or "matched" the template instead of filling/extending the real PPTX

Why it fails:

- A selected Shen-PPT sample deck is a locked base deck, not a mood board
- Recreating the look from memory causes font drift, logo drift, inconsistent spacing, and non-repeatable results
- Shen-PPT requires machine-like repeatability: the same prompt and same locked template should produce nearly identical layout grammar

Correct behavior:

- Resolve the selected style slug through `references/style-samples-v2-20260606/sample-deck-map.json`
- Open/copy the exact sample PPTX from `references/style-samples-v2-20260606/sample-decks/`
- Duplicate the closest sample page/layout for each new slide
- Replace only the content objects: text, images, tables, charts, diagrams, icons, and evidence assets
- Preserve masters, slide size, logo placement, navigation geometry, line rules, colors, spacing rhythm, and component proportions
- Record a slide-to-template layout trace in the design lock or QA artifacts

## Case: Font Lock Ignored

Observed behavior:

- The generated PPT contains visible text in Aptos, Calibri, DengXian, or arbitrary template fonts
- Chinese titles, body text, presenter name, module labels, English, and numbers use inconsistent fonts
- The agent says the template font was kept because it looked close enough

Why it fails:

- User-specified Shen-PPT fonts are hard constraints, not visual preferences
- Template fonts do not override explicit font instructions unless the user says so
- Mixed Chinese/English/number text must be split into runs or boxes when exact fidelity matters

Correct behavior:

- Use `微软雅黑` bold for cover title, directory title, section-divider number/title, and body big section title
- Use `方正小标宋简体` for body subtitles, presenter name, team members, body copy, card titles, module labels, and Chinese table/diagram text
- Use `Times New Roman` for English letters, code identifiers, formulas, page numbers, module numbers, chart/table numbers, and Arabic numerals
- Inspect text fonts before delivery when practical and treat unintended default fonts as QA failures
