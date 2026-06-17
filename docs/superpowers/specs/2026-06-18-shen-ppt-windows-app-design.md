# Shen PPT / 神了PPT Windows App Design

## Status

Date: 2026-06-18
Scope: MVP design for a fully local Windows installable desktop app.
Implementation status: design only. Do not start app code until this spec is approved.

## Product Goal

Shen PPT / 神了PPT is a Windows desktop application that turns the existing Shen-PPT skill pipeline into an installed local app. Users install it, open it from the desktop or Start Menu, select materials, confirm each required stage, and receive an editable PPTX plus a compact speaker script and likely Q&A document.

The app must not feel like a browser shortcut. It should open as a normal desktop window, run fully locally, and use the same generation rules as the `shen-ppt` Codex skill.

## Non-Negotiable Principles

- Fully local by default: no login, no upload, no cloud dependency, no remote database.
- Windows first: MVP targets Windows because PowerPoint COM and the local LaTeX-PPT workflow are Windows/Office dependent.
- Desktop app UX: installed app, app window, desktop icon, Start Menu entry, no external browser jump.
- Shared engine: the app and Codex skill must use the same production core where practical.
- Editable PPT first: final decks must use editable PowerPoint text, shapes, images, icons, equations, and tables where practical.
- Gate preservation: app UI must preserve Shen-PPT approvals instead of silently skipping them.
- No alternate PPT workflows: no HTML-PPT, PPT-master, `python-pptx`, or full-slide screenshot conversion as a compliant builder.

## Technical Choice

Use Electron for the installed Windows desktop shell, with local process calls to the existing Shen-PPT engine.

Recommended stack:

- Electron main process for native window, filesystem dialogs, process orchestration, and app packaging.
- Electron renderer for the step-by-step UI.
- Node IPC between renderer and main process.
- Existing Python and PowerShell scripts as the generation core:
  - `scripts/shen_ppt_engine.py`
  - `scripts/build_shen_ppt_com.ps1`
  - `scripts/generate-apple-svg-icons.py` where needed
  - `scripts/validate-repo.ps1` for development validation
- PowerPoint COM through the existing PowerShell renderer.
- Local LaTeX-PPT root configurable, defaulting to `D:\shen\test\latex-ppt` during development and to an app setting in release builds.

Rejected alternatives for MVP:

- Local Web App in browser: technically local but does not meet the requirement that it not jump to a browser page.
- PySide/PyQt: easier Python integration but slower to build a polished guided workflow UI.
- Tauri: smaller installer, but Rust/native integration adds avoidable complexity for PowerPoint COM and the current scripts.

## Repository Layout

The app should live inside the existing Shen-PPT repository without replacing the skill.

```text
shen-ppt/
  app/
    electron/
      package.json
      electron-builder config
      src/
        main/
        preload/
        renderer/
      assets/
        app-icon.ico
  scripts/
    shen_ppt_engine.py
    build_shen_ppt_com.ps1
    generate-apple-svg-icons.py
  references/
  tests/
  docs/
    superpowers/
      specs/
        2026-06-18-shen-ppt-windows-app-design.md
```

The `scripts/` directory is the shared engine boundary. APP code can call these scripts, but must not fork separate material parsing or PPT rendering logic unless a new shared script is created.

## Runtime Data Layout

Default local user data root:

```text
Documents/
  Shen PPT/
    Projects/
      2026-06-18-课程答辩-综合设计实践B/
        task.json
        inputs.json
        material_summary.json
        outline.md
        template_lock.md
        design_lock.md
        slide_cards.json
        sample/
          sample.pptx
          preview/
            slide-01.png
            slide-02.png
            slide-03.png
            slide-04.png
        final/
          deck.pptx
          deck_讲稿.md
          deck_问答.md
          qa.md
          preview/
            slide-01.png
            ...
        logs/
          engine.log
          renderer.log
          qa.log
```

The app should allow changing the workspace root in settings, but the default must be under Documents.

## Task State Machine

The app mirrors the Shen-PPT Stage 0-10 pipeline as local UI states.

| App State | Shen-PPT Stage | User Action Required | Main Artifacts |
|---|---:|---|---|
| `created` | 0 | none | `task.json` |
| `intake_ready` | 1 | fill task type, audience, output info | `inputs.json` |
| `materials_read` | 2 | review findings if needed | `material_summary.json` |
| `outline_waiting_approval` | 3 | approve or request edits | `outline.md` |
| `template_waiting_approval` | 4 | approve locked template/style | `template_lock.md` |
| `design_locked` | 5 | none | `design_lock.md`, `slide_cards.json` |
| `sample_waiting_approval` | 6 | approve or request edits | sample PPTX and previews |
| `full_deck_generating` | 7 | none | final PPTX in progress |
| `qa_running` | 8 | none unless blocking issue | `qa.md`, final previews |
| `docs_generating` | 9 | none | `讲稿.md`, `问答.md` |
| `complete` | 10 | open/export files | final package |
| `blocked` | any | fix missing dependency/input | logs and error reason |

Required gate rule:

- The app cannot enter `design_locked` until outline approval is recorded.
- The app cannot enter `sample_waiting_approval` until template/style lock is recorded.
- The app cannot enter `full_deck_generating` until four sample pages are approved.
- The app cannot enter `complete` until PPTX, speaker script, Q&A, and QA report exist.

Approval records should be written to `task.json` with timestamp, stage, and approved artifact path.

## Main Screens

### 1. Welcome

Purpose: start or resume work.

Controls:

- New PPT Task
- Open Existing Task
- Recent Tasks
- Settings

Display:

- Product name: `Shen PPT / 神了PPT`
- Local-only status indicator
- PowerPoint availability status if already checked

### 2. New Task

Purpose: collect stable task metadata.

Fields:

- Task type: 组会汇报, 课程答辩, 论文答辩, 论文讲解, 项目汇报
- Deck title
- Audience
- Presenter/team information
- Output workspace
- Optional template/style preference

Validation:

- Task title required
- Output folder writable
- Task type required

### 3. Materials

Purpose: choose source files and folders.

Inputs:

- Add PDF
- Add Word/Markdown/Text
- Add code folder
- Add report folder
- Add image/result folder
- Remove selected path

Display:

- Path list
- File type badges
- Local-only reminder

Validation:

- At least one source path required
- Missing paths blocked before material reading

### 4. Material Summary

Purpose: show what the engine found before outline generation.

Display:

- Topic summary
- Real figures/images found
- Tables found
- Formulas found
- Code/report modules found
- Missing or weak evidence warnings

Actions:

- Generate Outline
- Back to Materials

### 5. Outline Approval

Purpose: show only the PPT outline and asset/content plan.

Display:

- Page-by-page outline
- Intended source asset per page when known
- Page type per page

Actions:

- Approve Outline
- Request Edit
- Regenerate Outline

Constraint:

- Do not show visual style choices on this screen.

### 6. Template/Style Lock

Purpose: lock the base visual system.

Modes:

- User-specified template: show exact file path and state that it will be filled/extended directly.
- Shen-PPT sample style: show available sample decks and previews.
- Default: use highest-reference quality baseline.

Actions:

- Approve Template/Style
- Choose Different Style
- Select Custom PPTX Template

Constraint:

- If the user provided a template, do not recommend unrelated styles unless they explicitly ask.

### 7. Four Sample Pages

Purpose: review the generated four-page sample before full deck production.

Sample order:

1. cover
2. directory
3. section divider
4. body

Display:

- PNG previews in order
- Open sample PPTX
- Side panel listing applied fonts, style, template, and key QA checks

Actions:

- Approve Sample Pages
- Request Revision
- Regenerate Sample

### 8. Generation Progress

Purpose: run full generation and surface logs without overwhelming the user.

Display:

- Current step
- Progress timeline
- Last important log line
- Button to open detailed log

Substeps:

- Build slide cards
- Render PPTX
- Export previews
- Run QA
- Generate speaker script
- Generate Q&A

### 9. QA Review

Purpose: show whether final output meets Shen-PPT standards.

Checks:

- PPTX exists and is non-empty
- Final Markdown files exist
- Preview PNGs exported
- No animation
- Real images have captions
- Formula tag count matches expected count where formulas exist
- No obvious formula fallback unless accepted
- Required font roles checked where practical
- Template/style lock recorded
- Stage approvals recorded

Actions:

- Open QA Report
- Repair and Regenerate
- Accept with Notes if non-blocking
- Continue to Delivery

### 10. Delivery

Purpose: expose final artifacts.

Actions:

- Open PPTX
- Open Output Folder
- Open Speaker Script
- Open Likely Q&A
- Open QA Report
- Duplicate Task

## Engine Integration Contracts

### Material to Slide Cards

The app should call `scripts/shen_ppt_engine.py` through a process wrapper. The initial MVP can use the existing CLI subcommands, then add app-specific subcommands if needed.

Stable boundary:

- Input: source path(s), title, task type, output directory, optional slide count, optional template/style slug
- Output: slide-card JSON, material summary JSON/Markdown, speaker-script draft, likely-Q&A draft when final docs are requested

If the current engine only supports one source path, the app MVP can generate a manifest file listing multiple paths and either pass the root folder or add a new shared engine subcommand during implementation.

### Slide Cards to PPTX

The app should call `scripts/build_shen_ppt_com.ps1` with:

```powershell
-Cards <slide_cards.json>
-OutPptx <final.pptx>
-SkillRoot <repo-or-installed-skill-root>
-PreviewDir <preview-folder>
-LatexPptRoot <configured-latex-ppt-root>
```

The renderer must output a normal editable `.pptx`, not a screenshot deck.

### Formula QA

When slide cards contain `latex` entries, the app should verify that the PPTX contains matching `ShenPPT_LatexSource` tags unless a fallback was recorded and accepted.

### Preview QA

The app should treat preview PNGs as review artifacts. For MVP, automated visual overlap detection may be basic or manual, but preview generation must happen whenever PowerPoint COM can export.

## Settings

MVP settings:

- Workspace root
- Skill root
- LaTeX-PPT root
- PowerPoint availability check
- Default style slug
- Default output naming pattern
- Debug logging on/off

All settings are local JSON under the Electron app user data directory.

## Error Handling

Errors should be shown with action-oriented messages.

Common blocking errors:

- PowerPoint not installed or COM unavailable
- LaTeX-PPT root missing
- Source path missing
- Output folder not writable
- Template file missing
- Sample deck path missing
- Script execution failed
- Formula fallback occurred in formula-required deck

Every blocking error should include:

- human-readable message
- failed stage
- command or script that failed
- log path
- recommended next action

## Packaging and Release

MVP release target:

```text
Shen PPT Setup.exe
```

Packaging recommendation:

- Use `electron-builder` for NSIS Windows installer.
- App name: `Shen PPT`
- Product display name: `神了PPT`
- Desktop shortcut: yes
- Start Menu shortcut: yes
- File associations: not required in MVP
- Auto-update: not in MVP

Bundling strategy for MVP:

- Bundle Electron app code.
- Bundle Shen-PPT repository resources required at runtime: scripts, references, tests optional, icons, sample decks.
- Assume system Python and PowerPoint in developer MVP, then decide whether to bundle Python runtime in release hardening.
- In release hardening, include a dependency preflight screen for Python, PowerPoint, and LaTeX-PPT.

## Security and Privacy

- The app does not upload source files.
- The app does not require account login.
- The app does not perform web search unless a future explicit task-level option enables external research.
- Local task folders may contain source excerpts, extracted images, generated slide cards, and logs. The app should make this visible in settings/help.
- Logs should avoid storing API keys or secrets. If an error message includes a key-like string, redact it before display where practical.

## Testing Plan

Unit tests:

- Task state transition validation
- Settings loading/saving
- Path validation
- Engine command construction
- Artifact detection
- QA result parsing

Integration tests:

- Generate slide cards from a simple Markdown file
- Generate slide cards from the DRIFT PDF sample
- Render a formula smoke deck and verify `ShenPPT_LatexSource` tags
- Render a sample deck and verify preview PNG count
- Verify final package contains PPTX, speaker script, likely Q&A, and QA report

Manual acceptance tests:

- Install app on Windows
- Launch from desktop icon without opening an external browser
- Create a paper explanation task from PDF
- Approve outline
- Lock style/template
- Generate four sample pages and preview them in app
- Approve sample pages
- Generate final PPTX
- Open PPTX in PowerPoint and edit text, image, table, and formula objects
- Open final speaker script and Q&A Markdown

## MVP Done Definition

MVP is done when:

- Windows app installs with `Shen PPT Setup.exe`
- Launch opens a desktop app window, not an external browser
- User can create a local task and select materials
- App can run material reading and show summary
- App can show outline and record approval
- App can lock template/style and record approval
- App can show four sample page previews and record approval
- App can generate final PPTX through shared engine
- App can generate `讲稿.md` and `问答.md`
- App can run QA and show report
- Output files are stored in the task folder
- Existing Codex `shen-ppt` skill still works independently

## Open Implementation Decisions

These should be decided during implementation planning:

- Whether to bundle Python in the first public release or require an installed Python runtime.
- Whether the MVP app calls current engine CLI directly or first adds a richer `app-runner` CLI around the shared engine.
- Whether sample-page generation is a separate renderer mode or a full deck subset generated from sample slide cards.
- How much visual QA can be automated in MVP versus preview-based manual approval.
- Final app icon design and installer branding assets.
