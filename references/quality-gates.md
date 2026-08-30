# Shen-PPT 质量门禁（Quality Gates）· v4.1.0

> 本文件把 ppt-master 上游 v6.1.0（2026-08-30 发布）的质量机制吸收进 Shen-PPT 流程，
> 适配我们"内容单源 deck-spec + 确定性引擎"的架构。执行渲染后 QA（SKILL.md Step 7）时按此核对。

## 1. 内容保真核对（Carrier Receipt，对应上游 carrier-receipt review）

渲染完成后，逐页把 **deck-spec 承诺的要素** 与 **实际 PPTX 页面承载** 对一遍：

| spec 承诺 | 页面必须承载 | 缺失时的处理 |
|---|---|---|
| `type: cover` | 主标题 + 副标题/日期等 | 修复 spec 或骨架 |
| `type: toc` | 目录项与 sections[] 一一对应 | 缺项补项 |
| `type: section` | 章节号 + 章节标题 | 修复 |
| `type: content` + `section` | 页面上有该章节归属标识（导航条/角标） | **章节归属缺失 = 硬伤** |
| `layout: bullets` | 要点列表完整（无截断、无溢出） | 见 §3 文本校准 |
| `layout: image-right/left` | 图片按区域 fit，无变形 | 见 §2 图放大警告 |
| `layout: table` | 表头 + 全部行，无丢行 | 修复 |
| `layout: stats` | 每个 KPI 卡都有数值 | 补数 |
| 页码 | 每页右下页码连续（NN / 总页数） | 修复 |
| 结束页 | 有结束页 | 补齐 |

**Absence needs a reason（缺失必须有理由）**：
- 若某页 spec 声明了要素但页面没有（如 `layout: table` 却只有文字），必须回答一行：
  **"是什么承载了这个任务，为什么它比原方案对读者更好"**。
- 以下不是答案：省略了、"文字够了"、"可编辑就行"、"时间不够"。
- 说不出理由 → 按 spec 修复后重渲染，再核对一次。

## 2. 图放大警告（Image Upscale，对应上游 image upscale warning at 2x）

引擎已内置（`render_pptx.py` `add_image_fit`）：

- 任一方向显示尺寸 ≥ 源图 2 倍 → 渲染时输出 ⚠️ 警告，并汇总在渲染结束行。
- QA 动作：看到警告 → 换更高分辨率图，或接受放大并注明原因（截图/缩略图场景可接受）。
- 源图分辨率优于放大：优先用 2x 以上源图，保证投屏不糊。

## 3. 文本宽度校准（Text Calibration，对应上游 text_measure calibrate）

引擎 `estimate_text_height` 按"中文字宽≈字号"估算行数。校准纪律：

1. **每套风格校准一次**：第一次渲染某风格时，抽查 1 页实际换行 vs 估算值，偏差 >10% 时调整
   `styles/<style>/style-spec` 里的行距/字号或骨架区域高度。
2. 后续同风格页面**按该校准后的算术估计**，不再逐页目测——除非 QA 视觉检查发现溢出。
3. QA 时正文溢出（超出区域下缘）→ 先改 spec 文本（删减/精简），再调骨架，禁止用缩小字号硬塞。

## 4. 每页语义唯一归属（Relationships 唯一所有者，对应上游 Relationships）

- **每页一个主语义**：S2/S3 内容页的 `section` 归属 + 页面自身定位（论点/证据/对比/流程）。
- 一页塞多个无关任务（论点+表格+图+结论混排）是失败模式：拆页或降级为辅助承载。
- QA 检查：每个内容页能一句话说出"这页讲什么、属于哪章"——说不出 = 页面语义不清，重排。

## 5. 最终复查检查点（Final Review Checkpoint）

全部页面渲染 + 逐页 QA 后，**整 deck 最后复查一遍**（对应上游 final-review）：

1. 页数：spec 页数 = 实际页数（数一遍，别信印象）
2. 章节：S2/S3 每页章节归属完整，目录页数 = sections 数
3. 编号：页码连续无跳号
4. 保真：§1 核对表无未解释缺失
5. 放大：§2 警告全部处理（换图或注明接受）
6. 溢出：正文/表格无越界
7. 三件套：PPTX + 讲稿.md + 问答.md 就位

复查发现问题 → 回到对应 owning 层修复（页面问题改页，spec 问题改 spec，引擎问题改骨架/样式），
**不要用"重新截个图看看"糊弄过去**。复查通过才算交付完成。

## 与上游的映射（溯源）

| Shen-PPT v4.1.0 机制 | ppt-master v6.1.0 出处 |
|---|---|
| §1 内容保真核对 / Absence needs a reason | `workflows/generate-pptx.md` 最终载体收据复查（carrier receipt）、d8954f9a |
| §2 图放大警告 | d8954f9a "image upscale warning at 2x" |
| §3 文本宽度校准 | 788cd2d4 / f28caf7e "calibrate text widths once before P01" |
| §4 语义唯一归属 | 28638db5 "Relationships the single owner of page semantics" |
| §5 最终复查检查点 | c32c4d9b "a final-review checkpoint" |
| 修复纪律"owning 层" | 上游 Global Execution Discipline #7 "Act at the owning layer" |
