#!/usr/bin/env python3
"""
harakat.py — Membangun BASIS HARAKAT kata untuk seluruh kitab.

Dua lapis:
  1. KAMUS TERVERIFIKASI (data/kamus-harakat.json) — diketik manual, ikut i'rab.
  2. OTOMATIS (data/harakat-otomatis.json) — hasil mesin Mishkal + KOREKSI wajib.

Koreksi wajib ditulis di KOREKSI di bawah: mesin sering salah pada fi'il
madhi mutakallim, i'rab, dan hamzah washal. Yang tidak bisa dipastikan
TIDAK dikoreksi — dibiarkan bertanda "otomatis" agar jujur.

Pakai:
    python3 tools/harakat.py            # bangun ulang basis
    python3 tools/harakat.py --stat     # lihat statistik
"""
import glob
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAMUS = os.path.join(ROOT, "data", "kamus-harakat.json")
OTO = os.path.join(ROOT, "data", "harakat-otomatis.json")
SRC = os.path.join(ROOT, "terjemahan", "versi-baru")

HAR = "ًٌٍَُِّْـٰ"

# ── koreksi manual atas keluaran mesin (kiri: bentuk mesin, kanan: yang benar)
KOREKSI = {
    "أَقَسَّمَتْ": "أَقْسَمْتُ",
    "وَهَذِه": "وَهَذِهِ",
    "الْعَزِيمَةِ": "الْعَزِيمَةُ",
    "يُؤَخِّذُ": "يُؤْخَذُ",
    "وَتَوَكَّلَ": "وَتُوَكِّلُ",
    "اِبْيَضَّ": "أَبْيَض",
    "فَاُكْتُبْ": "فَاكْتُبْ",
    "فَاُخْرُجْ": "فَاخْرُجْ",
    "الْا": "الْ",
    "أَأ": "أَ",
}


def norm(w: str) -> str:
    w = unicodedata.normalize("NFC", w.strip())
    w = w.replace("ـ", "")
    # samakan bentuk huruf
    w = (w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
          .replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و"))
    return re.sub(rf"[{HAR}]", "", w)


def bersih_harakat(w: str) -> str:
    w = unicodedata.normalize("NFC", w.strip())
    return w.replace("ـ", "")


def kumpulkan_kata() -> list:
    kata = []
    for f in glob.glob(os.path.join(SRC, "BATCH-*.md")):
        s = open(f, encoding="utf-8").read()
        for blk in re.findall(r"```(.*?)```", s, re.S):
            for w in re.findall(r"[\u0600-\u06FF]{2,}", blk):
                kata.append(w)
        for blk in re.findall(r"^\| ([^|]+) \|", s, re.M):
            if re.fullmatch(r"\s*[\u0600-\u06FF]+\s*", blk):
                kata.append(blk.strip())
    return kata


def bangun():
    from mishkal.tashkeel import TashkeelClass
    tk = TashkeelClass()

    kamus = json.load(open(KAMUS, encoding="utf-8"))["kata"]
    sudah = {norm(k) for k in kamus}

    semua = kumpulkan_kata()
    unik = []
    dilihat = set()
    for w in semua:
        n = norm(w)
        if not n or n in sudah or n in dilihat:
            continue
        dilihat.add(n)
        unik.append(w)

    print(f"kata unik perlu harakat: {len(unik)} (dari {len(semua)} token)")

    hasil = {}
    gagal = 0
    for i, w in enumerate(unik):
        try:
            h = tk.tashkeel(w).strip()
        except Exception:
            gagal += 1
            continue
        if not h:
            gagal += 1
            continue
        for salah, benar in KOREKSI.items():
            h = h.replace(salah, benar)
        hasil[norm(w)] = bersih_harakat(h)
        if i % 500 == 0:
            print(f"  … {i}/{len(unik)}", flush=True)

    # gabung yang sudah ada (tidak ditimpa)
    lama = {}
    if os.path.exists(OTO):
        lama = json.load(open(OTO, encoding="utf-8")).get("kata", {})
    lama.update(hasil)

    json.dump({"_catatan": "Harakat OTOMATIS (Mishkal) + koreksi terbatas. "
                           "Wajib dicek untuk pemakaian formal.",
               "_versi": 2, "kata": lama},
              open(OTO, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"✅ {len(hasil)} kata baru → {OTO} (total {len(lama)}, gagal {gagal})")


def stat():
    kamus = json.load(open(KAMUS, encoding="utf-8"))["kata"]
    oto = json.load(open(OTO, encoding="utf-8"))["kata"] if os.path.exists(OTO) else {}
    k = {norm(x) for x in kamus}
    print(f"kamus terverifikasi : {len(k)}")
    print(f"harakat otomatis    : {len(oto)}")
    print(f"total               : {len(k | set(oto))}")


if __name__ == "__main__":
    if "--stat" in sys.argv:
        stat()
    else:
        bangun()


# ─────────────────────────────────────── perapi harakat (dipakai saat build)
FATHA, DHAMMAH, KASRAH = "\u064E", "\u064F", "\u0650"
FATHATAN, DHAMMATAN, KASRATAN = "\u064B", "\u064C", "\u064D"
SUKUN, SYADDAH = "\u0652", "\u0651"
VOKAL = {FATHA, DHAMMAH, KASRAH, FATHATAN, DHAMMATAN, KASRATAN}
ALL_HAR = VOKAL | {SUKUN, SYADDAH}


def rapikan_harakat(s: str) -> str:
    """Bersihkan harakat yang tumpang tindih.

    Aturan:
      • harakat kembar (ََ / ْْ / ِِ) → satu
      • vokal + sukun (ِْ) → sukun saja  (mis. الِْ → الْ)
      • dua vokal berbeda (َِ) → vokal terakhir
      • tasydid selalu diletakkan SEBELUM vokal (urutan kanonik Unicode)
      • harakat yatim (didahului spasi/awal teks) dibuang
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c not in ALL_HAR:
            out.append(c)
            i += 1
            continue
        # kumpulkan semua harakat berurutan
        j = i
        kumpulan = []
        while j < n and s[j] in ALL_HAR:
            kumpulan.append(s[j])
            j += 1
        # harakat yatim: tidak menempel pada huruf
        if not out or out[-1] in ALL_HAR or out[-1].isspace():
            i = j
            continue
        syadda = SYADDAH in kumpulan
        vokal = [x for x in kumpulan if x in VOKAL]
        sukun = SUKUN in kumpulan
        if sukun and vokal:
            v = SUKUN                    # ِْ / َْ tidak sah → sukun menang
        elif vokal:
            v = vokal[-1]                # vokal terakhir menang
        elif sukun:
            v = SUKUN
        else:
            v = ""
        if syadda:
            out.append(SYADDAH)
        if v:
            out.append(v)
        i = j
    return "".join(out)
