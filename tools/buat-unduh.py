#!/usr/bin/env python3
"""Bangun teks-koreksi.md dan dua paket ZIP di folder unduh/."""
from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNDUH = ROOT / "unduh"
INDEX = ROOT.read_text() if False else ROOT / "index.html"

BLOCK = {"h2", "h3", "p", "li", "div", "td", "th", "caption"}
SKIP_CLASS = {"ornament", "shamsa"}


def strip_tags(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>\s*<p[^>]*>", "\n\n", s, flags=re.I)
    s = re.sub(r"<li[^>]*>", "\n- ", s, flags=re.I)
    s = re.sub(r"</h2>", "\n\n", s, flags=re.I)
    s = re.sub(r"</h3>", "\n\n", s, flags=re.I)
    s = re.sub(r"<h2[^>]*>", "\n\n## ", s, flags=re.I)
    s = re.sub(r"<h3[^>]*>", "\n\n### ", s, flags=re.I)
    s = re.sub(r"<span class=\"num\">([^<]*)</span>", r"\1 — ", s, flags=re.I)
    s = re.sub(r"<p class=\"bab-ar\">([^<]*)</p>", r"\n*\1*\n", s, flags=re.I)
    s = re.sub(r"<p class=\"ayat\">([^<]*)</p>", r"\n> \1\n", s, flags=re.I)
    s = re.sub(r"<p class=\"ayat-tr\">([^<]*)</p>", r"\n> *\1*\n", s, flags=re.I)
    s = re.sub(r"<p class=\"rajah-cap\">([^<]*)</p>", r"\n_[Rajah: \1]_\n", s, flags=re.I)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.I | re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.I | re.S)
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s, flags=re.I | re.S)
    s = re.sub(r"<span class=\"arabic\">([^<]*)</span>", r"\1", s, flags=re.I)
    s = re.sub(r'<span class="badge[^"]*">([^<]*)</span>', r" [\1]", s, flags=re.I)
    s = re.sub(r"<img[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<table[\s\S]*?</table>", table_to_md, s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def table_to_md(m: re.Match) -> str:
    chunk = m.group(0)
    rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", chunk, flags=re.I)
    out = ["\n"]
    for i, row in enumerate(rows):
        cells = re.findall(r"<t[hd][^>]*>([\s\S]*?)</t[hd]>", row, flags=re.I)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        out.append("| " + " | ".join(cells) + " |")
        if i == 0:
            out.append("| " + " | ".join("---" for _ in cells) + " |")
    out.append("\n")
    return "\n".join(out)


def extract_article(html_text: str) -> str:
    m = re.search(r"<article class=\"page\">([\s\S]*)</article>", html_text)
    if not m:
        raise SystemExit("article.page tidak ditemukan")
    body = m.group(1)
    body = re.sub(r"<img class=\"ornament\"[^>]*>", "", body)
    body = re.sub(r'<section class="bab" id="unduh-edisi">[\s\S]*?</section>', "", body)
    text = strip_tags(body)
    lines = []
    for line in text.splitlines():
        lines.append(line if line.startswith("|") else line.strip())
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    header = (
        "# Asrār wa Khafiyyāt fī ʿIlm al-Rūḥāniyyāt\n"
        "# أسرار وخفايات في علم الروحانيات\n\n"
        "Terjemah beranotasi atas naskah cetak Syeikh ʿAṭiyyah ʿAbd al-Ḥamīd.\n"
        "Berkas ini untuk dikoreksi (ejaan, nomor halaman, judul fasal).\n"
        "Rumus irsal / taʿdhīb / ifsād / mandil istinzāl / manʿ zawāj **jangan** ditambah.\n\n"
        "---\n\n"
    )
    return header + text + "\n"


def referenced_naskah(html_text: str) -> list[str]:
    found = re.findall(r"naskah/([^\"']+\.jpg)", html_text)
    names = []
    seen = set()
    for n in found:
        if n not in seen:
            seen.add(n)
            names.append(n)
    return names


def add_tree(zf: zipfile.ZipFile, rel: Path, prefix: str = "Asrar-wa-Khafiyyat/") -> None:
    path = ROOT / rel
    if path.is_dir():
        for p in sorted(path.rglob("*")):
            if p.is_file() and p.name != ".DS_Store":
                zf.write(p, prefix + str(p.relative_to(ROOT)))
    elif path.is_file():
        zf.write(path, prefix + str(rel))


def main() -> None:
    UNDUH.mkdir(exist_ok=True)
    html_text = (ROOT / "index.html").read_text(encoding="utf-8")
    md = extract_article(html_text)
    md_path = UNDUH / "teks-koreksi.md"
    md_path.write_text(md, encoding="utf-8")
    print("tulis", md_path, "chars", len(md))

    prefix = "Asrar-wa-Khafiyyat/"
    core = [
        Path("index.html"),
        Path("unduh.html"),
        Path("README.md"),
        Path("css/kitab.css"),
        Path("js/kitab.js"),
        Path("unduh/CARA-KOREKSI.txt"),
        Path("unduh/teks-koreksi.md"),
    ]

    lengkap = UNDUH / "Asrar-wa-Khafiyyat-edisi-lengkap.zip"
    with zipfile.ZipFile(lengkap, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in core:
            add_tree(zf, rel, prefix)
        add_tree(zf, Path("assets"), prefix)
        add_tree(zf, Path("rajah"), prefix)
        add_tree(zf, Path("naskah"), prefix)
    print("zip", lengkap.name, lengkap.stat().st_size)

    ringan = UNDUH / "Asrar-wa-Khafiyyat-teks-koreksi.zip"
    refs = referenced_naskah(html_text)
    with zipfile.ZipFile(ringan, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for rel in core:
            add_tree(zf, rel, prefix)
        add_tree(zf, Path("assets"), prefix)
        add_tree(zf, Path("rajah"), prefix)
        for name in refs:
            p = ROOT / "naskah" / name
            if p.is_file():
                zf.write(p, prefix + "naskah/" + name)
    print("zip", ringan.name, ringan.stat().st_size, "naskah", len(refs))


if __name__ == "__main__":
    main()
