from __future__ import annotations

import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover
    Image = None
    ImageDraw = None
    ImageFont = None


ROOT = Path(__file__).resolve().parents[1]
ICON_ROOT = ROOT / "references" / "icons" / "apple-svg"
GENERATED = ICON_ROOT / "generated"

DEFAULT_COLOR_NAME = "shen-blue"
DEFAULT_COLOR = "#58C4D8"

ICONS = {
    "target": {
        "label": "目标",
        "tags": ["目标", "检测", "跟踪"],
        "paths": [
            '<circle cx="32" cy="32" r="17"/>',
            '<circle cx="32" cy="32" r="7"/>',
            '<path d="M32 8v8"/>',
            '<path d="M32 48v8"/>',
            '<path d="M8 32h8"/>',
            '<path d="M48 32h8"/>',
        ],
    },
    "code": {
        "label": "代码",
        "tags": ["代码", "实现", "模块"],
        "paths": [
            '<path d="M24 20 13 32l11 12"/>',
            '<path d="M40 20 51 32 40 44"/>',
            '<path d="M35 15 29 49"/>',
        ],
    },
    "cpu": {
        "label": "硬件",
        "tags": ["硬件", "计算", "嵌入式"],
        "paths": [
            '<rect x="18" y="18" width="28" height="28" rx="9"/>',
            '<rect x="25" y="25" width="14" height="14" rx="5"/>',
            '<path d="M24 10v8M32 10v8M40 10v8"/>',
            '<path d="M24 46v8M32 46v8M40 46v8"/>',
            '<path d="M10 24h8M10 32h8M10 40h8"/>',
            '<path d="M46 24h8M46 32h8M46 40h8"/>',
        ],
    },
    "database": {
        "label": "数据",
        "tags": ["数据", "存储", "样本"],
        "paths": [
            '<ellipse cx="32" cy="17" rx="17" ry="7"/>',
            '<path d="M15 17v28c0 4 8 7 17 7s17-3 17-7V17"/>',
            '<path d="M15 31c0 4 8 7 17 7s17-3 17-7"/>',
        ],
    },
    "network": {
        "label": "网络",
        "tags": ["网络", "连接", "通信"],
        "paths": [
            '<circle cx="17" cy="32" r="6"/>',
            '<circle cx="47" cy="18" r="6"/>',
            '<circle cx="47" cy="46" r="6"/>',
            '<path d="M22 29 42 20"/>',
            '<path d="M22 35 42 44"/>',
        ],
    },
    "chart": {
        "label": "结果",
        "tags": ["结果", "指标", "统计"],
        "paths": [
            '<path d="M14 50h38"/>',
            '<path d="M18 44V30"/>',
            '<path d="M30 44V20"/>',
            '<path d="M42 44V26"/>',
            '<path d="M18 23 29 16l13 6 8-10"/>',
        ],
    },
    "camera": {
        "label": "视觉",
        "tags": ["视觉", "图像", "相机"],
        "paths": [
            '<rect x="13" y="21" width="38" height="28" rx="11"/>',
            '<path d="M24 21c2-4 4-6 6-6h4c2 0 4 2 6 6"/>',
            '<circle cx="32" cy="35" r="9"/>',
            '<circle cx="45" cy="27" r="1.6" fill="currentColor" stroke="none"/>',
        ],
    },
    "experiment": {
        "label": "实验",
        "tags": ["实验", "验证", "测试"],
        "paths": [
            '<path d="M25 11h14"/>',
            '<path d="M29 11v15L17 47c-2 4 1 7 5 7h20c4 0 7-3 5-7L35 26V11"/>',
            '<path d="M22 42h20"/>',
            '<path d="M25 48h14"/>',
        ],
    },
    "route": {
        "label": "流程",
        "tags": ["流程", "路径", "步骤"],
        "paths": [
            '<circle cx="17" cy="18" r="5"/>',
            '<circle cx="47" cy="46" r="5"/>',
            '<path d="M22 18h12c7 0 10 4 10 9s-3 9-10 9h-6c-7 0-10 4-10 10"/>',
            '<path d="m38 27 6 6-6 6"/>',
        ],
    },
    "shield": {
        "label": "稳定",
        "tags": ["安全", "稳定", "保护"],
        "paths": [
            '<path d="M32 9 49 16v13c0 12-7 21-17 26-10-5-17-14-17-26V16l17-7Z"/>',
            '<path d="m24 32 6 6 12-14"/>',
        ],
    },
    "terminal": {
        "label": "终端",
        "tags": ["终端", "命令", "运行"],
        "paths": [
            '<rect x="12" y="16" width="40" height="32" rx="12"/>',
            '<path d="m21 27 6 5-6 5"/>',
            '<path d="M32 38h12"/>',
        ],
    },
    "document": {
        "label": "文档",
        "tags": ["文档", "报告", "材料"],
        "paths": [
            '<path d="M20 10h17l11 11v33H20z"/>',
            '<path d="M37 10v12h11"/>',
            '<path d="M26 32h18"/>',
            '<path d="M26 40h18"/>',
            '<path d="M26 48h11"/>',
        ],
    },
    "presentation": {
        "label": "汇报",
        "tags": ["汇报", "展示", "答辩"],
        "paths": [
            '<rect x="12" y="14" width="40" height="30" rx="11"/>',
            '<path d="M20 52h24"/>',
            '<path d="M32 44v8"/>',
            '<path d="M22 34 30 27l6 5 8-10"/>',
        ],
    },
    "team": {
        "label": "团队",
        "tags": ["团队", "成员", "协作"],
        "paths": [
            '<circle cx="32" cy="23" r="7"/>',
            '<path d="M20 52c2-9 7-14 12-14s10 5 12 14"/>',
            '<circle cx="17" cy="29" r="5"/>',
            '<path d="M8 50c2-7 5-11 10-12"/>',
            '<circle cx="47" cy="29" r="5"/>',
            '<path d="M56 50c-2-7-5-11-10-12"/>',
        ],
    },
    "cloud": {
        "label": "云端",
        "tags": ["云端", "服务", "部署"],
        "paths": [
            '<path d="M23 47h24c7 0 11-4 11-10 0-5-4-9-9-10-2-8-8-13-17-13-8 0-14 5-17 12-6 1-10 5-10 11 0 6 5 10 18 10Z"/>',
            '<path d="M25 36h14"/>',
            '<path d="m34 31 5 5-5 5"/>',
        ],
    },
    "robot": {
        "label": "机器人",
        "tags": ["机器人", "智能", "自动化"],
        "paths": [
            '<rect x="17" y="20" width="30" height="27" rx="12"/>',
            '<path d="M32 13v7"/>',
            '<circle cx="25" cy="32" r="2.5" fill="currentColor" stroke="none"/>',
            '<circle cx="39" cy="32" r="2.5" fill="currentColor" stroke="none"/>',
            '<path d="M26 40h12"/>',
            '<path d="M10 30h7"/>',
            '<path d="M47 30h7"/>',
        ],
    },
    "device": {
        "label": "设备",
        "tags": ["设备", "实物", "硬件"],
        "paths": [
            '<rect x="18" y="9" width="28" height="46" rx="13"/>',
            '<path d="M27 15h10"/>',
            '<path d="M28 49h8"/>',
            '<circle cx="32" cy="32" r="8"/>',
        ],
    },
    "layers": {
        "label": "分层",
        "tags": ["架构", "分层", "模块"],
        "paths": [
            '<path d="M32 10 55 22 32 34 9 22 32 10Z"/>',
            '<path d="M14 32 32 42 50 32"/>',
            '<path d="M14 42 32 52 50 42"/>',
        ],
    },
    "algorithm": {
        "label": "算法",
        "tags": ["算法", "模型", "推理"],
        "paths": [
            '<circle cx="19" cy="19" r="6"/>',
            '<circle cx="45" cy="19" r="6"/>',
            '<circle cx="32" cy="45" r="7"/>',
            '<path d="M24 22 29 39"/>',
            '<path d="M40 22 35 39"/>',
            '<path d="M25 19h14"/>',
        ],
    },
    "spark": {
        "label": "亮点",
        "tags": ["亮点", "创新", "重点"],
        "paths": [
            '<path d="M32 9 36 25 52 29 36 35 32 55 28 35 12 29 28 25 32 9Z"/>',
            '<path d="M50 11v10"/>',
            '<path d="M45 16h10"/>',
        ],
    },
}


def svg(icon_name: str, color: str, size: int, stroke: float) -> str:
    icon = ICONS[icon_name]
    paths = "\n    ".join(icon["paths"])
    title = escape(f"{icon['label']} / {icon_name}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" color="{color}" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">
  <title>{title}</title>
  <g>
    {paths}
  </g>
</svg>
'''


def write_manifest(size: int, stroke: float, color_name: str, color: str) -> None:
    manifest = {
        "style": "apple-like pure rounded line icons",
        "size": size,
        "stroke": stroke,
        "defaultColor": {"name": color_name, "hex": color},
        "rules": [
            "Use semantic icons only.",
            "Use one requested color per generated batch.",
            "Regenerate color variants by running the script with --color and --color-name.",
            "Do not use filled square pseudo-icons.",
            "Insert SVGs as independent PPT objects.",
        ],
        "icons": {
            name: {
                "label": spec["label"],
                "tags": spec["tags"],
                "path": f"generated/{name}.svg",
            }
            for name, spec in ICONS.items()
        },
    }
    (ICON_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def write_html(color_name: str) -> None:
    blocks = []
    for name, spec in ICONS.items():
        rel = f"generated/{name}.svg"
        blocks.append(
            f'<section class="card"><img src="{rel}" alt="{name}"><h2>{spec["label"]}</h2><p>{name}</p></section>'
        )
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Shen-PPT Apple SVG Icons</title>
<style>
body {{ margin: 0; background: #0b0f14; color: #eef3f8; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; }}
main {{ width: min(1120px, calc(100vw - 64px)); margin: 48px auto; }}
h1 {{ font-size: 34px; margin: 0 0 8px; }}
.sub {{ color: #93a4b7; margin: 0 0 28px; }}
.grid {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 18px; }}
.card {{ background: #111821; border: 1px solid #263241; border-radius: 22px; padding: 22px 14px 18px; text-align: center; }}
.card img {{ width: 60px; height: 60px; display: block; margin: 0 auto 14px; }}
h2 {{ margin: 0 0 6px; font-size: 18px; font-weight: 650; }}
p {{ margin: 0; color: #93a4b7; font-size: 13px; }}
</style>
</head>
<body>
<main>
<h1>Shen-PPT Apple-style SVG Icon System</h1>
<p class="sub">Pure rounded line SVG icons, generated as one color batch: {color_name}.</p>
<div class="grid">{''.join(blocks)}</div>
</main>
</body>
</html>
"""
    (ICON_ROOT / "preview.html").write_text(html, encoding="utf-8")


def make_contact_sheet(color_name: str, color: str) -> None:
    if Image is None:
        return
    cell_w, cell_h = 170, 138
    cols = 5
    rows = (len(ICONS) + cols - 1) // cols
    img = Image.new("RGB", (cell_w * cols, cell_h * rows + 92), "#0B0F14")
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
        font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((24, 30), "Shen-PPT Apple-style Pure Line Icons", fill="#EAF4EF", font=font_title)
    draw.text((24, 58), f"Color: {color_name} {color}", fill="#93A4B7", font=font_small)

    def tx(px: float, py: float, x: int, y: int, scale: float = 1.0) -> tuple[int, int]:
        return int(x + px * scale), int(y + py * scale)

    def draw_icon_shape(icon_name: str, color: str, x: int, y: int, scale: float = 0.82) -> None:
        line = color
        w = 4
        ox, oy = x + 6, y + 6

        def p(px: float, py: float) -> tuple[int, int]:
            return tx(px, py, ox, oy, scale)

        if icon_name == "target":
            draw.ellipse([*p(18, 18), *p(46, 46)], outline=line, width=w)
            draw.ellipse([*p(26, 26), *p(38, 38)], outline=line, width=w)
            draw.line([p(32, 8), p(32, 17)], fill=line, width=w)
            draw.line([p(32, 47), p(32, 56)], fill=line, width=w)
            draw.line([p(8, 32), p(17, 32)], fill=line, width=w)
            draw.line([p(47, 32), p(56, 32)], fill=line, width=w)
        elif icon_name == "code":
            draw.line([p(24, 20), p(13, 32), p(24, 44)], fill=line, width=w, joint="curve")
            draw.line([p(40, 20), p(51, 32), p(40, 44)], fill=line, width=w, joint="curve")
            draw.line([p(35, 15), p(29, 49)], fill=line, width=w)
        elif icon_name == "cpu":
            draw.rounded_rectangle([*p(18, 18), *p(46, 46)], radius=5, outline=line, width=w)
            draw.rounded_rectangle([*p(25, 25), *p(39, 39)], radius=3, outline=line, width=w)
            for px in (24, 32, 40):
                draw.line([p(px, 10), p(px, 18)], fill=line, width=w)
                draw.line([p(px, 46), p(px, 54)], fill=line, width=w)
            for py in (24, 32, 40):
                draw.line([p(10, py), p(18, py)], fill=line, width=w)
                draw.line([p(46, py), p(54, py)], fill=line, width=w)
        elif icon_name == "database":
            draw.ellipse([*p(15, 10), *p(49, 24)], outline=line, width=w)
            draw.arc([*p(15, 24), *p(49, 38)], start=0, end=180, fill=line, width=w)
            draw.arc([*p(15, 38), *p(49, 52)], start=0, end=180, fill=line, width=w)
            draw.line([p(15, 17), p(15, 45)], fill=line, width=w)
            draw.line([p(49, 17), p(49, 45)], fill=line, width=w)
        elif icon_name == "network":
            for cx, cy in ((17, 32), (47, 18), (47, 46)):
                draw.ellipse([*p(cx - 5, cy - 5), *p(cx + 5, cy + 5)], outline=line, width=w)
            draw.line([p(22, 29), p(42, 20)], fill=line, width=w)
            draw.line([p(22, 35), p(42, 44)], fill=line, width=w)
        elif icon_name == "chart":
            draw.line([p(14, 50), p(52, 50)], fill=line, width=w)
            for px, top in ((18, 30), (30, 20), (42, 26)):
                draw.line([p(px, 44), p(px, top)], fill=line, width=w)
            draw.line([p(18, 23), p(29, 16), p(42, 22), p(50, 12)], fill=line, width=w, joint="curve")
        elif icon_name == "camera":
            draw.rounded_rectangle([*p(13, 21), *p(51, 49)], radius=6, outline=line, width=w)
            draw.line([p(24, 21), p(28, 15), p(36, 15), p(40, 21)], fill=line, width=w)
            draw.ellipse([*p(23, 26), *p(41, 44)], outline=line, width=w)
            draw.ellipse([*p(44, 26), *p(47, 29)], fill=line)
        elif icon_name == "experiment":
            draw.line([p(25, 11), p(39, 11)], fill=line, width=w)
            draw.line([p(29, 11), p(29, 26), p(17, 47)], fill=line, width=w)
            draw.line([p(35, 11), p(35, 26), p(47, 47)], fill=line, width=w)
            draw.arc([*p(17, 40), *p(47, 56)], start=0, end=180, fill=line, width=w)
            draw.line([p(22, 42), p(42, 42)], fill=line, width=w)
        elif icon_name == "route":
            draw.ellipse([*p(12, 13), *p(22, 23)], outline=line, width=w)
            draw.ellipse([*p(42, 41), *p(52, 51)], outline=line, width=w)
            draw.line([p(22, 18), p(34, 18), p(44, 31), p(28, 36), p(18, 46)], fill=line, width=w, joint="curve")
            draw.line([p(38, 27), p(44, 33), p(38, 39)], fill=line, width=w)
        elif icon_name == "shield":
            draw.line([p(32, 9), p(49, 16), p(49, 29), p(42, 45), p(32, 55), p(22, 45), p(15, 29), p(15, 16), p(32, 9)], fill=line, width=w, joint="curve")
            draw.line([p(24, 32), p(30, 38), p(42, 24)], fill=line, width=w)
        elif icon_name == "terminal":
            draw.rounded_rectangle([*p(12, 16), *p(52, 48)], radius=7, outline=line, width=w)
            draw.line([p(21, 27), p(27, 32), p(21, 37)], fill=line, width=w, joint="curve")
            draw.line([p(32, 38), p(44, 38)], fill=line, width=w)
        elif icon_name == "document":
            draw.line([p(20, 10), p(37, 10), p(48, 21), p(48, 54), p(20, 54), p(20, 10)], fill=line, width=w, joint="curve")
            draw.line([p(37, 10), p(37, 22), p(48, 22)], fill=line, width=w)
            for py, x2 in ((32, 44), (40, 44), (48, 37)):
                draw.line([p(26, py), p(x2, py)], fill=line, width=w)
        elif icon_name == "presentation":
            draw.rounded_rectangle([*p(12, 14), *p(52, 44)], radius=6, outline=line, width=w)
            draw.line([p(32, 44), p(32, 52)], fill=line, width=w)
            draw.line([p(20, 52), p(44, 52)], fill=line, width=w)
            draw.line([p(22, 34), p(30, 27), p(36, 32), p(44, 22)], fill=line, width=w, joint="curve")
        elif icon_name == "team":
            draw.ellipse([*p(25, 16), *p(39, 30)], outline=line, width=w)
            draw.arc([*p(20, 34), *p(44, 62)], start=200, end=340, fill=line, width=w)
            draw.ellipse([*p(12, 24), *p(22, 34)], outline=line, width=w)
            draw.ellipse([*p(42, 24), *p(52, 34)], outline=line, width=w)
            draw.arc([*p(7, 36), *p(29, 60)], start=205, end=300, fill=line, width=w)
            draw.arc([*p(35, 36), *p(57, 60)], start=240, end=335, fill=line, width=w)
        elif icon_name == "cloud":
            draw.arc([*p(8, 27), *p(26, 49)], start=85, end=280, fill=line, width=w)
            draw.arc([*p(18, 14), *p(46, 44)], start=185, end=355, fill=line, width=w)
            draw.arc([*p(39, 24), *p(58, 48)], start=250, end=80, fill=line, width=w)
            draw.line([p(18, 47), p(47, 47)], fill=line, width=w)
            draw.line([p(25, 36), p(39, 36)], fill=line, width=w)
            draw.line([p(34, 31), p(39, 36), p(34, 41)], fill=line, width=w)
        elif icon_name == "robot":
            draw.rounded_rectangle([*p(17, 20), *p(47, 47)], radius=7, outline=line, width=w)
            draw.line([p(32, 13), p(32, 20)], fill=line, width=w)
            draw.ellipse([*p(23, 30), *p(27, 34)], fill=line)
            draw.ellipse([*p(37, 30), *p(41, 34)], fill=line)
            draw.line([p(26, 40), p(38, 40)], fill=line, width=w)
            draw.line([p(10, 30), p(17, 30)], fill=line, width=w)
            draw.line([p(47, 30), p(54, 30)], fill=line, width=w)
        elif icon_name == "device":
            draw.rounded_rectangle([*p(18, 9), *p(46, 55)], radius=8, outline=line, width=w)
            draw.line([p(27, 15), p(37, 15)], fill=line, width=w)
            draw.line([p(28, 49), p(36, 49)], fill=line, width=w)
            draw.ellipse([*p(24, 24), *p(40, 40)], outline=line, width=w)
        elif icon_name == "layers":
            draw.line([p(32, 10), p(55, 22), p(32, 34), p(9, 22), p(32, 10)], fill=line, width=w, joint="curve")
            draw.line([p(14, 32), p(32, 42), p(50, 32)], fill=line, width=w, joint="curve")
            draw.line([p(14, 42), p(32, 52), p(50, 42)], fill=line, width=w, joint="curve")
        elif icon_name == "algorithm":
            draw.ellipse([*p(13, 13), *p(25, 25)], outline=line, width=w)
            draw.ellipse([*p(39, 13), *p(51, 25)], outline=line, width=w)
            draw.ellipse([*p(25, 38), *p(39, 52)], outline=line, width=w)
            draw.line([p(24, 22), p(29, 39)], fill=line, width=w)
            draw.line([p(40, 22), p(35, 39)], fill=line, width=w)
            draw.line([p(25, 19), p(39, 19)], fill=line, width=w)
        elif icon_name == "spark":
            draw.line([p(32, 9), p(36, 25), p(52, 29), p(36, 35), p(32, 55), p(28, 35), p(12, 29), p(28, 25), p(32, 9)], fill=line, width=w, joint="curve")
            draw.line([p(50, 11), p(50, 21)], fill=line, width=w)
            draw.line([p(45, 16), p(55, 16)], fill=line, width=w)

    for idx, (name, spec) in enumerate(ICONS.items()):
        row = idx // cols
        col = idx % cols
        x = col * cell_w
        y = 92 + row * cell_h
        draw_icon_shape(name, color, x + 52, y + 14)
        draw.text((x + 24, y + 84), name, fill="#EAF4EF", font=font_title)
        draw.text((x + 24, y + 110), spec["label"], fill="#93A4B7", font=font_small)
    img.save(ICON_ROOT / "contact-sheet.png")


def generate(size: int, stroke: float, color_name: str, color: str) -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    for old_svg in GENERATED.glob("*.svg"):
        old_svg.unlink()
    for name in ICONS:
        (GENERATED / f"{name}.svg").write_text(
            svg(name, color, size, stroke), encoding="utf-8"
        )
    write_manifest(size, stroke, color_name, color)
    write_html(color_name)
    make_contact_sheet(color_name, color)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Shen-PPT Apple-style SVG icons.")
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--stroke", type=float, default=3.4)
    parser.add_argument("--color", default=DEFAULT_COLOR)
    parser.add_argument("--color-name", default=DEFAULT_COLOR_NAME)
    args = parser.parse_args()
    generate(size=args.size, stroke=args.stroke, color_name=args.color_name, color=args.color)
    print(f"Generated {len(ICONS)} SVG icons in {GENERATED}")
    print(f"Preview: {ICON_ROOT / 'preview.html'}")


if __name__ == "__main__":
    main()
