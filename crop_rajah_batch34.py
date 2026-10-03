#!/usr/bin/env python3
"""
Crop Rajah/Tilasm Batch 34 — Halaman 165-169 (Tilasm 21-25).

Kotak crop diperoleh dari deteksi bbox tinta otomatis (bukan tebakan):
blok teks tiap halaman ditentukan dulu lewat profil kolom, bingkai hiasan
dan bayangan lipatan dikecualikan, lalu kotak dirapatkan ke piksel tinta.

Pembersihan latar memakai koreksi flat-field, bukan ambang kecerahan tetap.
Alasannya: di sisi dalam halaman, bayangan lipatan buku membuat kecerahan
kertas melandai (pada Hal 168 dari ~130 ke ~190 dalam 45 px). Ambang tetap
akan ikut memotong glif rajah yang kebetulan berada di dalam gradien itu.
Flat-field membagi citra dengan taksiran latar kertasnya sendiri, sehingga
gradien hilang tanpa mengorbankan goresan tinta.

Catatan resolusi: scan sumber 1755x1275 px untuk satu bentangan 2 halaman,
jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan di-upscale 4x
LANCZOS mengikuti konvensi batch sebelumnya di repo ini — ketajaman optiknya
tetap setara sumber, bukan hasil scan ulang 300 DPI.
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "terjemahan", "assets")

# (sumber, keluaran, x0, y0, x1, y1) — fraksi lebar/tinggi bentangan
RAJAH = [
    ("Picture 084.jpg", "rajah-hal-167-tilasm21.jpg", 0.2245, 0.3569, 0.4667, 0.3866),
    ("Picture 084.jpg", "rajah-hal-167-tilasm22.jpg", 0.2068, 0.6830, 0.4883, 0.7625),
    ("Picture 085.jpg", "rajah-hal-168-tilasm23.jpg", 0.5880, 0.3522, 0.8450, 0.3961),
    ("Picture 085.jpg", "rajah-hal-169-tilasm24.jpg", 0.2410, 0.1490, 0.4900, 0.2447),
    ("Picture 085.jpg", "rajah-hal-169-tilasm25.jpg", 0.2427, 0.5890, 0.4917, 0.7600),
]

MARGIN_X = 0.007   # fraksi lebar bentangan
MARGIN_Y = 0.006   # fraksi tinggi bentangan
SCALE = 4
PAD = 70           # bingkai putih (piksel, setelah upscale)
BG_WINDOW = 31     # jendela taksiran latar; harus > tebal goresan
BLACK_AT = 0.55    # rasio gelap/latar yang dipetakan jadi hitam penuh
WHITE_AT = 0.88    # rasio di atas ini dipetakan jadi putih bersih 255


def flatten(img):
    """Ratakan pencahayaan lalu putihkan kertas, pertahankan goresan tinta."""
    g = np.array(img.convert("L")).astype(np.float32)

    # taksiran latar kertas: dilasi (MaxFilter) menutup goresan gelap,
    # lalu diperhalus supaya jadi permukaan pencahayaan yang mulus
    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.array(bg).astype(np.float32)
    bg = np.maximum(bg, 1.0)

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
    print(f"  {out:34s} {padded.size[0]:5d}x{padded.size[1]:<5d} "
          f"latar_putih={100 * (a > 250).mean():5.1f}%  tinta={100 * (a < 100).mean():4.1f}%")


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    print("Crop Rajah Batch 34 — Hal 165-169 (Tilasm 21-25):")
    for args in RAJAH:
        crop_rajah(*args)
    print(f"Selesai — {len(RAJAH)} rajah ke {OUTDIR}")
