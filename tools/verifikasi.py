#!/usr/bin/env python3
"""
verifikasi.py — Pemeriksa akhir hasil build.

Tiga lapis:
  A. KELENGKAPAN  — jumlah halaman & jumlah kata Arab per halaman
                    (lama vs baru) tidak ada yang hilang.
  B. HARAKAT      — tidak ada harakat dobel / salah tumpuk.
  C. KEBERSIHAN   — tidak ada huruf presentasi (U+FE70–FEFF),
                    simbol katib (Ǆ ǁ ǂ ƾ), karakter kontrol,
                    kata Arab yang "pecah", dan pagar kode ganjil.

Pakai: python3 tools/verifikasi.py
Keluar dengan kode 1 bila ada kegagalan.
"""
import glob
import os
import re
import sys
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAMA = os.path.join(ROOT, "terjemahan")
BARU = os.path.join(ROOT, "terjemahan", "versi-baru")
SCAN = os.path.join(ROOT, "data", "transkripsi-scan.json")

ARAB = "\u0600-\u06FF"
HAR = "ًٌٍَُِّْـٰ"
FATHA, DHAMMA, KASRA, SUKUN, SYADDA = "\u064E", "\u064F", "\u0650", "\u0652", "\u0651"
# harakat yang TIDAK boleh berdiri sendiri di luar huruf (tatweel bukan harakat)
HAR_SET = set("ًٌٍَُِّْٰ")
HAR_CLASS = "".join(sorted(HAR_SET))   # wajib string, bukan set, di dalam regex

gagal = []


def catat(pesan):
    gagal.append(pesan)


def bukan_huruf(c):
    """True bila c bukan huruf Arab dan bukan huruf Latin (mis. spasi/pagar)."""
    return not (0x0621 <= ord(c) <= 0x06FF or c.isalpha())


def tanpa_harakat(s):
    return re.sub(rf"[{HAR}]", "", unicodedata.normalize("NFC", s))


def kata_arab(s):
    return re.findall(rf"[{ARAB}]+", tanpa_harakat(s))


# ─────────────────────────────────────────────── A. kelengkapan
def cek_kelengkapan():
    print("\nA. KELENGKAPAN — tidak ada baris/halaman yang hilang")
    berkas = sorted(glob.glob(os.path.join(BARU, "BATCH-*.md")))
    total_hal = 0
    for f in berkas:
        lama_f = os.path.join(LAMA, os.path.basename(f))
        baru = open(f, encoding="utf-8").read()
        hal_baru = len(re.findall(r"^## 📄 HAL\.", baru, re.M))

        # kata Arab di blok teks Arab versi baru
        blok_baru = re.findall(r"\*\*🅰️ TEKS ARAB\*\*.*?```\n(.*?)```", baru, re.S)
        kata_baru = sum(len(kata_arab(b)) for b in blok_baru)

        if not os.path.exists(lama_f):
            print(f"  ⚠️  {os.path.basename(f):30s} hal={hal_baru:2d} (tak ada pembanding)")
            total_hal += hal_baru
            continue
        lama = open(lama_f, encoding="utf-8").read()
        blok_lama = re.findall(r"```(.*?)```", lama, re.S)
        kata_lama = sum(len(kata_arab(b)) for b in blok_lama)

        status = "✅"
        if hal_baru == 0:
            status = "❌"
            catat(f"{os.path.basename(f)}: 0 halaman terdeteksi")
        # toleransi: versi baru boleh LEBIH banyak kata (hasil transkripsi),
        # tetapi tidak boleh jauh lebih sedikit
        if kata_lama and kata_baru < kata_lama * 0.75:
            status = "❌"
            catat(f"{os.path.basename(f)}: kata Arab menyusut "
                  f"{kata_lama} → {kata_baru}")
        total_hal += hal_baru
        print(f"  {status} {os.path.basename(f):30s} hal={hal_baru:2d} "
              f"kata lama={kata_lama:5d} baru={kata_baru:5d}")

    print(f"\n  Total halaman versi baru: {total_hal}")
    if total_hal < 195:
        catat(f"total halaman {total_hal} < 195")


# ─────────────────────────────────────────────── B. harakat
def cek_harakat():
    print("\nB. HARAKAT — tidak ada harakat dobel / salah tumpuk")
    masalah = Counter()
    contoh = {}
    for f in sorted(glob.glob(os.path.join(BARU, "BATCH-*.md"))):
        teks = open(f, encoding="utf-8").read()
        blok = re.findall(r"\*\*🎧 ARAB BERHARAKAT\*\*.*?```\n(.*?)```", teks, re.S)
        for b in blok:
            for i, ch in enumerate(b):
                if ch in HAR_SET and i + 1 < len(b) and b[i + 1] in HAR_SET:
                    pasangan = b[i] + b[i + 1]
                    # urutan kanonik: tasydid SELALU sebelum harakat → sah
                    if b[i] == SYADDA and b[i + 1] in {
                            FATHA, DHAMMA, KASRA, SUKUN,
                            "\u064B", "\u064C", "\u064D"}:
                        continue
                    masalah[pasangan] += 1
                    contoh.setdefault(pasangan, b[max(0, i - 12):i + 4])
        # harakat yang tidak menempel pada huruf Arab (menggantung di spasi)
        for m in re.finditer(rf"\s[{HAR_CLASS}]", teks):
            sebelum = teks[m.start() - 1] if m.start() else " "
            if bukan_huruf(sebelum):
                masalah["harakat-menggantung"] += 1
                contoh.setdefault("harakat-menggantung",
                                  teks[max(0, m.start() - 25):m.start() + 8])

    if masalah:
        for k, n in masalah.most_common(12):
            catat(f"harakat dobel '{k}' × {n}  contoh: {contoh.get(k,'')!r}")
            print(f"  ❌ '{k}' × {n}   contoh: {contoh.get(k,'')!r}")
    else:
        print("  ✅ tidak ada harakat dobel")


# ─────────────────────────────────────────────── C. kebersihan
def cek_kebersihan():
    print("\nC. KEBERSIHAN TEKS ARAB")
    total = Counter()
    for f in sorted(glob.glob(os.path.join(BARU, "BATCH-*.md"))):
        teks = open(f, encoding="utf-8").read()
        nama = os.path.basename(f)

        presentasi = sum(1 for c in teks if 0xFE70 <= ord(c) <= 0xFEFF)
        katib = sum(teks.count(c) for c in "Ǆǁǂƾ")
        kontrol = sum(1 for c in teks if unicodedata.category(c)[0] == "C"
                      and c not in "\n\t")
        # pagar kode harus genap
        pagar = teks.count("```")
        # tag markdown yang bocor ke dalam blok kode Arab
        bocor = 0
        for blk in re.findall(r"^```\n(.*?)^```", teks, re.S | re.M):
            if re.search(r"\*\*(?:🎧|🔤|🇮🇩|📖|🧿)", blk):
                bocor += 1

        for k, v in (("presentasi", presentasi), ("katib", katib),
                     ("kontrol", kontrol)):
            total[k] += v
        if presentasi or katib or kontrol:
            catat(f"{nama}: presentasi={presentasi} katib={katib} kontrol={kontrol}")
            print(f"  ❌ {nama}: presentasi={presentasi} katib={katib} kontrol={kontrol}")
        if pagar % 2:
            catat(f"{nama}: pagar kode ganjil ({pagar})")
            print(f"  ❌ {nama}: pagar kode ganjil ({pagar})")
        if bocor:
            catat(f"{nama}: tag markdown bocor ke dalam blok kode × {bocor}")
            print(f"  ❌ {nama}: tag markdown bocor × {bocor}")

    if not any(total.values()):
        print("  ✅ tidak ada huruf presentasi / simbol katib / karakter kontrol")
        print("  ✅ semua pagar kode genap")


# ─────────────────────────────────────────────── D. placeholder
def cek_placeholder():
    print("\nD. PLACEHOLDER — sisa bagian yang belum ditranskripsi")
    import json
    scan = json.load(open(SCAN, encoding="utf-8"))["halaman"]
    sisa_teks, sisa_rajah = [], []
    for f in sorted(glob.glob(os.path.join(BARU, "BATCH-*.md"))):
        teks = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^> `(\[[^`]*)`", teks, re.M):
            isi = m.group(1)
            if re.search(r"lihat scan|teks panjang|jika ada|instruksi|lanjutan|samar|Tashrif|Da'wat|Hal\d",
                         isi, re.I):
                sisa_teks.append((os.path.basename(f), isi[:70]))
            else:
                sisa_rajah.append((os.path.basename(f), isi[:60]))

    print(f"  Halaman ditranskripsi dari scan : {len(scan)}")
    print(f"  Placeholder TEKS (harus 0)      : {len(sisa_teks)}")
    print(f"  Deskripsi RAJAH (bukan teks)    : {len(sisa_rajah)}")
    for n, i in sisa_teks:
        print(f"    ❌ {n}: {i}")
        catat(f"placeholder teks tersisa di {n}: {i}")
    if not sisa_teks:
        print("  ✅ tidak ada placeholder teks tersisa")


# ─────────────────────────────────────────────── E. halaman ganda
def cek_duplikat():
    """Satu nomor halaman HARUS hanya punya satu blok isi.

    Dulu tidak diperiksa, sehingga hal.36 dan hal.96 sempat muncul dua kali
    (satu blok placeholder + satu blok isi asli) tanpa terdeteksi.
    """
    print("\nE. HALAMAN GANDA — satu nomor hanya satu blok isi")
    peta = {}
    for f in sorted(glob.glob(os.path.join(BARU, "BATCH-*.md"))):
        teks = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^##+\s*(?:📄\s*)?(?:HAL\.|Halaman)\s*(\d{1,3})\b", teks, re.M):
            peta.setdefault(int(m.group(1)), []).append(os.path.basename(f))
    ganda = {n: v for n, v in peta.items() if len(v) > 1}
    hilang = [n for n in range(1, 205) if n not in peta]
    print(f"  Halaman unik     : {len(peta)}")
    print(f"  Halaman hilang   : {len(hilang)}" + (f" → {hilang[:10]}" if hilang else ""))
    print(f"  Halaman ganda    : {len(ganda)}")
    for n, v in sorted(ganda.items()):
        print(f"    ❌ hal.{n} muncul {len(v)}×: {v}")
        catat(f"halaman {n} ganda ({len(v)}×) di {v}")
    if hilang:
        catat(f"halaman hilang: {hilang}")
    if not ganda and not hilang:
        print("  ✅ 204 halaman, tidak ada yang ganda/hilang")


# ─────────────────────────────────────────────── F. kesetiaan huruf
def cek_kesetiaan():
    """Lapis 🎧 HARUS memuat huruf yang sama dengan lapis 🅰️.

    Harakat hanya menambah tanda baca, TIDAK boleh menambah/menghapus huruf.
    Dulu aturan "الْا"→"الْ" dan entri kamus berartikel membuat
    الاسم (nama) menjadi السم (racun) — lolos karena tidak diperiksa.
    Beda hamzah (أ/إ/آ→ا) dan ى→ي dianggap setara (pilihan ortografi).
    """
    print("\nF. KESETIAAN HURUF — harakat tidak mengubah huruf")
    def huruf(w):
        w = unicodedata.normalize("NFC", w)
        w = "".join(c for c in w if 0x0621 <= ord(c) <= 0x06FF and c not in HAR_SET)
        return (w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
                 .replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و"))
    cacat = Counter()
    contoh = {}
    total_kata = 0
    for f in sorted(glob.glob(os.path.join(BARU, "BATCH-*.md"))):
        teks = open(f, encoding="utf-8").read()
        G = re.findall(r"\*\*🅰️ TEKS ARAB\*\*.*?```\n(.*?)```", teks, re.S)
        H = re.findall(r"\*\*🎧 ARAB BERHARAKAT\*\*.*?```\n(.*?)```", teks, re.S)
        for a, b in zip(G, H):
            # bandingkan sebagai deret huruf (spasi/tanda baca diabaikan)
            g = "".join(huruf(x) for x in re.findall(rf"[{ARAB}]+", without(a)))
            h2 = "".join(huruf(x) for x in re.findall(rf"[{ARAB}]+", without(b)))
            total_kata += len(re.findall(rf"[{ARAB}]+", without(a)))
            if g != h2:
                cacat[os.path.basename(f)] += 1
                contoh.setdefault(os.path.basename(f), (a[:60], b[:60]))
    print(f"  Kata Arab diperiksa : {total_kata}")
    if cacat:
        for n, c in cacat.most_common(10):
            print(f"    ❌ {n}: {c} blok beda huruf")
            catat(f"kesetiaan huruf: {n} ({c} blok)")
    else:
        print("  ✅ semua blok setia — harakat tidak menambah/menghapus huruf")


def without(s):
    return re.sub(rf"[{HAR}]", "", unicodedata.normalize("NFC", s))


if __name__ == "__main__":
    print("=" * 78)
    print("VERIFIKASI HASIL BUILD — FORMAT 3 TINGKAT")
    print("=" * 78)
    cek_kelengkapan()
    cek_harakat()
    cek_kebersihan()
    cek_placeholder()
    cek_duplikat()
    cek_kesetiaan()

    print("\n" + "=" * 78)
    if gagal:
        print(f"❌ GAGAL — {len(gagal)} temuan")
        for g in gagal:
            print("   -", g)
        sys.exit(1)
    print("✅ SEMUA PEMERIKSAAN LULUS")
    sys.exit(0)
