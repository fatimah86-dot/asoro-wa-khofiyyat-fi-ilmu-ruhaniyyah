#!/usr/bin/env python3
"""
Crop Rajah Bergaris Presisi 2112x1808 — BATCH-44 (Hal 207-208), Rajah Hal 207.

Dipakai untuk satu rajah saja:

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

Catatan geometri (diukur dari scan Picture 105.jpg, 1755x1275 px,
satu bentangan 2 halaman = Hal207 kiri + Hal206 kanan):

  bingkai luar rajah bergaris hal 207 + SAKK 111 : x 130..785, y 50..300
  nama 4-5 penjuru terdekat                      : y 50..140
  angka 111 di atas huruf ك (kolom SAKK)         : y 280..305 (kepala panah
                                    SAKK paling atas — harus masuk utuh)
  bintang / seal di bawah                        : y 300..310
  nomor halaman cetak "207"                      : di kaki halaman (DI LUAR crop)

  Bingkai rajah  = x 130..785, y 50..300  (655 x 250 px)
  Margin 15% = 63 px kiri-kanan, 46 px atas-bawah -> seluruh SAKK 111 dan
  bintang di bawah masuk utuh, tepi kanan bingkai masuk utuh, sedangkan
  nomor halaman dan ornamen tepi bawah halaman tetap di luar crop.

  Kotak kerja akhir (dikelilingi margin 15%, dibatasi agar tidak melanggar
  gutur ke halaman 206 di x>=832):  x 95..805, y 45..325  (710 x 280 px)

Catatan resolusi: scan sumber 1755x1275 untuk satu bentangan 2 halaman,
jadi ~155 DPI optik per halaman. Output ditandai 300 DPI dan di-upscale
LANCZOS mengikuti konvensi batch sebelumnya di repo ini — ketajaman optiknya
tetap setara sumber, bukan hasil scan ulang 300 DPI.

Pengukuran target: latar putih murni 78-80% ( sasaran 78,6% ), bukan 95,5%.

Jalankan:  python3 crop_wafaq_presisi_2112x1808.py
"""
from PIL import Image, ImageFilter
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Picture 105.jpg")
OUTDIR = os.path.join(BASE, "terjemahan", "rajah")
OUTNAME = "rajah-hal-207-rajah-bergaris-presisi-2112x1808.jpg"

# Kotak kerja (koordinat px scan sumber, margin 15% di sekeliling bingkai
# rajah 130..785 x 50..300; kanan dibatasi di 805 agar tidak melanggut gutur
# halaman 206 yang dimulai x>=832; SAKK 111 pada y 280..305 masuk utuh)
BOX = (95, 45, 805, 325)

# Ukuran keluaran mutlak
W_OUT, H_OUT = 2112, 1808
DPI = (300, 300)

# Peta nada flat-field (tanpa threshold keras)
BG_WINDOW = 31
BLACK_AT = 0.60        # titik hitam: kertas kabur diubah gelap agar tinta tajam
WHITE_AT = 0.9263      # titik putih: disesuaikan agar latar (saat dibuka ulang JPEG) = 78,6% putih murni
WHITE_SNAP = 255       # piksel yang nyaris putih dikunci 255


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


def crop_rajah():
    im = Image.open(SRC).convert("RGB")
    flat = flatten(im.crop(BOX))

    # Skala seragam untuk MEMENUHI kanvas 2112x1808 (tanpa padding putih besar)
    flat = flat.resize((W_OUT, H_OUT), Image.LANCZOS)

    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, OUTNAME)
    flat.save(path, "JPEG", quality=100, subsampling=0, dpi=DPI)

    # Ukur pada berkas yang TERSIMPAN (dibuka ulang) — ini yang dihitung pengguna
    a = np.array(Image.open(path).convert("L"))
    ink = a < 100
    non = a[~ink]
    bersih = 100 * (non == 255).mean()
    titik = 100 * (((a >= 100) & (a < 200)).mean())
    print(f"  {OUTNAME}")
    print(f"    sumber px     : {BOX[2] - BOX[0]} x {BOX[3] - BOX[1]} "
          f"({SRC.split('/')[-1]} x{BOX[0]},{BOX[1]})")
    print(f"    ukuran akhir  : {W_OUT}x{H_OUT} px  LANCZOS  DPI {DPI[0]} (fill canvas)")
    print(f"    latar putih   : {bersih:5.1f}% putih murni 255   "
          f"tinta padat {100 * ink.mean():4.1f}%   "
          f"nada antara (titik/garis tipis) {titik:4.2f}%")
    return path


if __name__ == "__main__":
    print("Crop Rajah Bergaris Presisi 2112x1808 — BATCH-44 Hal 207:")
    p = crop_rajah()
    print(f"Selesai — {p}")
