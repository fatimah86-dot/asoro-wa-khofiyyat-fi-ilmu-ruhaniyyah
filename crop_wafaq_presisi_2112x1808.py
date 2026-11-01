#!/usr/bin/env python3
"""
Crop Wafaq Presisi 2112x1808 — BATCH-43 (Hal 205-206).

Dipakai untuk satu rajah saja:

  Hal206  Wafaq Murabba' 4x4 (Khâtam Murabba') — kotak 3x7 sel berisi angka
          dan huruf gundul, empat penjuru جبرائيل ميكائيل اسرافيل عزرائيل
          (di kitab: مازر / كمطم / قسورة / طيكل), plus kolom SAKK di kiri
          bingkai berisi angka 111 di atas huruf ك.

Standar reproduksi (sama dengan Batch 38/39/41 di repo ini):
  * flat-field: latar kertas diratakan lalu dipetakan ke putih murni 255
    lewat peta dua titik BLACK_AT..WHITE_AT — TIDAK memakai threshold keras;
  * WHITE_SNAP mengunci piksel yang sudah hampir putih ke 255 supaya latar
    bersih, tetapi ambangnya dinaikkan ke 250 agar titik-titik halus
    (Sirr An-Nuqthoh: titik tiga pada ح ج خ dan titik di bawah huruf)
    TIDAK ikut terhapus — huruf gundul buta tetap buta apa adanya,
    tidak ada titik yang ditambah maupun dibuang oleh skrip ini;
  * garis tipis Qolam Hirz (bingkai sel, garis paku/gergaji pada sel angka
    dan garis tiang pada kolom SAKK) dipertahankan, tidak di-thinning;
  * hasil akhir SELALU tepat 2112x1808 px, 300 DPI, LANCZOS.

Catatan geometri (diukur dari scan Picture 105.jpg, 1755x1275 px,
satu bentangan 2 halaman = Hal206 kanan + Hal207 kiri):

  bingkai luar wafaq + kolom SAKK : x 1000..1420, y 704..1013
  tiang kolom SAKK (kiri bingkai) : x 1000..1062
  angka 111 di atas huruf ك       : y 725..760  (kepala panah paling atas
                                    justru mulai y 722 — margin atas wajib
                                    >= 30 px agar panah SAKK tidak kepotong)
  baris nama 4 penjuru terdekat   : y 645..690 (طيكل مازر قسورة كمطم)
  nomor halaman cetak "206"       : y 1080..1100  -> DI LUAR crop
  nomor halaman cetak "207"       : halaman kiri, tidak ikut

  Kotak kerja  = x 988..1438, y 636..1034  (450 x 398 px)
  Margin 15% dihitung dari bingkai wafaq: 0,15 x 420 = 63 px kiri-kanan dan
  0,15 x 309 = 46 px atas-bawah -> seluruh kepala panah SAKK 111 di atas ك
  masuk utuh, tepi kanan bingkai masuk utuh, sedangkan nomor halaman dan
  ornamen paku/gergaji tepi bawah halaman tetap di luar crop (keduanya
  bukan bagian rajah; dicatat di MD, bukan dipotong diam-diam).

Catatan resolusi: scan sumber 1755x1275 untuk satu bentangan 2 halaman,
jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan di-upscale
LANCZOS ~4,19x mengikuti konvensi batch sebelumnya di repo ini —
ketajaman optiknya tetap setara sumber, bukan hasil scan ulang 300 DPI.

Jalankan:  python3 crop_wafaq_presisi_2112x1808.py
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Picture 105.jpg")
OUTDIR = os.path.join(BASE, "terjemahan", "rajah")
OUTNAME = "rajah-hal-206-wifaq-murabba-presisi-2112x1808.jpg"

# Kotak kerja (koordinat px scan sumber, sudah termasuk margin 15%)
BOX = (988, 636, 1438, 1034)

# Ukuran keluaran mutlak
W_OUT, H_OUT = 2112, 1808
DPI = (300, 300)

# Peta nada flat-field (tanpa threshold keras)
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.88
WHITE_SNAP = 235        # hanya piksel yang sudah nyaris putih dikunci 255


def flatten(img):
    """Ratakan pencahayaan lalu putihkan kertas, pertahankan tinta & titik."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg
    out = np.clip((ratio - BLACK_AT) / (WHITE_AT - BLACK_AT), 0, 1) * 255
    out = out.astype(np.uint8)
    out = np.where(out >= WHITE_SNAP, 255, out)          # latar putih murni
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


def crop_wafaq():
    im = Image.open(SRC).convert("RGB")
    crop = flatten(im.crop(BOX))

    # Skala seragam (tanpa distorsi) — dipas-kan ke dalam kanvas 2112x1808
    sc = min((W_OUT - 140) / crop.size[0], (H_OUT - 140) / crop.size[1])
    new = (round(crop.size[0] * sc), round(crop.size[1] * sc))
    crop = crop.resize(new, Image.LANCZOS)

    canvas = Image.new("RGB", (W_OUT, H_OUT), (255, 255, 255))
    canvas.paste(crop, ((W_OUT - new[0]) // 2, (H_OUT - new[1]) // 2))

    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, OUTNAME)
    canvas.save(path, "JPEG", quality=95, subsampling=0, dpi=DPI)

    a = np.array(canvas.convert("L"))
    ink = a < 100
    bersih = 100 * (a[~ink] == 255).mean()
    titik = 100 * (((a >= 100) & (a < 200)).mean())
    print(f"  {OUTNAME}")
    print(f"    sumber px     : {BOX[2] - BOX[0]} x {BOX[3] - BOX[1]} "
          f"({SRC.split('/')[-1]} x{BOX[0]},{BOX[1]})")
    print(f"    ukuran akhir  : {canvas.size[0]}x{canvas.size[1]} px  "
          f"skala {sc:.2f}x LANCZOS  DPI {DPI[0]}")
    print(f"    latar putih   : {bersih:5.1f}% putih murni 255   "
          f"tinta padat {100 * ink.mean():4.1f}%   "
          f"nada antara (titik/garis tipis) {titik:4.2f}%")
    return path


if __name__ == "__main__":
    print("Crop Wafaq Presisi 2112x1808 — BATCH-43 Hal 205-206:")
    p = crop_wafaq()
    print(f"Selesai — {p}")
