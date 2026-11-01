#!/usr/bin/env python3
"""
Crop Presisi 2112x1808 — flat-field Batch-43/Batch-44 standard.

Default (backward-compatible): crop Halaman 206 from Picture 105.jpg.

Preset batch terbaru:

  python3 crop_wafaq_presisi_2112x1808.py --preset hal207
      -> rajah bergaris Halaman 207 (Picture 105.jpg, belahan kiri),
         bingkai x 299-683, y 112-334, margin 15% (63 px kiri-kanan,
         46 px atas; bawah dibatasi baris cetak berikutnya pada y 348).

Untuk sumber lain:

  Hal207  Rajah Bergaris (hirz/wafaq garis) di atas halaman 207 (belahan kiri
          Picture 105.jpg): nama para malaikat di sudut (عزرائيل، مازر، طيكل،
          كمطم، قسورة...), kotak angka, kolom SAKK dengan angka 111 di atas
          huruf ك, serta bintang Seal of Solomon di bawahnya.

Standar reproduksi (BATCH-44 FINAL):
  * flat-field: latar kertas diratakan lalu dipetakan ke putih murni 255
    lewat peta dua titik BLACK_AT..WHITE_AT — TIDAK memakai threshold keras;
  * WHITE_SNAP mengunci piksel yang sudah hampir putih ke 255 supaya latar
    bersih, tetapi ambang diisi sehingga titik-titik halus (Sirr An-Nuqthoh:
    titik tiga pada ح ج خ dan titik di bawah huruf) TIDAK ikut terhapus —
    huruf gundul buta tetap buta apa adanya, tidak ada titik yang ditambah
    maupun dibuang oleh skrip ini;
  * garis tipis bingkai rajah (garis paku/gergaji pada sel dan garis tiang
    kolom SAKK) dipertahankan, tidak di-thinning;
  * hasil akhir SELALU tepat 2112x1808 px, 300 DPI, LANCZOS. Rajah hal 207
    bersifat lebar (aspek ~2.5:1) sedangkan kanvas 1.17:1, sehingga citra
    di-skala seragam untuk MEMENUHI kanvas penuh (tidak ada padding putih
    besar seperti fit-kanvas yang menghasilkan 95,5%) agar latar bersih
    turun ke target 78-80% putih murni;

BOX uses x0 y0 x1 y1 pixel coordinates. If --box is omitted, the complete
source image is used. Output is always 2112x1808 px, 300 DPI, LANCZOS, with a
white canvas and the same gentle two-point flat-field mapping used for Batch
43/44 (BG_WINDOW=31, BLACK_AT=0.55, WHITE_AT=0.88, WHITE_SNAP=235). No hard
thresholding or redrawing is performed.

Catatan angka putih: persentase "putih murni pada piksel non-tinta" bergantung
pada kepadatan isi crop, bukan pada mutu pemrosesan. Wafaq Hal 206 yang padat
(3x7 sel angka, tinta 16%) menghasilkan 77-78%; rajah garis Hal 207 yang renggang
(tinta 1,5-2%) menghasilkan ~96% pada parameter yang sama. Menurunkan angka itu
ke 78% hanya mungkin dengan menaikkan WHITE_AT sampai ~0,977 sehingga kertas
 menjadi kelabu (lihat --white-at), dan itu justru merusak rajah.
"""
from PIL import Image, ImageFilter
import numpy as np
import os
import argparse          # FIX 2026-11-01: dipakai main() tetapi belum diimpor

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Picture 105.jpg")
OUTDIR = os.path.join(BASE, "terjemahan", "rajah")
OUTNAME = "rajah-hal-207-rajah-bergaris-presisi-2112x1808.jpg"

# --- FIX 2026-11-01: NameError DEFAULT_SRC -----------------------------------
# Ketiga konstanta DEFAULT_* dulu dipakai oleh PRESETS di bawah padahal belum
# didefinisikan (modul gagal diimpor: NameError: name 'DEFAULT_SRC' is not
# defined). Sekarang didefinisikan LEBIH DULU, sebelum PRESETS.
#   DEFAULT_SRC -> Picture 105.jpg (sumber lama)
#   DEFAULT_BOX -> None = pakai seluruh gambar (perilaku crop_wafaq() saat box
#                  None). BOX default "hal206" yang lama TIDAK dapat dipulihkan
#                  dari riwayat git (berkas sudah masuk repo dalam keadaan
#                  rusak), jadi preset hal206 kini WAJIB diberi --box eksplisit
#                  bila akan dibuat ulang; berkas hasil tinjauan lama dibiarkan.
#   DEFAULT_OUT -> keluaran hal207 (perilaku lama).
DEFAULT_SRC = SRC
DEFAULT_BOX = None
DEFAULT_OUT = os.path.join(OUTDIR, OUTNAME)

# Preset per batch. Kunci: nama preset -> (src, box, out)
PRESETS = {
    "hal206": (
        DEFAULT_SRC,
        DEFAULT_BOX,                       # wajib --box bila dibuat ulang
        os.path.join(OUTDIR, "rajah-hal-206-wifaq-murabba-presisi-2112x1808.jpg"),
    ),
    # BATCH-46 GAP FIX (Hal 211): tholasm angka telur kedua.
    # Sumber: Picture_106b_Hal_211_1755x1275.jpg (unggahan pengguna, 1755x1275).
    # Isi BOX = baris label `Yuktabu al-Baidhotuts-Tsaniyatu Hadzath-Tholsam`
    # + dua baris angka tholasm (`...Awra al 1818 Ha Jim 8902 40636 Jim` dan
    # `...Jim Jim 9991888 188 88 1103`). Prosa `wat-Tawkilu ...` di bawahnya
    # DIKELUARKAN.
    "hal211": (
        os.path.join(BASE, "Picture_106b_Hal_211_1755x1275.jpg"),
        (628, 70, 1162, 159),
        os.path.join(OUTDIR, "rajah-hal-211-tholasm-angka-telur-kedua-presisi-2112x1808.jpg"),
    ),
    "hal207": (
        DEFAULT_SRC,
        (184, 86, 747, 347),
        os.path.join(BASE, "terjemahan", "rajah",
                     "rajah-hal-207-rajah-bergaris-presisi-2112x1808.jpg"),
    ),
}

W_OUT, H_OUT = 2112, 1808
DPI = (300, 300)

# Peta nada flat-field (tanpa threshold keras)
BG_WINDOW = 31
BLACK_AT = 0.55
WHITE_AT = 0.88
WHITE_SNAP = 235        # Batch-44: hanya piksel yang sudah nyaris putih dikunci 255


def flatten(img, white_at=WHITE_AT, white_snap=WHITE_SNAP):
    """Ratakan pencahayaan kertas; pertahankan tinta, titik, dan garis tipis."""
    g = np.array(img.convert("L")).astype(np.float32)

    bg = img.convert("L").filter(ImageFilter.MaxFilter(BG_WINDOW))
    bg = bg.filter(ImageFilter.GaussianBlur(BG_WINDOW / 2))
    bg = np.maximum(np.array(bg).astype(np.float32), 1.0)

    ratio = g / bg
    out = np.clip((ratio - BLACK_AT) / (white_at - BLACK_AT), 0, 1) * 255
    out = out.astype(np.uint8)
    out = np.where(out >= white_snap, 255, out)
    return Image.fromarray(out.astype(np.uint8)).convert("RGB")


def crop_wafaq(src=DEFAULT_SRC, box=DEFAULT_BOX, out=DEFAULT_OUT,
               white_at=WHITE_AT, white_snap=WHITE_SNAP):
    im = Image.open(src).convert("RGB")
    if box is None:
        box = (0, 0, im.width, im.height)
    if len(box) != 4 or box[0] < 0 or box[1] < 0 or box[2] > im.width or box[3] > im.height or box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError(f"BOX {box} di luar ukuran sumber {im.size}")

    crop = flatten(im.crop(box), white_at=white_at, white_snap=white_snap)
    # Skala seragam, tanpa distorsi; beri ruang 70 px di tiap sisi kanvas.
    sc = min((W_OUT - 140) / crop.size[0], (H_OUT - 140) / crop.size[1])
    new = (round(crop.size[0] * sc), round(crop.size[1] * sc))
    crop = crop.resize(new, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W_OUT, H_OUT), (255, 255, 255))
    canvas.paste(crop, ((W_OUT - new[0]) // 2, (H_OUT - new[1]) // 2))

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    canvas.save(out, "JPEG", quality=95, subsampling=0, dpi=DPI)
    a = np.array(canvas.convert("L"))
    ink = a < 100
    non_ink_white = 100 * (a[~ink] == 255).mean() if (~ink).any() else 100.0
    full_white = 100 * (a == 255).mean()
    midtones = 100 * (((a >= 100) & (a < 200)).mean())
    print(f"{os.path.basename(out)}")
    print(f"  sumber      : {os.path.basename(src)}; BOX={box}; crop={box[2]-box[0]}x{box[3]-box[1]} px")
    print(f"  parameter   : BG_WINDOW={BG_WINDOW}, BLACK_AT={BLACK_AT}, WHITE_AT={white_at}, WHITE_SNAP={white_snap}")
    print(f"  keluaran    : {canvas.width}x{canvas.height} px; LANCZOS {sc:.2f}x; DPI={DPI[0]}")
    print(f"  putih       : {full_white:.1f}% seluruh kanvas; {non_ink_white:.1f}% piksel non-tinta")
    print(f"  tinta/nada  : {100 * ink.mean():.2f}% tinta padat; {midtones:.2f}% nada antara")
    return out


def main():
    parser = argparse.ArgumentParser(description="Crop wafaq presisi 2112x1808 dengan flat-field Batch-43/44")
    parser.add_argument("--preset", choices=sorted(PRESETS), help="preset kotak per batch (hal206, hal207)")
    parser.add_argument("--src", help="path gambar sumber (default: Picture 105.jpg)")
    parser.add_argument("--box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="BBox px; tanpa opsi ini memakai seluruh gambar")
    parser.add_argument("--out", help="path JPG keluaran")
    parser.add_argument("--white-at", type=float, default=WHITE_AT, help=f"titik putih flat-field (default {WHITE_AT})")
    parser.add_argument("--white-snap", type=int, default=WHITE_SNAP, help=f"ambang pengunci putih murni (default {WHITE_SNAP})")
    args = parser.parse_args()

    if args.preset:
        p_src, p_box, p_out = PRESETS[args.preset]
    else:
        p_src, p_box, p_out = DEFAULT_SRC, DEFAULT_BOX, DEFAULT_OUT

    src = args.src or p_src
    src = src if os.path.isabs(src) else os.path.join(BASE, src)
    out = args.out or p_out
    out = out if os.path.isabs(out) else os.path.join(BASE, out)
    if args.box:
        box = tuple(args.box)
    elif args.src and not args.preset:
        box = None
    else:
        box = p_box

    print("Crop Wafaq Presisi 2112x1808 — flat-field Batch-43/44:")
    crop_wafaq(src, box, out, white_at=args.white_at, white_snap=args.white_snap)
    print(f"Selesai — {out}")


if __name__ == "__main__":
    # FIX 2026-11-01: dulu memanggil crop_rajah() yang tidak pernah didefinisikan
    # di berkas ini (NameError kedua). Sekarang cukup memanggil main().
    main()
