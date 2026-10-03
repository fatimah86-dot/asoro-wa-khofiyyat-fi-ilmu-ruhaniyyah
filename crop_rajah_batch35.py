#!/usr/bin/env python3
"""
Crop Rajah/Tilasm Batch 35 — Halaman 170-174 (Tilasm 26-30 + varian Tilasm 25).

Metode sama dengan Batch 34 (lihat crop_rajah_batch34.py):
kotak crop dari deteksi bbox tinta otomatis, latar diputihkan dengan
koreksi flat-field supaya bayangan lipatan buku hilang tanpa memotong
goresan rajah.

Khusus Hal 170 baris varian ke-3, prosa cetak `والثالث هكذا` berada
satu baris dengan goresan rajah. Keduanya dipisah lewat celah kolom
(rajah x 0.5567..0.7464, prosa x 0.7533..0.8274) sehingga yang ikut
ter-crop hanya rajahnya, sesuai kaidah "hanya Rajah tanpa teks cetak".

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2
halaman, jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan
di-upscale 4x LANCZOS mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1) — fraksi lebar/tinggi bentangan
RAJAH = [
    ("Picture 086.jpg", "rajah-hal-170-varian-sathr2.jpg", 0.5715, 0.1624, 0.8291, 0.1992),
    ("Picture 086.jpg", "rajah-hal-170-varian-sathr3.jpg", 0.5567, 0.2047, 0.7464, 0.2345),
    ("Picture 086.jpg", "rajah-hal-170-tilasm26.jpg",      0.5647, 0.5161, 0.8279, 0.7953),
    ("Picture 086.jpg", "rajah-hal-171-tilasm27.jpg",      0.1937, 0.3569, 0.4632, 0.4847),
    ("Picture 087.jpg", "rajah-hal-172-tilasm28.jpg",      0.5721, 0.2000, 0.8262, 0.5404),
    ("Picture 087.jpg", "rajah-hal-172-tilasm29.jpg",      0.5681, 0.6808, 0.8433, 0.7851),
    ("Picture 087.jpg", "rajah-hal-173-tilasm30.jpg",      0.1624, 0.4063, 0.4678, 0.7937),
]

MARGIN_X = 0.007
MARGIN_Y = 0.006
SCALE = 4
PAD = 70
BG_WINDOW = 31     # jendela taksiran latar; harus > tebal goresan
BLACK_AT = 0.55    # rasio gelap/latar yang dipetakan jadi hitam penuh
WHITE_AT = 0.88    # rasio di atas ini dipetakan jadi putih bersih 255


def flatten(img):
    """Ratakan pencahayaan lalu putihkan kertas, pertahankan goresan tinta."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg                      # 1.0 = kertas, makin kecil makin gelap
    out = np.clip((ratio - BLACK_AT) / (WHITE_AT - BLACK_AT), 0, 1) * 255
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
    print(f"  {out:38s} {padded.size[0]:5d}x{padded.size[1]:<5d} "
          f"latar_putih={100 * (a > 250).mean():5.1f}%  tinta={100 * (a < 100).mean():4.1f}%")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 35 — Hal 170-174 (Tilasm 26-30 + varian Tilasm 25):")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
