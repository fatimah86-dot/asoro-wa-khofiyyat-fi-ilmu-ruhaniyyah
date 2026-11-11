#!/usr/bin/env python3
"""
build-ulang.py — Membangun ULANG terjemahan menjadi FORMAT 3 TINGKAT.

   🅰️  Teks Arab (gundul, dijaga apa adanya — Muhafazhah)
   🎧  Arab berharakat (dari kamus terverifikasi + mesin, i'rab ditangguhkan)
   🔤  Latin & Makhraj
   🇮🇩  Terjemahan & Tata Cara
   📖  Kunci Kata (gundul → berharakat → dibaca → arti)
   🧿  Rajah / Wafaq asli (dijaga)

Sumber harakat:
   data/kamus-harakat.json   → terverifikasi manual (✅)
   data/harakat-otomatis.json → mesin Mishkal (⚙️, perlu dicek)

ATURAN KEJUJURAN: harakat akhir kata yang bergantung i'rab DITANGGUHKAN
(tidak ditulis), agar tidak menebak. Kata tanpa data dibiarkan gundul.

Pakai: python3 tools/build-ulang.py [--hanya BATCH-xx]
"""
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import latin as LATIN  # noqa
from harakat import rapikan_harakat

SRC = os.path.join(ROOT, "terjemahan")
OUT = os.path.join(SRC, "versi-baru")
F_KAMUS = os.path.join(ROOT, "data", "kamus-harakat.json")
F_OTO = os.path.join(ROOT, "data", "harakat-otomatis.json")
F_SCAN = os.path.join(ROOT, "data", "transkripsi-scan.json")

HAR = "ًٌٍَُِّْـٰ"
ARAB = "\u0600-\u06FF"

SIMBOL = {"\u01C4": "ال", "\u01C1": "ل", "\u01C2": "ل", "\u01BE": "أ",
          "\u0006": "أ", "\u0005": "أ", "\u0594": "،"}

# partikel yang menempel di depan kata
PARTIKEL = [("و", "وَ"), ("ف", "فَ"), ("ب", "بِ"), ("ل", "لِ"), ("ك", "كَ")]


# ══════════════════════════════════════════════ utilitas teks
def bersihkan(t: str) -> str:
    for k, v in SIMBOL.items():
        t = t.replace(k, v)
    o = []
    for ch in t:
        if 0xFE70 <= ord(ch) <= 0xFEFF:
            o.append(unicodedata.normalize("NFKC", ch))
        elif ch in "\n\t" or unicodedata.category(ch)[0] != "C":
            o.append(ch)
    t = "".join(o)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def norm(w: str) -> str:
    w = unicodedata.normalize("NFC", w.strip()).replace("ـ", "")
    w = (w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
          .replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و"))
    return re.sub(rf"[{HAR}]", "", w)


def tanpa_harakat(s: str) -> str:
    return re.sub(rf"[{HAR}]", "", unicodedata.normalize("NFC", s))


# ══════════════════════════════════════════════ kamus harakat
def muat():
    kamus = {}
    for k, v in json.load(open(F_KAMUS, encoding="utf-8"))["kata"].items():
        har, arti = v[0], v[1]
        kamus[norm(k)] = (har, arti)
    oto = {}
    if os.path.exists(F_OTO):
        for k, v in json.load(open(F_OTO, encoding="utf-8"))["kata"].items():
            oto[norm(k)] = v
    return kamus, oto


KAMUS, OTO = muat()
SCAN = {}
if os.path.exists(F_SCAN):
    SCAN = json.load(open(F_SCAN, encoding="utf-8")).get("halaman", {})

# harakat akhir yang bergantung i'rab → ditangguhkan
AKHIR_IRAB = {"َ", "ُ", "ِ", "ً", "ٌ", "ٍ"}


def tunda_irab(h: str) -> str:
    """Buang harakat akhir yang bergantung i'rab (bukan kepastian)."""
    h = h.strip()
    if not h:
        return h
    if h[-1] in AKHIR_IRAB:
        return h[:-1]
    return h


def _huruf_saja(w: str) -> str:
    w = unicodedata.normalize("NFC", w)
    return "".join(c for c in w if "\u0621" <= c <= "\u06FF" and c not in HAR)


def _netral(w: str) -> str:
    return (_huruf_saja(w).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
            .replace("ى", "ي").replace("ئ", "ي").replace("ؤ", "و"))


def huruf_utuh(asli: str, hasil) -> bool:
    """Harakat tidak boleh menambah/menghapus huruf (beda hamzah ditoleransi)."""
    return bool(hasil) and _netral(asli) == _netral(hasil)


def harakat_kata(w: str, izin_mesin=True):
    """-> (berharakat, sumber) ; sumber: 'kamus' | 'mesin' | None"""
    n = norm(w)
    if not n:
        return None, None
    if n in KAMUS:
        h = KAMUS[n][0]
        if huruf_utuh(w, h):            # tolak entri yang merusak huruf kata
            return h, "kamus"
    if izin_mesin and n in OTO:
        h = tunda_irab(OTO[n])
        if huruf_utuh(w, h):
            return h, "mesin"
    for p, ph in PARTIKEL:
        if w.startswith(p) and len(n) > 2:
            sisa = w[1:]
            h, s = harakat_kata(sisa, izin_mesin)
            if h and huruf_utuh(w, ph + h):
                return ph + h, s
    return None, None


def arti_kata(w: str):
    n = norm(w)
    if n in KAMUS:
        return KAMUS[n][1]
    for _, _ in PARTIKEL:
        pass
    return None


# ══════════════════════════════════════════════ baris Arab berharakat & latin
def baris_harakat(teks: str):
    """Kembalikan (teks_berharakat, teks_latin, cakupan%)"""
    keluar_h, keluar_l = [], []
    total = tahu = 0
    for tok in re.split(r"(\s+)", teks):
        if not tok.strip():
            keluar_h.append(tok)
            keluar_l.append(tok)
            continue
        if not re.fullmatch(rf"[{ARAB}{HAR}]+", tok):
            keluar_h.append(tok)
            keluar_l.append(tok)
            continue
        total += 1
        h, sumber = harakat_kata(tok)
        if h:
            tahu += 1
            keluar_h.append(h)
            keluar_l.append(LATIN.latin(h))
        else:
            keluar_h.append(tok)
            keluar_l.append(tok)
    cak = 100 * tahu / max(total, 1)
    return rapikan_harakat("".join(keluar_h)), "".join(keluar_l), cak


def kunci_kata(teks: str, maks=26):
    c = Counter()
    for w in re.findall(rf"[{ARAB}]+", tanpa_harakat(teks)):
        if norm(w) in KAMUS:
            c[norm(w)] += 1
    hasil = []
    for n, kali in c.most_common(maks):
        har, arti = KAMUS[n]
        hasil.append((n, har, LATIN.latin(har), arti, kali, "✅"))
    return hasil


# ══════════════════════════════════════════════ pemisah halaman
RX_HAL = re.compile(
    r"^#{2,4}\s*(?:HALAMAN|Halaman|Hal\.?|HAL\.?)\s*0*(\d{1,3})\s*[—–\-:]?\s*(.*)$", re.M)

RX_LABEL = re.compile(
    r"^[ \t]*(?:#{2,6}[ \t]*)?\**[ \t]*\[?[ \t]*"
    r"(Teks Arab Asli|TEKS ARAB ASLI|Terjemahan Indonesia|TERJEMAHAN INDONESIA|"
    r"Transliterasi Latin[^\]]*|TRANSLITERASI[^\]]*|Latin Fonetik[^\]]*)"
    r"([^\]]*)\]?\**[ \t]*$", re.M)


def kelas_label(s):
    s = s.lower()
    if "teks arab" in s:
        return "ARAB"
    if "terjemahan" in s:
        return "INDO"
    return "LATIN"


def praproses(isi: str) -> str:
    """Rapikan penanda internal: ### judul → teks tebal; hapus baris gambar-caption."""
    out = []
    for ln in isi.split("\n"):
        s = ln.strip()
        if s.startswith("![") and s.endswith(")") and "assets/" in s:
            out.append(ln)                      # gambar: biarkan
            continue
        if re.match(r"^\*{0,2}Gambar Rajah Asli", s):
            out.append("> " + s.strip("* "))
            continue
        if re.match(r"^#{1,4}\s", s) and not RX_LABEL.match(ln):
            out.append("**" + s.lstrip("# ").strip(" *") + "**")
            continue
        out.append(ln)
    return "\n".join(out)


def pecah_halaman(teks):
    tanda = [(m.start(), int(m.group(1)), m.group(2).strip(" —–-"))
             for m in RX_HAL.finditer(teks)]
    # jangan jadikan label bagian (### [Teks Arab ...]) sebagai judul halaman
    tanda = [(p, n, "" if re.match(r"^#+\s*\[", j) else j) for p, n, j in tanda]
    out = []
    for i, (pos, no, j) in enumerate(tanda):
        akhir = tanda[i + 1][0] if i + 1 < len(tanda) else len(teks)
        out.append((no, j, teks[pos:akhir]))
    return out


def pecah_label(isi):
    """Pisah blok per label — SADAR pagar ``` supaya label di dalam kode
    tidak dianggap judul bagian (bug lama: isi ikut tertelan)."""
    out = {"ARAB": [], "INDO": [], "LATIN": [], "LAIN": []}
    cur, buf = "LAIN", []
    suf_cur = ""
    dalam_kode = 0
    for ln in isi.split("\n"):
        if ln.strip().startswith("```"):
            dalam_kode = 1 - dalam_kode
            buf.append(ln)
            continue
        m = RX_LABEL.match(ln) if (not dalam_kode) else None
        if m:
            if "\n".join(buf).strip():
                out[cur].append((suf_cur, "\n".join(buf)))
            cur, buf, suf_cur = kelas_label(m.group(1)), [], (m.group(2) or "").strip(" —–-")
            continue
        buf.append(ln)
    if "\n".join(buf).strip():
        out[cur].append((suf_cur, "\n".join(buf)))
    return out


def ambil_gambar(s):
    imgs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", s)
    return imgs, re.sub(r"!\[[^\]]*\]\([^)]+\)", "", s)


RX_PLACEHOLDER = re.compile(r"^\s*\[\s*[^\]]*(?:lihat scan|Picture|tanpa Rajah|jika ada|\.\.\.)[^\]]*\]\s*$", re.I)


def pisah_placeholder(blok):
    """Pisahkan baris placeholder '[ ... lihat scan ... ]' dari isi sebenarnya."""
    nyata, ph = [], []
    for ln in blok.split("\n"):
        (ph if RX_PLACEHOLDER.match(ln) else nyata).append(ln)
    return "\n".join(nyata).strip(), [x.strip() for x in ph if x.strip()]


def rapikan_arab(s):
    s = bersihkan(s)
    s = re.sub(r"^[ \t]*```[a-zA-Z]*[ \t]*$", "", s, flags=re.M)
    return re.sub(r"\n{2,}", "\n", s).strip()


def rapikan_indo(s):
    if re.search("[Ǆǁǂƾ]", s):
        s = bersihkan(s)
    s = re.sub(r"^>\s*$", "", s, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def rapikan_judul(j):
    j = re.sub(r"\(?\s*(?:halaman\s+)?(?:kanan|kiri)?\s*(?:dari\s+)?`?Picture\s*\d+[^)]*\)?",
               "", j, flags=re.I)
    j = re.sub(r"[`*]|Picture\s*\d+(\.jpg)?", "", j, flags=re.I)
    j = re.sub(r"\s*[—–-]\s*(kanan|kiri)\s*$", "", j, flags=re.I)
    return re.sub(r"\s{2,}", " ", j).strip(" —–-,()")


def potong(j, n=78):
    return j if len(j) <= n else j[:n].rsplit(" ", 1)[0] + " …"


# ══════════════════════════════════════════════ kartu halaman
def kartu(nomor, judul, isi_kotor):
    isi = praproses(isi_kotor)
    p = pecah_label(isi)

    arab_blok, placeholder = [], []
    for suf, x in p["ARAB"]:
        if not x.strip():
            continue
        nyata, ph = pisah_placeholder(x)
        placeholder += ph
        if nyata:
            arab_blok.append((suf, rapikan_arab(nyata)))
    indo_blok = [(s, rapikan_indo(x)) for s, x in p["INDO"] if x.strip()]
    latin_manual = "\n\n".join(rapikan_indo(x) for _, x in p["LATIN"] if x.strip())
    lain = "\n\n".join(rapikan_indo(x) for _, x in p["LAIN"] if x.strip())

    imgs = ambil_gambar(isi)[0]
    lain = ambil_gambar(lain)[1]
    indo = "\n\n".join(x for _, x in indo_blok)
    indo = ambil_gambar(indo)[1]

    ket = ""
    m = re.search(r">?\s*\**Gambar Rajah Asli[^\n]*", lain)
    if m:
        ket = m.group(0).lstrip("> ").strip("* ")
        lain = lain.replace(m.group(0), "")

    sambung = [s for s, _ in arab_blok if re.search(r"sambung|lanjut", s, re.I)]
    arab = "\n\n".join(x for _, x in arab_blok)

    # ── transkripsi scan asli menimpa teks lama yang masih placeholder
    cat_scan = ""
    sc = SCAN.get(str(nomor))
    if sc:
        arab = sc["arab"].strip()
        if sc.get("indo"):
            indo = sc["indo"].strip()
        if sc.get("sumber"):
            cat_scan = f"> 📖 **Sumber teks:** {sc['sumber']} — ditranskripsi ulang dari scan asli, bukan OCR."
        if sc.get("catatan"):
            cat_scan += "\n" + "\n".join(f"> - {c}" for c in sc["catatan"])

    L = [f'<a id="hal-{nomor:03d}"></a>', ""]
    jd = potong(rapikan_judul(judul)) if judul else ""
    L.append(f"## 📄 HAL. {nomor:03d}" + (f" — {jd}" if jd else ""))
    L.append("")
    if sambung:
        L += [f"> ⤵️ *Sambungan: {'; '.join(dict.fromkeys(sambung))}*", ""]

    if arab:
        L += ["**🅰️ TEKS ARAB** — gundul, dijaga apa adanya", "", "```", arab, "```", ""]

        h, l, cak = baris_harakat(arab)
        L += ["**🎧 ARAB BERHARAKAT** — harakat akhir yang bergantung i'rab "
              "sengaja ditangguhkan (tidak ditebak)", "", "```", h, "```", ""]
        L += ["**🔤 LATIN & MAKHRAJ**", "", "```", l, "```", ""]
        if cak < 100:
            L += [f"> ⚠️ Cakupan harakat **{cak:.0f}%** dari kata di halaman ini. "
                  f"Kata sisanya dibiarkan gundul — **tidak ditebak**.", ""]
        if latin_manual:
            L += ["> *Transliterasi asli dari batch lama (pembanding):*", "",
                  latin_manual, ""]
    else:
        L += ["**🅰️ TEKS ARAB** — *halaman ini tanpa teks Arab*", ""]

    if indo:
        L += ["**🇮🇩 TERJEMAHAN & TATA CARA**", "", indo, ""]

    kk = kunci_kata(arab) if arab else []
    if kk:
        L += ["**📖 KUNCI KATA** — untuk pemula (✅ = harakat terverifikasi)", "",
              "| Kata | Berharakat | Dibaca | Arti | Muncul |", "|---|---|---|---|---|"]
        for w, har, lat, arti, kali, tag in kk:
            L.append(f"| {w} | {har} | {lat} | {arti} | {kali}× {tag} |")
        L.append("")

    if cat_scan:
        L += ["**🔎 CATATAN TRANSKRIPSI**", "", cat_scan, ""]

    if placeholder:
        L += ["**⚠️ BAGIAN YANG BELUM DITRANSKRIPSI**", "",
              "Baris berikut pada batch lama masih berupa catatan rujukan, bukan teks kitab. "
              "Belum ditranskripsi dari scan — **tidak diisi tebakan**:", ""]
        L += [f"> `{x}`" for x in placeholder]
        L += [""]

    if lain.strip():
        L += ["**📝 CATATAN HALAMAN**", "", lain.strip(), ""]

    if imgs or ket:
        L += ["**🧿 RAJAH / WAFAQ ASLI** — tidak diterjemah, angka tidak diubah", ""]
        for alt, src in imgs:
            L += [f"![{alt or 'Rajah asli'}]({src})", ""]
        if ket:
            L += [f"> {ket}", ""]
        L += ["> **[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]**", ""]

    L += ["---", ""]
    return "\n".join(L), bool(arab), bool(imgs)


# ══════════════════════════════════════════════ batch
LEGENDA = (
    "> **Kunci baca Latin:** ā ī ū = vokal panjang · ḥ ṣ ḍ ṭ ẓ = huruf tebal "
    "(emfatik) · ‘ = ع · ’ = ء · sy = ش · kh = خ · dz = ذ · ts = ث · "
    "al- berasimilasi (asy-, ar-, aṭ- …)"
)


def build(path):
    teks = open(path, encoding="utf-8", errors="replace").read()
    judul_batch = teks.split("\n", 1)[0].lstrip("# ").strip()
    halaman = pecah_halaman(teks)
    if not halaman:
        return None

    atas = teks[: RX_HAL.search(teks).start()]
    m = re.search(r">\s*\[!(?:CAUTION|WARNING)\][\s\S]*?(?=\n##|\Z)", atas)
    peringatan = m.group(0).strip() if m else ""

    isi = [f"# {judul_batch}", "",
           "> **FORMAT 3 TINGKAT**: 🅰️ Arab gundul → 🎧 Arab berharakat → 🔤 Latin & "
           "Makhraj → 🇮🇩 Terjemahan → 📖 Kunci Kata → 🧿 Rajah dijaga", "",
           LEGENDA, ""]
    if peringatan:
        isi += [peringatan, ""]

    daftar, kartu_kumpul, n_rajah = [], [], 0
    for nomor, judul, isi_hal in halaman:
        k, ada_arab, ada_img = kartu(nomor, judul, isi_hal)
        kartu_kumpul.append(k)
        daftar.append((nomor, rapikan_judul(judul), ada_arab, ada_img))
        n_rajah += 1 if ada_img else 0

    toc = ["## 🧭 DAFTAR HALAMAN", "", "| Hal. | Judul | Arab | Rajah |", "|---|---|---|---|"]
    for nomor, judul, ada_arab, ada_img in daftar:
        toc.append(f"| [{nomor:03d}](#hal-{nomor:03d}) | {potong(judul, 68) or '—'} "
                   f"| {'✓' if ada_arab else '—'} | {'🧿' if ada_img else '—'} |")
    toc += ["", f"*{len(daftar)} halaman · {n_rajah} rajah · "
                f"sumber: `{os.path.basename(path)}`*", "", "---", ""]

    return "\n".join(isi + toc + kartu_kumpul), daftar, n_rajah


def main():
    os.makedirs(OUT, exist_ok=True)
    pola = os.path.join(SRC, "BATCH-*.md")
    if len(sys.argv) > 2 and sys.argv[1] == "--hanya":
        pola = os.path.join(SRC, f"BATCH-*{sys.argv[2]}*.md")

    semua, total_rajah, gagal = [], 0, []
    for f in sorted(glob.glob(pola)):
        r = build(f)
        if not r:
            gagal.append(os.path.basename(f))
            print(f"⚠️  {os.path.basename(f)} — tanpa penanda halaman")
            continue
        teks, daftar, nr = r
        open(os.path.join(OUT, os.path.basename(f)), "w", encoding="utf-8").write(teks)
        total_rajah += nr
        semua.extend((os.path.basename(f), n, j, a, i) for n, j, a, i in daftar)
        print(f"✅ {os.path.basename(f):34s} {len(daftar):2d} hal · {nr:2d} rajah · "
              f"{len(teks)//1024:3d} KB")

    if not (len(sys.argv) > 2 and sys.argv[1] == "--hanya"):
        tulis_induk(semua, total_rajah, gagal)


def tulis_induk(semua, total_rajah, gagal):
    per = {}
    for nama, n, j, a, i in semua:
        per.setdefault(nama, []).append((n, i))

    idx = ["# 📚 ASRAR WA KHAFAYYAT — TERJEMAHAN FORMAT 3 TINGKAT", "",
           "**Kitab:** أسرار و خفايات في علم الروحانيات",
           "**Penulis:** Syaikh Athiyah Abdul Hamid (شيخ الروحانيين)", "",
           "## Cara baca setiap halaman", "",
           "| # | Bagian | Isi |", "|---|---|---|",
           "| 1 | **🅰️ TEKS ARAB** | Naskah gundul apa adanya — tidak diubah |",
           "| 2 | **🎧 ARAB BERHARAKAT** | Harakat lengkap; harakat yang bergantung i'rab ditangguhkan |",
           "| 3 | **🔤 LATIN & MAKHRAJ** | Cara membunyikan (gaya pesantren) |",
           "| 4 | **🇮🇩 TERJEMAHAN** | Makna & tata cara |",
           "| 5 | **📖 KUNCI KATA** | Kata → berharakat → dibaca → arti |",
           "| 6 | **🧿 RAJAH** | Dijaga: tidak diterjemah, angka wafaq tidak diubah |",
           "", LEGENDA, "",
           "## Catatan kejujuran", "",
           "- Harakat yang **sudah terverifikasi** bertanda ✅ di Kunci Kata.",
           "- Harakat hasil **mesin** dipakai untuk baris berharakat, dan harakat akhir",
           "  yang bergantung pada i'rab **dibuang** — supaya tidak menebak.",
           "- Kata yang belum punya data harakat **dibiarkan gundul**, dan cakupannya",
           "  dilaporkan per halaman.", "",
           "---", "", "## 🗂️ Daftar Batch", "",
           "| Batch | Hal. | Halaman | Rajah |", "|---|---|---|---|"]
    for nama in sorted(per):
        ns = [n for n, _ in per[nama]]
        raj = sum(1 for _, i in per[nama] if i)
        idx.append(f"| [{nama}]({nama}) | {min(ns):03d}–{max(ns):03d} | {len(ns)} | "
                   f"{raj if raj else '—'} |")
    idx += ["", "---", "",
            f"**Total:** {len(semua)} halaman · {len(per)} batch · {total_rajah} rajah", ""]
    if gagal:
        idx += ["### ⚠️ Batch perlu perbaikan manual", ""]
        idx += [f"- `{g}` — tidak punya penanda halaman" for g in gagal]
        idx += [""]
    idx += ["> ⚠️ **Peringatan etis:** naskah ini berisi azimah/wafaq/thilasm. Disajikan",
            "> untuk studi naskah & literasi baca kitab gundul — **bukan** anjuran praktik.",
            "> Tidak ada bukti ilmiah efek supranatural. Jangan pakai untuk merugikan orang."]
    open(os.path.join(OUT, "00-DAFTAR-ISI.md"), "w", encoding="utf-8").write("\n".join(idx))


if __name__ == "__main__":
    main()
