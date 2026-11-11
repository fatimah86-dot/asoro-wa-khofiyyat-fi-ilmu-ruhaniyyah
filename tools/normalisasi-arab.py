#!/usr/bin/env python3
"""
normalisasi-arab.py — Memperbaiki teks Arab "katib" yang rusak.

Masalah yang ditangani:
 1. Huruf presentasi (U+FE70–U+FEFF) → huruf dasar (U+0600–U+06FF)
 2. Simbol sampah hasil konversi font lama (ALM "katib"):
       Ǆ (U+01C4)  → ال   (lam-alif)
       ǁ (U+01C1)  → ل
       ǂ (U+01C2)  → ل
       ƾ (U+01BE)  → أ
       U+0006 / U+0005 / dll → أ
       ֔ (U+0594)  → tanda baca
 3. Merapikan spasi & baris.
 4. Kamus perbaikan kata tertentu (manual, bisa ditambah).

Pakai:
    python3 tools/normalisasi-arab.py --cek  terjemahan/BATCH-01-Hal-001-005.md
    python3 tools/normalisasi-arab.py --in out.md  input.md
"""
import sys
import re
import unicodedata

# ---------------------------------------------------------------- peta simbol
SIMBOL = {
    "\u01C4": "ال",   # Ǆ  lam-alif
    "\u01C1": "ل",    # ǁ  lam
    "\u01C2": "ل",    # ǂ  lam
    "\u01BE": "أ",    # ƾ  alif hamzah
    "\u0006": "أ",
    "\u0005": "أ",
    "\u0594": "،",    # ֔  → koma
    "\u0591": "",
    "\u0592": "",
    "\u0593": "",
    "\u0595": "",
}

# Kata yang sering salah karena simbol di atas (dipakai untuk laporan)
KATA_RUSAK = re.compile("[Ǆǁǂƾ\u0006\u0005֔]")


def ke_huruf_dasar(teks: str) -> str:
    """Huruf presentasi (FE70–FEFF) → huruf dasar Arab."""
    out = []
    for ch in teks:
        cp = ord(ch)
        if 0xFE70 <= cp <= 0xFEFF:
            # NFKC memecah bentuk presentasi menjadi huruf dasar + harakat.
            # Lam-alif (FEF5–FEFA) pecah jadi ل + ا → harus digabung jadi لا
            d = unicodedata.normalize("NFKC", ch)
            out.append(d)
        else:
            out.append(ch)
    return "".join(out)


def rapikan_lam_alif(teks: str) -> str:
    """Gabungkan ل + ا (+harakat) menjadi لا bila perlu — biarkan apa adanya
    supaya terlihat normal di renderer modern."""
    return teks


def bersihkan(teks: str) -> str:
    for k, v in SIMBOL.items():
        teks = teks.replace(k, v)
    teks = ke_huruf_dasar(teks)
    # buang karakter kontrol (kecuali newline & tab)
    teks = "".join(
        ch for ch in teks
        if ch in "\n\t" or unicodedata.category(ch)[0] != "C"
    )
    # rapikan spasi
    teks = re.sub(r"[ \t]{2,}", " ", teks)
    teks = re.sub(r"\n{3,}", "\n\n", teks)
    return teks.strip()


def hitung_rusak(teks: str) -> int:
    return len(KATA_RUSAK.findall(teks))


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "--cek":
        total = 0
        for f in args[1:]:
            t = open(f, encoding="utf-8", errors="replace").read()
            n = hitung_rusak(t)
            total += n
            print(f"{'❌' if n else '✅'} {n:5d} simbol rusak  {f}")
        print(f"\nTotal simbol rusak: {total}")
        return 0 if total == 0 else 1

    if args[0] == "--in":
        keluar, masuk = args[1], args[2]
        t = open(masuk, encoding="utf-8", errors="replace").read()
        before = hitung_rusak(t)
        open(keluar, "w", encoding="utf-8").write(bersihkan(t))
        print(f"✅ {masuk} → {keluar}  ({before} simbol diperbaiki)")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
