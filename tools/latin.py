#!/usr/bin/env python3
"""
latin.py — Transliterasi Arab → Latin gaya pesantren Indonesia.

Prinsip: pisahkan kata menjadi "satuan huruf" (huruf + harakat/shadda/sukun
miliknya), lalu rangkai ulang. Ini yang benar, bukan membaca per karakter.

Aturan:
  • "ال" di awal → "al-" + asimilasi huruf syamsiyah (الشَّمْس → asy-syams)
  • َ a · ُ u · ِ i · ً an · ٌ un · ٍ in · ْ sukun · ّ gandakan huruf
  • ا panjang → ā · و/ي tanpa harakat → ū / ī (bila vokal cocok), selain itu w/y
  • ة akhir → h · ى akhir → ā
  • Kata khusus: الله، لله، بالله، والله

    latin("الرَّحْمَنِ")  -> 'ar-raḥmān'
    latin("يُنْجِي")       -> 'yunji'
"""
import re
import unicodedata

HARAKAT = set("ًٌٍَُِّْـٰ")

LETTER = {
    "ا": "", "أ": "’", "إ": "’", "آ": "ā", "ٱ": "",
    "ء": "’", "ؤ": "’", "ئ": "’",
    "ب": "b", "ت": "t", "ث": "ts", "ج": "j", "ح": "ḥ", "خ": "kh",
    "د": "d", "ذ": "dz", "ر": "r", "ز": "z", "س": "s", "ش": "sy",
    "ص": "ṣ", "ض": "ḍ", "ط": "ṭ", "ظ": "ẓ", "ع": "‘", "غ": "gh",
    "ف": "f", "ق": "q", "ك": "k", "ل": "l", "م": "m", "ن": "n",
    "ه": "h", "و": "w", "ي": "y", "ة": "t", "ى": "",
}
SYAMSIYAH = set("تثدذرزسشصضطظلن")

FATHAH, DHAMMAH, KASRAH = "\u064E", "\u064F", "\u0650"
FATHATAN, DHAMMATAN, KASRATAN = "\u064B", "\u064C", "\u064D"
SUKUN, SYADDAH = "\u0652", "\u0651"

# kelas vokal
V_A, V_U, V_I, V_AN, V_UN, V_IN = "a", "u", "i", "an", "un", "in"

KHUSUS = {
    "الله": "Allāh", "لله": "lillāh", "بالله": "billāh",
    "والله": "wallāh", "تالله": "tallāh", "اللهم": "Allāhumma",
    "اللَّهُمَّ": "Allāhumma",
}


def _bersih(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return "".join(c for c in s if 0x0600 <= ord(c) <= 0x06FF or c in HARAKAT)


def _satuan(kata: str):
    """Pecah jadi list (huruf, shadda:bool, vokal:str, sukun:bool)."""
    out = []
    i = 0
    while i < len(kata):
        c = kata[i]
        if c in HARAKAT:
            i += 1
            continue
        if c not in LETTER:
            i += 1
            continue
        shadda = False
        vokal = ""
        sukun = False
        j = i + 1
        while j < len(kata) and kata[j] in HARAKAT:
            d = kata[j]
            if d == SYADDAH:
                shadda = True
            elif d == SUKUN:
                sukun = True
            elif d == FATHAH:
                vokal = V_A
            elif d == DHAMMAH:
                vokal = V_U
            elif d == KASRAH:
                vokal = V_I
            elif d == FATHATAN:
                vokal = V_AN
            elif d == DHAMMATAN:
                vokal = V_UN
            elif d == KASRATAN:
                vokal = V_IN
            j += 1
        out.append((c, shadda, vokal, sukun))
        i = j
    return out


def _rangka(satuan, akhir_kata: bool) -> str:
    hasil = []
    vokal_lalu = ""
    for idx, (c, shadda, vokal, sukun) in enumerate(satuan):
        akhir = idx == len(satuan) - 1
        kons = LETTER[c]

        # --- huruf 'illat berfungsi sebagai vokal panjang
        if c == "ا":
            if akhir and vokal_lalu in (V_AN, "a"):
                continue
            hasil.append("ā")
            vokal_lalu = "ā"
            continue
        if c == "ى":
            hasil.append("ā")
            vokal_lalu = "ā"
            continue

        if c in "وي":
            if not vokal and not shadda:
                if c == "و" and vokal_lalu in ("u", "ū"):
                    hasil.append("ū")
                    vokal_lalu = "ū"
                    continue
                if c == "ي" and vokal_lalu in ("i", "ī"):
                    hasil.append("ī")
                    vokal_lalu = "ī"
                    continue
                if c == "و" and vokal_lalu == "a":      # awwal
                    hasil.append("w")
                    vokal_lalu = ""
                    continue

        # --- ta marbuthah
        if c == "ة":
            hasil.append("h" if akhir or not vokal else "t")
            vokal_lalu = vokal
            continue

        hasil.append(kons)
        if shadda:
            hasil.append(kons)
        if vokal:
            hasil.append(vokal)
            vokal_lalu = vokal if vokal in (V_A, V_U, V_I) else vokal[0]
        else:
            # huruf mati memutus hubungan vokal panjang pada و/ي berikutnya
            vokal_lalu = "" if c not in "اويى" else vokal_lalu

    teks = "".join(hasil)
    # vokal panjang ganda
    teks = teks.replace("aa", "ā").replace("uu", "ū").replace("ii", "ī")
    teks = teks.replace("aā", "ā").replace("uū", "ū").replace("iī", "ī")
    return teks


def latin(kata: str) -> str:
    kata = _bersih(kata).strip()
    if not kata:
        return ""
    if kata in KHUSUS:
        return KHUSUS[kata]
    _g = "".join(c for c in kata if c not in HARAKAT)
    if _g in KHUSUS:
        return KHUSUS[_g]
    kata = kata.replace("ـ", "")

    # وَ/فَ/بِ/لِ/كَ + ال  →  wal-, fal-, bil-, lil-, kal-
    m = re.match(r"^([وفبلك])([\u064B-\u0652]*)(ال)(.*)$", kata)
    if m:
        pref = {"و": "wa", "ف": "fa", "ب": "bi", "ل": "li", "ك": "ka"}[m.group(1)]
        sisa = m.group(4)
        if sisa.startswith("ل"):                 # بِاللَّهِ → billāhi
            sisa = sisa.replace(SYADDAH, "", 1)
            return pref + "l" + _rangka(_satuan(sisa), True)
        r = pref + "l-" + _rangka(_satuan(sisa), True)
        return (r.replace("l-’a", "l-a").replace("l-’i", "l-i")
                 .replace("l-’u", "l-u").replace("l-’ū", "l-ū").replace("l-ā", "l-a"))

    awalan = ""
    if kata.startswith("ال") and len(kata) > 2:
        sisa = kata[2:]
        # huruf pertama sesudah ال
        first = next((c for c in sisa if c in LETTER), "")
        if first in SYAMSIYAH:
            kons = LETTER[first]
            awalan = "a" + kons + "-"
            # buang SATU shadda (penggandaan sudah diwakili awalan)
            i = sisa.index(first)
            j = i + 1
            while j < len(sisa) and sisa[j] in HARAKAT:
                if sisa[j] == SYADDAH:
                    sisa = sisa[:j] + sisa[j + 1:]
                    break
                j += 1
            kata = sisa
        else:
            awalan = "al-"
            kata = sisa

    hasil = (awalan + _rangka(_satuan(kata), True))
    # hamzah washal setelah al-/wal-/bil-: "al-’ardh" → "al-ardh"
    hasil = hasil.replace("l-’a", "l-a").replace("l-’i", "l-i")
    hasil = hasil.replace("l-’u", "l-u").replace("l-’ū", "l-ū")
    hasil = hasil.replace("wal-ū", "wal-ū").replace("l-ā", "l-a")
    hasil = hasil.replace("l-aa", "l-a").replace("l-ā", "l-a")
    return hasil


def latin_teks(teks: str) -> str:
    out = []
    for tok in re.split(r"(\s+)", teks):
        if tok.strip() and re.fullmatch(r"[\u0600-\u06FFًٌٍَُِّْـٰ]+", tok):
            out.append(latin(tok))
        else:
            out.append(tok)
    return "".join(out)


if __name__ == "__main__":
    uji = ["الرَّحْمَنِ", "الرَّحِيمِ", "الصِّدْقُ", "يُنْجِي", "أَنْجَى",
           "الْعَبْدُ", "عَلَيْهِ", "دَائِمًا", "كُلِّ", "حَالٍ", "الشَّمْس",
           "الْقَمَر", "بِسْمِ", "الله", "مُحَمَّد", "الطَّلْسَم", "خُدَّام",
           "الْوَحَا", "الْعَجَلَ", "السَّاعَةَ", "فُلَانَة", "بِنْت",
           "يَشْكُرُ", "وَيَحْمَدُهُ", "الْكِتَاب", "أَسْرَار", "الرُّوحَانِيَّات"]
    for u in uji:
        print(f"{u:24s} → {latin(u)}")
