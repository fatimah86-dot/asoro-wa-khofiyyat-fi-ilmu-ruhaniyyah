#!/usr/bin/env python3
"""
Crop Rajah/Tilsam Batch 41 — Halaman 200-202.

Satu rajah pada batch ini:
  Hal201  Tilsam al-Kashf wal-Istinsar — bingkai persegi berisi lingkaran
          berlapis dengan bintang segi enam (khatam Sulaiman) di tengah,
          huruf `انه من سليمان` di pusat, huruf penjuru م ع ا ى ر.
Hal200 dan Hal202 murni teks — tanpa rajah.

Standar flat-field + latar putih murni 255 sama persis dengan Batch 38/39:
peta dua titik BLACK_AT..WHITE_AT dengan WHITE_AT = 0.84, lalu WHITE_SNAP
mengunci setiap piksel >= 235 tepat ke 255.

Catatan geometri: kolom vertikal kiri di luar bingkai (keterangan cetak
`للكشف والاستنصار` + nomor stempel perpustakaan `00201062022238`,
x=343-365) DIBUANG dari crop — tepi kiri efektif 366 px, tepat di kanan
kolom itu. Koordinat diukur dari scan tepi bingkai (bingkai miring):
kiri x=365(atas)-389(bawah), kanan x=833(atas)-855(bawah), atas
y=462-465, bawah y=862; bayangan lipatan buku (gutter) mulai x~860 ikut
dibuang. Huruf م menjulur di atas bingkai (y~452) sehingga y0 efektif
452. Baris keterangan di atas bingkai (`يستخدم في الساعات القمرية` dst.,
y<=451) dan judul bab di bawah bingkai (`دعوة السباسع الكبرى...`,
y>=890) tidak ikut — keduanya teks, bukan rajah (dicatat penuh di MD).

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2
halaman, jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan
di-upscale 4x LANCZOS mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.

Pemetaan sumber yang sudah diverifikasi lewat nomor halaman cetak:
Picture 102 -> Hal200 (kanan) / Hal201 (kiri)
Picture 103 -> Hal202 (kanan) / Hal203 (kiri)
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1)
RAJAH = [
    ("Picture 102.jpg", "rajah-hal-201-tilsam-kashf-istinsar.jpg", 0.2145, 0.3595, 0.4829, 0.6758),
]

# Pita baris (koordinat sumber, y0..y1) yang teks keterangan cetak ikut
# terpotong di dalamnya dan diputihkan, KECUALI jendela-x (huruf م yang
# menjulur di atas bingkai: x=605-665). Baris `شيخ الروحانيين ...`
# (y=448-462) bersinggungan vertikal dengan م sehingga tidak bisa
# dipisahkan lewat kotak crop saja.
TEXT_MASK = [(448, 460, 612, 612), (460, 462, 605, 665)]

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
    # putihkan pita teks keterangan yang bersinggungan dengan rajah,
    # kecuali jendela-x huruf rajah (م)
    px = np.array(im)
    for my0, my1, wx0, wx1 in TEXT_MASK:
        px[my0:my1, :wx0] = 255
        px[my0:my1, wx1:] = 255
    im = Image.fromarray(px)
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
    print("Crop Rajah Batch 41 — Hal 200-202:")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
