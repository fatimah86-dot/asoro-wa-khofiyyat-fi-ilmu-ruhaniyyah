# 🔥 asoro-wa-khofiyyat - KHATAM KUBRO 120% 150 RAJAH + LATIN ARAB 🔥

> **Alhamdulillah 150 Rajah HQ + Latin Arab - 2 Repo Gabung!**

## 🔑 KUNCI PERMANEN — USTADZ YOAD (Nahwu Sharaf)
Pengaturan bedah teks Arab gundul **10 LANGKAH WAJIB** + aturan Kitab Hikmah (Muhafazhah)
ada di ➡️ **`panduan/USTADZ-YOAD-KUNCI-PERMANEN-10-LANGKAH.md`**

| Berkas | Isi |
|---|---|
| `AGENTS.md` | Pintu masuk aturan repo |
| `panduan/USTADZ-YOAD-KUNCI-PERMANEN-10-LANGKAH.md` | File induk aturan |
| `panduan/10-LANGKAH-CEPAT.md` | Kartu saku |
| `panduan/template-output.md` | Kerangka output |
| `panduan/contoh-terap.md` | Benchmark Teks 1 & 2 |
| `panduan/kamus-istilah-hikmah.md` | Kamus Falak/Hikmah |
| `tools/cek-10-langkah.py` | Pemeriksa otomatis 10 langkah |

## Sumber:
- Repo 1 (001-099): 99 gambar
- Repo 2 (100-149 + Picture.jpg): 51 gambar
- Total: 150 Rajah HQ

## Fitur Baru LATIN ARAB:
Setiap halaman sekarang ada:
1. Arab Gundul (asli)
2. **Latin Arab (transliterasi) - BARU!**
3. Terjemah Indonesia pesantren

## Struktur:
| Batch | Hal | Rajah | Fitur |
|-------|-----|-------|-------|
| 01-33 | 001-164 | 149R | Arab+Terjemah |
| 34-42 | 165-204 | 19R | Arab+Latin+Terjemah |

Total: 204 Hal - 150 Rajah - Latin Arab
BATCH-42: Hal 203-204 (terjemahan/BATCH-42-Hal-203-204.md) - 0 rajah, teks penuh

© 2026 fatimah86-dot

---

## 📘 VERSI BARU — FORMAT 3 TINGKAT (`terjemahan/versi-baru/`)

Struktur terjemahan **dibangun ulang** agar mudah dibaca. Setiap halaman berisi 5 blok berurutan:

| # | Blok | Isi |
|---|---|---|
| 1 | **🅰️ TEKS ARAB** | Naskah gundul apa adanya (Muhafazhah) |
| 2 | **🎧 ARAB BERHARAKAT** | Harakat lengkap; harakat akhir yang bergantung i'rab **ditangguhkan** (tidak ditebak) |
| 3 | **🔤 LATIN & MAKHRAJ** | Transliterasi gaya pesantren + kunci baca (ā ī ū, ḥ ṣ ḍ ṭ ẓ, ‘/’, sy/kh/dz/ts) |
| 4 | **🇮🇩 TERJEMAHAN** | Makna & tata cara |
| 5 | **📖 KUNCI KATA** | Kata → berharakat → dibaca → arti (✅ = terverifikasi) |
| + | **🧿 RAJAH** | Dijaga: tidak diterjemah, angka wafaq tidak diubah |

👉 Mulai dari **[`terjemahan/versi-baru/00-DAFTAR-ISI.md`](terjemahan/versi-baru/00-DAFTAR-ISI.md)**

### Hasil verifikasi akhir

| Pemeriksaan | Hasil |
|---|---|
| Halaman | **204 / 204** lengkap (1–204), tidak ada yang hilang |
| Rajah | 108 crop asli, angka tidak diubah |
| Harakat dobel / salah tumpuk | **0** |
| Huruf presentasi / simbol katib rusak (Ǆ ǁ ǂ ƾ) | **0** |
| Placeholder teks yang belum ditranskripsi | **0** |
| Cakupan harakat | rata-rata **94,9 %** (sisanya dibiarkan gundul, tidak ditebak) |

Jalankan sendiri: `python3 tools/verifikasi.py`

### Perbaikan besar yang dilakukan

1. **Transkripsi ulang 25 halaman langsung dari scan** (`data/transkripsi-scan.json`) — halaman yang sebelumnya masih berupa `[ ... lihat scan ... ]`, termasuk Batch 27, 28, 29, 30, 31, 32 dan halaman **11, 12, 13, 140, 141** yang sebelumnya belum ada sama sekali.
2. **Struktur seragam** — semua batch memakai satu kerangka yang sama (dulu 12 variasi judul berbeda).
3. **Harakat** — 8.453 kata diberi harakat (mesin Mishkal + 12 koreksi manual + perapi tumpang-tindih), plus 472 kata di kamus terverifikasi (`data/kamus-harakat.json`).
4. **Transliterasi** — mesin baru `tools/latin.py`: asimilasi syamsiyah (asy-, ar-, aṭ-), `wal-/bil-/lil-/kal-`, hamzah washal, vokal panjang, ta' marbuthah.
5. **Pembersih bug lama** — teks yang tertelan pagar kode (Batch 12 dulu kehilangan isi), halaman ganda (136–139, 150/151, 158/159), dan tag markdown bocor ke blok kode.

### Alat (semua bisa dijalankan ulang)

| Berkas | Fungsi |
|---|---|
| `tools/latin.py` | Transliterasi Arab → Latin |
| `tools/harakat.py` | Bangun basis harakat + perapi tumpang-tindih |
| `tools/build-ulang.py` | Rakit ulang struktur 3 tingkat |
| `tools/verifikasi.py` | Pemeriksa akhir (4 lapis) |
| `tools/normalisasi-arab.py` | Perbaiki teks Arab rusak (katib) |
| `tools/versi-terjemahan.py` | Laporan cakupan per batch |
| `data/transkripsi-scan.json` | Transkripsi manual dari scan |
| `data/kamus-harakat.json` | Kamus harakat terverifikasi |
| `data/harakat-otomatis.json` | Harakat mesin + koreksi |

> ⚠️ **Peringatan etis:** naskah ini berisi azimah/wafaq/thilasm. Versi ini disajikan untuk **studi naskah & literasi baca kitab gundul** — bukan anjuran praktik. Tidak ada bukti ilmiah efek supranatural. Jangan gunakan untuk merugikan orang lain.
