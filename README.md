# أسرار وخفايات في علم الروحانيات

Terjemah Indonesia atas naskah cetak **Syeikh ʿAṭiyyah ʿAbd al-Ḥamīd**.

## Sumber foto naskah

Folder `naskah/` diabaikan git (berkas besar). Salin dua ekstrak agar pembaca lembar-demi-lembar dan rajah di bawah tiap bab tampil:

1. Commit `cf70ec0142be5fcc5318566bb2a67bae8c10c8ae` — Picture 001–099 + `1.jpg` (kira-kira hlm. 1–195).
2. Repo [asror-wa-khofiyyat](https://github.com/fatimah86-dot/asror-wa-khofiyyat) @ `a8b761e48d66fa68b1676f9509012e33bf4624f9` — Picture 100–149 (hlm. 196–297, termasuk fihris).

```bash
git checkout cf70ec0142be5fcc5318566bb2a67bae8c10c8ae -- '*.jpg'
mkdir -p naskah
mv Picture\ *.jpg 1.jpg naskah/

git clone https://github.com/fatimah86-dot/asror-wa-khofiyyat.git /tmp/asror-next
git -C /tmp/asror-next checkout a8b761e48d66fa68b1676f9509012e33bf4624f9
cp /tmp/asror-next/*.jpg naskah/
```

Pemetaan kasar: Picture N ≈ hlm. 2N | 2N+1 (N≥2). Picture 149 ≈ hlm. 296–297.

## Membaca

```bash
python3 -m http.server 8080 --bind 0.0.0.0
```

Buka `index.html`. Setiap rajah diambil dari halaman naskah yang bersangkutan. Pager 150 lembar (Picture 001, 1.jpg, Picture 002–149).

## Unduh untuk dikoreksi

Halaman pratinjau: `unduh.html`.

```bash
python3 tools/buat-unduh.py
```

Menghasilkan (tidak di-commit, berkas besar):

- `unduh/Asrar-wa-Khafiyyat-edisi-lengkap.zip` — HTML + foto naskah 150 lembar
- `unduh/Asrar-wa-Khafiyyat-teks-koreksi.zip` — HTML + rajah yang dikutip saja
- `unduh/teks-koreksi.md` — teks polos untuk Word / Google Docs

## Fihris naskah (hlm. 296)

| Fasal | Isi | Halaman |
| --- | --- | --- |
| I | Jalb, tahyīj, mahabbah | 2–94 |
| II | Taṣrīf daʿwah jāmiʿah | 95–148 |
| III | Empat puluh ṭilasm | 149–176 |
| IV | Daʿwah rūḥāniyyah kubrā | 150–212 |
| V | Mandil | 213–228 |
| VI | Jalb zabūn, zawāj bāʾir, fakk ʿukūs | 229–238 |
| VII | Irsāl hātif | 239–251 |
| VIII | Awfāq | 252–291 |

## Batas terjemahan

Judul masʾalah, maksud, dan foto rajah diterjemahkan/ditampilkan.
Azimah jalb–tahyīj, rajah dalam makanan, ṭilasm sakit/gila, irsal taʿdhīb/ifsād, mandil istinzāl, manʿ safar/zawāj berdarah, dan menyembelih hewan untuk sihir **tidak** diturunkan sebagai petunjuk praktis.
