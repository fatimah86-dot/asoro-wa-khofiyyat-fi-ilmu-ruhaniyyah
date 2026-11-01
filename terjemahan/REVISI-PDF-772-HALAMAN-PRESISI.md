# Revisi crop presisi — PDF 772 halaman

## Metode dan pemetaan

Nomor yang dipakai adalah **indeks halaman di `PDF-772-HALAMAN-FINAL.pdf`**, bukan nomor halaman cetak kitab. Tiap rajah diproses sebagai salinan scan (tanpa redraw) dengan skrip `crop_wafaq_presisi_2112x1808.py`: flat-field `BG_WINDOW=31`, `BLACK_AT=0.55`, `WHITE_AT=0.88`, `WHITE_SNAP=235`, tanpa threshold keras; keluaran 2112×1808 px, 300 DPI, LANCZOS.

> PDF halaman 10 memiliki gambar dengan teks keterangan yang menyebut “Halaman 3”, tetapi bentuk rajahnya cocok dengan wafaq di halaman cetak 5 pada `Picture 002.jpg` dan dengan bagian Halaman 05 di BATCH 01. Crop merujuk ke rajah sumber, bukan label gambar yang tidak konsisten.

## Halaman PDF 10

Sumber: `Picture 002.jpg`, BOX `(245,230,815,535)` px. Memuat empat baris tabel, tiang/simbol sisi kiri, dan tulisan/titik di bawah tabel; prosa di bawah rajah dikeluarkan.

![Crop presisi PDF halaman 10 — Wafaq Halaman cetak 05](rajah/rajah-hal-005-wafaq-tehij-presisi-2112x1808.jpg)

Hasil: 2112×1808 px, 300 DPI, LANCZOS 3.46×. Putih murni 88.2% seluruh kanvas (92.9% piksel non-tinta); tidak ada threshold keras atau redraw.

---

## Halaman PDF 16, 22, 28, 31–32, 42, 49, 54

Akan ditambahkan setelah verifikasi dan crop tiap indeks halaman.
