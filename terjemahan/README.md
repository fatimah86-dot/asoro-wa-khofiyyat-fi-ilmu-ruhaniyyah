# Terjemahan Lengkap: *Asrār wa Khafāyāt fī 'Ilm al-Rūḥāniyyāt*
*(Rahasia-Rahasia dan Hal-Hal Tersembunyi dalam Ilmu Ruhaniyat)*
Karya: Syekh 'Aṭiyya 'Abdul Ḥamīd

## Isi kitab
Kitab ini terdiri dari **149 foto pindaian** (setiap foto = 1 sebaran berisi 2 halaman kitab):
- Sampul: `1.jpg`
- Halaman 1 + halaman judul (kuning): `Picture.jpg` (dari repo lanjutan)
- Halaman 2–299: foto `Picture 001.jpg` s.d. `Picture 149.jpg`
  - Setiap foto memuat **2 halaman kitab** (sebaran buku terbuka): halaman kanan (genap) dulu, lalu halaman kiri (ganjil).
  - `Picture 001` = halaman 2–3, `Picture 002` = halaman 4–5, …, `Picture 099` = halaman 198–199.
- Repo lanjutan (asror-wa-khofiyyat) berisi `Picture 100.jpg` s.d. `Picture 149.jpg` + `Picture.jpg` — **sudah digabungkan ke repo ini** (foto 100–149 = halaman 200–299).

## Aturan terjemahan yang diterapkan
1. **100% dari awal sampai akhir** — setiap baris teks diterjemahkan, tidak ada yang diringkas.
2. **Format 3 bagian per paragraf**: [Arab asli] di atas → [Latin] di tengah → [Terjemahan Indonesia] di bawah (dalam bentuk tabel 3 baris).
3. **Rajah / Wafaq / Tabel / Angka mistik tidak ditranskripsikan** — disajikan sebagai gambar hasil crop presisi (folder `../images/rajah/`), dengan keterangan **"Gambar Rajah Asli Halaman X"** di bawahnya. Jika ada banyak rajah dalam satu halaman, dipisah: Rajah 1 (atas), Rajah 2 (bawah), dst.
4. **Istilah kunci hikmah** dibiarkan Arab + penjelasan dalam kurung (mis. *'azīmah* = sumpah/incantasi pengikat; *taḥwīj* = pengikat; *shuf'ah* = kertas amalan; *lubān dhakir* = kemenyan jantan; *jāwī* = kemenyan kayu jawa; *kuzbarah* = jintan).
5. Bahasa Indonesia **sederhana dan luwes**, bukan bahasa terjemahan kaku.
6. Dikerjakan **per 10 halaman** (1 file per batch).

## Penomoran
- "Halaman" = nomor halaman yang tercetak pada kitab (di bagian bawah halaman).
- Halaman 1 kitab tidak ada dalam pindaian (foto 001 dimulai dari halaman 2).
- Sampul (`1.jpg`) diterjemahkan terpisah sebagai bagian awal.

## Peta batch
| File | Halaman kitab | Foto sumber |
|---|---|---|
| `sampul.md` | Sampul | `1.jpg` |
| `halaman-001.md` | 1 (mukadimah + judul) | `Picture.jpg` |
| `halaman-002-011.md` | 2–11 | `Picture 001`–`005` |
| `halaman-012-021.md` | 12–21 | `Picture 006`–`010` |
| `halaman-022-031.md` | 22–31 | `Picture 011`–`015` |
| `halaman-032-041.md` | 32–41 | `Picture 016`–`020` |
| … | … | … |
| `halaman-290-299.md` | 290–299 | `Picture 145`–`149` |

## Progres
- ✅ Sampul (`sampul.md`)
- ✅ **Halaman 1 mukadimah** (`halaman-001.md`)
- ✅ **Batch 1: halaman 2–11** — selesai (bab 1: amalan maḥabbah, jalab, taḥwīj — ritual 1–9)
- ✅ **Batch 2: halaman 12–21** — selesai (ritual 10–16; 3 wafaq + tabel 8×8 + tabel angka 4×4)
- ✅ **Batch 3: halaman 22–31** — selesai (soal 17–25 + Bab Jalab Qawī; 8 rajah/wafaq)
- ✅ **Batch 4: halaman 32–41** — selesai (7 lembar ḥarīq, Bab Jalab al-Ḥaqq, ʿaqd nawm, ʿazīmah malaikat, maḥabbat ʿajābiyyah; 1 tajsm)
- ⏳ Batch 5 dst. — dikerjakan berurutan per 10 halaman

### Rajah/wafaq yang sudah di-crop
| Gambar | Halaman | Keterangan |
|---|---|---|
| `images/rajah/rajah-halaman-05-01.png` | 5 | Wafaq 4 baris + deretan "99" (untuk shuf'ah ritual ke-3) |
| `images/rajah/rajah-halaman-07-01.png` | 7 | Tabel *al-Ḫātim* (dituliskan pada 7 lembar) |
| `images/rajah/rajah-halaman-12-01.png` | 12 | Deretan wafaq 2 baris (ritual ke-10, ditulis di kertas putih) |
| `images/rajah/rajah-halaman-13-01.png` | 13 | Satu baris wafaq (shuf'ah ritual ke-11) |
| `images/rajah/rajah-halaman-14-01.png` | 14 | Empat baris ṭilasm (ritual ke-12, tinta kuku/rambut) |
| `images/rajah/rajah-halaman-16-01.png` | 16 | Tabel wafaq besar 8×8 huruf ("al-jadwāl") |
| `images/rajah/rajah-halaman-19-01.png` | 19 | Tabel wafaq angka 4×4 (al-Ḫātim yang diisyaratkan) |
| `images/rajah/rajah-halaman-22-01.png` | 22 | Wafaq 2 baris "ما بيطح / يبالاه" |
| `images/rajah/rajah-halaman-23-01.png` | 23 | Deretan wafaq 3 baris huruf-angka (untuk pelat timah) |
| `images/rajah/rajah-halaman-24-01.png` | 24 | Wafaq "كفحص وز بعدصمدك عمشكع / لعصه" (Rajah 1 atas, soal 18) |
| `images/rajah/rajah-halaman-24-02.png` | 24 | Wafaq "فطبت حطقي... / عمر طقمها... + deretan bulatan" (Rajah 2 bawah, soal 19) |
| `images/rajah/rajah-halaman-26-01.png` | 26 | Wafaq angka 4 baris berlabel lembar (soal 22, daun zaitun) |
| `images/rajah/rajah-halaman-27-01.png` | 27 | Rangkaian nama 4 baris yang ditulis pada telur (soal 23) |
| `images/rajah/rajah-halaman-27-02.png` | 27 | Wafaq "هذه الآية ٩٩٩..." + kolom angka (soal 24, mujarrab ṣarīḥ) |
| `images/rajah/rajah-halaman-28-01.png` | 28 | Wafaq 9 baris dengan potongan ayat (soal 25) |
| `images/rajah/rajah-halaman-41-01.png` | 41 | Tajsm figur manusia (angka + huruf) untuk maḥabbat ʿajābiyyah |

## ⚠️ Catatan akidah
Kitab ini berisi materi **sihir dan khurafat** yang bertentangan dengan akidah Islam (menjadikan jin/nama gaib sebagai sebab hajat, menyalahgunakan ayat Al-Qur'an untuk sihir, bersumpah kepada selain Allah). Terjemahan disajikan **utuh untuk keperluan akademik/studi tekstual** atas permintaan, dan tidak merestui pengamalan isi kitab ini.
