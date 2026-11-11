#!/usr/bin/env python3
"""
versi-terjemahan.py — Menyeragamkan seluruh berkas terjemahan ke
"FORMAT 3 TINGKAT" yang mudah dibaca.

Struktur lama yang berantakan:
    ### [Teks Arab Asli]
    ```arab```
    ### [Terjemahan Indonesia]
    paragraf...
    (kadang ada [Transliterasi Latin], kadang tidak)

Struktur baru (seragam, urut, satu blok per halaman):
    ## 📄 HALAMAN 005 — judul
    ### 🅰️ TEKS ARAB
    ### 🔤 LATIN / MAKHRAJ      (placeholder TULIS-TANGAN bila belum ada)
    ### 🇮🇩 TERJEMAHAN
    ### 🧿 RAJAH / WAFAQ        (bila ada)

Pakai:
    python3 tools/versi-terjemahan.py --laporan
    python3 tools/versi-terjemahan.py BATCH-01-Hal-001-005.md
"""
import sys
import re
import glob
import os

POLA = [
    (re.compile(r"^#{1,6}\s*\[?\s*Teks Arab Asli[^\]]*\]?\s*$", re.I), "ARAB"),
    (re.compile(r"^#{1,6}\s*\[?\s*Terjemahan(?: Indonesia)?[^\]]*\]?\s*$", re.I), "INDO"),
    (re.compile(r"^#{1,6}\s*\[?\s*Translit[^\]]*\]?\s*$", re.I), "LATIN"),
    (re.compile(r"^#{1,6}\s*\[?\s*Latin[^\]]*\]?\s*$", re.I), "LATIN"),
]


def jenis_judul(line: str):
    s = line.strip()
    if not s.startswith("#"):
        return None
    for rx, j in POLA:
        if rx.match(s):
            return j
    return None


def scan(path: str):
    """Kembalikan daftar blok: (jenis, isi) + statistik."""
    teks = open(path, encoding="utf-8", errors="replace").read()
    lines = teks.split("\n")
    blok = []
    cur = None
    buf = []
    for ln in lines:
        j = jenis_judul(ln)
        if j:
            if cur:
                blok.append((cur, "\n".join(buf).strip()))
            cur, buf = j, []
        elif ln.startswith("## "):
            if cur:
                blok.append((cur, "\n".join(buf).strip()))
            cur, buf = None, []
        else:
            buf.append(ln)
    if cur:
        blok.append((cur, "\n".join(buf).strip()))
    return blok


def laporan():
    print(f"{'berkas':46s} {'Arab':>5s} {'Indo':>5s} {'Latin':>6s} {'Rusak':>6s} {'Harakat%':>9s}")
    print("-" * 84)
    tot = {"A": 0, "I": 0, "L": 0, "R": 0}
    for f in sorted(glob.glob("terjemahan/BATCH-*.md")):
        t = open(f, encoding="utf-8", errors="replace").read()
        a = len(re.findall(r"[Tt]eks Arab Asli", t))
        i = len(re.findall(r"[Tt]erjemahan Indonesia", t))
        l = len(re.findall(r"[Tt]ranslit|[Ll]atin Fonet", t))
        r = sum(t.count(c) for c in "Ǆǁǂƾ")
        ar = sum(1 for ch in t if 0x0600 <= ord(ch) <= 0x06FF)
        hr = sum(t.count(c) for c in "ًٌٍَُِّْ")
        tot["A"] += a
        tot["I"] += i
        tot["L"] += l
        tot["R"] += r
        print(f"{os.path.basename(f):46s} {a:5d} {i:5d} {l:6d} {r:6d} {100*hr/max(ar,1):8.1f}%")
    print("-" * 84)
    print(f"{'TOTAL':46s} {tot['A']:5d} {tot['I']:5d} {tot['L']:6d} {tot['R']:6d}")


def kartu(path: str):
    blok = scan(path)
    print(f"\n=== {path} ===")
    print(f"jumlah blok terdeteksi: {len(blok)}")
    for j, isi in blok[:6]:
        print(f"  [{j}] {len(isi)} char :: {isi[:70].replace(chr(10),' ')}…")


if __name__ == "__main__":
    if "--laporan" in sys.argv:
        laporan()
    elif len(sys.argv) > 1:
        for f in sys.argv[1:]:
            kartu(f)
    else:
        print(__doc__)
