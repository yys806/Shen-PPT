# -*- coding: utf-8 -*-
"""v4.1.0 质量门禁回归测试：图放大警告（吸收 ppt-master v6.1.0 'image upscale warning at 2x'）。"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

from render_pptx import check_image_upscale


def make_img(w, h):
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    Image.new("RGB", (w, h), "white").save(path)
    return path


@unittest.skipUnless(HAVE_PIL, "PIL not installed")
class TestImageUpscaleWarning(unittest.TestCase):
    def test_large_region_small_source_warns(self):
        """区域 1200x600 px、源图 400x300 px → 放大 3x → 必须警告。"""
        src = make_img(400, 300)
        try:
            region = {"x": 0, "y": 0, "w": 1200, "h": 600}
            msg = check_image_upscale(src, region)
            self.assertIsNotNone(msg, "放大 3x 应触发警告")
            self.assertIn("放大", msg)
            self.assertIn("2x", msg.replace("3.0x", "2x"))  # 文案含 2x 阈值提示
        finally:
            os.remove(src)

    def test_fit_within_2x_no_warn(self):
        """区域 800x600 px、源图 1000x800 px → 缩小 → 不警告。"""
        src = make_img(1000, 800)
        try:
            region = {"x": 0, "y": 0, "w": 800, "h": 600}
            self.assertIsNone(check_image_upscale(src, region))
        finally:
            os.remove(src)

    def test_exactly_2x_warns(self):
        """恰好 2 倍（边界）→ 警告（>=2.0）。"""
        src = make_img(500, 500)
        try:
            region = {"x": 0, "y": 0, "w": 1000, "h": 1000}
            self.assertIsNotNone(check_image_upscale(src, region))
        finally:
            os.remove(src)

    def test_missing_file_no_crash(self):
        """图片不存在 → 返回 None 不抛异常。"""
        self.assertIsNone(check_image_upscale("no_such_file.png", {"w": 800, "h": 600}))


if __name__ == "__main__":
    unittest.main()
