#!/usr/bin/env python3
"""
Crop Rajah/Tilsam Batch 39 — Halaman 190-194.

Dua rajah, keduanya tilsam baris (bukan wafaq berkotak):
  Hal191  Tilsam at-Tashrif ats-Tsani  — dua baris goresan bergaris bawah
  Hal192  Tilsam at-Tashrif as-Sadis   — satu baris goresan bergaris bawah
Hal190, Hal193, dan Hal194 murni teks — tanpa rajah.

Standar flat-field + latar putih murni 255 sama persis dengan Batch 38:
peta dua titik BLACK_AT..WHITE_AT dengan WHITE_AT = 0.84, lalu WHITE_SNAP
mengunci setiap piksel >= 235 tepat ke 255.

Catatan geometri khusus batch ini: kedua tilsam adalah coretan satu baris
yang diapit teks cetak di atas (judul `وهذا ما تكتب`) dan di bawahnya.
Deteksi kotak karena itu dibatasi pada pita-y di antara kedua teks
tersebut. Pada Hal192 pembatasan sumbu-x juga wajib: goresan garis bawah
tilsam dan **bingkai hiasan tepi halaman** berada pada baris piksel yang
sama, sehingga pengukuran tanpa batas-x melaporkan tepi kanan di
x=0.8741 (itu bingkai halaman, bukan tilsam). Tepi kanan yang benar
adalah x=0.7396.

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2
halaman, jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan
di-upscale 4x LANCZOS mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.

Pemetaan sumber yang sudah diverifikasi lewat nomor halaman cetak:
Picture 097 -> Hal190 (kanan) / Hal191 (kiri)
Picture 098 -> Hal192 (kanan) / Hal193 (kiri)
Picture 099 -> Hal194 (kanan) / Hal195 (kiri)
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1)
RAJAH = [
    ("Picture 097.jpg", "rajah-hal-191-tilasm-tashrif-tsani.jpg", 0.1812, 0.1733, 0.4541, 0.2612),
    ("Picture 098.jpg", "rajah-hal-192-tilasm-tashrif-sadis.jpg", 0.5510, 0.6588, 0.7396, 0.6878),
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
    print(f"  {out:42s} {padded.size[0]:5d}x{padded.size[1]:<5d} "
          f"non-tinta_putih_murni={bersih:5.1f}%  tinta={100 * ink.mean():4.1f}%")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 39 — Hal 190-194:")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
