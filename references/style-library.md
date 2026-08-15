# 风格资产库（v1.0）—— 解决"素材风格"

## 设计原则

1. **一处定义，两管道同步**：style-spec.json 是唯一风格源。PPTX 管道读它渲染，HTML 管道（三期）读它生成 CSS 变量
2. **锁定 vs 可选**：S1/S3 风格锁定（scenario 硬绑定，不询问）；S2 风格组内可选（预览挑选）
3. **禁止自由发明**：锁定场景不接受用户自定义 hex；可选场景也只从库中选，不手搓配色
4. **每个风格带禁令**：decor.forbidden 列出该风格禁止的装饰（AI 味重灾区）

## 风格索引（styles/index.json）

```json
{
  "scenarios": {
    "s1-pku":    {"style": "pku-report",    "locked": true},
    "s2-course": {"style": "course-showcase", "locked": false},
    "s3-thesis": {"style": "thesis-formal", "locked": true}
  },
  "styles": {
    "pku-report":    {"path": "pku-report/style-spec.json",    "scenarios": ["s1-pku"]},
    "thesis-formal": {"path": "thesis-formal/style-spec.json", "scenarios": ["s3-thesis"]}
  }
}
```

## style-spec.json 字段

```json
{
  "name": "pku-report",
  "display": "北大组会（楷体学术）",
  "scenarios": ["s1-pku"],
  "skeleton": "report",
  "palette": {
    "base": "#FFFFFF", "panel": "#F7F8FA", "panel_dark": "#EEF1F5",
    "line": "#D5DCE6", "text": "#1F2328", "muted": "#6B7280",
    "accent": "#2F6FD0", "accent2": "#1E2761", "grid": "#E5E9F0"
  },
  "fonts": {
    "cn": "楷体", "cn_title": "楷体", "en": "Times New Roman",
    "mono": "Consolas"
  },
  "sizes": {
    "title": 40, "h1": 24, "h2": 22, "body": 22,
    "tag": 14, "footer": 12, "stat-num": 44, "stat-label": 14
  },
  "skeleton_overrides": {},
  "decor": {
    "motif": "细线角标",
    "forbidden": ["装饰线", "色条", "侧边竖条", "阴影浮动卡片"]
  }
}
```

| 字段 | 说明 |
|---|---|
| skeleton | 用哪套版式骨架（report / defense） |
| palette | 9+ token：base 底 / panel 卡片 / panel_dark 深面板 / line 线 / text 主文字 / muted 弱文字 / accent 强调 / accent2 次强调 / grid 网格（可扩展如 red） |
| fonts | cn 中文、cn_title 标题中文、cn_cover 封面专用（如方正小标宋）、en 英文/数字、mono 等宽 |
| sizes | 字号 token：title/cover_title/cover_sub/cover_date/cover_body/h1/h2/h3/body/tag/footer/stat-num/stat-label |
| bullets | **正文层级配置（原生项目符号）**：l0 正文 / l1 一级 / l2 二级 / l3 三级，每级 `{char 符号字符, bullet_font 符号字体(模板=Wingdings), mark_color 符号色(hex), lum_mod/lum_off 符号色亮度调制, size 字号token, color 文字色, bold, lvl 大纲级别0-3, marL 左缩进EMU}`。**参数直接从单位模板 XML 抄**（北大模板：一级 q/A40503红/lvl0/marL228600、二级 v/0432FF/lvl1/marL685800、三级 Ø/4F81BD/lvl2/marL1143000）。渲染为 PowerPoint 原生段落格式：回车自动延续层级与符号，与手做一致 |
| decor.motif | 视觉母题（贯穿每页的元素） |
| decor.forbidden | 该风格禁区（AI 味重灾区） |
| assets | （骨架 logo 区域引用）`<SKILL_ROOT>/assets/<style>/` 放单位 LOGO 等图片资产 |

## 现有风格一览（一期）

| 风格 | 服务场景 | 骨架 | 特征 |
|---|---|---|---|
| pku-report | S1 北大组会 | report | **已定稿（2026-08-14）**：楷体+TNR 中英分工，accent=#002B85 深蓝，封面楷体38/日期TNR28银灰/摘要楷体16银灰，正文层级 24/20/18 原生 Wingdings（q/v/Ø + A40503/0432FF/4F81BD），双细蓝线 80/86，LOGO 校徽[1118]+PCNI[1199]，页码 x1150，参考文献左下角贴边 9pt 灰，上标 baseline+30000。完整规格见 `template-specs.md` |
| thesis-formal | S3 论文答辩 | defense | 正式学术：深蓝主色，衬线标题，克制冷色 |
| course-showcase | S2 课程答辩 | defense | **组容器**：内含多个子风格（academic-clean/dark-engine/magazine-warm…），二期填充 |

## 新增风格指南

1. 在 `styles/<name>/style-spec.json` 写完整 spec（9 token 色板必须全）
2. 注册进 `styles/index.json`（styles 段 + 对应 scenario 映射）
3. 锁定风格：scenario 段 `"locked": true`，且 scenarios 数组含该场景
4. 用 demo spec 渲染验收：`python scripts/render_pptx.py -s templates/deck-spec.example.json -o test.pptx --style <name>`，导出预览 vision 检查
5. 更新本文档的现有风格表

## 风格预览流程（S2 用）

从 course-showcase 组取 2-3 个子风格 → 各渲染 1 页封面预览 PNG → 用户挑选 → 全量渲染。
