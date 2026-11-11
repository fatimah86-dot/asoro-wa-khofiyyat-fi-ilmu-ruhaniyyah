#!/usr/bin/env python3
"""
cek-10-langkah.py — Penjaga Kunci Permanen Ustadz Yoad.
Memeriksa apakah sebuah file bedah teks memuat 10 langkah wajib secara URUT
dan memuat 3 bagian output wajib + penanda thilasm bila perlu.

Pakai:
    python3 tools/cek-10-langkah.py terjemahan/BATCH-01-Hal-001-005.md
    python3 tools/cek-10-langkah.py --all terjemahan/*.md
"""
import sys
import re
import glob

LANGKAH = [
    (1, "JENIS KATA"),
    (2, "AKAR KATA"),
    (3, "MUBTADA"),
    (4, "KHOBAR MUQODDAM"),
    (5, "HURUF AN"),
    (6, "FI'IL MUDHARI"),
    (7, "MAF'UL BIH"),
    (8, "HURUF ATHAF"),
    (9, "DHOROF ZAMAN"),
    (10, "JAR MAJRUR"),
]

OUTPUT_WAJIB = [
    ("Teks Arab", [r"teks arab"]),
    ("Terjemah Harfiah", [r"harfiah", r"per kata"]),
    ("Terjemah Bebas", [r"terjemah bebas", r"makna keseluruhan"]),
]

ZONA_MERAH = r"TEKS ASLI DIJAGA\s*-\s*TIDAK DITERJEMAH KARENA THILASM/WAFAQ"
KATA_THILASM = r"(وفق|طلسم|عزيمة|توكيل|خادم|اسم برهتية|wafaq|thilasm|azimah)"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).lower()


def cek(path: str) -> tuple[bool, list[str]]:
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    txt = norm(raw)
    msgs: list[str] = []
    ok = True

    # 1. Urutan 10 langkah
    pos = -1
    for no, kata in LANGKAH:
        pat = norm(kata)
        found = txt.find(pat)
        if found == -1:
            msgs.append(f"  ✗ Langkah {no:>2} ({kata}) TIDAK DITEMUKAN")
            ok = False
        elif found < pos:
            msgs.append(f"  ✗ Langkah {no:>2} ({kata}) KELUAR URUTAN")
            ok = False
        else:
            pos = found
    if ok:
        msgs.append("  ✓ 10 langkah lengkap & urut")

    # 2. Tiga bagian output wajib
    for nama, pats in OUTPUT_WAJIB:
        if not any(re.search(p, txt) for p in pats):
            msgs.append(f"  ✗ Bagian output wajib hilang: {nama}")
            ok = False
    if ok:
        msgs.append("  ✓ 3 bagian output wajib ada")

    # 3. Zona merah thilasm/wafaq
    has_thilasm = re.search(KATA_THILASM, raw) is not None
    has_penjaga = re.search(ZONA_MERAH, raw) is not None
    if has_thilasm and not has_penjaga:
        msgs.append("  ✗ Ada kata thilasm/wafaq/azimah TANPA penanda "
                    "'[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]'")
        ok = False
    elif has_penjaga:
        msgs.append("  ✓ Penanda zona merah thilasm/wafaq ada")

    return ok, msgs


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--all"]
    if not args:
        print(__doc__)
        return 2
    files: list[str] = []
    for a in args:
        files.extend(sorted(glob.glob(a)))
    if not files:
        print("Tidak ada file yang cocok.")
        return 2

    gagal = 0
    for f in files:
        ok, msgs = cek(f)
        print(("✅ LULUS  " if ok else "❌ GAGAL  ") + f)
        for m in msgs:
            print(m)
        if not ok:
            gagal += 1
        print()

    print(f"— {len(files) - gagal}/{len(files)} file lulus —")
    return 0 if gagal == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
