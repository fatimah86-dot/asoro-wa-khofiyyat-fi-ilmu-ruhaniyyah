#!/usr/bin/env python3
"""
Crop Rajah/Khatam Batch 37 — Halaman 180-184.

Batch ini hanya memuat satu rajah: Khatam Da'wah al-Jalalah (wafaq 3x3
berhuruf) di Hal180. Empat halaman sisanya murni teks doa.

Dua catatan khusus pada crop ini:

1. Khatam berada di sisi lipatan buku, sehingga tepi kirinya (tulisan
   tepi menurun `تقوله ... الله العظيم`) terbenam dalam bayangan
   gutter. Deteksi tinta mentah tidak mampu melihatnya — batas kotak
   karena itu ditetapkan dari pemeriksaan visual atas citra yang sudah
   dikoreksi flat-field, bukan dari ambang kecerahan.

2. Teks cetak `وهذا صفة الخاتم لدعوة الجلالة` berada hanya ~1-2 px di
   sebelah kanan bingkai khatam. Margin kanan karena itu dibuat nol
   (MARGIN_R) supaya prosa itu tidak ikut terpotong, sementara ketiga
   sisi lain tetap diberi margin normal.

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2
halaman, jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan
di-upscale 4x LANCZOS mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.

Catatan sumber: `Picture 092.jpg` adalah foto ulang dari bentangan yang
sama dengan `Picture 091.jpg` (keduanya Hal180-181). Dipakai 091 karena
keduanya praktis identik; 092 tersedia sebagai cadangan.
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1, margin_kanan)
RAJAH = [
    ("Picture 091.jpg", "rajah-hal-180-khatam-jalalah.jpg", 0.5527, 0.5922, 0.7219, 0.7953, 0.0015),
]

MARGIN_X = 0.006
MARGIN_Y = 0.005
SCALE = 4
PAD = 70
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.82   # lebih rendah dari Batch 34/35 (0.88): khatam ini
                  # menempel lipatan buku, titik putih diturunkan agar
                  # sisa bayangan gutter benar-benar jadi kertas putih


def flatten(img):
    """Ratakan pencahayaan lalu putihkan kertas, pertahankan goresan tinta."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg
    out = np.clip((ratio - BLACK_AT) / (WHITE_AT - BLACK_AT), 0, 1) * 255
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


def crop_rajah(src, out, x0, y0, x1, y1, margin_r=None):
    mr = MARGIN_X if margin_r is None else margin_r
    im = Image.open(os.path.join(BASE, src)).convert("RGB")
    w, h = im.size
    box = (
        max(0, int(w * (x0 - MARGIN_X))),
        max(0, int(h * (y0 - MARGIN_Y))),
        min(w, int(w * (x1 + mr))),
        min(h, int(h * (y1 + MARGIN_Y))),
    )
    crop = flatten(im.crop(box))
    crop = crop.resize((crop.size[0] * SCALE, crop.size[1] * SCALE), Image.LANCZOS)

    padded = Image.new("RGB", (crop.size[0] + PAD * 2, crop.size[1] + PAD * 2), (255, 255, 255))
    padded.paste(crop, (PAD, PAD))
    padded.save(os.path.join(OUTDIR, out), "JPEG", quality=95, dpi=(300, 300))

    a = np.array(padded.convert("L"))
    print(f"  {out:40s} {padded.size[0]:5d}x{padded.size[1]:<5d} "
          f"latar_putih={100 * (a > 250).mean():5.1f}%  tinta={100 * (a < 100).mean():4.1f}%")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 37 — Hal 180-184 (Khatam Da'wah al-Jalalah):")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
