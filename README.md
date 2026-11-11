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

---

## 🔍 REKAP AUDIT AKHIR — 11 November 2026

Audit dilakukan **langsung dari isi PR #16** (bukan dari laporan lama), lalu cacatnya diperbaiki di branch yang sama. **Tidak ada transkripsi baru** yang dibuat — seluruh audit memakai berkas yang sudah ada.

### Hasil 4 lapis

| Lapis | Diperiksa | Hasil |
|---|---|---|
| **A. Kelengkapan** | Halaman 1–204 termasuk 11, 12, 13, 140, 141 | **204/204 unik, 0 hilang, 0 ganda** ✅ |
| **B. Harakat** | 9 pola dobel (`ِْ` `ََ` `ٍٍ` `ُُ` `ًً` `ْْ` `َِ` `ُِ` `َّ`) | **8 pola = 0**; `َّ` = 6.640 → **urutan kanonik, bukan dobel** ✅ |
| **C. Kebersihan** | Huruf presentasi U+FE70–FEFF, simbol katib `Ǆ ǁ ǂ ƾ`, karakter kontrol | **0 / 0 / 0** ✅ |
| **D. Placeholder** | `[ ... lihat scan ... ]`, "akan dilengkapi" | **0** ✅ |

### Soal `َّ` (tasydid + fathah) — 6.640 kemunculan

Ini **bukan** harakat dobel. Dalam Unicode, tasydid (U+0651) **wajib** mendahului harakat (fathah U+064E) — ini urutan kanonik. Yang dicari adalah urutan terbaliknya (`fathah` lalu `tasydid`):

- urutan kanonik `َّ` : **6.640**
- urutan terbalik `َّ` (salah) : **0**

Contoh: `الرَّحْمٰن` — benar. Maka pemeriksa hanya menandai **tasydid-setelah-vokal**, bukan tasydid-sebelum-vokal.

### Cacat yang ditemukan audit dan sudah diperbaiki

| # | Cacat | Dampak | Perbaikan |
|---|---|---|---|
| 1 | **Halaman 36 ganda** — BATCH-07 memuat blok placeholder "akan dilengkapi setelah Picture 018" | 2 blok untuk 1 halaman | Blok placeholder dihapus → "## Catatan Halaman 036" |
| 2 | **Halaman 96 ganda** — BATCH-19 keliru melabeli isi hal.97 sebagai hal.96 | 2 blok untuk 1 halaman | Duplikat dihapus; BATCH-20 jadi satu-satunya blok hal.96 bertanda `[SCAN TIDAK JELAS - HALAMAN 96]` |
| 3 | **Rule `"الْا"→"الْ"` dan `"أَأ"→"أَ"` menghapus HURUF** | `الاسم` (nama) → `السم` (**racun**); `الاستدلال` → `الستدلال` | Kedua rule dibuang, diganti penjaga `jaga_huruf()` |
| 4 | **Entri kamus berartikel bocor ke kata tanpa artikel** (`setdefault(norm(k)[2:])`) | `حكيم` → `الْحَكِيم` (padahal tanpa ال) | Mekanisme `setdefault` dihapus |
| 5 | **23 entri data harakat merusak huruf** (mis. `الاستدلال` → `الْسْتِدْلَاَلُ`) | 1.150 kata salah tulis di lapis 🎧 | Entri dibersihkan, data dibangun ulang: **8.921 entri, 0 merusak** |
| 6 | **`tools/verifikasi.py` tidak mendeteksi halaman ganda** | hal.36 & 96 lolos | Ditambah pemeriksa **E. Halaman Ganda** |
| 7 | **`tools/verifikasi.py` tidak memeriksa kesetiaan huruf** | cacat #3–#5 lolos | Ditambah pemeriksa **F. Kesetiaan Huruf** |

### Muhafazhah (المحافظة على القديم الصالح) — terverifikasi utuh

| Objek | Status |
|---|---|
| Asma' Suryani `بصلكمشلهنيد` `بخششطوخ` `كلمموشيا` `هملهليو` `شمخلوش` `اقطيازش` | **6/6 utuh** ✅ |
| Angka wafaq/thilasm (1.690 token angka, termasuk `١١٢ ١١٢ ١١٣ ١١٣ ٣٠٠`, `٧٦٥٨٤٩`, `٦١٩`) | **0 berubah** — urutan angka lapis 🅰️ = lapis 🎧 ✅ |
| Tag `[TEKS ASLI DIJAGA - TIDAK DITERJEMAH KARENA THILASM/WAFAQ]` | **106** ✅ |
| Gambar rajah/wafaq asli (tidak digambar ulang, crop background putih) | **178 gambar, 0 tautan rusak** ✅ |

### Batch yang diperiksa khusus

| Batch | Status |
|---|---|
| **BATCH-03** (hal. 11–15) | Utuh 32 KB — hal.11 tidak menimpa hal.12–16 ✅ |
| **BATCH-12** (hal. 57–61) | Utuh 29 KB — tidak kehilangan isi karena pagar kode ✅ |
| **Hal. 136–139** (tashrif 1–12) | 1 blok masing-masing, tidak tertimpa ✅ |
| **Hal. 150/151** (thilasm) | 1 blok masing-masing; nomor thilasm sudah الثالث/الرابع ✅ |
| **Hal. 158–159** (qasam syarif) | 1 blok masing-masing, tidak kosong ✅ |
| **BATCH-28** (hal. 136–141) | 6 halaman, termasuk 140 & 141 ✅ |

### Perintah verifikasi

```bash
python3 tools/harakat.py            # bangun basis harakat (dengan penjaga huruf)
python3 tools/build-ulang.py        # rakit ulang 42 batch versi 3 tingkat
python3 tools/verifikasi.py         # 6 lapis pemeriksaan
```

Keluaran terakhir: `✅ SEMUA PEMERIKSAAN LULUS` — 204 halaman, 0 ganda, 0 hilang, harakat dobel 0, kesetiaan huruf 33.354 kata / 0 blok menyimpang.
