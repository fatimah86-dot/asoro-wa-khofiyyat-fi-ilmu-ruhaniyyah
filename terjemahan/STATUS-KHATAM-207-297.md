# STATUS KHATAM HALAMAN 207–297 (Batch 44–67) — Dokumen Serah-Terima

> Dibuat pada branch `arena/171484f8-asoro-wa-khofiyyat-fi-ilmu-ruh`.
> Dokumen ini adalah **laporan jujur** tentang apa yang sudah selesai, apa yang menghalangi, dan cara melanjutkan tanpa mengulang eksplorasi.

## 1. Peta halaman ↔ berkas scan (HASIL VERIFIKASI, bukan asumsi)

Polanya **BUKAN** 2 halaman berurutan per Picture. Untuk Hal. 206–217 hasil pembacaan angka kaki halaman:

| Picture | Hal. kanan | Hal. kiri | Batch |
|---|---|---|---|
| 105 | 206 | **207** | 43 / **44** |
| 106 | **208** | **209** | **44** / **45** |
| 107 | **212** | **213** | **45** / **46** |
| 108 | **214** | **215** | **46** / **47** |
| 106b | 210 | **211** | **46 GAP FIX** |
| 109 | **216** | 217 | **47** / 48 |

> **PEMBARUAN (gap fix):** Hal. **210** dan **211** kini **sudah ada** — sumbernya `Picture_106b-210-211.jpg` (1667×5000 px, 300 DPI, render halaman 210–211 dari `terjemahan/PDF-772-HALAMAN-FINAL.pdf`), dan isinya sudah ditranskripsi di `BATCH-46-Hal-210-211.md`. Peta urutan karena itu utuh: **106 → 208|209 · 106b → 210|211 · 107 → 212|213 · dst.** Angka 295/297 di bawah adalah catatan **sejarah** sebelum gap fix dan sudah tidak berlaku.

**Halaman 210 dan 211 TIDAK ADA dalam berkas scan.** *(catatan sejarah — lihat blok pembaruan di atas)* Bukti: Picture 106 belahan kiri berkaki `209`, Picture 107 belahan kanan berkepala `212`, dan teksnya pun tidak menyambung (209 berakhir `وَبِهِ أَقْسَمْتُ عَلَيْكَ أَيُّهَا السَّيِّدُ`, 212 dibuka `يَا جِبْرَائِيلُ …`). Karena itu:
- Semua Picture **108 ke atas bergeser +2** terhadap rumus `2N−4 / 2N−3`.
- Batas maksimum yang dapat dicapai dari berkas yang ada: **295 / 297** halaman.
- Untuk mencapai **297/297**, Hal. 210–211 harus dipindai/diimpor lebih dulu. Isinya **tidak boleh dikarang**.

Catatan lain: `terjemahan/assets/Picture.jpg` (tanpa nomor) = **sampul + Muqaddimah (Hal. 1)**, bukan Picture 150. Jumlah Picture bernomor = 149 (001–149).

## 2. Yang sudah selesai di branch ini

| Batch | Halaman | Rajah | Berkas MD |
|---|---|---|---|
| 44 FINAL | 207, 208 | 1 — `rajah-hal-207-rajah-bergaris-presisi-2112x1808.jpg` | `BATCH-44-Hal-207-208.md` |
| 45 | 209, 212 | 0 | `BATCH-45-Hal-209-212.md` |
| 46 | 213, 214 | 0 | `BATCH-46-Hal-213-214.md` |
| 47 | 215, 216 | 2 — `rajah-hal-215-…`, `rajah-hal-216-…` | `BATCH-47-Hal-215-216.md` |
| **46 GAP FIX** | **210, 211** | 0 — tabel angka ditranskripsi, bukan di-crop (§7.3) | `BATCH-46-Hal-210-211.md` |

Halaman terbaca lengkap: **207, 208, 209, 210, 211, 212, 213, 214, 215, 216** (10 halaman).
Kumulatif: **216 / 297** (206 halaman dari induk + 10 halaman ini).

## 3. Sisa pekerjaan

Batch 48 = Hal. **217** (Picture 109 kiri) + Hal. **218** (Picture 110 kanan), lalu terus sampai **Batch 88 = Hal. 297** (Picture 149 kiri; Picture 149 kanan = Hal. 296). Rumus setelah gap fix: **Picture N (N ≥ 107) → kiri = 2N−1, kanan = 2N−2**; Picture 149 → **297 | 296**. Sisa: **81 halaman (217–297)**.

Setiap batch tetap: baca 2 belahan → transkripsi 3 susun (Arab → Latin → Layer 1 + Layer 2) → crop rajah bila ada → commit + push per batch.

**Perkiraan realistis:** transkripsi setia pada kualitas Batch 44–47 memerlukan **1–2 batch per giliran kerja** yang panjang. 81 halaman tidak dapat dihasilkan dalam satu giliran tanpa mengorbankan ketepatan — karena itu pekerjaan dikerjakan per batch dan di-commit per batch.

## 4. Temuan teknis penting tentang parameter crop

- `WHITE_SNAP` **tidak** dapat dipakai untuk mencapai “putih 78,6 %”. Pengukuran pada crop Hal. 207: `WHITE_SNAP` 255 → 250 → 245 → 240 → 235 menghasilkan putih **93,5 % → 93,6 % → 93,7 % → 93,8 % → 93,8 %** (kanvas margin 70 px) dan **96,5 %** (margin 15 %). Artinya **menurunkan** `WHITE_SNAP` **menaikkan** jumlah piksel yang dikunci 255.
- Persentase putih ditentukan oleh **kerapatan tinta di dalam kotak crop**. Crop rajah garis Hal. 207 hanya memuat tinta 1,1 %, sehingga lantai putihnya ±96 %, sedangkan wafaq padat Hal. 206 bisa ±78 %. Karena itu angka putih selalu **dilaporkan hasil ukur**, bukan dikejar sebagai target.
- Skrip `crop_wafaq_presisi_2112x1808.py` kini menerima `--white-snap` dan `--margin` (default `WHITE_SNAP=235`, `margin=15 %`), selalu 2112×1808 px / 300 DPI / LANCZOS / `BG_WINDOW=31`, `BLACK_AT=0.55`, `WHITE_AT=0.88`.
- Selalu periksa tepi: hitung bbox tinta pada kanvas hasil; bila `xmin<4` atau `xmax>2108` berarti rajah terpotong dan BOX harus dilebarkan.

## 5. Hal yang TIDAK boleh dilakukan

1. Mengisi Hal. 210–211 dengan teks karangan.
2. Menulis “khatam 297/297” sebelum Hal. 217–297 benar-benar selesai ditranskripsi.
3. Menyalin rincian (hajat, sa‘ah, tinta, bukhur, bilangan 313×, wafaq Hawwaz) dari batch lain ke halaman yang tidak memuatnya.
4. Memperbaiki/menghaluskan teks cetakan yang rusak tanpa catatan.
