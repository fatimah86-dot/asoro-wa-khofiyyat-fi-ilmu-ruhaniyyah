#!/usr/bin/env python3
"""
Crop Rajah Batch 48 — Halaman 217 dan 218 (bentangan Picture 109 / Picture 110).

Dua rajah, keduanya khatam bujur sangkar bergaris dengan bulatan di tengah dan
tulisan hîrzî kursif di keempat sudut:

  Hal 217  Khatam "Mundal Âkhar"  — Picture 109.jpg, belahan KIRI
  Hal 218  Khatam "Mandâl Nafsî"  — Picture 110.jpg, belahan KANAN

Standar reproduksi sama persis dengan Batch 43/44/47 (tanpa redraw, tanpa
threshold keras):

  * flat-field: latar kertas diratakan (BG_WINDOW=31) lalu dipetakan dua titik
    BLACK_AT=0.55 .. WHITE_AT=0.88; WHITE_SNAP=235 mengunci piksel yang sudah
    nyaris putih ke 255;
  * titik-titik pada huruf kursif di sudut khatam DIPERTAHANKAN apa adanya —
    skrip ini tidak menambah dan tidak membuang titik;
  * garis tipis kotak khatam tidak di-thinning;
  * keluaran SELALU tepat 2112x1808 px, 300 DPI, LANCZOS, kanvas putih dengan
    margin 70 px (isi di-skala seragam agar memenuhi kanvas, tanpa distorsi).

Catatan geometri (hasil verifikasi lewat pengukuran tinta, bukan tebakan):

  Hal 217: khatam menempati px x 394..718, y 516..828 pada Picture 109.jpg
           (belahan kiri, lebar 877 px). Tulisan sudut kiri-atas `روش` dan
           ekor tulisan sudut bawah keluar dari kotak, jadi BOX dilebarkan ke
           x 386..726, y 508..836. Judul cetak `وهذا هو الخاتم` di atas rajah
           dan baris `صفة مندل عليه المعمول` di bawahnya DIKELUARKAN.

  Hal 218: khatam menempati px x 1074..1346, y 385..640 pada Picture 110.jpg
           (belahan kanan, mulai x = 877). BOX x 1062..1342, y 376..646.
           Judul `وهذا ما تكتب` di atasnya DIKELUARKAN.

  Tidak ada SAKK 111 pada kedua rajah; tidak ada angka pada kedua rajah.
  Tulisan sudut dibiarkan sebagai gambar (kursif, tanpa harakat) dan TIDAK
  ditranskripsikan sebagai huruf pasti — sama dengan perlakuan Batch 47.
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "rajah")

W_OUT, H_OUT = 2112, 1808
DPI = (300, 300)
PAD = 70
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.88
WHITE_SNAP = 235

# (sumber, keluaran, x0, y0, x1, y1)
RAJAH = [
    ("Picture 109.jpg",
     "rajah-hal-217-khatam-mandal-akhir-presisi-2112x1808.jpg",
     386, 508, 726, 836),
    ("Picture 110.jpg",
     "rajah-hal-218-khatam-mandal-nafsi-murabba-presisi-2112x1808.jpg",
     1062, 376, 1342, 646),
]


def flatten(img):
    """Ratakan pencahayaan kertas; pertahankan tinta, titik, dan garis tipis."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg
    out = np.clip((ratio - BLACK_AT) / (WHITE_AT - BLACK_AT), 0, 1) * 255
    out = out.astype(np.uint8)
    out = np.where(out >= WHITE_SNAP, 255, out)
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


def crop_rajah(src, out, x0, y0, x1, y1):
    im = Image.open(os.path.join(BASE, src)).convert("RGB")
    if not (0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height):
        raise ValueError(f"BOX {x0},{y0},{x1},{y1} di luar {im.size}")

    crop = flatten(im.crop((x0, y0, x1, y1)))
    sc = min((W_OUT - PAD * 2) / crop.width, (H_OUT - PAD * 2) / crop.height)
    new = (round(crop.width * sc), round(crop.height * sc))
    crop = crop.resize(new, Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (W_OUT, H_OUT), (255, 255, 255))
    canvas.paste(crop, ((W_OUT - new[0]) // 2, (H_OUT - new[1]) // 2))
    canvas.save(os.path.join(OUTDIR, out), "JPEG", quality=95, subsampling=0, dpi=DPI)

    a = np.array(canvas.convert("L"))
    ink = a < 100
    non_ink_white = 100 * (a[~ink] == 255).mean() if (~ink).any() else 100.0
    full_white = 100 * (a == 255).mean()
    ys, xs = np.where(ink)
    print(f"{out}")
    print(f"  sumber    : {src}; BOX={x0},{y0},{x1},{y1} = {x1-x0}x{y1-y0} px")
    print(f"  keluaran  : {canvas.width}x{canvas.height} px; LANCZOS {sc:.2f}x; DPI 300")
    print(f"  putih     : {full_white:.1f}% kanvas; {non_ink_white:.1f}% piksel non-tinta")
    print(f"  tinta     : {100 * ink.mean():.2f}%")
    print(f"  tepi tinta: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()} "
          f"(kanvas 0..{W_OUT-1} / 0..{H_OUT-1})")
    return out


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 48 — Hal 217 & 218:")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
