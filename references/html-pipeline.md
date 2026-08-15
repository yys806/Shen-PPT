# HTML 演示管道（S4 · guizang / frontend-slides）

> 2026-08-14 用户拍板：**HTML 演示固定用这两个 skill**——guizang-ppt-skill（默认，演讲工具链完备）/ frontend-slides（视觉惊艳备选）。本次实战沉淀（世界模型调研 10 页瑞士风，已交付 `D:\hermes\docs\PPT_output\world_model_html\`）。

## 资产位置（⚠️ 已迁移，勿用旧路径）

```
D:\hermes\dev\ppt-refs\guizang-ppt-skill\      # op7418/guizang-ppt-skill
  ├── SKILL.md               # 工作流（启动前 git 检查更新 → 需求澄清 → 生成）
  ├── assets/template.html   # 风格A 电子杂志×电子墨水（衬线+流体 WebGL）
  ├── assets/template-swiss.html  # 风格B 瑞士国际主义（无衬线+网格点阵）2935 行
  ├── assets/motion.min.js   # 动效库（本地优先，CDN 兜底）
  └── references/            # themes.md / themes-swiss.md / layouts.md / layouts-swiss.md
D:\hermes\dev\ppt-refs\frontend-slides\        # zarazhangrui/frontend-slides
  ├── SKILL.md               # 反 AI slop 设计哲学、1920×1080 固定舞台
  ├── STYLE_PRESETS.md       # 12 套风格预设（Dark×4/Light×4/Specialty×4）
  ├── bold-template-pack/    # deck-stage.js + 模板包
  └── viewport-base.css      # 必读必内嵌
```

## 场景选择

| 需求 | 用谁 |
|---|---|
| 科技/数据/学术汇报，**要演讲**（翻页讲、观众屏、讲稿、计时、激光笔） | **guizang 瑞士风**（template-swiss.html） |
| 人文/商业/发布，"杂志感"演讲 | **guizang 杂志风**（template.html） |
| 视觉惊艳/独特设计、PPT 转网页、无演讲功能需求 | **frontend-slides**（12 风格预设） |

## guizang 标准流程（本次实战验证）

1. **检查上游更新**（guizang SKILL 必做）：`git -C <repo> fetch --quiet && git rev-list --count HEAD..@{u}`，>0 问用户是否 pull
2. **主题色**：瑞士风 `references/themes-swiss.md` 四选一（IKB 克莱因蓝 #002FA7 默认 / 柠檬黄 / 柠檬绿 / 安全橙），整体替换 template-swiss.html 的 `:root` 块；科技/AI 内容默认 IKB
3. **⚠️ 版式类必须先验证**：`layouts-swiss.md` 示例代码引用的类（cell-6/sub-card-stack/h-statement 等）**与模板 CSS 不同步**（2026-08-14 实测模板里不存在！）——**必须以模板实际类为准**，先 `grep -oE '^\s*\.[a-z][a-z0-9-]+' template-swiss.html` 列出真实类再构建。可用布局：grid-2-4-8/grid-3/grid-6/kpi-row-4/kpi-big/timeline-h/sub-card/card-fill/card-ink/card-accent/duo-compare/chrome-min/canvas-card/t-meta 等
4. **动效 recipes**（data-animate 必须命中，21 个）：hero/statement/grid-reveal/stack-build/measure-up/bar-grow/duo-mirror/split-statement/timeline-walk/manifesto/three-forces/loop-form/matrix-fill/field-notes/system-diagram/why-now/four-cards/stacked-ledger/tech-spec/image-hero
5. **组装**（写生成脚本，勿手改 3000 行模板）：
   - 读模板 → 定位 `<!-- SLIDES_HERE` 注释 → 找其后的所有 `</section>` 取最后一个 → 其后第一个 `</div>` = deck 关闭 → 替换该区间为你的 slides
   - **每页 section 必须带 `data-slide-id`**（导航 dots 与 SPEAKER_NOTES 依赖；cover/closing 用模板示例 id，中间页自定 p2/p3…）
   - `chrome-min` 每页必填（左 Deck 标题 + 右 `WM · 26.07 · NN / 10 · 章节`）
   - **替换 SPEAKER_NOTES 数组**（10 条，id 必须与 slide id 一致，含 title/section/minutes/purpose/talk[]/transition/cue）
   - 替换 `<title>`
   - **复制 `assets/motion.min.js` 到输出目录**（模板 `./assets/motion.min.js` 本地优先，CDN 兜底；缺本地库=离线动画失效）
6. **验证（Playwright，勿信 browser_vision）**：
   ```python
   # playwright 逐页截图 → PIL 平均亮度（<60 = 黑屏/白屏异常）
   # file:// 打开（用户双击场景）→ 10 页亮度全 >60 + body.motion-ready + 0 pageerror
   ```

## 坑（2026-08-14 实测）

- ⚠️ **browser_vision 黑屏是工具 bug**（file:// 与翻页后截图间歇全黑）——**以 Playwright 截图为最终裁决**；browser_console 在 file:// 下可能评估到空文档（slides=0），http 下正常
- ⚠️ layouts 文档与模板类不同步（见上）
- ⚠️ deck 切换 = `deck.style.transform = translateX(-idx*100vw)`（横向滚动），无 .active class；当前页查 `window.__currentSlideIndex`
- ⚠️ 模板示例页在 SLIDES_HERE 注释后（cover 1251 行/closing 1279 行附近），组装时整区替换
- ⚠️ `[必填]` 占位符要清干净（grep 自检）
- ⚠️ 模板 `<title>` 是 `[必填] 替换为 PPT 标题 · Deck Title`，必须替换
- lucide 图标仅 CDN（无本地兜底）；**不用图标就完全离线可用**（本次 10 页零图标全文字）
- python http.server 起在**错误目录**（background 进程 cwd 未生效）→ 用 `workdir` 参数或直接 file:// 验证

## frontend-slides 要点（备用）

- 固定 1920×1080 舞台 + viewport-base.css 全量内嵌；slides 切换用 `.active/.visible`（禁 display:none）
- 密度模式先问用户：reading deck（阅读型）/ speaking deck（演讲型）
- 风格发现法：先看 selection-index 小卡再选模板，禁 Inter/Roboto/Arial 与紫渐变白底
