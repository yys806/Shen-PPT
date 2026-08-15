# 版式骨架系统（v1.0）—— 解决"各部分位置协调"

## 概念

每个 slide 类型 = 一组**区域（region）**。区域有固定坐标（1280×720 画布，左上原点）+ 对齐 + 字体/颜色映射。位置即配置：改布局改 JSON，不动引擎代码。

区域类型是**引擎认识的固定集合**，引擎按区域类型决定渲染方式（文本/图片/列表/表格/页码…）。

## 区域类型全集

| 区域类型 | 渲染内容 | 来源 |
|---|---|---|
| `title` | 封面大标题 | spec.deckTitle / cover.title |
| `subtitle` | 封面副标题 | cover.subtitle |
| `meta` | 封面信息行（作者/单位/日期，`·` 分隔） | spec author/affiliation/date |
| `header` | 内容页页头标题 | content.title |
| `sectionTag` | **章节归属条**（`01·研究背景`） | slide.section → sections[] |
| `tocTitle` | 目录页标题 | toc.title 或 "目录" |
| `tocItems` | 目录项列表 | sections[] 自动 |
| `sectionNo` | 章节页大号（如 `01`） | slide.section |
| `sectionTitle` | 章节页大标题 | slide.title |
| `sectionTagline` | 章节页概述 | slide.tagline |
| `body` | 正文/要点/双栏/表格/KPI 主体 | content.body |
| `image` | 图片（等比 fit，不裁切） | content.image |
| `caption` | 图注 | content.caption |
| `pageNum` | 页码 | 自动（从 cover 后计） |
| `footer` | 页脚（deck 标题 + 作者） | spec 自动 |
| `footerDate` / `footerMid` | 页脚三格（日期/单位） | spec 自动 |
| `rule` / `rule2` | 分隔线组（**北大定稿：双细蓝线 y=80/y=86 h=2，颜色 accent，间隔 6px，第一条在 LOGO 下方**） | 骨架静态 |
| `logo` | 右上角 LOGO 组：`{"assets":[{"src","x","y","w","h"},...]}` **dict 形式=绝对坐标**（北大：校徽[1118,1,70,70]+PCNI[1199,5,66,66]）；字符串列表=区域横排等比 | 骨架静态，资产在 `<SKILL_ROOT>/assets/<style>/` |
| `references` | **参考文献框（左下角贴边）**：`{"x":0,"y":720,"w":950,"size":"ref","anchor":"bottom-left"}`，引擎按条数动态算高、底对齐到 720 | content.references |
| `thanks` | 结束页大字 | ending.title |
| `thanksSub` | 结束页致谢 | ending.thanks |
| `contact` | 结束页联系方式 | ending.contact |

## skeleton JSON 结构

```json
{
  "name": "report",
  "canvas": {"w": 1280, "h": 720},
  "slides": {
    "cover": {
      "bg": {"fill": "base", "accentBar": true},
      "regions": {
        "title":    {"x": 80,  "y": 240, "w": 1120, "h": 120, "size": "title",  "align": "left"},
        "subtitle": {"x": 80,  "y": 370, "w": 1120, "h": 60,  "size": "h1",    "align": "left"},
        "meta":     {"x": 80,  "y": 620, "w": 1120, "h": 40,  "size": "footer", "align": "left"}
      }
    },
    "content": {
      "bg": {"fill": "base"},
      "regions": {
        "header":     {"x": 80,  "y": 50,  "w": 1120, "h": 70,  "size": "h1",    "align": "left"},
        "sectionTag": {"x": 80,  "y": 130, "w": 320,  "h": 34,  "size": "tag",   "align": "left", "accent": true},
        "body":       {"x": 80,  "y": 190, "w": 1120, "h": 450, "size": "body",  "align": "left"},
        "image":      {"x": 820, "y": 190, "w": 380,  "h": 380, "fit": "contain"},
        "pageNum":    {"x": 1200,"y": 680, "w": 60,   "h": 30,  "size": "footer", "align": "right"},
        "footer":     {"x": 80,  "y": 680, "w": 600,  "h": 30,  "size": "footer", "align": "left", "muted": true}
      }
    }
  }
}
```

## 区域属性

| 属性 | 必填 | 说明 |
|---|---|---|
| x/y/w/h | ✅ | 坐标（px，1280×720 画布） |
| size | 条件 | 字号 token 名（见 style-spec sizes：title/h1/h2/body/tag/footer/stat-num） |
| align | 条件 | left / center / right |
| accent | 否 | true 时用风格 accent 色 |
| muted | 否 | true 时用 muted 色 |
| fit | 图片区 | contain（等比完整显示）/ cover（裁切填满） |
| bold | 否 | true 加粗 |

## 骨架文件与场景映射

| 骨架 | 服务场景 | 说明 |
|---|---|---|
| `layouts/skeleton-report.json` | S1 | 组会锁定版式：页头+章节条+正文+页码+页脚 |
| `layouts/skeleton-defense.json` | S2/S3 | 答辩版式：封面/目录/章节页/正文/结束页，每页带 sectionTag |

骨架选择逻辑：`style-spec.skeleton` 指定（如 pku-report → "report"）。S2 用 defense。

## 溢出与密度规则（引擎内置）

- 文本区域渲染后按估算行数检查：超出区域高度 → **警告并建议**（缩短文案/拆页/换 layout），不自动缩字号
- 正文密度：bullets ≤6 条、text ≤4 段
- 区域之间互不重叠是骨架设计前提；新增区域时遵循 80px 左/右边距、40px 垂直间距
