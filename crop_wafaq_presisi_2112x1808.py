#!/usr/bin/env python3
"""
Crop Presisi 2112x1808 — flat-field Batch-43 standard.

Default (backward-compatible): crop Halaman 206 from Picture 105.jpg.
For a one-off crop from a different scan or PDF-extracted image:

  python3 crop_wafaq_presisi_2112x1808.py \\
      --src scratch/pdf-embedded/p016-i01.jpeg \\
      --out terjemahan/rajah/rajah-pdf-016-image-01-presisi-2112x1808.jpg

  python3 crop_wafaq_presisi_2112x1808.py --src 'Picture 002.jpg' \\
      --box 245 230 815 535 \\
      --out terjemahan/rajah/rajah-pdf-010-image-01-presisi-2112x1808.jpg

BOX uses x0 y0 x1 y1 pixel coordinates. If --box is omitted, the complete
source image is used. Output is always 2112x1808 px, 300 DPI, LANCZOS, with a
white canvas and the same gentle two-point flat-field mapping used for Batch
43 (BG_WINDOW=31, BLACK_AT=0.55, WHITE_AT=0.88, WHITE_SNAP=235). No hard
thresholding or redrawing is performed.
"""
from PIL import Image, ImageFilter
import numpy as np
import argparse
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(BASE, "Picture 105.jpg")
DEFAULT_OUT = os.path.join(
    BASE, "terjemahan", "rajah",
    "rajah-hal-206-wifaq-murabba-presisi-2112x1808.jpg",
)
DEFAULT_BOX = (988, 636, 1438, 1034)

W_OUT, H_OUT = 2112, 1808
DPI = (300, 300)
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.88
WHITE_SNAP = 250        # hanya piksel yang sudah nyaris putih dikunci 255


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


def crop_wafaq(src=DEFAULT_SRC, box=DEFAULT_BOX, out=DEFAULT_OUT):
    im = Image.open(src).convert("RGB")
    if box is None:
        box = (0, 0, im.width, im.height)
    if len(box) != 4 or box[0] < 0 or box[1] < 0 or box[2] > im.width or box[3] > im.height or box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError(f"BOX {box} di luar ukuran sumber {im.size}")

    crop = flatten(im.crop(box))
    # Skala seragam, tanpa distorsi; beri ruang 70 px di tiap sisi kanvas.
    sc = min((W_OUT - 140) / crop.size[0], (H_OUT - 140) / crop.size[1])
    new = (round(crop.size[0] * sc), round(crop.size[1] * sc))
    crop = crop.resize(new, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W_OUT, H_OUT), (255, 255, 255))
    canvas.paste(crop, ((W_OUT - new[0]) // 2, (H_OUT - new[1]) // 2))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, "JPEG", quality=95, subsampling=0, dpi=DPI)
    a = np.array(canvas.convert("L"))
    ink = a < 100
    non_ink_white = 100 * (a[~ink] == 255).mean() if (~ink).any() else 100.0
    full_white = 100 * (a == 255).mean()
    midtones = 100 * (((a >= 100) & (a < 200)).mean())
    print(f"{os.path.basename(out)}")
    print(f"  sumber      : {os.path.basename(src)}; BOX={box}; crop={box[2]-box[0]}x{box[3]-box[1]} px")
    print(f"  keluaran    : {canvas.width}x{canvas.height} px; LANCZOS {sc:.2f}x; DPI={DPI[0]}")
    print(f"  putih       : {full_white:.1f}% seluruh kanvas; {non_ink_white:.1f}% piksel non-tinta")
    print(f"  tinta/nada  : {100 * ink.mean():.2f}% tinta padat; {midtones:.2f}% nada antara")
    return out


def main():
    parser = argparse.ArgumentParser(description="Crop wafaq presisi 2112x1808 dengan flat-field Batch-43")
    parser.add_argument("--src", default=DEFAULT_SRC, help="path gambar sumber (default: Picture 105.jpg)")
    parser.add_argument("--box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="BBox px; tanpa opsi ini memakai seluruh gambar")
    parser.add_argument("--out", default=DEFAULT_OUT, help="path JPG keluaran")
    args = parser.parse_args()
    src = args.src if os.path.isabs(args.src) else os.path.join(BASE, args.src)
    out = args.out if os.path.isabs(args.out) else os.path.join(BASE, args.out)
    box = tuple(args.box) if args.box else (DEFAULT_BOX if args.src == DEFAULT_SRC and args.box is None else None)
    print("Crop Wafaq Presisi 2112x1808 — flat-field Batch-43:")
    crop_wafaq(src, box, out)
    print(f"Selesai — {out}")


if __name__ == "__main__":
    main()
