# STATUS KHATAM 297 FULL

**Pembaruan:** 1 Oktober 2026, 18:49 WIB
**Status batch 41–60:** **BELUM LENGKAP — VALIDASI KETAT GAGAL**

## KHATAM 297 HAL — Batch 41–60: peta scan dan crop awal

Status ini sengaja **tidak** memakai klaim “BATCH 1–60 COMPLETE”, “150 Gambar Asli Tanpa Kotak Hitam”, atau “RTL FIX” sebagai hasil akhir. Isi yang ada belum mendukung klaim tersebut.

### Hasil pemeriksaan

- Tersedia 20 dokumen batch dengan cakupan tidak tumpang tindih: Batch 41–58 (hal. 200–289), Batch 59 (290–292), dan Batch 60 (293–297).
- Scan sumber terhubung untuk 96 dari 98 nomor halaman: Picture 102–106 memuat hal. 200–209; Picture 107–149 memuat hal. 212–297.
- **Halaman cetak 210–211 tidak ditemukan** pada rangkaian scan yang ada: Picture 106 berakhir pada hal. 208–209 dan Picture 107 mulai pada hal. 212–213. Tidak ada teks yang direka untuk menutup celah ini.
- Bagian “Arab Gundul” saat ini menunjuk ke scan asli, bukan transkripsi Arab yang telah diperiksa. **Latin Arab dan Terjemah Pesantren belum diisi untuk 98 halaman.**
- Tiga crop rajah awal tersedia di `rajah/` (hal. 201, 215, 248). Metadata raster setara 300 DPI dan empat sudutnya putih. **54 dari target 57 crop belum tersedia atau belum diaudit.**
- Batch 1–40 belum diaudit sebagai bagian dari status ini. Beberapa file lama, termasuk contoh format BATCH-34, berisi teks placeholder; karena itu status seluruh Batch 1–60 tidak dapat dinyatakan khatam.

### Daftar yang masih harus diselesaikan

- [ ] Temukan scan halaman 210–211 atau catat secara resmi bahwa halaman tersebut tidak tersedia.
- [ ] Transkripsikan teks Arab Gundul dan verifikasi per halaman.
- [ ] Lengkapi Latin Arab dan terjemah pesantren berdasarkan scan, bukan placeholder.
- [ ] Inventarisasi semua rajah yang benar-benar ada, lalu selesaikan target 57 crop; jangan menambah crop rekaan.
- [ ] Jalankan validasi ketat sampai lulus, lalu audit Batch 1–40 sebelum menyebut “BATCH 1–60 COMPLETE”.
- [ ] Periksa GitHub Actions setelah perubahan dipublikasikan pada branch yang diizinkan.

### Validator

Jalankan `python3 scripts/validate_batch_41_60.py`. Validator ketat memang akan **gagal** sampai teks halaman, sumber yang hilang, serta crop dan metadata yang diminta benar-benar lengkap. Opsi `--structure-only` hanya memeriksa struktur dokumen dan keberadaan scan; opsi itu bukan bukti khatam.

### Publikasi dan GitHub Actions

- Commit `08e1e56` (`docs: map batches 41-60 scans and add strict validation`) sudah dipush ke branch sesi `arena/01a0f72a-asoro-wa-khofiyyat-fi-ilmu-ruh`.
- Branch `main` tetap pada `07ae0a1`; tidak ada force-push ke `main`.
- Belum ada workflow run untuk branch sesi setelah push. Run `KHATAM 297 FULL` terbaru yang terlihat di GitHub Actions berstatus sukses pada 29 September 2026, tetapi berjalan pada SHA lama `b7cfbaa` di `main`; itu **bukan** validasi commit ini.
- Dengan demikian, tidak ada klaim bahwa Actions untuk perubahan ini hijau atau bahwa hasil ini siap dinyatakan lengkap.
