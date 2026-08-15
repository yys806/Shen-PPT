#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_preview.py — 导出 pptx 每页预览 PNG（QA 用）
策略: ① soffice(LibreOffice) headless 转 PDF → pymupdf 转 PNG
      ② 无 soffice 且 Windows → PowerPoint COM 导出（注意单实例冲突，先问用户）
用法:
  python export_preview.py input.pptx <预览目录>
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_soffice():
    for cand in ["soffice", "libreoffice"]:
        p = shutil.which(cand)
        if p:
            return p
    for cand in [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]:
        if Path(cand).exists():
            return cand
    return None


def soffice_export(pptx_path, out_dir):
    soffice = find_soffice()
    if not soffice:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "deck.pdf"
        r = subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(pptx_path)],
            capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not pdf_path.exists():
            print(f"soffice 转换失败: {r.stderr[:300]}")
            return False
        try:
            import fitz  # pymupdf
        except ImportError:
            print("缺少 pymupdf，尝试 pdftoppm…")
            r2 = subprocess.run(["pdftoppm", "-png", "-r", "80", str(pdf_path), str(out_dir / "slide")],
                                capture_output=True, text=True, timeout=300)
            return r2.returncode == 0
        out_dir.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=80)
            pix.save(str(out_dir / f"slide-{i+1:02d}.png"))
        print(f"✓ 已导出 {len(doc)} 页预览 → {out_dir}")
        return True
    return False


def com_export(pptx_path, out_dir):
    """PowerPoint COM 导出（Windows 回退）。注意：PowerPoint 单实例，操作前确认用户没在开 PPT。"""
    pptx_path = str(Path(pptx_path).resolve())  # COM 进程 cwd 不同，必须绝对路径
    out_dir = str(Path(out_dir).resolve())
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    ps = r"""
param($src, $outDir)
$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($src, $true, $false, $false)  # ReadOnly, WithWindow=$false
  $pres.Export($outDir, "PNG", 1280, 720)
  $pres.Close()
  Write-Host "COM_EXPORT_OK"
} finally {
  $pp.Quit()
}
"""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8-sig") as f:
        f.write(ps)
        ps_path = f.name
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps_path,
             "-src", str(pptx_path), "-outDir", str(out_dir)],
            capture_output=True, text=True, encoding="gbk", errors="replace", timeout=600)
        ok = "COM_EXPORT_OK" in r.stdout
        if ok:
            n = len(list(Path(out_dir).glob("*.png")))
            print(f"✓ 已导出 {n} 页预览（COM）→ {out_dir}")
        else:
            print(f"COM 导出失败: {r.stdout[-300:]} {r.stderr[-300:]}")
        return ok
    finally:
        Path(ps_path).unlink(missing_ok=True)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out_dir = sys.argv[1], sys.argv[2]
    if not soffice_export(src, out_dir):
        print("soffice 不可用，回退 PowerPoint COM…")
        if not com_export(src, out_dir):
            sys.exit("预览导出失败：请安装 LibreOffice 或确认 PowerPoint 可用且未被占用")


if __name__ == "__main__":
    main()
