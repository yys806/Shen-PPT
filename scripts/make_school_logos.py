#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合成三校横版校徽：圆形官方校徽 + 书法体校名 + 英文校名"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ASSETS = Path(r"D:\hermes\skills\productivity\ppt\assets\schools")
FONTS = r"C:\Windows\Fonts"

# 学校配置：目录 / 校名 / 英文 / 校色 / 中文字体
SCHOOLS = {
    "pku":      {"cn": "北京大学", "en": "PEKING UNIVERSITY", "color": "#9A0001", "font": "FZSTK.TTF"},
    "tsinghua": {"cn": "清华大学", "en": "TSINGHUA UNIVERSITY", "color": "#660874", "font": "STLITI.TTF"},
    "tongji":   {"cn": "同济大学", "en": "TONGJI UNIVERSITY", "color": "#0055A4", "font": "FZSTK.TTF"},
}

def compose(school, cfg):
    seal = Image.open(ASSETS / school / "圆形校徽.png").convert("RGBA")
    # 校徽高度 120px（横版总高约 150）
    seal_h = 120
    seal_w = int(seal.width * seal_h / seal.height)
    seal = seal.resize((seal_w, seal_h), Image.LANCZOS)

    cn_font = ImageFont.truetype(FONTS + "\\" + cfg["font"], 64)
    en_font = ImageFont.truetype(FONTS + "\\arial.ttf", 24)

    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    cn_w = d.textlength(cfg["cn"], font=cn_font)
    en_w = d.textlength(cfg["en"], font=en_font)

    gap = 28
    W = int(seal_w + gap + max(cn_w, en_w) + 8)
    H = 160
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.paste(seal, (0, (H - seal_h) // 2), seal)

    dd = ImageDraw.Draw(canvas)
    # 中文校名（书法体，校色）
    dd.text((seal_w + gap, 18), cfg["cn"], font=cn_font, fill=cfg["color"])
    # 英文校名
    dd.text((seal_w + gap, 108), cfg["en"], font=en_font, fill="#333333")

    out = ASSETS / school / "横版校徽.png"
    canvas.save(out)
    print(f"✅ {school}: {canvas.size} → {out.name}")

for s, cfg in SCHOOLS.items():
    compose(s, cfg)
