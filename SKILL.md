---
name: shen-ppt
description: "Use when 做PPT/答辩/组会/汇报/科普. 场景路由：S1组会/S2课程/S3论文走PPTX引擎，S4日常走HTML。"
version: 4.0.0
metadata:
  hermes:
    tags: [ppt, powerpoint, presentation, slides, chinese, deck-spec, python-pptx, codex]
    category: productivity
    related_skills: [docx, xlsx, pdf, powerpoint]
---

# Shen-PPT（神了PPT）v4：S1-S4 场景路由 + 双管道

触发词：**做PPT、组会汇报、答辩PPT、论文答辩、课程大作业、介绍一下XX、做个科普、演示文稿**。

## 核心架构（一句话）

**一个大脑（场景路由 + 内容单源 deck-spec）+ 两条手臂（PPTX 交付臂 / HTML 演示臂）**。风格只在风格资产库定义一次，两管道共享。

```
"做组会PPT/答辩PPT/介绍XX"
  │ 场景识别（S1-S4，拿不准时问≤2个问题）
  ▼
┌──────────────────────────────────────────┐
│ 内容单源：写 deck-spec.json              │
│   （封面/目录/章节/每页{内容,章节归属,备注}） │
└──────────────┬───────────────────────────┘
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│ PPTX 管道      │  │ HTML 管道      │
│ S1/S2/S3      │  │ S4 日常/自媒体  │
│ render_pptx.py│  │ guizang/frontend│
│ 版式骨架渲染    │  │ 风格库融合      │
└──────────────┘  └──────────────┘
```

## 场景路由表（第一步必做）

| 场景 | 识别词 | 纪律 | 产出 | 结构要求 |
|---|---|---|---|---|
| **S1 组会汇报** | 北大组会/组会汇报 | 🔒 锁定模板零发散 | PPTX | 严格按北大模板（pku-report） |
| **S2 课程大作业答辩** | 课程作业/大作业/课设答辩 | 🔓 结构完整风格可变 | PPTX | 封面+目录+章节页+**每页章节归属**（复用 ppt-master 官方管线） |
| **S3 论文答辩** | 论文答辩/毕设/学位论文 | 🔒 正式固定版式 | PPTX | 封面+目录+章节页+**每页章节归属**+公式/引用 |
| **S4 日常/自媒体/科普** | 介绍一下/科普/自媒体/分享 | 🎨 自由叙事 | HTML | 叙事弧（钩子→定调→主体→转折→收束） |
| **S5 正式答辩/夏令营** | 夏令营/正式答辩/自我介绍 | 🔒 三校变体 | PPTX | 封面+目录+章节页+内容页(导航条反转)+结束页，见 `references/formal-defense.md` |

## 流程（PPTX 管道 S1/S2/S3）

### Step 1 · 场景识别
按上表确定场景。S1 直接按北大模板执行（无需追问单位）。其他场景拿不准时问用途/时长/素材，一次问完。

### Step 2 · 素材收集
读论文/代码/报告/旧 PPT → 提炼要点。也可用 `scripts/shen_ppt_engine.py`（原版引擎，读 Markdown/text/PDF 生成结构化卡片与压缩草稿）。

### Step 3 · 大纲预览（必做，等用户确认）
动手写 spec 前，先输出 **MD 大纲**（格式见 `references/deck-spec.md` 附录"大纲模板"），用户确认内容与页面规划后才能进 Step 4。**未经确认不得渲染。**

| 场景 | 目录/章节页 | 风格选择 | 完整流程 |
|---|---|---|---|
| **S1 组会** | ❌ 不要目录、不要章节页 | ❌ 不选风格（锁定 pku-report） | 大纲确认 → **直接完整渲染** |
| **S2 课程答辩** | ✅ 封面+目录+章节页+每页章节归属 | ✅ 风格预览挑选 | 大纲确认 → 风格预览(2-3个) → 样板 → 确认 → 完整渲染 |
| **S3 论文答辩** | ✅ 同上 | ✅ 风格预览挑选（thesis-formal 首选） | 同上 |

### Step 4 · 写 deck-spec.json
**内容单源规范见 `references/deck-spec.md`**。要点：
- `scenario` + `style` 字段决定渲染管线和风格
- `sections[]` 定义章节（id/title/short），short ≤4 字
- 每个 slide 必须带 `type`；S2/S3 的 content 页**必须带 `section` 章节归属**
- S1 组会：**不写 toc/section 类型页**，直接封面+内容页+结束页
- **S1 锁定模板的精确规格（坐标/字体/层级/引用）见 `references/template-specs.md`，以该文件为准，禁止自由发挥**
- 示例：`templates/deck-spec.example.json`

### Step 5 · 选风格（S1 跳过）
- S1：锁定（pku-report），**不询问不更换**
- S3：首选 thesis-formal，也可预览挑选
- S2：从 `styles/index.json` 的 course-showcase 组生成 2-3 个封面样板预览让用户挑；或走 ppt-master 官方管线（手写官方视觉风格 SVG → ppt-master `svg_to_pptx.create_pptx_with_native_svg` 转换器 → 原生 PPTX，官方素材在本地 `ppt-refs/ppt-master/`，18 视觉风格/20 品牌模板/21 官方示例/34 图表）

### Step 6 · 渲染
```bash
python <SKILL_ROOT>/scripts/render_pptx.py \
  -s <deck-spec.json> -o <输出.pptx> \
  [--style <风格名>] [--preview-dir <预览目录>]
```
- 引擎自动：读 style-spec（风格 token）+ skeleton（区域坐标）→ 逐页渲染
- **输出目录（硬规则）：`D:\hermes\docs\PPT_output\<项目名>\`** —— 一个 PPT 项目一个子文件夹，所有素材（spec/pptx/预览/讲稿/图片）都放里面

### Step 7 · QA（必须）
```bash
python <SKILL_ROOT>/scripts/export_preview.py <输出.pptx> <预览目录>
```
导出每页 PNG → 视觉检查：文字溢出/重叠、章节标识完整、页码正确、位置协调。发现问题 → 改 spec 或骨架 → 重渲染。

### Step 8 · 交付
三件套：**PPTX + 讲稿.md + 问答.md**（后两者按需）。

## 流程（HTML 管道 S4）

**🔒 固定**：HTML 演示用 **guizang-ppt-skill**（默认）+ **frontend-slides**（备选）两个外部 skill，资产在本地 `ppt-refs/`。完整实战手册见 `references/html-pipeline.md`，要点：

1. 需求/场景选 skill：要演讲（观众屏/讲稿/计时/激光笔）→ **guizang 瑞士风**（template-swiss.html，科技数据默认 IKB 克莱因蓝）；杂志感 → guizang 杂志风；视觉惊艳/PPT 转网页 → frontend-slides（12 风格预设）
2. guizang 流程：`git` 检查上游更新（>0 问用户）→ 选主题色（themes-swiss.md 四选一，整体替换 :root）→ **⚠️ 版式类以模板实际 CSS 为准**（layouts-swiss.md 示例类与模板不同步，先 grep 验证）→ 生成脚本组装（替换 SLIDES_HERE 区 + SPEAKER_NOTES + title；**每页必带 data-slide-id**）→ 复制 `assets/motion.min.js` 到输出目录 → 交付
3. 验证：**Playwright 逐页截图 + PIL 亮度检查**（file:// 双击场景 + motion-ready + 0 JS 错误）；⚠️ browser_vision 黑屏是工具 bug，勿信
4. 分享：单文件复制即用（index.html + assets/motion.min.js 两件套）

## 原版引擎保留（v1-v3 兼容）

| 文件 | 角色 |
| --- | --- |
| `scripts/shen_ppt_engine.py` | 读 Markdown/text/PDF 源 → 结构化 slide cards + 压缩 Markdown 草稿 |
| `scripts/build_shen_ppt_com.ps1` | 官方 PowerPoint COM 回退渲染器（无 python-pptx 环境时从 slide cards 生成可编辑 PPTX） |
| `scripts/generate-apple-svg-icons.py` | Apple 风格 SVG 图标生成 |
| `scripts/validate-repo.ps1` | 仓库布局校验（CI 使用） |
| `tests/test_shen_ppt_engine.py` | slide-card 生成、压缩文档、PDF 前页清理的回归测试 |

原版固定管道（Assembly Line，阶段不可跳过）：
`0 Activation → 1 Intake → 2 Material Reading → 3 Outline Only → 4 Template/Style Lock → 5 Design Lock → 6 Four Sample Pages → 7 Full Deck Production → 8 QA And Repair → 9 Final Documents → 10 Delivery`

## 模板库

所有 PPT 样例、参考图、参数规格、最高质量参考都在 `references/`：

| 类型 | 数量 | 位置 |
| --- | --- | --- |
| 通用可编辑样例 | 8 | `references/style-samples-v2-20260606/sample-decks/` |
| 同济可编辑样例 | 7 | `references/style-samples-v2-20260606/sample-decks/` |
| 最高质量参考 | 1 | `references/highest-references/orangepi-defense-final-v9-20260607/` |
| 参数规格 | 1 | `references/parameter-spec.md` |
| Apple 风格 SVG 图标 | - | `references/icons/apple-svg/` |

可用风格 slug：
`academic-minimal business-roadshow chinese-academic dark-engineering data-analytics education-clean research-blue tech-launch tongji-blue-clean tongji-green-academic tongji-green-vitality tongji-guangying tongji-guangying-jiyi tongji-sakura tongji-study-space`

## 目录结构

```
shen-ppt/
├── SKILL.md                    # 本文档（S1-S4 场景路由）
├── README.md / README_CN.md    # 双语介绍
├── LICENSE                     # MIT
├── references/                 # 模板库 + 规格文档
│   ├── deck-spec.md            # 内容单源 schema 全表
│   ├── layout-skeletons.md     # 版式骨架系统说明
│   ├── style-library.md        # 风格资产库索引
│   ├── template-specs.md       # ⭐ S1 北大精确参数
│   ├── formal-defense.md       # ⭐ S5 三校变体规格
│   ├── html-pipeline.md        # ⭐ S4 HTML 管道实战手册
│   ├── parameter-spec.md       # 原版参数规格
│   ├── style-samples-v2-20260606/  # 原版 15 可编辑模板
│   ├── highest-references/     # orangepi 答辩最高质量参考
│   └── icons/                  # Apple 风格 SVG 图标
├── layouts/                    # 版式骨架（skeleton-report / skeleton-defense）
├── styles/                     # 风格资产（index.json + 9 风格 style-spec）
├── assets/                     # 校徽（pku/tsinghua/tongji）+ 北大 LOGO
├── templates/                  # deck-spec.example.json
├── scripts/                    # 渲染引擎 + 原版引擎
└── tests/                      # 回归测试
```

## 外部依赖（S2/S4 管线）

- **S2 ppt-master 官方管线**：`ppt-master` 仓库（18 视觉风格/20 品牌模板/21 官方示例/34 图表），本地 clone 于 `ppt-refs/ppt-master/`，上游 https://github.com/ 官方仓库
- **S4 HTML 演示**：`guizang-ppt-skill`（默认）+ `frontend-slides`（备选），本地 clone 于 `ppt-refs/`，每周检查上游更新

## 安装

Clone 到 Codex skills 目录：

```bash
git clone https://github.com/yys806/Shen-PPT.git ~/.codex/skills/shen-ppt
```

S2/S4 外部管线按需 clone：
```bash
mkdir -p ~/ppt-refs && cd ~/ppt-refs
git clone <ppt-master上游> && git clone <guizang-ppt-skill上游> && git clone <frontend-slides上游>
```

## 已知限制

- 公式：python-pptx 无原生公式。需要真公式时按需调用 ppt-master 的 `native-formula.md` 流程（latex → OMML），或图片形式插入
- 图片区域：图片按区域等比 fit，不裁切；需要精确裁切先预处理
- 修改已有 PPTX：看（export_preview 导出）→ 诊断（视觉）→ 改（python-pptx 纯文件操作）→ 验证（再导出对比）。⚠️ PowerPoint 单实例冲突：操作前先确认用户是否在用 PPT

## License

MIT License.
