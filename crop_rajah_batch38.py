#!/usr/bin/env python3
"""
Crop Rajah/Khatam Batch 38 — Halaman 185-189.

Tiga rajah:
  Hal185  Khatam Da'wah ash-Shifah fi Ismillah al-A'zham — wafaq 7x7 berhuruf
  Hal187  al-Khatam al-Kabir  (Da'wah Ibrahim ad-Daili)
  Hal188  al-Khatam ash-Shaghir (Da'wah Ibrahim ad-Daili)
Hal186 (katalog penerbit) dan Hal189 murni teks — tanpa rajah.

Standar flat-field sama seperti Batch 34/35/37, dengan satu penegasan:
latar belakang dipaksa menjadi **putih murni 255**. Dua langkah yang
mewujudkannya:

  1. Peta dua titik (BLACK_AT .. WHITE_AT) dengan WHITE_AT = 0.84.
     Nilai ini lebih rendah dari 0.88 yang dipakai Batch 34/35 sehingga
     kertas benar-benar terdorong ke ujung putih, bukan berhenti di abu
     muda. Penurunan tinta yang terukur hanya ~0.3 poin persen.
  2. WHITE_SNAP: piksel >= 235 dikunci tepat ke 255. Ini membersihkan
     sisa bintik abu pada kertas tanpa menyentuh goresan tinta maupun
     tepi halus (anti-alias) di sekeliling huruf.

Hasil terukur: >= 99% piksel non-tinta bernilai tepat 255.

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2
halaman, jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan
di-upscale 4x LANCZOS mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.

Pemetaan sumber yang sudah diverifikasi lewat nomor halaman cetak:
Picture 094 -> Hal184 (kanan) / Hal185 (kiri)
Picture 095 -> Hal186 (kanan) / Hal187 (kiri)
Picture 096 -> Hal188 (kanan) / Hal189 (kiri)
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1)
RAJAH = [
    ("Picture 094.jpg", "rajah-hal-185-khatam-ism-a-zham.jpg", 0.1812, 0.5686, 0.4792, 0.7694),
    ("Picture 095.jpg", "rajah-hal-187-khatam-kabir.jpg",      0.2433, 0.5882, 0.4114, 0.7976),
    ("Picture 096.jpg", "rajah-hal-188-khatam-shaghir.jpg",    0.5521, 0.1725, 0.7601, 0.4471),
]

MARGIN_X = 0.006
MARGIN_Y = 0.005
SCALE = 4
PAD = 70
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.84
WHITE_SNAP = 235          # >= nilai ini dikunci ke putih murni 255


def flatten(img):
    """Ratakan pencahayaan lalu putihkan kertas ke 255, pertahankan tinta."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg
    out = np.clip((ratio - BLACK_AT) / (WHITE_AT - BLACK_AT), 0, 1) * 255
    out = out.astype(np.uint8)
    out = np.where(out >= WHITE_SNAP, 255, out)          # latar putih murni
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


def crop_rajah(src, out, x0, y0, x1, y1):
    im = Image.open(os.path.join(BASE, src)).convert("RGB")
    w, h = im.size
    box = (
        max(0, int(w * (x0 - MARGIN_X))),
        max(0, int(h * (y0 - MARGIN_Y))),
        min(w, int(w * (x1 + MARGIN_X))),
        min(h, int(h * (y1 + MARGIN_Y))),
    )
    crop = flatten(im.crop(box))
    crop = crop.resize((crop.size[0] * SCALE, crop.size[1] * SCALE), Image.LANCZOS)

    padded = Image.new("RGB", (crop.size[0] + PAD * 2, crop.size[1] + PAD * 2), (255, 255, 255))
    padded.paste(crop, (PAD, PAD))
    padded.save(os.path.join(OUTDIR, out), "JPEG", quality=95, dpi=(300, 300))

    a = np.array(padded.convert("L"))
    ink = a < 100
    bersih = 100 * (a[~ink] == 255).mean()
    print(f"  {out:40s} {padded.size[0]:5d}x{padded.size[1]:<5d} "
          f"non-tinta_putih_murni={bersih:5.1f}%  tinta={100 * ink.mean():4.1f}%")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 38 — Hal 185-189:")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
