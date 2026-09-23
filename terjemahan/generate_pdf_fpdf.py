#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF versi hanya PDF - Batc 01-02 (Hal 001-011) dengan format 2 tingkat Arab-Indonesia + Rajah HQ
Uses fpdf2 + Amiri font + arabic_reshaper + bidi
"""
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import pathlib

# Paths
BASE = pathlib.Path("/home/user/asoro-wa-khofiyyat-fi-ilmu-ruhaniyyah/terjemahan")
# Fallback to DejaVu if Amiri missing (tmp cleanup) — DejaVu still renders Arabic (less calligraphic)
import os
_amiri_reg = "/tmp/amiri/fonts/Amiri-Regular.ttf"
_amiri_bold = "/tmp/amiri/fonts/Amiri-Bold.ttf"
AMIRI_REG = _amiri_reg if os.path.exists(_amiri_reg) else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
AMIRI_BOLD = _amiri_bold if os.path.exists(_amiri_bold) else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RAJAH_05 = str(BASE / "assets/rajah-hal-005-wafaq-tehij.jpg")
RAJAH_07 = str(BASE / "assets/rajah-hal-007-khatam-7waraq.jpg")
RAJAH_12 = str(BASE / "assets/rajah-hal-012-thilasm-final.jpg")
RAJAH_13 = str(BASE / "assets/rajah-hal-013-thilasm-final.jpg")
RAJAH_14 = str(BASE / "assets/rajah-hal-014-tilasm-final.jpg")
RAJAH_16 = str(BASE / "assets/rajah-hal-016-khatam-besar.jpg")
RAJAH_19 = str(BASE / "assets/rajah-hal-019-khatam-4x4.jpg")
RAJAH_23 = str(BASE / "assets/rajah-hal-023-inscription.jpg")
RAJAH_24T = str(BASE / "assets/rajah-hal-024-top-thilasm.jpg")
RAJAH_24B = str(BASE / "assets/rajah-hal-024-bottom-thilasm.jpg")
RAJAH_26 = str(BASE / "assets/rajah-hal-026-waraq-7numbers.jpg")
RAJAH_27 = str(BASE / "assets/rajah-hal-027-thilasm-baidah.jpg")
RAJAH_28 = str(BASE / "assets/rajah-hal-028-thilasm-ah-hah.jpg")
RAJAH_41 = str(BASE / "assets/rajah-hal-041-figures-mahabbah.jpg")
RAJAH_48T = str(BASE / "assets/rajah-hal-048-top-thilasm.jpg")
RAJAH_48B = str(BASE / "assets/rajah-hal-048-bottom-jadwal.jpg")
RAJAH_49T = str(BASE / "assets/rajah-hal-049-top-thilasm.jpg")
RAJAH_49B = str(BASE / "assets/rajah-hal-049-bottom-thilasm.jpg")
RAJAH_51W = str(BASE / "assets/rajah-hal-051-wafaq-murabba.jpg")
RAJAH_51B = str(BASE / "assets/rajah-hal-051-bottom-thilasm.jpg")
RAJAH_52 = str(BASE / "assets/rajah-hal-052-thilasm.jpg")
RAJAH_53 = str(BASE / "assets/rajah-hal-053-wafaq-diamond.jpg")
RAJAH_54 = str(BASE / "assets/rajah-hal-054-lion-sun.jpg")
RAJAH_55 = str(BASE / "assets/rajah-hal-055-mizan-table.jpg")
RAJAH_56T = str(BASE / "assets/rajah-hal-056-top-grid.jpg")
RAJAH_56B = str(BASE / "assets/rajah-hal-056-star-wafaq.jpg")
RAJAH_57 = str(BASE / "assets/rajah-hal-057-couple-wafaq.jpg")
RAJAH_58 = str(BASE / "assets/rajah-hal-058-couple-sitting.jpg")
RAJAH_59 = str(BASE / "assets/rajah-hal-059-face-bust.jpg")
RAJAH_60 = str(BASE / "assets/rajah-hal-060-script-shabaz.jpg")
RAJAH_61 = str(BASE / "assets/rajah-hal-061-face-torso.jpg")
RAJAH_62 = str(BASE / "assets/rajah-hal-062-shabaz-pair.jpg")
RAJAH_63 = str(BASE / "assets/rajah-hal-063-top-thilasm.jpg")
RAJAH_64 = str(BASE / "assets/rajah-hal-064-wafaq-top.jpg")
RAJAH_65T = str(BASE / "assets/rajah-hal-065-top-figures.jpg")
RAJAH_65B = str(BASE / "assets/rajah-hal-065-bottom-wafaqs.jpg")
RAJAH_66T = str(BASE / "assets/rajah-hal-066-top-thilasm.jpg")
RAJAH_66M = str(BASE / "assets/rajah-hal-066-script-jar.jpg")
PDF_OUT = str(BASE / "Asrar-wa-Khofayyat-Terjemahan-Lengkap-B01-B13.pdf")
PDF_FULL = str(BASE / "Asrar-wa-Khofayyat-Terjemahan-Lengkap-FULL.pdf")  # same for now, will be updated

def ar(text):
    # reshape + bidi for Arabic
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('DejaVu', 'I', 7)
        self.set_text_color(120,120,120)
        self.cell(0, 6, 'كتاب أسرار و خفايات في علم الروحانيات - Terjemahan Lengkap Indonesia (Batch 01-13)', align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200,200,200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font('DejaVu', '', 7)
        self.set_text_color(120,120,120)
        self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_font('Amiri', '', AMIRI_REG)
pdf.add_font('Amiri', 'B', AMIRI_BOLD)
pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
pdf.add_font('DejaVu', 'I', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
# Hack: map I to regular since italic file not needed for test

# Helvetica is built-in

# Helper functions
def add_label(text):
    pdf.set_font('DejaVu', 'B', 7)
    pdf.set_text_color(100,116,139)
    # uppercase label
    pdf.cell(0, 4, text.upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0,0,0)

def add_arabic_block(text, size=11, bold=False):
    pdf.set_font('Amiri', 'B' if bold else '', size)
    # Use multi_cell for wrapping, align R
    # Need to handle reshaping per line? fpdf will wrap reshaped text correctly if we reshape whole paragraph?
    # Reshape whole text then multi_cell
    reshaped = ar(text)
    # Use multi_cell with align R
    pdf.multi_cell(0, 6, reshaped, align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def add_indo_block(text, size=9, bold=False, italic=False):
    # For mixed styling, we use Helvetica
    style = ''
    if bold: style += 'B'
    if italic: style += 'I'
    # Use Helvetica family; for bold+italic, need to handle
    if style == '':
        pdf.set_font('DejaVu', '', size)
    elif style == 'B':
        pdf.set_font('DejaVu', 'B', size)
    elif style == 'I':
        pdf.set_font('DejaVu', 'I', size)
    elif style == 'BI':
        pdf.set_font('DejaVu', 'BI', size)
    else:
        pdf.set_font('DejaVu', '', size)
    pdf.multi_cell(0, 5, text, align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def add_block_box(label, arab_text, indo_text, arab_size=11):
    # Draw a box around the block
    x = pdf.get_x()
    y = pdf.get_y()
    # Estimate height: we will draw after content using rect
    # Instead use a cell with border
    # Simpler: add label, arab, indo inside a bordered rect via multi_cell with border?
    # We'll just add content without box but with light background
    # Use a filled rect approach: draw after
    start_y = pdf.get_y()
    add_label(label)
    if arab_text:
        add_arabic_block(arab_text, size=arab_size)
    if indo_text:
        # add small label for indo
        pdf.set_font('DejaVu', 'B', 7)
        pdf.set_text_color(100,116,139)
        pdf.cell(0, 3, '[TERJEMAHAN INDONESIA]', new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0,0,0)
        add_indo_block(indo_text, size=9)
    end_y = pdf.get_y()
    # Draw border around block
    pdf.set_draw_color(226,232,240)
    pdf.set_line_width(0.3)
    # Use rect with start_y
    # Need to handle page break: if block spans pages, rect will be broken – skip for multi-page blocks
    # For simplicity, skip border if height > 0 and not too large, just draw light
    # We'll draw a rounded rect effect via line
    # For now, just add a light separator
    pdf.set_draw_color(226,232,240)
    pdf.line(pdf.l_margin, end_y, pdf.w - pdf.r_margin, end_y)
    pdf.ln(2)

def add_rajah(image_path, caption, details):
    # Check if need page break
    if pdf.get_y() > 240:
        pdf.add_page()
    pdf.set_font('DejaVu', 'B', 8)
    pdf.set_text_color(15,23,42)
    pdf.cell(0, 5, 'GAMBAR RAJAH ASLI - ' + caption.upper(), align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    # Image
    # Calculate width to fit page
    page_w = pdf.w - pdf.l_margin - pdf.r_margin
    # Reserve height
    # Use image with w=page_w*0.9, centered
    img_w = page_w * 0.85
    x = (pdf.w - img_w)/2
    y = pdf.get_y()
    # Check if image exists
    try:
        pdf.image(image_path, x=x, y=y, w=img_w)
        # Get image height to move cursor
        # FPDF doesn't return height, estimate via PIL
        from PIL import Image
        with Image.open(image_path) as im:
            iw, ih = im.size
            img_h = (img_w * ih) / iw
        pdf.set_y(y + img_h + 3)
    except Exception as e:
        pdf.set_font('DejaVu', '', 8)
        pdf.cell(0, 6, f'[Gagal load gambar: {e}]', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('DejaVu', 'I', 7)
    pdf.set_text_color(100,116,139)
    pdf.multi_cell(0, 4, details, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0,0,0)
    pdf.ln(2)

# --- BUILD PDF ---
pdf.add_page()

# COVER
pdf.set_font('Amiri', 'B', 18)
pdf.set_text_color(124,45,18)
pdf.multi_cell(0, 9, ar("كتاب"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Amiri', 'B', 22)
pdf.multi_cell(0, 10, ar("أسرار و خفايات في علم الروحانيات"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Amiri', '', 11)
pdf.multi_cell(0, 7, ar("تأليف وجميع"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Amiri', 'B', 14)
pdf.multi_cell(0, 8, ar("شيخ الروحانيين"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Amiri', 'B', 12)
pdf.multi_cell(0, 8, ar("الشيخ عطية عبد الحميد"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Amiri', '', 9)
pdf.multi_cell(0, 6, ar("قدس الله سره"), align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_font('DejaVu', 'B', 14)
pdf.set_text_color(124,45,18)
pdf.cell(0, 8, 'ASRAR WA KHOFAYYAT', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 10)
pdf.set_text_color(71,85,105)
pdf.cell(0, 6, 'FI ILMI RUHANIYYAT - Terjemahan Lengkap 100% Arab -> Indonesia', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 8)
pdf.cell(0, 6, 'Format 2 Tingkat: [Teks Arab Asli] di atas - [Terjemahan Indonesia] di bawah', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 5, 'Batch 01–13 (Halaman 001–066) • Versi PDF • 23 Sep 2026', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_draw_color(124,45,18)
pdf.set_line_width(0.5)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
pdf.ln(4)

# CAUTION BOX
pdf.set_fill_color(254,242,242)
pdf.set_draw_color(252,165,165)
pdf.set_line_width(0.3)
x = pdf.l_margin
y = pdf.get_y()
w = pdf.w - pdf.l_margin - pdf.r_margin
# We'll use multi_cell with fill
pdf.set_xy(x, y)
pdf.set_font('DejaVu', 'B', 7)
pdf.set_text_color(127,29,29)
pdf.cell(w, 5, '  PERINGATAN ETIS & HUKUM - WAJIB DIBACA', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 7)
pdf.set_text_color(127,29,29)
pdf.set_fill_color(254,242,242)
pdf.multi_cell(w, 4, 'Kitab ini berisi kepercayaan tradisional ilmu hikmah. Terjemahan disajikan 100% untuk studi akademik & pelestarian naskah, BUKAN anjuran praktik. Banyak amalan menarget orang tanpa izin - dalam etika modern termasuk manipulasi/pemaksaan yang bertentangan dengan norma agama & hukum. Tidak ada bukti ilmiah atas khasiat supranatural. Jangan gunakan untuk merugikan orang lain.', border=1, fill=True, align='L', new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)

# TOC
pdf.set_font('DejaVu', 'B', 11)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'Daftar Isi - Batch 01–13', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 8)
pdf.set_text_color(15,23,42)
pdf.multi_cell(0, 4.5,
'Batch 01 (001–005): Cover, Fasal 1 Alfah 20 daun + 72x + Syaqfah + Rajah05\n'
'Batch 02 (006–011): 7 lembar + Khatam7 Hal07 + 400x Humazah + Maimun + Harut + Mahmala\n'
'Batch 03 (012–016): Susi Rajah13 + Qallama Rajah14 + Sulaiman\n'
'Batch 04 (016–021): Khatam 8x8-19 + Fatihah + 7 kertas\n'
'Batch 05 (022–026): Faras + timah21 Rajah23 + darah kaki 2x Rajah24 + 7 zaitun Rajah26\n'
'Batch 06 (027–031): Telur Rajah27 + Rajah28 + Syam`atain + 2figur Jim + Wafaq693\n'
'Batch 07 (032–036): Wafaq693 HurufNur + 7 barwat + RujuZauj + Irsal Haq70x + AqdNaum71x\n'
'Batch 08 (037–041): Ta`qid Naum 7 kerikil Hal36 + Fatihah malaikat Hal37 + Yaqutah Tsaminah Hal38-41 + Ghazal 21x Barhat + Mahabbah 3 rambut 131x Hal41 (1 Rajah)\n'
'Batch 09 (042–046): Qomash71x Jin+Zalzalah Hal42 + Ya Dauuh21x+Khatam28x Hal43 + Shurah ALQAYTU Hal44+Lilin100 + Shulh Ayat+ Tahyij12x Hal45 + LilinLebah Hal46+ Sari104x (0 Rajah)\n'
'Batch 10 (047–051): Ihraq Laymun Hal47 + Thilasm7Gula+ Paku4Mulk Hal48(2) + Qawiyy Misrajah Hal49(2) + Yasin Tadhyiq Hal50 + Wafaq Yasin Hal51(2) — 6 Rajah baru — total 20\n'
'Batch 11 (052–056): Thilasm Ahmar 49x Hal52 + HarfHa Diamond Hal53 + Lion-Sun Hal54 + Mizan Yusuf Hal55 + Star Wafaq Rahman Hal56(2) — 6 Rajah baru — total 26\n'
'Batch 12 (057–061): Zawjain Couple Hal57 + Ruh Sitting Hal58 + Qawathi Yasin Hal59 + Shabaz Script Hal60 + 2 Shabaz Face Hal61 — 5 Rajah baru — total 31\n'
'Batch 13 (062–066): Hadid 4H + Hawa Hu + Turab Jinn21x Hal63 + Fatilah Mirrikh11x Hal64 + 2Figur & 2Wafaq Barhat11x Hal65 + Qarurah Nar35x Hal66 + Baidah — 7 Rajah baru — total 38\n'
'Batch 14–30 (067–~150) - menyusul per 5 hal., PDF FULL auto', new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- HAL 01 COVER already done, now detailed per page ---
pdf.add_page()
pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 01 - COVER / SAMPUL', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "كتاب\nأسرار و خفايات في علم الروحانيات\nتأليف وجميع\nشيخ الروحانيين\nالشيخ عطية عبد الحميد\nقدس الله سره", "KITAB ASRAR WA KHOFAYYAT FI ILMI RUHANIYYAT (Rahasia-Rahasia dan Hal-Hal Tersembunyi dalam Ilmu Keruhanian)\nKarya dan Kompilasi Syaikh Ar-Ruhaniyyin Syaikh Athiyah Abdul Hamid - Qaddasallahu sirrahu (semoga Allah mensucikan rahasianya).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 02 - Pembuka Fasal Pertama', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "الفصل الأول\nفى\nأعمل المحبة والجلب والتهييج", "FASAL PERTAMA - TENTANG AMAL-AMAL MAHABBAH, JALB, DAN TAHYIJ\nMahabbah=menumbuhkan kasih, Jalb=menarik/mendatangkan, Tahyij=membangkitkan gejolak rindu.")
add_block_box('Teks Arab Asli - Daftar Terbitan', "من اصدارات شيخ الروحانيين الشيخ عطية عبد الحميد في المكتبات\nمجلة السهم الصائب في تنقية العلوم الروحانية من الشوائب\nمجلة الدعوات الروحانية في حل الارصاد الفلكية خاص بعلم الكنوز\nكتاب الابراج اكتشف اسرار من تريد\nكتاب عجائب وفوائد النباتات والحيوانات وخواصهم الروحانية\nكتاب الصولجان في الاستلام على بنات الجان\nكتاب زجرات ميططرون في الاقسام الحاكمة على قبائل الجان\nكتاب تصريف دعوة البرهتية الثلاثية الروحانية والارضية والسفلية\nكتاب حكمة الحكماء في علم السماء والكيمياء\nكتاب الاستدلال علي الضمائر الخفية بالقوانين الحرفية\nكتاب سر الاسرار في التواصل مع روحانيات القرآن\nكتاب أسرار و خفايات في علم الروحانيات\nشيخ الروحانيين في الوطن العربي الشيخ عطية عبد الحميد 00201062022238", "Daftar terbitan penulis (12 judul) - Terjemahan lengkap di Markdown. Barhatiyyah (برهتية) adalah rangkaian asma kunci hikmah, dibiarkan Arab.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 03 - Mas-alah 1 & 2', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 1 Bab Alfah', "تأخذ على بركة الله تعالى عشرين ورقة من ورق الليمون المالح ثم تكتب على الأولى طلل وعلى الثانية ملل وعلى الثالثة أفش وعلى الرابعة فجش وعلى الخامسة هلش وعلى السادسة داش وعلى السابعة أبراس وعلى الثامنة أثراش وعلى التاسعة طيوخ وعلى العاشرة تماسية - ثم تكتب العشرة الباقية . أمنى تكتب على كل واحدة منهم (حمداني في باب الكلب خميري) وتأخذ المرأة ورقتين في كل يوم وتمحيها في ماء وسكر وتشرب حتى تنتهي العشرين ورقة في عشرة أيام فإن الرجل يحبها حباً شديداً . فصل - وإن كان الكره من المرأة فإن الرجل يأخذ العشرين ورقة المذكورين ويمحي ورقتين في ماء ويدهن به فإن المرأة تحبه حباً شديداً وهو من المجربات.", "Ambil dengan berkah Allah 20 lembar daun lemon asin. Tulis: 1) Thalal (طلل), 2) Malal (ملل), 3) Afsy (أفش), 4) Fajasy (فجش), 5) Halasy (هلش), 6) Dasy (داش), 7) Abras (أبراس), 8) Atrasy (أثراش), 9) Thuyukh (طيوخ), 10) Tamasiah (تماسية). Sepuluh lembar sisanya masing-masing tulis “Hamdani fi babi al-kalb Khumairi” (حمداني في باب الكلب خميري).\nCara pakai: Jika istri ingin suami lebih cinta -> lebur 2 lembar/hari ke air bergula & diminum, habis 10 hari. Jika istri yang menjauh -> suami melebur 2 lembar/hari ke air lalu diusapkan ke badan. Kata naskah: mujarrabat (teruji menurut penulis).")

add_block_box('Teks Arab Asli - Mas-alah 2 Bab Mahabbah Tahyij Halus', "ليس له نظير وليس له وقت معين إذا قرأت وإذا كتبت وهو يكتب على شريط من أثر المطلوب أو على ملبوس ملبسه أو على مأكول ويأكله أو على مشروب ويشربه أو على مشموم ويشمه والعدد ٧٢ مرة والبخور لبان ذكر وكزبرة وجاوي . في سعد القمر . وهذا ما تكتب ويه تعزم .", "Tidak ada bandingannya & tidak terikat waktu. Ditulis di pita/atsar, pakaiannya, makanan/minuman/wewangian yang akan ia pakai - 72 kali. Bukhur: luban dzakar, ketumbar, jawi. Waktu: saat bulan di posisi sa’d (baik). Lafaz azimah bersambung hal. 4.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 04 - Azimah Mas-alah 2 & Mas-alah 3', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Azimah', "الله أكبر عددا. خطفت قلب فلانة بنت فلانة إلى فلان ابن فلانة بالسحر والزلزلة وميليتها وسجنتيها ووضعت فيه محبة فلان ابن فلانة حتى لا تغفل ولا تنام عن محبة فلان ابن فلانة درجة واحدة إلا قلقانة ولهانة حيرانة بالنار والنيران والوهيج والغليان مرج البحرين يلتقيان بشماشم عددا شماشم عددا سميم عددا شموم عدد طحوم عدد عموم عدد ملجوم عدد علجوم عدد أبروم عدد ٢ حيوم غد ٢ قيوم غد ٢ ديوم ٢ سبحان من بذكره تطمئن القلوب ويعلم خائنة الأعين وما تخفي الصدور وأصحاب الشمال ما أصحاب الشمال في سموم وحميم وظل من يحموم لا بارد ولا كريم حتى تأتي فلانة بنت فلانة إلى فلان ابن فلانة فرحانة مسرورة ضاحكة مستبشرة أجب وتوكل يا وسواس وياخناس والبس فلانة بنت فلانة من القدم إلى الرأس وحرك طبعها وقلبها بالوسواس الخناس لا تنفك محبة فلان ابن فلانة من قلب فلانة بنت فلانة حتى يغفر لها بالفأس سنستدرجهم من حيث لا يعلمون ها هي هاجت ومن عوائد السحر ما خابت.", "Allahu Akbar beberapa kali. “Aku telah menyambar hati si Fulanah binti Fulanah menuju si Fulan bin Fulanah dengan sihir... (asma Bisyamasyim, Syamasyim, Samim... Hayyum-Ghad 2, Qayyum-Ghad 2, Dayyum 2, kutipan Marajal Bahrain, Wa Ashhabus Syimal, dll.) ... sehingga datang gembira - Jawablah wahai Waswas & Khannas, pakaikan dari kaki ke kepala, jangan lepas cinta...” (Lengkap di Markdown; semua asma dibiarkan Arab).")

add_block_box('Teks Arab Asli - Mas-alah 3 Bab Tahyij', "المسألة الثالثة باب تهييج يكتب على شقفة نية يوم الثلاثاء عند طلوع الشمس وتوضعها في نار دائمة الوقود وتعزم عليها ٢١ مرة والبخور مطلوق وهو صندل أحمر وسندروس ولبان ذكر وجاوي وهو مجرب لا شك فيه وإياك والحرام .", "Mas-alah 3 - Tahyij di Syaqfah: Tulis di pecahan kendi mentah hari Selasa terbit matahari, letak di api terus menyala, baca 21x. Bukhur: cendana merah, sandarus, luban dzakar, jawi. “Mujarrab - tapi jangan untuk haram.”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 05 - Rajah Wafaq Tahyij & Azimah', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Pengantar Rajah', "وهذا ما تكتب على الشقفة كما ترى فانهم ترشد", "“Dan inilah yang engkau tulis di atas pecahan tembikar sebagaimana engkau lihat.”")
add_rajah(RAJAH_05, "Halaman 05 - Wafaq Tahyij", "Wafaq 4 baris + simbol vertikal kiri + thilasm horizontal bawah. Tidak diterjemahkan, tidak digambar ulang. Crop presisi 2916×1372 px, putih bersih, 4x upscale, siap cetak. Media: syaqfah nayyah, waktu Selasa terbit matahari, di api 21x, bukhur cendana merah, sandarus, luban, jawi.")
add_block_box('Teks Arab Asli - Azimah setelah Rajah', "وهذه العزيمة تقول أقسمت عليكم أيتها الأرواح الروحانية بالنار والنور والظل والحرور بعلشاقش عدد ٢ مهراقش عدد ٢ بمن أنزل الأمطار ومجري الأنهار ونور الشمس والقمر وأحيا بأمره كل ميت وأرسى الجبال رواسي الذي تجلى للجبل فجعله دكاً وخر موسى صعقاً إلا ما هيجتم وأطلقتم النار في قلب فلانة إلى محبة فلان الوحا ٢ العجل ٢ الساعة ٢ إن كانت إلا صيحة واحدة فإذا هم جميع لدينا محضرون.", "“Aku bersumpah kepada arwah ruhaniyyah, demi api-cahaya-naungan-panas, demi Ba‘lasyaqisy 2x & Mahraqisy 2x, demi Yang menurunkan hujan... yang menampakkan diri ke gunung lalu hancur dan Musa pingsan - kecuali kalian telah membangkitkan api (rindu) di hati Fulanah untuk Fulan - Al-Waha 2, Al-‘Ajal 2, As-Sa’ah 2 - ‘in kanat illa shaihataw wahidatan...’ (QS Yasin:53).”")

add_block_box('Teks Arab Asli - Mas-alah 4', "المسألة الرابعة باب آخر مثله وهو أن تكتب الوفق الآتي وتوكل بما تريد في سبع أوراق", "Mas-alah 4 - Bab Lain yang Serupa: Tulis wafaq berikutnya dan wakilkan sesuai hajat pada 7 lembar. (Wafaq di hal. 6–7)")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 06 - Lanjutan Mas-alah 4 (7 Lembar) - Picture 003 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "وتجعل في كل ورقة عدد ٢ حبات لبان ذكر وثلاث عدد ٢ حبات كزبرة وتجعلها على النار حتى يفرغ دخانها إلى آخر السبعة تكمل القراءة عدد ٢١ مرة. وهذه العزيمة بسم الله العظيم مجرى البحار والأنهار ومكون الليل والنهار وهو السميع العليم أقسمت عليكم يا معاشر الجن والشياطين والمردة والوساوسة والتوابعة من بني شمراخ وبني وقاض وبني كماخ من قام منكم وقعد وعلى الخلائق تمرد وفي الطريق بعد ورصد بقول الله هو الله أحد الله الصمد لم يلد ولم يولد ولم يكن له كفواً أحد ليس كمثله شيء وهو السميع البصير اقبلوا من كل فج عميق إلى فلان ابن فلانة إن كان نائماً فأيقظوه وإن كان يقظاناً فأوقفوه وعلى خيولكم فركبوه وافتحوا له الباب واكسروا له الأقفال والأغلال ومشوه على جمر النيران وهيجوه واجلبوه إلى فلانة بنت فلانة تريكلوا يا معشر العمار والملوك العلوية والسفلية والأرضية والسحابية والغمامية والمستمرون في الهوا أجيبوا من معاشر الأرض ومغاربها هيجوا واجلبوه إلى فلانة أين ذهب أين شمراخ أين طيكل أجيبوا بقدرة من يحيي العظام وهي رميم أقسمت عليكم بانسماء وما أظلت والأرض وما أقلت والرياح وما لفحت والمياه وما جرت ارعدوا وازجروا وزلزلوا وانزلوا على فلان ابن فلانة وهيجوه واجلبوه إلى فلانة بنت فلانة بحق اهيا شراهيا أذرناي اصباؤوت ال شداي ما أعظم سلطان الله الوحا العجل الساعة هيا يا خدام هذه الأسماء لا يعصى منكم كبير ولا صغير ولا ملك ولا مملوك إن كل من في السماوات والأرض إلا آتي الرحمن عبداً السماء بكم تنقذف والأرض من تحت أقدامكم تشعل ناراً حتى تأتوا بفلان إلى محبة فلانة إن كانت إلا صيحة واحدة فإذا هم جميع لدينا محضرون.", "Jadikan di tiap lembar 2 butir luban + 6 butir ketumbar, bakar sampai habis sampai lembar ke-7, baca 21x. Azimah panjang: sumpah kepada Jin, Syaitan, Maradah, Waswasah, Tawabi’ Bani Syamrakh, Waqadh, Kamakh dengan Qul Huwallahu Ahad & Laisa kamitslihi syai-un, datang dari tiap lembah, bangunkan/tahan, naikkan ke kuda, buka pintu, pecah gembok, jalankan di bara api, Trikal, wahai Ammar & Raja Ulwiyyah/Sufliyyah/Ardhiyyah/Sahabiyyah/Ghamamiyyah... Di mana Dzahab? Syamrakh? Thaykal? Dengan kuasa Yang menghidupkan tulang, demi langit-bumi-angin-air, gemuruhkan, guncang, turunkan kepada Fulan... dengan hak Ahya Syarahya Adranai, Ashba-ut Al Syaddai, Al-Waha Al-‘Ajal As-Sa’ah...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 07 - Khatam 7 Waraq & Mas-alah 5 - Picture 003 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "وهذا الخاتم الذي يكتب في ٧ أوراق", "Dan inilah Khatam yang ditulis pada 7 lembar.")
add_rajah(RAJAH_07, "Halaman 07 - Khatam 7 Waraq", "Tabel 3x3 angka 9 2 ع / 3 5 7 / 8 1 6 + اهطل x4 kanan, فشنت x4 kiri, ekor bertitik bawah. HANYA kotak, tanpa teks sekitar, 2404x1244 px, putih bersih, 4x.")
add_block_box('Teks Arab Asli', "وإن كتبت العزيمة المذكورة في ورقتين ويبخرنهم ويحمل واحدة الطالب والأخرى تعلق في الهواء فإن المطلوب يحضر. المسألة الخامسة باب تهييج لحضور يتلى عدد ٤٠٠ مرة بعد صلاة العشاء والبخور كزبرة فإن الخادم يأتيك بعد عدد ٣٠٠ مرة وينفخ حتى تنتهي من العدة واضحاً يده على صدره فبعد فراغك يقول سريعاً ما تريد فاطلب منه حاجتك وهذا ما تقول: أجب يا عنقود بحق الأيمان والعهود والدوايب والسود وبحق الأيمان المنزلة على اليهود وبحق الاسم الذي تفجر منه الماء من الحجر الجلمود وهو قاني لكنوت اكوت", "Jika azimah tadi ditulis di 2 lembar, diasapi, satu dibawa pencari & satu digantung di udara -> target hadir.\nMas-alah 5 - Tahyij Hudhur: Dibaca 400x setelah Isya, bukhur ketumbar. Khadam datang setelah 300x, meniup sampai selesai 400x, tangan di dada, lalu berkata “apa yang kau mau?” - Jawab: “Ya ‘Unqud, dengan hak Aiman & ‘Uhud, Dawabib & Sud, sumpah kepada Yahudi, dan Nama yang memancarkan air dari batu keras - Qani Lakanut Akut.”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 08 - Mas-alah 5 (Humazah) - Picture 004 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 5 Humazah', "المسألة الخامسة باب محجة تكتب سورة الهمزة على شمعة اسكندراني بتمامها باسم من تريد ثم توقدها وتبخرها بجاوي ولبان وعود قاقلي واتل العزيمة عليها فما تفرغ إلا والمطلوب يأتي سريعاً. وهذه العزيمة تقول - بانقش عدد ٢ ياجلجميش عدد ٢ ياجلجميش عدد ٢ هويش عدد ٢ مهراقش مهورقش عجل أيها الملك جرنوش أجلب وهيج فلان ابن فلانة إلى فلانة بنت فلانة بالذي قال للسموات والأرض اتينا طوعاً أو كرهاً قالتا أتينا طائعين بحق ويل لكل همزة لمزة الذي جمع مالاً وعدده أيحسب أن ماله أخلده كلا لينبذن في الحطمة وما أدراك ما الحطمة نار الله الموقدة في قلب فلانة بنت فلانة التي تطلع على الأفئدة إنها عليهم مؤصدة في عمد ممددة.", "Mas-alah 5 Humazah: Tulis Surat Al-Humazah lengkap di lilin Iskandari dengan nama target, nyalakan & asapi jawi+luban+qaquli, baca azimah -> target datang cepat. Azimah: “Banqasy 2x, Ya Jaljamyisy 2x, Huwaisy 2x, Mahraqisy Mahuraqisy - Wahai Raja Jarnusy, tarik & gelisahkan Fulan bin Fulanah ke Fulanah binti Fulanah, dengan Yang berfirman kepada langit-bumi ‘i’tiya thau’an au karhan...’ & hak ‘Wailul likulli humazah... Narullahil muqadah fi qalbi Fulanah...’ (Al-Humazah 1–9).”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 09 - Mas-alah 7 & 8 - Picture 004 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 7', "المسألة السابعة باب محبة يكتب يوم الأربع وتعـلقه على شجرة شرقية ويخره لبان ذكر وهذا ما تكتب وبه تعزم تقول: أن لا ملجأ من الله إلا إليه وحيل بينهم وبين ما يشتهون فضرب بينهم بسور له باب باطنه فيه الرحمة وظاهره من قبله العذاب توكل يا ميمون الطيار ويا ميمون أبي نوخ واضربوا بأيديكم العملة الغوية فلان على صوره وترهـموا عقله بهوتر عدد ٢ كرش عدد ٢ لوش عدد ٢ نفخ عدد ٢ أنا عدد ٢ أجب أيها السيد أنا واحـضروا وازعجوا فلان واحرقوا قلبه بمحبة فلانة الرحا عدد ٢ العجل عدد ٢ الساعة عدد ٢.", "Mas-alah 7 - Mahabbah Rabu pohon timur: Tulis hari Rabu, gantung di pohon menghadap timur, bukhur luban. Tulis & azimah: “La malja-a minallah... fasuriba bainahum bi sur... (Quran), tawakkal Maimun Thayyar & Maimun Abi Nukh, pukul patung Fulan, hilangkan akal dengan Bahutar 2x, Karasy 2x, Lusy 2x, Nafakh 2x, Ana 2x - Ya Sayyid Ana hadirkan, ganggu & bakar hati Fulan dengan cinta Fulanah - Ar-Raha 2, Al-‘Ajal 2, As-Sa’ah 2.”")

add_block_box('Teks Arab Asli - Mas-alah 8', "المسألة الثامنة باب محبة يكتب على أثر من تريد أو على بغنة هندي وهذا ما تكتب أجب يا عبد النار ويا هارش ويا احمر ويا سريع ويا برق ويا أجيبوا وأعطوها وازعجوا واحرقوا وأقلقوا قلب فلان ابن فلانة بمحبة فلانة حتى لا يأكل ولا يشرب ولا ينام حتى يأتي إلى فلانة بنت فلانة طلاعاً ذليلاً الوحا عدد ٢ العجل عدد ٢ الساعة عدد ٢ ثم اجعلهم في سراج أخضر جديد وتأخذ ماجورا وتكتب في قعره هاروت وماروت وميمون افراطيش بشماهوج أجيبوا أيها الخدام واحضروا", "Mas-alah 8 - Mahabbah atsar/sutra India: Tulis di bekas atau sutra India: “Ya ‘Abdan Nar, Harisy, Ahmar, Sari’, Barq - jawablah, ganggu, bakar, gelisahkan hati Fulan bin Fulanah dengan cinta Fulanah sampai tak bisa makan/minum/tidur sampai datang tunduk - Al-Waha 2, Al-‘Ajal 2, As-Sa’ah 2. Masukkan ke lampu hijau baru, tulis di dasar bejana Harut-Marut & Maimun Afrathisy Basyamahuj - wahai khadam hadirkan...” (bersambung hal. 10).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 10–11 - Lanjutan Mas-alah 8 & Mas-alah 9 - Picture 005', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Lanjutan bejana', "وماروت وميمون افراطيش بشماهوج أجيبوا أيها الخدام واحضروا بفلان إلى مكان فلانة العجل الوحا الساعة بحق اهطمفشذ أسرعوا به ثم اكفي الماجور على الموقود ثم تعزم عليها بهذه العزيمة عدد ٣١ مرة على مهلك وإن كان عدد اسم المطلوب كان أخرى. المسألة التاسعة باب محبة وجلب يكتب على أثر المطلوب أو على خرقة كتان جديدة وتوقده في سراج جديد بدهن ياسمين ليلة الثلاثاء . وهذا ما تكتب على الأثر محـملع همـعلسعطـلمم مـمعلـسعطلمـمـسلح سلسكلسمـكا مسـلفمـلي لحـمين لهـوسـا عوسـا والنجـمل ناهـويا العجل بكذا توكل بجلب فلان إلى فلانة بحق هذه الأسماء عليكم والبخور مقل أزرق وكندر وسنكي.", "“...Harut-Marut & Maimun Afrathisy Basyamahuj - hadirkan Fulan ke tempat Fulanah - Al-‘Ajal Al-Waha As-Sa’ah dengan hak Ahtamfasyadz - segeralah! Balikkan bejana di atas tungku, baca 31x pelan, jika hitungan nama target ada maka ulangi.”\nMas-alah 9 - Mahabbah Jalb: Tulis di bekas atau kain linen baru, bakar di lampu baru minyak Yasamin malam Selasa. Tulis di atsar: “Mahmala‘ Ham‘alsa‘thalamam... Salsakalsamaka... Lahmin Lahawsa ‘Awsa wan Najm Nahu-ya - Al-‘Ajal, wakilkan tarik Fulan ke Fulanah dengan hak asma ini.” Bukhur: muqul azraq, kundur, sanki.")

add_block_box('Teks Arab Asli - Azimah Mas-alah 9 (1)', "وهذه العزيمة الحمد لله الذي كان قبل وجود المخلوقات الذي خلق بنوره الظلمات وعلم ما كان وما يكون وما هو كائن لاإله إلا هو الملك المعبود يخرج الأشياء من العدم إلى الوجود فسبحان الذي بيده ملكوت كل شيء وإليه ترجعون أقسمت عليكم يا خدام هذه الأسماء بحقها عليكم وطاعتها لديكم إلا ما توكلتم وأجرتم وجلبتم فلان إلى فلانة عنكموش عدد ٢ هيوش عدد ٢ طلوش عدد ٢ فروش عدد ٢ أميوش عدد ٢ طايوش عدد ٢ طهموش عدد ٢ ميوش عدد ٢ كرميانوش عدد ٢ نوش عدد ٢ هيجوا واجلبوا واثنوني به سريعاً عاجلاً حتى يأتي إلى فلانة بنت فلانة الوحا عدد ٢ العجل عدد ٢ الساعة عدد ٢.", "“Segala puji bagi Allah yang ada sebelum makhluk, menciptakan kegelapan dengan cahaya-Nya... Maha Suci yang di tangan-Nya kerajaan segala sesuatu... Aku bersumpah kepada khadam asma ini... kecuali kalian menarik Fulan ke Fulanah - dengan Ankamyusy, Hayusy, Thalusy, Farusy, Amyusy, Thayusy, Thahmusy, Miyusy, Karmiyanusy, Nusy masing-masing 2x - gelisahkan, tarik, datangkan cepat - Al-Waha 2, Al-‘Ajal 2, As-Sa’ah 2.”")

add_block_box('Teks Arab Asli - Azimah Mas-alah 9 (2) - 31x', "وهذه العزيمة تقول - أقسمت عليكم يا معاشر الجن والشياطين والأبالسة والمردة والزوابع والنوابع واكسيام ملك السفلية وملك العمار وملك القرينة بحق هذه الأسماء العظيمة وهو اسم الله الأعظم المخزون الذي بين الكاف والنون الذي ذلت له رقاب الجبابرة وأطاعت له الملوك الأكاسرة وسجدت له ملوك الأرض مشرقاً ومغرباً قالوا إنا لله طائعين ولعظمته خاضعين ولمز هيبته ساجدين باسم اهيا شراهيا. ادوناي أصباؤوت. ال شداي. أهيا اهيا العزيز المعتز الذي نظر إلى السماء فارتفعت وانجلت وإلى الأرض فاستعدت وما جت وإلى الجبال زلت وخر موسى صعقاً الذي أوحى في كل سماء أمرها أن تلقوا محبة فلان ابن فلانة في قلب فلانة بنت فلانة وتهيجوها وتقلقوها وتزعجوها قلب فلانة لمحبة فلان الوحا العجل الساعة عدد ٢ أجيبوا يا خدام هذه الأسماء بحقها عليكم أجيبوا داعي الله من كل فج عميق وأطيعوا وأسرعوا وهيجوا واجلبوا واحرقوا قلب فلانة بمحبة فلان من قبل ما تحترق هذه الأسماء فتكونوا من النادمين أسرعوا بارك الله فيكم وعليكم عدد ٣١ مرة.", "“Aku bersumpah kepada Jin, Syaitan, Iblis, Maradah, Zawabi’, Nawabi’, Aksiyam Raja Sufliyyah, Raja Ammar, Raja Qarinah, dengan Ismullah Al-A’dham antara Kaf-Nun, yang tunduk leher jababirah, patuh raja Persia, sujud raja timur-barat ‘inna lillahi tha-i’in’ - dengan Ahya Syarahya, Adonai Ashba-ut, Al Syaddai, Ahya Ahya, Yang melihat langit lalu meninggi, bumi lalu terhampar, gunung lalu berguncang & Musa pingsan, yang mewahyukan tiap langit - lemparkan cinta Fulan bin Fulanah ke hati Fulanah, gelisahkan, ganggu - Al-Waha Al-‘Ajal As-Sa’ah 2x - jawablah dاعي Allah dari tiap lembah, taat, cepat, bakar hati Fulanah sebelum asma ini terbakar, kalian menyesal - 31x.”")


pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 12 — Mas-alah 10 : Bab Mahabbah wa Tahyij — Malam Ahad — Picture 006 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Mas-alah 10', "المسألة العاشرة\nباب محبة وتهييج\nتكتب ليلة الأحد بعد نوم الناس في كاغد أبيض اسم الطالب وامه والمطلوب وامه مع هذه الأسماء وأنت تقول هيجوا فلانة وأزعجوا واحرقوا قلبها على محبة فلان ابن فلانة بحق اه. شاه. أهيا شراهيا. ادوناي. اصباؤوت ال شداي.\nوهذا ما تكتب", "MAS-ALAH KE-10 — MAHABBAH DAN TAHYIJ Malam Ahad setelah orang tidur, di kertas putih, tulis nama pencari+ibunya & yang dicari+ibunya bersama asma, sambil berkata: “Gelisahkan, ganggu, bakar hati Fulanah untuk cinta Fulan bin Fulanah, dengan hak Ah, Shah, Ahya Syarahya, Adonai, Ashba-ut Al Syaddai.” Dan inilah yang engkau tulis:")
add_rajah(RAJAH_12, "Halaman 12 — Thilasm 2 Baris", "2 baris thilasm horizontal — baris atas `ااااطم 2 م 211 اطاا م` + `هيجوا فلان على`, baris bawah `5 111 3 ح ع م . ق 11 ح م م م م محبة فلان` — disalin persis di kertas putih malam Ahad. HANYA 2 baris (186KB, putih 4x, tanpa teks sekitar).")
add_block_box('Teks Arab Asli — Azimah', "وهذه العزيمة تقول شموشيش. طفيويش. فريش. عبيد. بهيا فلانة إلى محبة فلان بحق هذه الأسماء عليكم الوحا عدد 2 العجل عدد 2 الساعة عدد 2. والبخور لبان وجاوي وكزبرة ناشفة.", "Azimahnya: “Syamusyisy, Thafyuwisy, Farisy, Abid, Bahya Fulanah kepada cinta Fulan, dengan hak asma ini — Al-Waha 2, Al-Ajal 2, As-Saah 2. Bukhur: luban, jawi, ketumbar kering.”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 13 — Mas-alah 12 : Tahyij Shahih (Susi) — Picture 006 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Mas-alah 12', "المسألة الثانية عشرة\nللمحبة والتهييج الصحيح\nقال الشيخ الإمام الفقيه عبدالله أحمد السوسي صار لي أربعين عاماً وأنا في طلبها فوجدتها في بلاد غرناطة عند ملك من الملوك فأعطيته فيها مائة دينار ونقلتها في قرطاس قال الشيخ - خذ شيئاً من شعر الرأس وشيئاً من شعر الباط وشيئاً من شعر الوسط وأظافر اليدين والرجلين واحرقهم وأنت وحدك واجعل منهم مداداً واكتب به هذه الطلاسم واسقيهم لمن شئت ولابد أن تبخر بالفلفل الأسود وتقول عند بخورك.\nأخذت قلبك يا فلان يا ابن فلانة بمحبة فلانة بنت فلانة حتى لا تأكل ولا تشرب ولا تجلس ولا تنام حتى ترى وجه فلانة بنت فلانة.", "MAS-ALAH KE-12 UNTUK MAHABBAH DAN TAHYIJ YANG SHAHIH: Berkata Syaikh Imam Faqih Abdullah Ahmad As-Susi: 40 tahun aku mencarinya, menemukannya di Granada, aku bayar 100 dinar. Ambil sedikit rambut kepala, rambut ketiak, rambut tengah (bulu kemaluan), kuku tangan & kaki, bakar sendirian, jadikan tintanya, tulis thilasm ini dan beri minum kepada siapa kau mau. Wajib asap dengan lada hitam dan ucap: “Aku telah mengambil hatimu wahai Fulan bin Fulanah dengan cinta Fulanah binti Fulanah, sehingga engkau tidak makan, minum, duduk, tidur sampai melihat wajah Fulanah.”")
add_block_box('Teks Arab Asli — Pengantar Rajah', "وهذا ما تكتب على الشقفة", "Dan inilah yang engkau tulis di atas pecahan tembikar:")
add_rajah(RAJAH_13, "Halaman 13 — Thilasm Susi 1 Baris", "1 baris horizontal thilasm `هـ 2229 م هـ ... // 99 عع 15 مـ 33 9ـم 511111 هـ` + ekor bawah — disalin dengan tinta abu rambut/kuku di syaqfah, diasapi lada hitam. HANYA garis thilasm (135KB, putih 4x, tanpa teks sekitar).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 14 — Rajah Hal.14 & Mas-alah 13 Qallama — Picture 007 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Pengantar Rajah', "وهذه الطلاسم", "Dan inilah thilasm-thilasmnya:")
add_rajah(RAJAH_14, "Halaman 14 — Thilasm 2 Baris Da'wah Qallama", "2 baris thilasm — atas `كمل ووو 3 ر 82 01 8 ل`, bawah `هو مل رط ل س ك ووو ر 989 ل` + 2 baris lagi `صع و و وريه د عط 7 111 ك ارا لظم حج اش ...` — untuk Da’wah Qallama Ra-aitahu Akbar. HANYA blok thilasm (161KB, putih 4x).")
add_block_box('Teks Arab Asli — Azimah & Mas-alah 13', "طيوش طيشوا عقلها واخطفوا قلبها بمحبة فلان ابن فلانة\nالمسألة الثالثة عشرة\nفي دعوة قلما رأيته أكبرنه\nوهي تصلح لكل شيء - فإن أردتها للقبول فاجعلها في حرز واجعلها على عضدك الأيمن ويكون عند الزوال - وإن أردتها للتمييل فاكتبها في حرزين واحد اسقيه للمطلوب والآخر تجعله المرأة في حزامها وإن كان للرجل فيحمله على عضده الأيمن وإن أردتها للخطبة فاكتبها مع الدعوة وعلقها بين عينيك يسهل الله لك ما تريد وإن أردتها للمحبة فاكتبها يوم الخميس أو يوم الجمعة قبل طلوع الشمس وعلقها للريح بشعر رأس من تريده أو بخيط أحمر وبالله الذي لا إله إلا هو ما جربتها مراراً ما خابت أبداً وتستجاب في الوقت والحين والكاذب عليه لعنة الله وهذه أمانة الله لا تفعلها إلا في الحلال.", "“Thayusy, Thisyû ‘aqlaha wa-khthafu qalbaha bi-mahabbati Fulan bin Fulanah.”\nMAS-ALAH KE-13 TENTANG DOA QALLAMA RA-AITAHU AKBARNAH — Cocok segala hajat: Qabul: jimat di lengan kanan saat zawal; Tamyiil: 2 jimat, satu diminum, satu di ikat pinggang; Khithbah: gantung di antara mata; Mahabbah: tulis Kamis/Jumat sebelum subuh, gantung diterpa angin dengan rambut/benang merah. “Demi Allah tidak pernah gagal, terkabul seketika. Pendusta dilaknat. Amanah Allah, hanya untuk halal.”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 15 — Khatam Mahabbah Sulaiman — Picture 007 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Khatam', "وهذا ما تكتب مع الخاتم\nبسم الله الرحمن الرحيم الحمد لله الذي جعل الظلمات والنور اللهم نور قلب فلان وفلانة بمحبة لو أنفقت ما في الأرض جميعاً إلى قوله حكيم اللهم ألف بين فلان وفلانة فلبثت سنين في أهل مدين ثم جئت على قدر يا موسى كذلك يجعل الله محبة فلان في قلب فلانة شهد الله أنه لا إله إلا الله هو والملائكة إلى حكيم عسى الله أن يجعل بينكم وبين الذين عاديتم منهم مودة والله قدير والله غفور رحيم اللهم عطف قلب فلان في قلب فلانة اللهم ألف بينهم كما ألفت بين سيدنا محمد وعائشة وكما ألفت بين علي وفاطمة وكما ألفت بين يوسف وزليخا يا الله يا الله يا رحمن يارحمن يارحيم يا رحيم يارحيم يارحيم ياودود ياودود ياودود يارؤوف يارؤوف يارؤوف يارؤوف يارؤوف يارؤوف يارؤوف يارؤوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف ياعطوف اللهم عطف قلب فلان إلى محبة فلانة بحق هذه الأسماء عليكم يا الله بحق اسمك الظاهر ياذا الجلال والإكرام عدد ٣ ألم نشرح لك صدرك إلى آخرها اللهم رغب محبة فلانة في قلب فلان ربنا عليك توكلنا وإليك أنبنا وإليك المصير اللهم يارب بحق أسمائك الظاهرة وملائكتك وأنيائك أن تجعل محبة فلانة في قلب فلان بالريح العاصف والبرق الخاطف إنه من سليمان وإنه بسم الله الرحمن الرحيم", "Dan inilah yang engkau tulis bersama Khatam: Bismillah... Segala puji bagi Allah yang menjadikan gelap & cahaya. Ya Allah terangilah hati Fulan & Fulanah... (kutip QS Al-Anfal:63, Thaha, Ali Imran:18, Al-Mumtahanah:7, doa ta’lif antara Muhammad-Aisyah, Ali-Fatimah, Yusuf-Zulaikha, Ya Allah Ya Rahman Ya Rahim Ya Wadud Ya Ra’uf Ya ‘Athuf (diulang), Ya Allah lembutkan hati Fulan kepada Fulanah dengan hak asma ini, dengan Nama-Mu Zahir, Wahai Pemilik Keagungan, 3x Alam nasyrah, Ya Allah jadikan cinta Fulanah di hati Fulan dengan angin topan & kilat — Innahu min Sulaimana wa innahu Bismillahir Rahmanir Rahim.")


pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 16 — Khatam Besar 8x8 + Penutup Doa Sulaiman — Picture 008 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Lanjutan doa Sulaiman', "الرحيم أن لا تعلوا علي وأتوني مسلمين يالغو اثه رب العالمين\\nلياخيم أجب يا مذهب بحق دائرة الشمس أجب يامرة بحق دائرة\\nالقمر لبلاغمو أجب يا احمر بحق دائرة المريخ ليافور أجب يا برقان\\nبحق دائرة الكاتب لياروع أجب ياشمهورش بحق دائرة المشتري\\nلباروت أجب يا أبيض بحق دائرة الزهرة لياروش أجب يا ميمون\\nبحق دائرة زحل ليابلاش توكلوا يا معشر السادات الأقربين بحق\\nهذا الخاتم بمحبة فلان في قلب فلانة.\\nوهذا الجدول\\nشيخ الروحانيين\\nالشيخ عطية عبد الحميد\\nنسألكم الفاتحة والدعاء", "Lanjutan doa dari Hal.15 (Innahu min Sulaimana...): “...Ar-Rahim, alla ta’lu ‘alayya wa’tuni muslimin, Ya Alghu Rabbal ‘Alamin, Ya Liyakhim jawablah Mudzahhab dengan hak lingkaran matahari, Murrah lingkaran bulan, Ahmar-Mars, Barqan-Utarid, Syamhuris-Musytari, Abyadh-Zuhrah, Maimun-Zuhal, Liyabalasy, wakilkan wahai pemuka yang dekat, demi Khatam ini untuk mahabbah Fulan di hati Fulanah.” Dan inilah tabelnya — Syaikh Ar-Ruhaniyyin Syaikh Athiyah Abdul Hamid, mohon Fatihah.")
add_rajah(RAJAH_16, "Halaman 16 — Khatam Besar 8x8 Fawatih", "Khatam 8 kolom x 8 baris isi huruf muqatha'ah/angka + 4 sigil di pojok. Tulis di murabba' diasapi wangi di jam Mars. HANYA tabel (1.1MB, 2884x2152 px, 4x, putih bersih, tanpa teks sekitar), siap cetak.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 17 — Mas-alah 14 : Doa Fatihah Murabba — Picture 008 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli — Mas-alah 14', "المسألة الرابعة عشرة\\nمسألة للمحبة\\nمجربة على يد كاتبها وهي لدعوة الفاتحة في مربع وتبخر\\nبرائحة طيبة وتكتب في يوم ساعة المريخ وتكتب وتحمل في أي\\nيوم كان سعيد\\nوهذا ما تكتب وبه تعزم\\nتقول بسم الله الرحمن الرحيم الحمد لله رب العالمين ياحي\\nياقيوم أجب يارو قيائيل أنت وأعوانك العلوية واجلب فلان إلى\\nفلانة بحق الحمد لله رب العالمين الحي القيوم وبحق سيدنا\\nمحمد ﷺ وبحرمة الملائكة الموكلين بقوائم العرش أبجد أجب يا\\nمذهب أنت وخدامك الأرضية واجلبوا وهيجوا واجذبوا فلان إلى\\nفلانة بحق الملك الغالب عليك أمره السيد ورقيائيل الرحمن\\nالرحيم الرؤوف العطوف أجب ياجبرائيل أنت وأعوانك العلوية\\nواجلب وهيج واحرق قلب فلان بمحبة فلانة بحق الرحمن الرحيم\\nالرؤوف العطوف وبحق سيدنا ﷺ وبحق الملك الموكل بالقوائم\\nالعرشية هوزح أجب يا أبيض أنت وخدامك الأرضية أجب واجلب\\nوهيج واحرق قلب فلان بمحبة فلانة بحق الملك الغالب عليك\\nأمره جبرائيل مالك يوم الدين يا مقلب القلوب والأبصار أجب\\nياسمسائيل أنت وأعوانك العلوية أجب واجلب وهيج واحرق\\nقلب فلان بمحبة فلانة بحق مالك يوم الدين يا مقلب القلوب", "MAS-ALAH 14 — DOA AL-FATIHAH Mujarrabah: Tulis di murabba' diasapi wangi, di jam Mars, dibawa di hari sa’id. Azimah panjang: Bismillah Alhamdulillahi Rabbil ‘Alamin Ya Hayyu Ya Qayyum jawablah Ruqya’ilulwiyyah, bawa Fulan ke Fulanah dengan hak Alhamdulillah, hak Nabi ﷺ, kemuliaan malaikat tiang Arsy — Abjad jawablah Mudzahhab ardiyyah tarik Fulan, dengan hak Sayyid Ruqya’il Ar-Rahman Ar-Rahim, wahai Jibra’il... Hawzah jawablah Abyadh... Maliki Yaumid Din Ya Muqallib... wahai Samsama’il... (pola diulang tiap ayat Fatihah + malaikat penjaga).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 18 — Lanjutan Azimah Doa Fatihah — Picture 009 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "والأبصار وبحق سيدنا محمد ﷺ وبحرمة الملك المزكل بغائم\\nالعرش طيكل أجب يا احمر أنت وخدامك الأرضية أجب واجلب\\nوهيج واحرق قلب فلان بمحبة فلانة بحق الملك الغالب عليك\\nأمره والأخذ بناصيتك سمسائيل إياك نعبد وإياك نستعين السريع\\nالقريب وبحق سيدنا محمد ﷺ وبحرمة الملك الموكل بقائم العرش\\nمنسع أجب يا برقان أنت وخدامك الأرضية أجب واجلب وهيج واحرق\\nقلب فلان بمحبة فلانة بحق الملك الغالب عليك أمره والأخذ\\nبناصيتك ميكائيل اهدنا الصراط المستقيم ياقادر يامقتدر أجب\\nياصرفيائيل أنت وأعوانك العلوية أجب واجلب وهيج واحرق قلب\\nفلان بمحبة فلانة بحق اهدنا الصراط المستقيم وبحق القادر\\nالمقتدر وبحق سيدنا محمد ﷺ وبحرمة الملك الموكل بقائم\\nالعرش فصقر أجب ياشمهورش أنت وخدامك الأرضية أجب\\nواجلب وهيج واحرق قلب فلان بمحبة فلانة بحق الملك الغالب\\nعليك أمره والأخذ بناصيتك صرفيائيل صراط الذين أنعمت عليهم\\nيا عليم ياحكيم أجب ياعنيائيل أنت وأعوانك العلوية أجب واجلب\\nواحرق قلب فلان بمحبة فلانة بحق صراط الذين أنعمت عليهم\\nوبحق العليم الحكيم وبحق سيدنا محمد ﷺ وبحق الملك الموكل\\nبقائم العرش شننخ أجب يازوبعة أنت وخدامك الأرضية أجب واجلب\\nوهيج واحرق قلب فلان بمحبة فلانة بحق الملك الغالب عليك\\nأمره والأخذ بناصيتك عنيائيل غير المغضوب عليهم ولا الضالين\\nوبحق القاهر العزيز وبحق سيدنا محمد ﷺ وبحرمة الملك الموكل", "Lanjutan azimah Hal.17 tiap ayat Fatihah: Thaykal-Ahmar, Munsa’-Barqan, Mikail-Ihdinas Shirath, Sharfaya’il-Syamhursy, ‘Anyail-Ghairil maghdhubi... semua diakhiri “jawablah, bawa, gelisahkan, bakar hati Fulan dengan cinta Fulanah dengan hak Raja Yang Mengalahkan & memegang ubunmu...” + hak Al-Qahir Al-‘Aziz, hak Nabi ﷺ.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 19 — Khatam 4x4 837x & Penutup Mas-alah 14 — Picture 009 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "بقائم العرش ضظغض أجب يا ميمون ابانوح أنت وخدامك الأرضية\\nواجلب وهيج واحرق قلب فلان بمحبة فلانة بحق الملك الغالب\\nعليك أمره والأخذ بناصيتك كسفيائيل أجيبوا يا معاشر الأرواح\\nالروحانية العلوية والخدام السفلية والملائكة العرشية أجيبوا واجلبوا\\nواحرقوا قلب فلان بمحبة فلانة بحق السبعة المثاني وبحق السماء\\nالعظام والآيات الكرام أجيبوا واجلبوا وهيجوا واحرقوا قلب فلان\\nبمحبة فلانة بحق ما تعتقدونه فيها من العظمة والكبرياء الوحا عدد ٢\\nالعجل عدد ٢ الساعة عدد ٢ بارك الله فيكم وعليكم.\\nوهذا هو الخاتم المشار إليه\\nوالقسم عليك", "“...Dhazaghadh Maimun Abanuh ardiyyah, Kasfayail, jawablah wahai arwah ruhaniyyah ulwiyyah, khadam suflyyah, malaikat Arsy, bakar hati Fulan dengan hak As-Sab’u al-Matsani (Fatihah 7 ayat) & langit & ayat mulia, dengan keagungan — Al-Waha 2 Al-‘Ajal 2 As-Sa’ah 2, Barakallahu fikum. Dan inilah Khatam yang dimaksud, sumpah atasmu:”")
add_rajah(RAJAH_19, "Halaman 19 — Khatam 4x4 Angka 837x", "Khatam 4x4 angka baris 1: 8368 8280 8278 8372, baris 2: 8379 8266 8271 8376, baris 3: 8267 8282 8273 8370, baris 4: 8372 8269 8268 8281 + sigil pojok + tulisan Wal-qasam ‘alaik. Tulis di murabba’ jam Mars. HANYA 4x4 (767KB, 2744x1976 px, 4x putih bersih).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 20 — Mas-alah 15 : Tahyij 7 Kertas Sabtu Jam 11 — Picture 010 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "المسألة الخامسة عشرة\\nباب تهييج ومحبة\\nيكتب في سبعة أوراق الساعة ١١ يوم السبت وهي ساعة\\nالشمس في أول الشهر ثم اجعل في كل ورقة سبع حبات فلفل\\nأبيض وسبع حصوات لبان ذكر وشيء من أثر المطلوب ثم القى\\nورقة في النار وهكذا تحرق واحدة بعد واحدة يحضر المطلوب\\nمذهول العقل.\\nوهذا ما تكتب في الأوراق السبعة\\nاحون عدد ٢ احماطيس عدد ٢ كملموصا عدد ٢ كهلموصا عدد ٢\\nهمير كدهير عدد ٢ اطلع عدد ٢ أفراطين عدد ٢ دليهوو عدد ٢ طلههميك\\nعدد ٢ توكلوا يا خدام هذه الأسماء بتهييج وحرق قلب فلانة على\\nمحبة فلان بحقها بحكم عليكم بحكم عليكم بجلب وتهييج فلانة بنت فلانة في محبة\\nفلان ابن فلانة الوحا العجل الساعة عدد ٢.\\nوهذه العزيمة\\nتقول - السلام عليك يا فلانة يا بنت فلانة إن كنت نائمة أو\\nيقظانة فإني جلبتك في هذه الساعة سبعة السماء فاهبنك وحيرتك\\nودهمشت عقلك ودخلت عليك بسحر هاروت وماروت فاشتغلتك\\nوضربت الأرض من تحتك وعقدت الجن من خلفك نطقت\\nقرينتك لبست جنتك فأطلقت محبة فلان ابن فلانة في قلبك وفي\\nذكرك وفي دمك وفي لحمك فاشتعل قلبك بالهيجان وعقلك", "MAS-ALAH 15 TAHYIJ 7 KERTAS: Tulis 7 lembar jam 11 Sabtu (jam Syams awal bulan), tiap lembar 7 lada putih + 7 luban dzakar + atsar, bakar satu-satu target hadir linglung. Tulis di 7 lembar: “Ahun 2x Ahmathis 2x Kamalmuwsa 2x ... Thalhahmik 2x — wakilkan gelisahkan bakar hati Fulanah — Al-Waha Al-‘Ajal As-Sa’ah 2x.” Azimah: “Salam Fulanah, kuterik di jam 7 langit, kubingungkan, kumasuki sihir Harut-Marut, kupukul bumi bawahmu, kuikat jin belakangmu, kubuat qarinmu bicara, kulepas cinta Fulan di hati-darah-dagingmu, menyala...”")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 21 — Lanjutan Azimah & Mas-alah 16 — Picture 010 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "بالطيران وقريبتك لهياج الجان وأحرقتك بالنار نار على نار واشتد\\nالقلب منك وطار وتنخبل العقل منك وحار ووسواس الصدافيقنا\\nبالأذكار ولقي بك الغرام بنار المحبة فاحترقت حرقاً ٢ ورشحت\\nعرقاً ٢ وهامت عشقاً ٢ وذابت قلقاً كنليان الماء في القدور على\\nالنار إذا ألقوا فيها سمعوا لها شهيقاً وهي تفور ذبتي يا فلانة يا بنت\\nفلانة كما ذابت المونى في القبور فلا ينفك عملي هذا حتى ينفخ\\nإسرافيل في الصور وتخرج الموتى من القبور إن لغير مشكور\\nبرجمت بقسمي وههمت بنفسي وتوكلت على ربي وقلت إنه من\\nسليمان وإنه بسم الله الرحمن الرحيم أن لا تعلوا علي وأتوني\\nمسلمين مسرعين طائعين لله رب العالمين بحق اهيا شراهيا ادوناي\\nاصباؤوت ال شداي وإنه لقسم لو تعلمون عظيم أن ٢ ايل ٢ اه ٢\\nاهيا ٢ مهليل ٢ شلهيب ٢ دوسم ٢ اهمليلا طرخيثا ٢ ميا يا\\nأصحاب الكلام طلس ٢ طلوس ٢ بها ٢ بهوبط ٢ بهابيل مهولة ٢\\nبمعاطفة عطوفة بخاطفة خطوفة اخطفوا قلب فلانة بنت فلانة في\\nمحبة فلان ابن فلانة حتى لا تأكل ولا تشرب ولا تهدتي ولا تنام\\nبحق بعضكم على بعض العجل فيكم وعليكم بارك الله فيكم وكان أمر\\nالله مفعولاً وصلى الله على سيدنا محمد وعلى آله وصحبه وسلم.\\nالمسألة السادسة عشرة\\nمسألة للمحبة\\nتأخذ قطعة عجين وصور منها صورة فرس ونأخذ شيء من", "Lanjutan azimah Hal.20: “...terbang, bakar api di atas api, hati terbang, akal gila, was-was memuncak, bakar cinta 2x keringat 2x mabuk 2x meleleh seperti air mendidih, leleh Fulanah seperti mayat di kubur, tidak lepas sampai Israfil tiup... Aku bersumpah Innahu min Sulaimana... musri’in tha’i’in, Ahya Syarahya Adonai Ashba-ut Al Syaddai, wa innahu la-qasamun lau ta’lamuna ‘azhim, An 2 Il 2 Ah 2 Ahya 2 Mahalil 2, Thalas 2 Thalus 2 Biha 2 Bahubath 2 Bahabil Mahulah, dengan kasih yang menarik menyambar, sambar hati Fulanah sampai tak makan-minum-tidur — bi-haqqi ba’dhikum ‘ala ba’dh, Barakallahu fikum, washalallah ‘ala Muhammad.”\\nMAS-ALAH 16 MAHABBAH: Ambil adonan bentuk kuda (faras), ambil sesuatu dari... (bersambung Hal.22)")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 22 — Mas-alah 16 Lanjutan (Kuda Adonan) & Awal 17 — Picture 011 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "أثر المطلوب وتكتب عليها هذه الأسماء الآتي ذكرها وتلونها\\nقطران وزيت طيب وتبخرهما مثل الفتيلة وتجعلهما في فم الفرس\\nوأيضا تكتبهم في كفك الشمال قبل أن توضع الفتيلة في فم\\nالفرس.\\nوهذا ما تكتب على الكف والأثر\\nقزن قزن قرن هزن هزن هزن خزن خزن خزن فرش فرش\\nفرش الجلبيوش الجلبيوش ذو العزة والسلطان انفروا خفافا وثقالا\\nفإذا قضيت الصلاة فانتشروا في الأرض\\nيا ابا طح بابا لا وتبخرهم بمقل أزرق ولبان ذكر\\nثم توقد الفتيلة وتزعم فإنك ملك روحاني افتح يدك في وجهه\\nوتكون كاتب الكتابة في الكف.\\nوهذا ما تعزم به\\nتقول - معترايش جه مقـرش لطوش هند وفطش طيطيش هيا\\nفلطش بحق فهروش لشـهبا فقـرش الساعة إلى فلان ابن فلانة بارك\\nالله فيكم وعليكم.\\nالمسألة السابعة عشرة\\nللمحبة والتهييج\\nتكتب في صفيحة من الرصاص وتنقش عليها هذه الطلاسم\\nثم تأخذ شيئا من أثر المطلوب وتجيب شقفة جديدة وتوضعها في", "Lanjutan Mas-alah 16 kuda adonan: Tulis nama di atsar, warnai ter+minyak wangi, jadikan sumbu di mulut faras, juga tulis di telapak kiri sebelum sumbu dimasukkan. Yang ditulis di telapak & atsar: “Qazan Qazan Qaran Hazan... Farasy, Ya Jalbuyusy... Infiru khifafan wa tsiqala, fa-idza qudhiyatish shalah... Ya Aba Thah Baba La” — diasapi muqul biru+luban, nyalakan sumbu, klaim sebagai raja ruhani “buka tanganmu”. Azimah: “Ya Mu’tarai Jih Miqrasy Lathusy Hind wa Fathasya... Fahrusy Syahba Fa-qarsy ke Fulan jam ini.”\\nMAS-ALAH 17 UNTUK MAHABBAH & TAHYIJ: Tulis di lembar timah, ukir thilasm, ambil atsar, ambil shafqah baru...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 23 — Mas-alah 17 Lanjutan + Ta`widh — Picture 011 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "النار فإذا حميت الشقفة ترمي عليها الأثر والرصاص فوق الأثر\\nوتعزم عليها ٢١ مرة والبخور لبان ذكر وكسبرة.\\nوهذا ما تنقش على الرصاص مع اسم المطلوب وأمه كما\\nترى انهم ترشد\\n٩٥٠١١١ ط ٦٢٢١٩ ٦٦ا؛ ٩١٩٦ ط ٠٤٢ اع ٦٢٢١٩\\nهنا ليس ط ١٦ كذا ط ك لم ٦١ لما ط ٢٠٠ا تعالى الحى السلطان\\nسورية ٩١٩ ١١ ١١ ٩١٦٩ ٦٩٩١ سوية ٦٩١٢ ا ٩١٦\\nوهذه العزيمة التي تعزم بها\\nتقول - هيجتك يا فلان يا ابن فلانة وجلبتك مع الكلاب\\nالنابحة وهيجتك مع السباع الضارية هيجتك مع الذئاب العاوية\\nهيجتك مع الديوك الصائحة هيجتك يا فلان مع الرياح الهائلة\\nبالمردة المستر قين السمع من سحب ابا النار والنور والظل\\nوالحرور اعزم على سكان الحمامات والقميدات والبراري\\nوالقفاري والأسواق والأبيار والرياسين عجلوا واسرعوا وهيجوا\\nفلان ابن فلانة مدكيوش هيوش دهوش هاروت وماروت بزوبعة\\nولوبعة والمغاريت الأربعة بحق كبارهم وصغارهم وصغاركم على\\nكباركم بحق بكشارش كشارش وكوش طموش شلبنايشا قدقد\\nوعيال بالغ شهر وش عدد ٧ حلش ٢ هليوش ٢ شلوش ٢ بقلوش\\n٢ وطبطون ٢ رعشتر ٢ اسرعوا ٢ وعجلوا ٢ والقوا محبة فلانة\\nبنت فلانة في قلب فلان ابن فلانة الوحا العجل الساعة.", "“...Shafqah panas lempar atsar+timah di atas atsar, azimah 21x, bukhur luban & kasbarah.” Yang diukir di timah bersama nama+ibu target — lihat Rajah bawah. Azimah: “Aku gelisahkan Fulan bin Fulanah dengan anjing menyalak, binatang buas, serigala, ayam, angin topan, maradah pencuri dengar, Aba An-Nar... aku sumpahi penghuni hammam, padang, pasar, sumur — segeralah gelisahkan Fulan — Madkayusy Hayusy Dahusy Harut-Marut Zau-ba‘ah Lub‘ah Magharit 4 — Kas-yarasy Syalabla-nayasya Qadqad — Halasya 7x Haliyusy 2x Syalusy 2x Baqlusy 2x Thab-thun 2x Ra‘syatar 2x — segeralah lempar cinta Fulanah ke hati Fulan — Al-Waha...”")
add_rajah(RAJAH_23, "Halaman 23 — Ukiran Timah Mas-alah 17", "2 baris angka/huruf tulisan tangan `٩٥٠١١١ ط ٦٢٢١٩...` + `هنا ليس ط...` — ukiran di timah + nama target/ibu. HANYA blok ukiran (3020x864 px, 203KB, 4x putih bersih).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 24 — Mas-alah 18 & 19 : Darah Kaki — Picture 012 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 18', "٢ وطبطون ٢ رعشتر ٢ اسرعوا ٢ وعجلوا ٢ والقوا محبة فلانة\\nبنت فلانة في قلب فلان ابن فلانة الوحا العجل الساعة.\\nالمسألة الثامنة عشرة\\nمسألة للمحبة\\nتكتب بدم رجلك وتضرب بها من شئت فإنه يتبعك من شدة\\nالمحبة وإن شككت فيها فاضرب بها حمارة فإن تبعك.\\nوهذا ما تكتب\\nك هـ ح ع وز نعص ع هـ ط ص ط ل ك ك ساكح\\nلعمه", "Penutup Mas-alah 17: “...Thab-thun 2x...”\\nMAS-ALAH 18 UNTUK MAHABBAH: Tulis dengan darah kaki (dam rijlik), pukul siapa kau mau — ia ikut karena sangat cinta. Tes: pukul himarah (keledai); jika ikut terbukti. Yang ditulis: lihat Rajah Atas.")
add_rajah(RAJAH_24T, "Halaman 24 Atas — Thilasm Mas-alah 18", "Baris `كـ هـ ح ع وز نـعـصـ عـ هـ طـ صـ طـ لـ ك ك سـا كـح` + 3 sigil bawah `لعمه`. Darah kaki. HANYA thilasm+sigil (2952x956 px, 233KB, 4x).")
add_block_box('Teks Arab Asli - Mas-alah 19', "المسألة التاسعة عشرة\\nمسألة للمحبة\\nتكتب بدم رجلك وتضرب بها من شئت من شئت ثلاث مرات على\\nرأسها لاشك فيها وإن شككت فيها فاضرب بها حمارة فإنها تتبعك\\nوتكون الكتابة يوم الجمعة ترى عجبا عظيما.\\nوهذا ما تكتب\\nفقطط هـ هـ هـ طو مـعص الطو طـلا ق كـ يحصه\\nعمر طـطـ مـعـ هـم هـ مـ هـ\\n...", "MAS-ALAH 19 JUGA DARAH KAKI: Pukul 3x di kepala, tanpa ragu; tes himarah. Tulis hari Jumat — lihat keajaiban. Yang ditulis: lihat Rajah Bawah.")
add_rajah(RAJAH_24B, "Halaman 24 Bawah — Thilasm Mas-alah 19 (Jumat)", "Baris `فـقـطـط هـ هـ هـ طـو مـعـص...` + `عـمـر طـطـ...` + baris titik ○○○○ — khas Jum'at. HANYA thilasm+titik (3092x1000 px, 303KB, 4x).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 25 — Mas-alah 20 & 21 — Picture 012 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 20', "المسألة العشرون\\nباب محبة\\nيكتب على شقفة بمعتبر معتبر طيبير طيبير منفرد منفرد منفرد\\nمنفرد ينفرد بهشهشة ٢ بكشكشة ٢ مكشكشة ٢ هاطلة ٢ مهولة ٢\\nخاطفة ٢ خطوفة ٢ احتفظ يا هـاروش وانت ياماروش وانت يا سريع\\nوانت يا بريق وانت يا عبد النار قلب فلانة بنت فلانة إلى محبة\\nفلان ابن فلانة الوحا العجل الساعة والبخور لبان ذكر وكسبرة\\nوتقرأ العزيمة بعد كتابتها على الشقفة عدد ٤ مرات أو عدد ٢١ مرة\\nوهي في النار دائمة الوقود.\\nالمسألة الواحدة والعشرون\\nباب السر المصون\\nملمون ثم ملمون من يطلع عليه غير أهله وهو من ذخائر\\nالملوك وهو يتصرف في أمور شتى فمنها للتهيج فمنها لإحضار الخصم\\nومنها لإرسال الهواتف ومنها لصرع المصاب.", "MAS-ALAH 20 BAB MAHABBAH: Tulis di shafqah dengan Mu‘tabir Thaybir Munfarid... Hasyhasyah 2x Kasykasyah... Hathilah Mahulah Khathifah — “Jagalah Harusy Marusy Sari‘ Bariq ‘Abdan Nar hati Fulanah ke Fulan — Al-Waha...” bukhur luban+kasbarah, baca 4x atau 21x di api tetap nyala.\\nMAS-ALAH 21 BAB SIRR MASHUN: “Malmoun yang menampakkan ke bukan ahli — simpanan raja, untuk tahyij/hadirkan lawan/kirim hawatif/robohkan orang kesurupan.”")
add_block_box('Teks Arab Asli - Sirr Mashun lanjut', "فإذا أردت التهيج تكتب يوم الأحد عند طلوع الشمس\\nواجعلها عليك بعد قراءة العزيمة ٢١ مرة واتقي الله ويبخرها\\nبالصندل الأحمر وإن أردت للإرسال تقرؤه ليلة الجمعة. وإن\\nأردت للصرع اكتبه في كف المصاب.\\nوهي هذه هياش مياش شالوش طاشي وتركل بهم بهذه\\nالأسماء تقول:", "Jika ingin tahyij: tulis Ahad terbit matahari, bawa setelah baca 21x, takutlah Allah, asapi cendana merah. Jika kirim: baca malam Jumat. Jika robohkan: tulis di telapak orang kesurupan. Mantranya: Hayasy Mayasy Syalusy Thasyi — wakilkan dengan nama berikut: (bersambung Hal.26).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 26 — Sirr Mashun Lanjutan + Mas-alah 22 Daun Zaitun — Picture 013 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "كشارش ٢ مشارش ٢ طرباش ٢ ايغوش ٢ جالهوش ٢\\nتعملوش ٢ كندريوش ٢ عواديوش ٢ هيا ٢ يا أهل النار والنار والشرار\\nوالأزعاج والأمراض وتركلـوا وافعلوا كذا بحق هذه الأسماء عليكم\\nوطاعتها لديكم نار واحراق من عصى منكم يكون قتيلا الوحا ٢\\nالعجل ٢ الساعة ٢\\nواصرافه\\nوالصافات إلى قوله ناقب يا راصد الجن ياغليطا امتنع دبيلح\\nبخ ٢ سلام ٢ هيو ٢ ميهو ٢ الملك لله الواحد القهار.\\nالمسألة الثانية والعشرون\\nباب محبة\\nيكتب على ورق الزيتون يوم الأحد قبل طلوع الشمس على\\nسبع ورقات زيتون ونجعل في ورقة حصوة لبان ذكر واحرتهم\\nواحدة بعد واحدة وأنت تقول يا خدام هذه الأسماء احرقوا قلب\\nفلان ابن فلانة في محبة فلانة بنت فلانة.\\nوهذا ما تكتب على الورقة الأولى ٦٣٨٢١ ٩٥١١٩٩١١ هـ ٩٥١١\\nالثانية ٩٨٢١١٢١١٠ ٢١٩٦٣ ٨٨٨٨٢٢١٨٢١٣\\nالثالثة\\nالرابعة طنـش طـلع طـسمح الخامسة د١١١٧ ك ١١١١ ٨٢ ١١\\nالسادسة\\nالسابعة ٨٢١٨١ ١١٣٢ م ٦٨٢١١ السادسة ١١ا على ملح", "Lanjutan Hayasy Mayasy: “Kas-yarasy 2x... Jalhasy 2x... Kandariyusy ‘Awadiyusy — hayya ya Ahlan Nar wasy-Syarar... dengan hak asma & ketaatannya, api bakar yang durhaka akan terbunuh — Al-Waha 2...” Israf: “Wash-Shaffat... tsaqib, Ya Rashidul Jin Ya Ghalitha Imtana‘ Dubailah Bakh 2 Salam 2 Hayw 2 Mihaw — milik Allah Al-Wahid Al-Qahhar.”\\nMAS-ALAH 22 BAB MAHABBAH 7 DAUN ZAITUN: Tulis di daun zaitun Ahad sebelum terbit matahari pada 7 lembar, tiap daun 1 kerikil luban, bakar satu-satu sambil berkata “wahai khadam bakar hati Fulan bin Fulanah”. Tulis di waraq 1-7 lihat Rajah bawah.")
add_rajah(RAJAH_26, "Halaman 26 — 7 Waraq Daun Zaitun", "7 baris untuk 7 daun: W1 `٦٣٨٢١ ٩٥١١٩٩١١`, W2 `٩٨٢١١٢١١٠ ٢١٩٦٣...`, W4 `طـنـش طـلـع طـسـمـح` W5 `د١١١٧ ك ١١١١`, W6-7 `٨٢١٨١ ١١٣٢ م ٦٨٢١١` + catatan. Tulis di daun zaitun tiap 1 luban, bakar 1-1 Ahad subuh. HANYA 7 baris (3092x1176 px, 416KB, 4x).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 27 — Mas-alah 23 & 24 : Telur & Bawah Ranjang — Picture 013 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Mas-alah 23', "المسألة الثالثة والعشرون\\nباب محبة\\nيكتب على بيضة بنت يومها وتبخرها بلبان وسندروس\\nومسكتكي وكبريت وادفنها في نار\\nوهذا ما تكتب على البيضة\\nكموخين كلوخين عطوشين مره مروشين طلوشين ابن كزير ابن\\nزريعا طهوشين شلوشين ظهرفين جلاجين خورشين ابن الرياح\\nالموكل بالرياح وأعوانك وخدامك واحرق قلب فلانة على محبة فلان\\nالعجل عدد ٢ الوحا عدد ٢ الساعة عدد ٢ بحق هذه الأسماء عليكم يا خدام\\nهذه الأسماء كونوا عونا لي بحق سليمان بن داود عليه السلام.\\nالمسألة الرابعة والعشرون\\nباب محبة النساء\\nتكتب يوم الاثنين مع اسم الرجل واسم المراة وتدفنه في\\nالأرض تحت فراشك فإن المراة تحبك حبا شديدا، وهي هذه\\nالطلاسم مجرب صحيح\\nهذه الآية ٩٩٩ ططه ١١٩٩ ط طها باسم", "MAS-ALAH 23 TELUR HARI ITU: Tulis di telur baru hari itu (binti yaumihi), asap luban+sandar+mustaki+belerang, kubur di bara. Yang ditulis: “Kamukhain Kalukhain ‘Athusyain Marrah... Thahusyain Jalajain... Ibnu Ar-Riyah — yang diserahi angin — bakar hati Fulanah untuk Fulan — Al-‘Ajal 2... dengan hak Sulaiman bin Dawud.”\\nMAS-ALAH 24 CINTA WANITA: Tulis Senin bersama nama lelaki+wanita kubur bawah kasur — maka sangat cinta. Thilasm: lihat Rajah bawah — `999 Thatha 1199...`")
add_rajah(RAJAH_27, "Halaman 27 — Thilasm Senin Bawah Ranjang", "2 baris + 3 sigil — `٩٩٩ ططه ١١٩٩ ط طها باسم` + `طـ هـ ٧ حـ ٧ وصا ٧` + 3 sigil ***. Tulis Senin + nama pasangan kubur bawah kasur. HANYA thilasm+sigil (3092x1352 px, 426KB, 4x putih).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 28 — Mas-alah 25 : Bawa di Kepala & Ambang Pintu — Picture 014 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "المسألة الخامسة والعشرون\\nباب محبة مجرب صحيح\\nتكتب هذه الأسماء في ورقة ويحمل على الرأس وتكتب\\nأيضا وتدفن تحت عتبة باب من تريد فإنه لا يصبر عليك ساعة\\nواحدة\\nوهذا ما تكتب واحذر من الغلط\\nاخ ح ح ح ح ح ح ح ح لعله له له له لم لم لم لم لم لم\\nلم صر صر صر صر صر صر ص ص ص ص ص ص ص ص ص ص\\nلك ك ك ك ك ك !! طو طو طو طو طو طو طو طو اكر طو طر ه ٥\\n........... وتذكر اسمه واسم أمه فإنه لا يصبر عليك إنسي حم\\nمم فلان ابن ثلاثة في محبة فلانة بنت فلانة الم نشرح لك صدرك\\nووضعنا عنك وزرك يا جبريل والضحى والليل إذا سجى\\nما ودعك ربك وما قلى وللآخرة خير لك من الأولى ولسوف\\nيعطيك ربك فترضى ألم يجدك يتيما فآوى ووجدك ضالا فهدى ٢\\nاهدي فلان ابن فلانة إلى محبة فلانة بنت فلانة وتكون الكتابة أول\\nثلاث في الشهر قبل طلوع الشمس بمسك وزعفران وماء ورد\\nويحملها الطالب تحت العمامة في مقدم رأسه ويقبل على\\nالمطلوب.", "MAS-ALAH 25 SHAHIH: Tulis di kertas bawa di kepala, tulis lagi kubur di ambang pintu target — tidak tahan sejam. Yang ditulis hati-hati: lihat Rajah bawah — `اخ ح ح... لم صر... لك ك ك !! طو طو...` + sebut nama+ibu, lalu `Alam nasyrah... Wadhdhuha... al am yajidka yatiman...` 2x — hadiahkan Fulan ke cinta Fulanah. Tulis 3 hari pertama bulan sebelum terbit dengan misk+za‘faran+mawar, bawa di bawah sorban depan kepala.")
add_rajah(RAJAH_28, "Halaman 28 — Thilasm اخ ح ح لم صر", "Blok 3 baris `اخ ح ح ح... لعله له لم لم` + `لم صر صر ص ص...` + `لك ك ك !! طو طو اكر طو طر ه٥` + titik. Bawa di kepala & bawah ambang. HANYA blok (2884x1176 px, 495KB, 4x).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 29 — Lanjutan + Jalb Syam`atain — Picture 014 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "شيخ الروحانيين\\nالشيخ عطية عبد الحميد\\nنسألكم الفاتحة والدعاء\\nباب محبه مجرب صحيح والله لا شك فيه\\nبسم الله ابدء كلامي واصلي في الثاني على من بحبه ويجب اتباع سنته ناداني محمد\\nالنبي الظاهر صلاة الله وسلامه عليك وعلى ال بيتك الطاهرين وعلى اصحابك التابعين\\nبإحسان الى يوم الدين امين صلى الله عليه وسلم...اما بعد ,, لمن اراد ان ينعم بحب\\nالمحبوب يكتب بالمداد الطاهر المعروف لدينا جميعا قوله تعالى وداود وسليمان اذ يحكمان\\nفي الحرث اذ نفشت فيه غنم القوم وكنا لحكمهم شاهدين كذلك حكمت وملكت محبة فلان\\nابن فلانه في قلب فلانه بنت فلانه هل اتى على الانسان حين من الدهر لم يكن شيئا\\nمذكورا انا خلقنا الانسان من نطفة امشاج نبتليه نبليه نبتليه كذلك يبتلي او تبتلاى فلانه\\nبنت فلانه بمحبة فلان ابن فلانه بالمحبه الدائمه بدوام ملك الله تم\\nوكمل على وضعه الصحيح وفهما الله واياكم على كل ما هو في الخير دائما ان شاء الله\\nاللهم لا تكلنا الى احد غيرك طرفة عين بجاه النبي الامين\\nجلب الشمعتين\\nاكتب على شمعتين الاتي\\nعلى الاولى : ومن الجن من يعمل بين يديه بإذن ربه الى الشكور توكلوا يا خدام هذه\\nالايات بجلب وتهيج فلان بن فلانه\\nوعلى الثانية : ومن الجن من يعمل بين يديه بإذن ربه الى الشكور بمحبة فلانة بنت فلانة\\nومن الجن من يعمل بين يديه بإذن ربه الى الشكور ثم اطلق الجاوي والكسبره واللبان الذكر وعزم\\nعليهما حتى يلتقيان ثم اشعل الشمعتين فان المطلوب يأتى سريعا وجرب وحكم والعزيمه\\nهى الايه التى كتبتها على الشمع بدون عدد", "Syaikh Athiyah — Mohon Fatihah. BAB MAHABBAH SHAHIH (sambungan doa): Bismillah awali kalam, shalawat kedua kepada pembawa sunnah Muhammad Nabi Zhahir... Bagi ingin dicinta, tulis tinta suci firman ‘wa Dawuda wa Sulaiman idz yahkumani fil harts...’ demikian kuhukumi cinta Fulan di hati Fulanah, ‘hal ata ‘alal insani... inna khalaqnal insana min nuthfatin amsyaj...’ demikian diuji Fulanah dengan cinta kekal selama kerajaan Allah. Doa ‘La takilna... bi-jahil Nabi.’\\nJALB SYAM`ATAIN: Tulis di 2 lilin — Lilin1: ‘wa minal jinni... ilas Syakur — tawakkalu bi-jalbi Fulan.’ Lilin2: ‘... bi-mahabbati Fulanah.’ + ulang ayat ketiga — bakar jawi+ketumbar+luban, azimah sampai lilin bertemu lalu nyalakan — datang cepat, tanpa hitungan.")
add_block_box('Teks Arab Asli - Catatan Syam`atain', "ملحوظه\\nتضع كل شمعة في يد ثم تضع اليدين على الركب وانت مستقبل القبلة ثم تعزم ثم تعزم فان اليدين\\nيجتمعان فعندها اشعل الشمعتين\\nباب جلب قوى", "Catatan: Tiap lilin di tiap tangan, tangan di lutut menghadap kiblat, beri azimah — maka tangan akan bertemu — saat itu nyalakan. BAB JALB KUAT (berikutnya).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 30 — Jalb Figur Jim 50 Luban & Sumbu Humazah — Picture 015 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "تأخذ على بركة الله تعالى ورقة بيضاء وتشخص منها شخصين وبخور عمال وهو\\nالذكر وهو ان تأخذ 50حمصة لبان ذكر وتكتب عليها حرف الجيم (( ج )) وهذا ما\\nعلى الشخصين وبه تعزم تقول جلبت بجاه جلال الجبروت بعزة العظمة وبالكبرياء و\\nمن تجلى للجبل فجعله دكا وخر موسى صعقا جلبت محبوبي من مطلوبي لأى حبيب\\nالقريب المحيب اجب ياطلفايل خادم حرف الجيم بما فيك من الشر والثلجج بتلجلج\\nوبجلطننج وفولحنج وعولحنح وارجحنح برجحنح كرجحنح الشمس في الوهيج جعلتك جوا\\nواقسمه عليك برب العباد سبحان من ليس كمثله شياء وهو السميع البصير...\\nملحوظة\\nتحرم من كل شخص ورق خرم من جانب الصدر الجانب اليمين ويوضع فيهم خيط ابيض\\nمثل حبل الكتان او من القطن وتعزم عليهم حتى يقفوا الشخصين وينجمعوا فهذه علامة\\nالاجابة\\nومن الفوائد الجليلة للمحبة والجلب\\nتأخذ قطعة من أثر المطلوب وتكتب عليها وبل لكل همزة الى نار وتوكل اجلبوا كذا الى\\nمحبة كذا الواحا العجل الساعتو الكتابة بمسك وزعفران وماء ورد وتعملها فتيلة وتوقد\\nفي سراج بدهن الياسمين مقايلا لبيت المطلوب وتعزم عليه بما يأتى 21 مرة وأنت تبه\\nبعد منقوع في ماء ورد وهو ان تقول اعزم عليكم أيها الأرواح الروحانية المتوكلين\\nبهذه الفتيلة أنت يادهنش وأنت يا زوبعة وأنت يا لوبعة وأنت يا مهقال وأنت يا عبدان\\nوان يا سيدوك بالذى جل وارتفع واثقن ما صنع وشتت وجمع وأمر البرق فلمع والغيث\\nفهمع وكلم موسى فاستمع وتجلى للجبل فجعله دكا وخر موسى صعقا ساجدا راكعا من\\nالخوف والفزع فقال الله تعالى يا موسى ) إنى انا الله لا إله إلا انا خالق السماوات", "JALB DENGAN 2 FIGUR: Ambil kertas putih bentuk 2 figur, ambil 50 luban dzakar tulis حرف ج di atasnya — yang ditulis pada figur + azimah ‘Jalabtu bi-jahi Jalal Jabarut... Tajalla lil jabal... Jalabtu mahbubiy... ya Thalthafayil khadim harf Jim... Taljuj... Syams fil wahij...’ — sumpah demi Rabb ‘laysa kamitslihi...’ Catatan: lubangi dada kanan tiap figur, masukkan benang putih linen/kapas, azimah sampai figur berdiri bertemu = tanda terkabul.\\nFAEDAH AGUNG LAIN: Ambil atsar tulis ‘wailun likulli humazah ila nar’ wakilkan ‘ajlibu kaza ila mahabbat kaza — Al-Waha...’ tulis misk+za‘faran+mawar jadi sumbu nyalakan di lampu Yasamin hadap rumah target, azimah 21x sambil rendaman mawar: ‘A‘zim ‘alaikum ayyuhal arwah... ya Dahnisy ya Zau‘ba‘ah ya Lau‘ba‘ah ya Mahqal ya ‘Abadan ya Sayyiduk... kallama Musa... tajalla... kharra Musa saajidan... fa-qala Allahu ya Musa inni Ana Allah... Khaliqis Samawat...’ (sambung Hal.31).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 31 — Lanjutan Sumbu + Wafaq 693 Mutsallats Tijani — Picture 015 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "والأرض ) أقسمت عليكم يا خدام هذه الأسماء بالإسم الذى خلق الله به البحر العجاج\\nفهاج وماج وتلاطم بالأمواج وصار كالليل الداج فسبحت حيتانه واضطربت أركانه من\\nهيبة الله ذى الجلال والإكرام بديع السموات والأرض عزمت عليكم بكهيعص وحم عسق\\nوبطه ويس ويسور ن وبص ويسورة ق والقرآن وبطلسم القرآن وبسورة الرحمن\\nوالحواميم والدخان والطور وكتاب مسطور في رق منشور والبيت المعمور والسقف\\nالمرفوع والبحر المسجور ان عذاب ربك لواقع ماله من دافع ) وانه لقسم لو تعلمون\\nعظيم ) أن ( تسرعوا وتهيجوا كذا كذا بحق هذه الأسماء والأقسام وإلا يرسل عليكما\\nشواظ من نار ونحاس فلا تنتصران أو يرسل عليكم صاعقة مثل صاعقة عاد وثمود\\nفتنكو كما أخبر الله في القرآن فانما خر من السماء فتخطفه الطير او تهوى به الرياح\\nفي مكان سحيق \"إلا ما هيجتم كذا كذا بحق هذه الأسماء فإن خالفتم رميتكم بشهاب\\nثاقب وشواظ من نار فتلتهبوا كما تلتهب هذه الفتيلة حتى تأتوا بكذا الى كذا بحق ايها\\nشراهيا ادوناى اصباؤوت ال شداي الواحا2 العجل2الساعة2\\nباب محية وجلب وعطف بين المراة وزوجها\\nوهو سريع الإجابة لكل أمر من جلب خير ودفع كل شر تركب مثلث وهو عدده 693\\nوتوكل بما تريد حول الجدول وهو مدور وقوله أهم سقف حلع يص طرن وعلقه في\\nالسبيية من عيدان الرومان الحلو ويبخر بالكندر والقزبور والجاوي وعنبر وأنت نتلو\\nعليه الإسم الأعظم المذكور عدد 1111 فان الوفق يدور فإذا دار فأعلم بأن الحاجة التى\\nوكلت عليها إنقضت سواء كان خيرا لم شر وهذه من مجربات التجاني الكبير وهو أن\\nنطرح من العدد 12 ونقسمه على 3 وادخل في بيت الواحد بزيادة الى بيت الياء ثم الى", "Lanjutan sumpah sumbu: ‘...wal ardh) uqsimu ‘alaikum bi-Ism alladzi khalaqa bihar ‘ajjaj... tasabbaḥat hittaanuh... bi-Kaf Ha Ya ‘Ain Shad Ha Mim ‘Ain Sin Qaf Thaha Ya Sin... wa tilasm Qur’an Ar-Rahman Hawa-mim Dukhan Thur kitab mastur... inna ‘adzaba Rabbika lawaqi‘... wa innahu la-qasamun... an tusri‘u wa tuhayyiju kaza bih haqq... illa yursil ‘alaikuma syuwaazh... au yursil shaa‘iqah ka-‘Ad wa Tsamud... illa ma hayyajtum kaza... fa-in khalaftum ramaitukum bi-syihab tsaqib... ka ma talta hib hathihil fatilah hatta ta’tu bi-kaza — bi-haqqi Ahya Syarahya Adonai Ashba-ut Al Syaddai — Al-Waha2...’\\nBAB MAHABBAH-JALB-‘ATHF SUAMI ISTRI: Cepat untuk tiap kebaikan & tolak kejahatan. Susun wafaq **mutsallats 693**, wakalkan sekelilingnya yang bundar, ucap ‘Ahammu Saqafa Hala‘ Yash Tharan’ gantung di anyaman ranting delima manis asap kundur+ketumbar+jawi+anbar sambil baca Ism A‘dham 1111x — maka wafaq akan berputar, jika berputar hajat selesai, baik/buruk. Dari mujarrabat Tijani Kabir: kurangi 12 bagi 3 masukkan di bait Alif + ke Ya’... (bersambung Hal.32 Picture 016 wafaq 693).")

# FOOTER FOR PDF
pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 32 — Wafaq 693 Huruf Nur + 7 Barwat + Ruju` Zauj — Picture 016 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Wafaq 693 lanjut', "الجيم ثم غلى الدال ثم إلى الهاء ثم إلى الواو ثم إلى الزين ثم إلى الحاء ثم الى الص\\nودور حوله الحروف النورانية أهم سقف حلع يص طرن حروف مفرقة\\nباب محبة وجلب حريق على 7 بروات\\nأكتب على سبعة أوراق وتضع في كل ورقة بخور طيب واجرقهم في النار ورقة بعد\\nولا تضع الورقة الثانية إلا بعد إنتهاء الأولى إلى كذا حتى نهاية الورق\\nالورقة الاولى : هيور 3 طرش 3 بطرش 3 أهطم فشز يا روحانية هذه الأسماء بحق\\nعليكم وطاعتها لديكم اجلبوا كذا إلى كذا بالمحبة والمودة القوية الدائمة الشديدة قبل\\nتحرق هذه الأسماء الواحا العجل الساعة\\nالورقة 2: برش 3 مرش 3 وكمالة التوكيل\\nالورقة 3: أيكموش 3 إزرش 3 زربوش 3 وكمالة التوكيل الذي فوق هو هو الورقة\\nفيونش 3 بيوش 3 إلش 3 الورقة 5: طهفش 3 قمش3 الورقة 6: طيوش3 طوش3\\nطونش 3الورقة 7: مهليوش 3 مهطايش 3 ونفس التوكيل على كل ورقة", "Lanjutan Wafaq 693: Jim→Dal→Ha’→Waw→Zai→Ha’→Shad, kelilingi huruf Nur ‘Ahammu Saqafa Hala‘...’ huruf terpisah. BAB 7 BARWAT HARQ: tulis 7 kertas, tiap + bukhur wangi, bakar satu-satu — jangan letak lembar2 sebelum 1 habis. W1: Hayur3 Tharasy3 Bathrasy3 Ahthama... ya ruhaniyyah dengan hak... bawalah si anu dengan kasih kuat kekal sebelum terbakar — Al-Waha... W2: Barasy3 Marasy3 ... W3: Aikumusy3 Izrasy3 Zarbusy3 + tawkil Huwa Huwa ... W5-7: Thahfasy3 Qamasy3 ... Thayusy3 Thusy3... Thunsy3... Mahlayusy3 Mahthayisy3 + tawkil sama.")
add_block_box('Teks Arab Asli - Ruju` Zauj', "باب رجوع الزوج إلى زوجته\\nبسم الله قبل يدي والله الأمر من قبل ومن بعد اللهم إن السماء سماؤك والأرض أرضك\\nوالسهل سهلك والبر برك والبحر بحرك والجبل جبالك والأودية أوديتك والوعر وعرة\\nوالعباد عبادك أنت لا إله إلا أنت وحدك لا شريك لك أسألك اللهم بنور جلالك وعظمتك\\nسلطانك أن تجعل البلدان والمدن والقرى ضيقة على فلان بن فلانة حتى يرجع إلى\\nزوجته فلانة بنت فلانة اللهم إجعل عليه الدنيا أضيق من حلقة الخاتم على الأصابع\\nيرجع إلى زوجته فلانة بنت فلانة وإلى هذا المكان الذي علق فيه كتابي هذا ونفخ", "BAB RUJU` ZAUJ: ‘Bismillah sebelum tanganku, urusan milik Allah. Ya Allah langit-Mu bumi-Mu... sempitkan negeri kota desa kepada Fulan bin Fulanah sampai kembali kepada istrinya Fulanah ... jadikan dunia sempit seperti cincin di jari... kembali ke tempat kitabku digantung...’ (lanjut Hal.33).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 33 — Lanjutan Ruju` + Irsal Haq — Picture 016 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "الصور فجمعناهم جمعا وهو على جمعهم إذ يشاء قدير اللهم حير فلان بن فلانة كما حيرت\\nالجمل في عقلي والطير في وقره والولد على محبة أمه حتى يرجع إليها ومكانها الذى\\nخرج منه ونفخ في الصور فإذا هم من الأجداث إلى ربهم ينسلون قالوا ياويلنا من بعثنا\\nمن مرقدنا هذا ما وعد الرحمن وصدق المرسلون إن كانت إلا صيحة واحدة فإذا هم جميعا\\nلدينا محضرون ولا تحويه الأرض ولا تحويه دار ولا مكان حتى يرجع إلى زوجته فلانة\\nبنت فلانة اللهم كما ردت موسى الى امه وكما ردت يوسف على يعقوب وكما ردت العفية\\nعلى جسد أيوب أرية جال قدرتك بقدرتك وجالك يا قادر يا مقتدر اللهم يا جامع الشتات\\nيا جامع الناس لا ريب فيه إن الله لا يخلف الميعاد رد كذا إلى كذا إلى مكانه الذى خرج\\nمنه واجمع شمله بشملها إنك على كل شىء قدير الواحا العجل الساعة\\nبخوره : لبان ذكر وكزبرة وجاوي ويكتب ويعلق في الهواء والله الذى لا رب غيره لو كان\\nفي عمق البحار يأتي الزوج ويرجع إلى زوجته\\nباب إرسال لجلب الحق\\nإذا كان لك حق عند إنسان من مال وغير المال مثل البناء والأرضى وهو عون شديد إذا\\nأردت العمل به تصوم يوم السبت برياضة كاملة وتفطر عند المغرب ثم تأخذ جريدة\\nخضراء وتكتب عليها سورة والعاديات ضبحا إلى آخرها وبعد العشاء تأخذ مجمرة للفحم\\nجديدة ويخورك الصندل قوي وعلى نار قوية وأنت ماسك الجريدة في يدك", "‘...kumpulkan mereka, Allah Maha Kuasa, Ya Allah bingungkan Fulan seperti bingung unta, burung, anak kepada ibu sampai kembali — ‘wa nufikha fish shur... ya wailana... hadza ma wa‘ada Ar-Rahman... in kanat illa shaihah...’ tidak ditampung bumi/rumah sampai kembali kepada Fulanah — seperti Kembalikan Musa kepada ibu, Yusuf kepada Ya‘qub, kesehatan Ayub — ya Jami‘... rudda kaza... Al-Waha... Bukhur: luban, ketumbar, jawi, gantung di udara — demi Allah andai di dasar laut suami akan kembali.’\\nBAB IRSAL HAQ: jika punya hak harta/bangunan/tanah — puasa Sabtu riyadah, buka maghrib, ambil pelepah hijau tulis Al-‘Adiyat sampai akhir, setelah Isya ambil perapian arang baru bukhur cendana kuat di api menyala sambil pegang pelepah ... (sambung 70x qasam).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 34 — Qasam Murrah + `Aqd Naum — Picture 017 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "عمياخ أجب يا مرة وتوكل بكذا فإني سلطتك عليه نزلت ملائكة الغضب على من\\nفسعى ومن يشرك بالله فكأنما خر من السماء فتخطفه الطير أو تهوى به الرياح فهو\\nفي مكان سحيق الواحا العجل الساعة ) وهذا هوم الإصراف إنصرف بسلام يامرة وإن\\nبكذا وإفعل ما أمرتك به بحق هذه الاسماء قياش2 كياش2 عديوش 2 بخش 2 توكل\\nالسيد مهجيائيل باصرف مرة إلى كذا وكذا اجب يا مرة وافعل ما امرتك به بحق\\nالاسماء ولا تخالف فتحرق بنار السموم هيا الواحا العجل الساعة\\nباب عقد نوم ومحبة واعلم حبيبك لم ينم قط\\nإذا أردت العمل به فتفعل شخص من ورق مثل المطلوب وتكتب على رأسه فلان بن\\nواكتب على جبهته فإذا نفر في النقور وعلى يده اليمنى غلت أيديهم وعلى يده اليسرى\\nقدر الوش وعلى رجله اليمنى ميططرون وعلى الشمال كشطورش كشطاروش وخل\\nصدره الخناس الذى يوسوس في صدور الناس ثم تدق مسمار في صدر الشخص", "Lanjutan qasam Hal.33: ‘Amiyakh ya Murrah... nazalat malaikat ghadab... man yusrik billah fa-kaannama kharra... fi makani sahiq Al-Waha...’ Israf: ‘Insharif bi-salam ya Murrah... Qayasy2 Kayasy2 ‘Adyusy2 Bakhsy2 — wakalkan Mahjayail...’\\nBAB ‘AQD NAUM: buat figur kertas seperti target, tulis kepala nama, dahi ‘fa-idza nuqira fin-naqur’, tangan kanan ‘ghullat aidihim’, kiri ‘Qadar al-Wasys’, kaki kanan ‘Mithathrun’, kiri ‘Ksythurusy’, dada ‘Al-Khannas...’ lalu tancapkan paku di dada ... (sambung Hal.35 7 sutra).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 35 — Tashrif 71x + `Aqd Naum Maimun — Picture 017 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "معالق وضع البخور بجانبيها واقرأ العزيمة الاتية بنفسها 71 مرة ثم علقها للريح فان\\nالمطلوب لا يبطئ الا مسافة الطريق مجرب صحيحكم ليكم العزيمة بسم الله الملك الودود\\nالجامع المعيد مقلب القلوب والابصار علام الغيوب الذي قال وقوله الحق وضاقت عليهم\\nالارض بما رحبت وضاقت عليهم انفسهم وظنوا ان لا ملجأ من الله الا اليه فضرب بينهم\\nبسور له باب فيه الرحمة وظاهره من قبله العذاب توكل ياميمون الطيار ويا ميمون\\nالغواص ويا ميمون الاسود ويا ميمون الازرق ويا ميمون ابا نوخ السحابي السياف\\nوتوكلوا واجلبوا واخطفوا باياديكم القوية فلانة بنت فلانة صاحبة هذه الصورة الى محبة\\nومودة وطاعة وعشق ووصال وجماع ونكاح فلان ابن فلانة وافعلوا ذلك مسر عين في\\nالوقت والساعة هذهفبهرة عزيز فلا عزيز غيره ولا اعز منه وبحق انموه 2 هاتج 2\\nباشمخ شمخ شماخ شامخ شموخ 2 اشخ كمشيخ كاشخ اشخ اجيبو وتوكلوا وعجلوا", "Lanjutan tashrif: taruh bukhur di sisi, baca azimah 71x lalu gantung angin — target tidak lambat kecuali jarak jalan — sahih. Azimah: ‘Bismillah Al-Malik Al-Wadud Al-Jami‘ Al-Mu‘id ... wa dhaqat ‘alaihim arth... an la malja-a... fa-dhuriba bainahum bi-sur...’ wakalkan Maimun Thayyar/Ghawwash/Aswad/Azraq/Aba Nukh As-Sayyaf bawalah Fulanah pemilik gambar ke cinta/nikah Fulan segera — dengan Hatzifbaharah ... Ba Syamakh... Ashakh Kamsyakh...’ (sambung sampai Hal.36).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 36 — Ta`qid Naum 7 Kerikil + Fatihah Malaikat — Picture 018 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Ta`qid', "وهو إذا أردت العمل به أن تجلس لوحدك في مكان خالى من الناس بعد العشاء وتنام\\nالعزيمة الآتية على 7 سبع حصوات لبان ذكر أبيض وعلى كل حصوة من اللبان\\nمرات وترميها في النار وتفعل ذلك الى تمام السبع 7 حصوات لبان وتنام فإن المطلوب\\nينام ولا ينقفل له جفن من شدة المحبة والقلقت حتى يأتيك سريعا وهذا ماتمزم به يشتم\\n2طش2 خط2 طحطيح2 بهكويل2 أجب ياريوش وتوكل بتهييج وجلب وعقد\\nكذا وكذا واعقدوا نومهما بمحبته حتى لاتنام لإتمام لافى ليل ولا فى نهار من شدة القلق", "Duduk sepi setelah Isya, baca azimah pada 7 kerikil luban putih, lempar ke api satu-satu, tidur — target tidak terpejam karena rindu: ‘2-Thasy 2-Khath 2-Thahthah 2-Bihakwil ... Ya Rayusy ... ikat tidurnya ...’")
add_block_box('Teks Arab Asli - Yaqutah awal', "بمحبته بحق نهرطيح2 نمليح2 ق ليح2 شلشميخ2 أن كانت إلا صيحة واحدة فإذاهم\\nلدينا محضرون الواحا2 العجل2 الساعة2", "‘... Nahrathih2 Namlih2 ... in kanat illa shaihah ... Al-Waha...’")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 37 — Doa Fatihah Malaikat Lengkap — Picture 018 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "المتكبر أجب يا جبرائيل ... هوزح ... ملك يوم الدين يا مقلب القلوب ... سمسائيل ... طيكل ... ميكائيل ... منسع ... صرفيائيل ... فصقر ... عنيائيل ... شنئخ ... ميمون أبانوخ ... دضظغ", "Lanjutan Fatihah tiap ayat dengan malaikat penjaga Arsy (pola sama Hal.19) — Jibra’il Hawzah, Samsa’il Thaykal, Mika’il Munsa‘, Sharfaya’il Fashaqar, ‘Anyā’il Syannakh, Maimun Dhadhazagh — ditutup Arwah Ruhaniyyah ... Al-Waha...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 38 — Yaqutah Lanjutan + Alam Nasyrah Wanita — Picture 019 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "وأفعلوا كذا بحق السبع وبحق الأسماء العظام ... وألقيت عليك محبة منى ... هذا هو خاتمها ولقد أخرجناها للزوجة الغضبانة ... التيجاني وهى شغله اليومى ... الم تشرح للنساء فقط بسم الله الرحمن الرحيم اختى الزوجة الصالحة انصحك ان تستخدمى هذا العمل لزوجك هذا الزمن الصعب تكتبي سورة الم نشرح 3 مرات بماء الورد والزعفران", "Tawkil ‘hak Saba‘... wa alqaytu ‘alaika mahabbatan minni’ 4x wafaq — dari Tijani wirid harian — suci wudhu 2 rakaat + bukhur luban jawi gaharu — baca 7x — mujarrab. Alam Nasyrah khusus wanita: tulis 3x dengan mawar za‘faran + garam dirham + Asma 99x — campur celak/inai.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 39 — Yaqutah Ats-Tsaminah Doa Panjang — Picture 019 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "اللهم يا واحد فى اسمائه يا الله و يا منفرد ... يا من كلم موسى ... يا من رفع ادريس ... عن ايوب ... رد يوسف ... اللهم اقلّ قلب فلان بمحبة و اجعل فى قلبها الرقاقة و الرحمة ... فاكشفنا عنك غطائك فاقبصرك اليوم حديد يكاد البرق الى قامو 7 مرات توكيل و من الناس من يتخذ من دون الله اندادا", "Doa Yaqutah Tsaminah — tawassul panjang Ya Allah Ya Wahid... Ya Man kallama Musa... sampai Ya Man allafa qulub mu’minina — wa auhaina ila Musa... kath-thaudil ‘azhim — Allahuma aqill qalba Fulan... 7× qamu tawkil — wa minan nasi man yattakhidzu... qala rajulani...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 40 — Tawassul Huruf + Faedah Ghazal — Picture 020 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "هو الذى ايدك بنصره ... هل اتى على الانسان ... اسالك بالالف المعطوف ... و بصاد الصدق و بضاد الضياء ... دخلت فى كنف الله تشفعت برسول الله ... اللهم انى اسالك بحرمة مضيائك و بحمالة عرشك الى ما سخرت لين قلبها له كما لينت الحديد لداوود ... فائدة تهيج رأس العفريت تكتب فى رق غزال بمسك وزعفران وماء ورد وتبخرة بكندر وميعة سائلة وتعزم بالبرهتية 21 مرة بعد صرف العمار ثم تعلق فى الهواء مع اثر المطلوب", "Tawassul huruf hija’iyah 28 + ‘dakhaltu fi kanafillah...’ + ‘Allahumma inni as’aluka bi-hurmati...’ lunakkan hati seperti besi Dawud + sujud Qur’an — tulis jadwal & putar nama — beri minum taat. Faedah Ghazal: kulit kijang misk za‘faran mawar kundur mi‘ah cair + Barhatiyyah 21x setelah sharf ‘ammar gantung bersama atsar.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 41 — Mahabbah 3 Rambut 131x + Rajah — Picture 020 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "محبة عجيبة إذا أردت ذلك فخذ ثلاث شعرات من رأس المطلوب ثم تكتب سورة الفاتحة بالصفحة الايمنة توكل باسم الطالب والمطلوب وتوضع الشعر فى قلب الورقة بعد البخور وتحمل وهذا ما تكتب بسم الله الرحمن الرحيم الرال كهيعص مالك يوم الدين طسم طسم طسم اياك نستعين الم الم المر اهدنا الصراط المستقيم يس ق ن صراط الذين أنعمت طس طسم عليهم غير المغضوب عليهم والاضالين امين امين امين توكلوا يا خدام هذه السورة الشريفة والاحرف النورانية والقو محبة فلان ابن فلانة فى قلب فلانة بنت فلانة حتى لايستقر لها حال ولا قرار ولا مكان ولا يأخذها هدوء ولا صبر عن محبة وعشق وطاعة فلان ابن فلانة بحق سر الفاتحة وما فيها من الاسماء العظماء الاحرف النورانية ثم تعرم عليها 131 وشمعها وقابل بيها من عملت له تری عجبا", "Mahabbah ‘Ajibah: ambil 3 rambut, tulis Fatihah di halaman kanan, wakukan nama, letak rambut tengah setelah bukhur — yang ditulis Bismillah... Alif Lam Ra Kaf Ha Ya ‘Ain Shad Maliki... Tha Sin Mim 3x Iyyaka nasta‘in... Ya Sin Qaf Nun... Tha Sin Tha Sin Mim... Amin 3x — tawakkalu ya khuddam... jatuhkan cinta Fulan bin Fulanah di hati Fulanah sampai tidak tenteram — dengan sirr Fatihah & Huruf Nur — azimah 131x nyalakan hadapkan — lihat ajaib.")
add_rajah(RAJAH_41, "Halaman 41 — 2 Figures Top Mahabbah `Ajibah", "2 Rajah atas judul — Atas figur manusia + angka `19 9 111...` + `حـ مو...`, Bawah 2 sigil silang `X` + `77< حجه...` + 5 sigil. Untuk kulit kijang Hal40 + 3 rambut Hal41. HANYA 2 gambar (3092x1708 px, 497KB, 4× putih).")

# ========== BATCH 09: Hal042-046 (Picture 021-023) ==========
pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 42 — Qomash Mahabbah 71x + Azimah Surat Jin — Picture 021 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "ليحضرو خدام سورة الجن الشريفه والطريقه هي تحضر قطعة قماش من أثر المطلوب والطالب مثلا قطعة ثوب من هذا ومن هذا تكتب عليها بقلم السبورة الأسود آية عَلَيْكَ مَحَبَّةً مِّنِّي حروف مفرقة وتكتب على ثوب المطلوب فلان ابن فلانة من غير وتوصل القماشتين بوصلة في النص وتكتب عليها يعشق وتكتب على الوصلة الثانية الطالب فلانة بنت فلانة ثم تبخرها بفلفل أسود وأبيض وشب وتقرأ عليها الآية 71 (وَأَلْقَيْتُ عَلَيْكَ مَحَبَّةً مِّنِّي) ثم تأتي بعد أن تبخرها بما تقدم تضعها في قدر ماء يغلي وتضعها بداخله ولا تنسى صرف العمار بسورة الزلزلة مرة واحدة حتى كلمة أشتاتا ثلاثا 7 مرات ولا تنسى التحصين بآية الكرسي 7 مرات قبل العمل وقبل الصرف مع آخر من سورة البقرة ثم بعدما تضع القماش بعد تبخيره في الإناء تقرأ عليه سورة الجن وطريقة العزيمة بسورة الجن تقول (أعزم عليكم بقل أوحي إلي أنه استمع نفر من حتى آخر السورة ثم بعد كل مرة تقرأ سورة الجن تقرأ التوكيل والقسم الآتي (توكلوا سورة الجن الشريفة أعزم وأقسم عليكم بحق من خلقكم من نار السموم أن تلقوا فلانة بنت فلانة في قلب فلان ابن فلانة وتثبتوها للأبد وأنكم والله لتقدرون على وبحق هذه السورة الشريفة عليكم وطاعتها لديكم إلا ما أجبتموني في الحال وقضيتم حاجتي الوحا 2 العجل 2 الساعة 2 بارك الله فيكم وعليكم) بعد ذلك تكمل حتى نهاية السبع مرات قراءة السورة ولا تنسى بعد كل مرة قراءة تقرأ التوكيل والقسم ثم تقول (وَلَقَدْ عَلِمَتِ الْجِنَّةُ إِنَّهُمْ لَمُحْضَرُونَ) 71 مرة وتختم بالصلاة على النبي وما أن الماء حتى يبدأ مفعول العمل بإذن الله والسلام ختام وأرجو من الله العلي العظيم يستخدمها من جار عليها زوجها أو ظلمها أو هجرها لأنها لا تستخدم", "Qomash (kain) mahabbah 71x — Ambil kain atsar target & thalib, tulis با قلم سبورة hitam WA ALQAYTU ‘ALAIKA MAHABBATAN MINNI huruf mufarraqah + nama, sambung tengah tulis YA‘SYAQ, sisi kedua nama thalibah, ukup lada hitam/putih+tawas, baca ayat 71x, masukkan ke periuk mendidih. Jangan lupa sharf ‘ammar Zalzalah sampai ASYTATAN 3x tiap lafaz 7x, tahshin Ayat Kursi 7x + akhir Baqarah. Baca Surat Jin 7x, tiap selesai baca tawkil/qasam Jin Syarifah sumpah demi Pencipta dari nar samum agar lempar cinta ke hati Fulan bin Fulanah kekal — Al-Waha2... lalu WA LAQAD ‘ALIMATIL JINNAH 71x tutup shalawat. Hanya untuk wanita dizalimi suami.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 43 — Ya Dauuh 21x + Khatam Mutsallats 28x Barhatiyyah — Picture 021 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "محبة وقبول تكتب وتحمل ويعلق في الهواء يدوح 21 مرة توكل يادوح يا صاحب الفتوح بحق آدم ونوح والنبي الممدوح وفاتح افتوح افتح قلب فلانة إلى عشق فلان سيجعل لهم الرحمن ودا وألقيت عليك محبة مني إلى ...عيني الله نور السموات والأرض بشمهلا 2 شمهلاب 2 يا عباد الله الصالحين ويا رجال الله في أرضه الذين يردون الضالة ويهدون السبيل أقسمت عليكم بهذه الأسماء وهي أسماء نورانية الاما ايتم ووضعتم محبة فلان ابن فلانة في قلب فلانة بنت فلانة حتى لا يستطيع عن رؤية وجهها صبرا إن نام قياما وإن قام هيجانا وإن هاج جنونا وإن تجنن طيروه وإن طار اجلبوه بمحبة وعشق وطاعة وسماع قول فلانة بنت فلانة في منزل فلانة بنت فلانة ارموه واطرحوه ولا تدعوه يقر له قرار ولا يأخذه اصطبار لا في ليل ولا في نهار فلا طعام يهنيه ولا شراب يرويه ولا قرار يأتيه العجل العجل قبل فوات الوقت وقبل انتهاء الأجل كلما دار الفلك تجري به الشمس ويأتي به القمر ويجيبه عطارد ويجننه المريخ واذناب المشترى وعشقة الزهرة وانجلة الزهرة وانجلة زحل توكلو يا خدام الأيام السبعة العلوية وأعوانكم الملوك الأرضية وخدام الفلك الدوار وخدام الساعات وطلسم الليل والنهار ولا تحلوا عزيمة فلان ابن فلانة حتى يأتي خاضعا ذليلا إلى فلانة بنت فلانة وإلا يرسل عليكم شواظ من نار ونحاس فلا تنتصران فلا تنتصران الوحا العجل الساعة جلب ومحبة وهو أن تصور صورة من أنثى وذكر من ورق غزال وتنزل الخاتم المثلث كما أضعه لك تضع الذكر ثم تحط فيه قطعة سكر نبات وتلقي الأنثى على الذكر على بعضهم لبعض وتنزل البرهتية دائرة في ورقة بيضاء وتقرأ عليهم البرهتية عدد 28 مرة والبخور صاعد وهو لبان ذكر", "Mahabbah Qabul 21x Ya Dauuh digantung udara — tawkil panjang Adam-Nuh-Nabi Mamduh, RAHMAN WUDDA, ALQAYTU... Nur Samawati, BISYAMHALA, ya ‘ibad shalihin rijaal — asma nuraniyyah ALAMA AYTAM letakkan cinta sampai tidak sabar lihat wajah — jika tidur berdiri, gelisah, gila, terbangkan tarik — jangan tenang siang malam tak enak makan/minum — falak Syams-Qamar-Utharid-Mirrikh-Musytari-Zuhrah-Zuhal — khuddam ayyam sab‘ah ulwiyyah, muluk ardhiyyah, falak dawwar, sa‘at, thilasm lail-nahar — datang tunduk hina atau syuwazh nar+ nuhas — Al-Waha... Jلب gambar 2 sosok waraq ghazal + Khatam Mutsallats + Barhatiyyah melingkar 28x bukhur sha‘id luban dzakar — gula batu ditimpuk.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 44 — Lanjutan Jلب Gambar + Shurah ALQAYTU & Jلب Lilin Murabbaah 100 — Picture 022 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "وبعد ذلك تحط الشخصين في الورق وتلف عليهم خيطا أبيضا وتدفنهم في محل مظلم لا أحد يرى فيه شمس ولا قمر وتنزل صورة الرجل وتنزل صورة الأنثى واسم الأنثى في صورة الرجل تكتب بزعفران وماء الورد ودم الأخوين وهذا صورة الرجل | صورة الأنثى - و ألقيت ح ب عليك - عليك فلانة مني محبة فلان و - ب محبة د ح مني - جلب الشمعة شمعة مربعة تكتب على كل وجه من أمين أقش 2 قال عفريت من الجن أنا آتيك به قبل أن تقوم من مقامك وإني عليه أمين الأسماء بجلب قشهوش 2 كشليخ 2 كيكوش 2 نوخ 2 يوع 2 توكلو ياخدام ثم احضر مائة حبة كذالك كذا بحق من قسم بمواقع النجوم وانه لقسم لو تعلمون من الفلفل وتغربها من فيك وتتلو من الفلفل يعني الإزار الأبيض وتوقد الشمعة وتأخذ كل بما تريد وتلقي في النار ال ى أن تفرغ مائة عليها ما كتبته على الشمعة بتمامه و جلب مجرب وصحيح الشمعة موقدة في مكانها إلى أن تنتهي حبة فإذا انتهيت اقرأ بعد صلاة العشاء إلى أن يحقق الله طلبك وملائكاتك على الله شريطة التكرار كل ليلة للصلح بين الزوجين مجرب", "Lilit 2 sosok benang putih kubur gelap tak kena matahari/bulan — tulis gambar pria/wanita za‘faran+mawar+dam akhawain — tabel huruf: WA ALQAYTU terbagi (atas). Jلب Lilin Murabba‘ah 4 sisi Amin Aqisya Qala ‘Ifrit... Qashhush Kashlikh Kikush Nukh Yau‘ — siapkan 100 lada, hembus + QS Waqi‘ah MAWAQI‘ NUJUM, nyalakan lilin lempar 1-1 ke api sampai 100 habis ditulis di lilin — shahih lilin tetap menyala. Baca ba‘da Isya tiap malam sampai hajat — lulus — untuk Shulh Zawjayn mujarrab.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 45 — Ayat Shulh Panjang + Tahyij 12x Kursi — Picture 022 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "بسم الله الرحمن الرحيم وَمِنَ النَّاسِ مَن يَتَّخِذُ مِن دُونِ اللَّهِ أَندَادًا يُحِبُّونَهُمْ كَحُبِّ اللَّهِ وَالَّذِينَ آمَنُوا أَشَدُّ حُبًّا لِّلَّهِ وَلَوْ يَرَى الَّذِينَ ظَلَمُوا إِذْ يَرَوْنَ الْعَذَابَ أَنَّ الْقُوَّةَ لِلَّهِ جَمِيعًا وَأَنَّ اللَّهَ شَدِيدُ الْعَذَابِ فَمَنْ خَافَ مِن مُّوصٍ جَنَفًا أَوْ إِثْمًا فَأَصْلَحَ بَيْنَهُمْ فَلَا إِثْمَ عَلَيْهِ إِنَّ اللَّهَ غَفُورٌ رَّحِيمٌ . وَإِنِ امْرَأَةٌ خَافَتْ مِن بَعْلِهَا نُشُوزًا أَوْ إِعْرَاضًا فَلَا جُنَاحَ عَلَيْهِمَا أَن يُصْلِحَا بَيْنَهُمَا صُلْحًا وَالصُّلْحُ خَيْرٌ وَأُحْضِرَتِ الْأَنفُسُ الشُّحَّ وَإِن تُحْسِنُوا وَتَتَّقُوا فَإِنَّ اللَّهَ كَانَ بِمَا تَعْمَلُونَ خَبِيرًا. وَإِنْ خِفْتُمْ شِقَاقَ بَيْنِهِمَا فَابْعَثُوا حَكَمًا مِّنْ أَهْلِهِ وَحَكَمًا مِّنْ أَهْلِهَا إِن يُرِيدَا إِصْلَاحًا يُوَفِّقِ اللَّهُ بَيْنَهُمَا إِنَّ اللَّهَ كَانَ عَلِيمًا خَبِيرًا يَسْأَلُونَكَ عَنِ الْأَنفَالِ قُلِ الْأَنفَالُ لِلَّهِ وَالرَّسُولِ فَاتَّقُوا اللَّهَ وَأَصْلِحُوا ذَاتَ بَيْنِكُمْ وَأَطِيعُوا اللَّهَ وَرَسُولَهُ إِن كُنتُم مُّؤْمِنِينَ رَبَّنَا وَأَدْخِلْهُمْ جَنَّاتِ عَدْنٍ الَّتِي وَعَدْتَّهُمْ وَمَنْ صَلَحَ مِنْ آبَائِهِمْ وَأَزْوَاجِهِمْ وَذُرِّيَّاتِهِمْ إِنَّكَ أَنتَ الْعَزِيزُ الْحَكِيمُ اللهم بحق هذه الآيات الشريفة اعطف قلب فلانة بنت فلانة على فلان بن فلانة بالمحبة الدائمة والألفة والعطف والحنان فسيكفيكهم الله وهو السميع العليم ولا حول ولا قوة إلا بالله العلي العظيم وصلى الله على سيدنا محمد وآله وصحبه وسلم تكتب هذا في ورقتين يوم الجمعة ساعة الزهرة بماء الورد والزعفران قد طرح فيه يسيرا من المسك ويخر عملك بالجاوي والعنبر و واحدة يحملها الطالب والأخرى تسقى للمطلوب فإنه لا يغرب عليه شمس ذلك اليوم حتى يتوصل الطالب بمطلوبة بمطلوبية فاتقي الله في عملك فائدة تهييج للمحبة عمل تهييج محبة مجرب يكتب بالحبر الروحاني قطعة قماش من الكتان والبخور مقل ولبان وجماجم ثمر الحنا ويعزم عليه بآية الكرسي 12 مرة ) تينانور 7 هيتامور 7 كيبانور 7 جهمانور 7 ) ثم يعزم توكلو خدام هذه الرقعة المباركة الشريفة وبما فيها من اسرار", "Ayat Shulh lengkap Baqarah165,182 Nisa128,35 Anfal1 Ghafir8 + doa i‘thif qalba Fulanah binti Fulanah ‘ala Fulan — fa-sa-yakfikahumullah... Jum‘at Sa‘ah Zuhrah mawar+za‘faran+sedikit misk, bukhur jawi+anbar, 1 dibawa thalib 1 diminum matlub — sebelum matahari tenggelam sampai. Faidah Tahyij mujarrab hibr ruhaniyyah kain kattan muqul+luban+jamajim henna, azam 12x Kursi + Tinanur7 Hitamur7 Kaibanur7 Jahmanur7 + tawakkalu khuddam ruq‘ah mubarakah...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 46 — Sambungan Tahyij + Jلب Sari 104x QulHu — Picture 023 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "شريفة بتهييج فلان ابن فلانة على فلانة بنت فلانة توكلوا ابتهيج روحانيته وفكره لمحبة فلانة بنت فلانة توكلوا خدام هذه الرقعة الشريفة المباركة بيتمتم وتعلم فلان ابن فلانة على محبة فلانة بنت فلانة الساعة الساعة الوحا العجل وانه لقسم تعلمون عظيم ثم يلف قطعة القماش على شمعة عسل ويوقدها بعد منتصف الليل يكون الناس نيام ويعزم بنفس ما ذكر ويكرر هذه الطريقة ثلاثة أيام وسيرى العجب تعلق روحانية المطلوب بالطالب بشكل لا يتصوره العقل من شدة المحبة والمودة اذا بظهر الغيب الفاضل الحبر الروحاني هو الزعفران وماء الورد وهو أساس في جميع الأعمال اما اذا كان البعض يكتبون الطلاسم بأمور أخرى فهذا ليس بالصحيح بخصوص التعزيم فبعد الكتابة واثناء الحرق بالعدد المذكور بدون زيادة ولا نقصان محبة وجلب سريع الاجابة بسم الله والصلاة والسلام على خير الأنام وهو مجرب ولا شك فيه تصور صورة من تريد من ورق وتكتب على رأس الصورة المطلوب واسم امه وقل هو الله احد وعلى يده اليمنى (الله الصمد) وعلى يده اليسرى (لم يلد) وعلى صدره (ولم يولد) وعلى رجله اليمنى مع فخذه (ولم يكن له) وعلى رجله اليسرى مع فخذه (كفوا احد) وتكون تلك الكتابة احرف مفرقة بغير طمس . وبين كل حرف (ع) وتوضع الشخص قدامك. وتعزم عليه القسم الآتي 104 مرة فإن الصورة تقوم على رجلها فتقول (بارك الله فيكم وعليكم) فهي علامة اجابة بحضور المطلوب والبخور لبان ذكر وكزبرة وهذا هو القسم (بهووتر كوش كوش قوش قوش نفخ نفخ هنوش طيوش اطى اتى اجب يا سيد اتى اجلب وهيج واسحب عقل فلان ابن فلان", "Sambungan tahyij — tawkil ibtahij ruhaniyyah+fikr — lipat kain pada lilin lebah nyalakan selepas tengah malam saat tidur, azam sama 3 hari lihat ajaib ta‘alluq ruhaniyyah tak terbayang. Hibr utama za‘faran+mawar dasar semua amal. Mahabbah Sari‘ mujarrab — gambar kertas, tulis kepala Qul Huwa, tangan kanan Allah Shamad, kiri Lam Yalid, dada Lam Yulad, kaki kanan Lam Yakun lahu, kiri Kufuwan Ahad — huruf mufarraqah bighair thams, antara huruf ‘ain (ع), hadapkan qasam 104x maka gambar berdiri — baraka Allahu — tanda ijabah. Bukhur luban+kuzbarah — qasam Bi-huwatar... Hanush Thayush...")

# ========== BATCH 10: Hal047-051 (Picture 023-025) 6 Rajah ==========
pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 47 — Ihsan Jلب Sari + Ihraq Laymunah — Picture 023 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "بمحبة فلانة بنت فلانة حتى لا ينام ولا ياكل ولا يشرب حتى يكون معها بين يديها طائعا ذليلا لجميع كلامها الوحا العجب الساعة 104 مرة وتقرأه الصورة فاعد العمل حتى تتحرك وتقوم الصوم الصورة وان ابطا العمل عليك والخدام فازجرهم بهذه الاية الشريفة (ويل لكل الاية الشريفة فستسمع ايات الله تتلى عليه ثم يصر مستكبرا كأن في اذنيه وقرا فبشره بعذاب اليم ) اقسمت عليكم يا خدام هذه الايات الشريفة اجلبوا كذا وكذا الى محبة كذا وكذا الوحا العجل الساعة واصراف الزلزلة الى اشتاتا ثلاث مرات وتكرر اشتاتا في كل مرة ثلاث مرات. احراق الليمونة مجرب وصحيح اكتب هذه الأسماء في ورقة واجعل في قلبها حصوة لبان ذكر ثم تحضر الليمونة وتقورها في رأسها وتعصر منها قليل من الماء ثم توضع داخلها الورقة المكتوبة واكتب مع الأسماء الطالب والمطلوب ثم توضع الليمونة في طاسة وضع معها زيت طيب وتكتب طلسم الطاسة بمسلة وضعها على النار وأنت تعزم إلى أن تحرق الليمونة فمتى احترقت احترق قلب المعمول له بالمحبة وهذا ما تكتب على الورقة ويا حبذا لو يكون على الأثر وهو هذا = لا لم لا تلم نفسك فيما مضى وتنترك البعد وتأتي الى الصديق وإن لم تأتي إلى كذا وكذا وميناك على جمرة بهارش 2 مع قارش 2 في حريق يلفقك في نار لها زفرة بشمشع مع زعزعان زعزعان في سحيق توكلو يا خدام هذه الأسماء وهيجوا كذا إلى كذا وكذا بحق اطمهفشذ وبحق جليش جليش إنه من سليمان وإنه بسم الله الرحمن الرحيم أن لاتعلوا علي واتوني مسرعين طائعين وهيجوا واجلبوا كذا وكذا بحق هذه الأسماء عليكم الوحا العجل العجل الساعة الساعة ونكتب هذا الطلسم في الطاسة", "Sambungan Sari 104x — tidak tidur/makan/minum sampai patuh — gambar bergerak berdiri tanda ijabah — izjar WAILUN LI-KULLI... Ayat Jatsiyah — sharf Zalzalah Asytatan 3x. Ihraq Laymunah shahih: kertas+lubān di perut limun, tutup, taruh di thasah minyak wangi, tulis thilasm thasah dengan paku, bakar sambil azam — ketika limun hangus hangus hati — tulisan kertas ‘La lam... Bi-harasy2 Qa rasy2... Bi-haqqi Athmahfasyadz Jalysy... Innahu min Sulaiman...’ + thilasm thasah.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 48 — Thilasm 7 Gula + Paku 4 Wajah Mulk 11x — Picture 024 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "و 1 2 هـ روح مهـ وا ل ماهو و ٢٣١١ و لا و م والو ٤٤٣م مول مـ ٢٢٤ فائدة للمراة التى تغضب من زوجها تاخذ مسمار حديد من عند الحداد مربع ويكون لم يستعمل من قبل وتكتب على كل وجة من اوجهته الاربعة ما ياتى وبعد الانتهاء من الكتابة يبخر بـ والجاوى والكسبرة وتعزم علية بسورة الملك 11 مرة وبعد كل مرة توكل وصفة الـ توكلو يا روحانية هذه السورة الشريفة بغفلة حتى لا تغضب ولا تترك البيت ابدا المسمار مدقوق وبعد ان تدق المسمار عزم مرة اخرى بنفس السورة 7 مرات وهو مجربة وصحيحة الوجه الاول: كيلهم حتى اذا مزقوا نتلا ورث فلانة بنت فلانة. الوجه الثاني: قسورة و ربضنا على قلوبهم اذ قاموا فلانة بنت فلانة. الوجه الثالث: طيكل هذا يركم الذى كفرتم توره و لايزد لزام فيتدر2. الوجه الرابع: مازر وتل ائمروا مع القاعدين فلانة بنت فلانة الى محبة فلانة محبة ياكلها المطلوب او يشرب يكتب هذا الطلسم على 7 قطع سكر او شوكلاتة او سبع فواكة تفاح او غيره فانة غاية في المحبة تكتب الطلسم المشار الية وتبخر باللبان الذكر وتعزم علية بالبرهتية 7 او 11 او 21 مرة وبعد تقرء هذه الاية الشريفة وذللناها لهم فمنها ركوبهم ومنها ياكلون", "Thilasm 7 gula (atas) — tulis 7 gula/coklat/apel, bukhur luban 11/21x Barhatiyyah + ayat ‘wa dzallalnaha...’. Faidah paku marah: paku persegi baru tulis 4 sisi — W1 Kilhum hatta idza muzziqa, W2 Qaswarah wa rabathna, W3 Thaykal, W4 Mazar — ukup Mulk 11x tiap selesai tawkil ‘ya ruhaniyyah hingga tidak marah’, tancap, Mulk 7x lagi — mujarrabah. Ujung bawah ‘mahabbah dimakan’ = pembuka Hal49.")
add_rajah(RAJAH_48T, "Halaman 48 Atas — Thilasm 7 Gula", "Thilasm tangan 3 baris `و 1 2 هـ روح... / ماهو و 2311... / 443 م مول` — tulis di 7 gula/buah, bakhur luban + Barhatiyyah 7/11/21x + ayat. HANYA tulisan (415KB, 3356x1488 px, 4x putih).")
add_rajah(RAJAH_48B, "Halaman 48 Bawah — Jadwal 4 Wajah Paku", "Jadwal 4 sisi paku besi: W1 Kilhum..., W2 Qaswarah..., W3 Thaykal..., W4 Mazar... — tulis di paku persegi baru. HANYA tabel (411KB, 3356x1384 px, 4x).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 49 — Jلب Qawiyy Misrajah + Yasin — Picture 024 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "لمقفيجل ٣٣٣ طلح ٤٠٣٣ طح ٤هه جلب قوى للمحبوب يكتب على اثر المطلوب هذا الطلسم واجعلة فتيلة بزيت طيب فى مسرجة واوقدها واجلس امامها وتخيل المطلوب فانة يتجسد امامك فى الفتيلة وهو تقرء العزيمة الازعاجية وهى موجودة فى قسم الدعوات الموجود بكتابنا السهم الصائب فى تنقية العلوم الروحانية من الشوائب وبخورك اللبان والعود ويكون عملك ليلة الخميس بعد المغرب اول الشهر العربى وينفع ايضا لتفريقة بنفس الكيفية ولكن اخر الشهر العربى يوم السبت وهذا الطلسم المشار الية مهـوسـه مع والتوكيل جلب قوى بسورة يس يكتب فى ورقة ويعلق فى الهواء وهذا ما تكتب يس الى قولة تسعى كذلك تسعى فلان فلانة الى فلانة بنت فلانة فى مكان تواجدها واينما تكونو ياتى بكم الله جميعا ان ان كل شياء قدير وكذلك ياتى فلان ابن فلانة الى هذا المكان ونفخ فى الصور فجمعناهم كذلك يجتمع فلان ابن فلانة الى فلانة بنت فلانة فى هذا المكان قال عفريت من الجن اتيك بة قبل ان تقوم من مقامك وانى علية لقوى امين قال الذى عنده علم من الكتاب اتيك بية قبل ان يرتد اليك طرفك كذلك ياتى فلان ابن فلانة الى فلانة بنت فلانة", "Thilasm salib 4 lingkaran + لمقفيجل333 — Jلب Qawwiy: atsar jadi sumbu misrajah minyak wangi, nyala, bayangkan — menjelma di nyala — azimah iz‘ajiyyah di kitab Sahm Sha’ib — Kamis malam awal bulan, tafriqah akhir bulan Sabtu. Yasin gantung: ‘Ya Sin... yas‘a... ya’ti bikumullah... nufikha... qala ‘ifrit...’")
add_rajah(RAJAH_49T, "Halaman 49 Atas — Thilasm Salib 4", "Salib 4 lingkaran + `لمقفيجل 333 طلح` — untuk sumbu misrajah. HANYA thilasm (266KB, 3320x976 px, 4x putih).")
add_rajah(RAJAH_49B, "Halaman 49 Bawah — مهوسه مع", "Tulisan `مهوسه مع` + sigil `∷` + `والتوكيل` — penempel nama sumbu. HANYA baris (64KB, 2968x568 px, 4x).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 50 — Lanjutan Yasin Doa Tadhyiq — Picture 025 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "دعوتى واستاذنو من عمار مكانى حتى يساعدونى فى قضاء حاجتى وتوكلو على فلان ابن فلانة حتى لا يتهنا فى اكل ولا شرب ولا يتهنا فى عيش ولا نوم حتى ياتى اى فلانة بنت فلانة الوحا العجل الساعة وهذا الوفق يكتب فى ورقة ويعلق فى الهواء وهذا ما تكتب يس الى قولة تسعى كذلك تسعى فلان فلانة الى فلانة بنت فلانة فى مكان تواجدها واينما تكونو ياتى بكم الله جميعا ان ان كل شياء قدير وكذلك ياتى فلان ابن فلانة الى هذا المكان ونفخ فى الصور فجمعناهم كذلك يجتمع فلان ابن فلانة الى فلانة بنت فلانة فى هذا المكان قال عفريت من الجن اتيك بة قبل ان تقوم من مقامك وانى علية لقوى امين قال الذى عنده علم من الكتاب اتيك بية قبل ان يرتد اليك طرفك كذلك ياتى فلان ابن فلانة الى فلانة بنت فلانة الى فلانة بنت فلانة هذا المكان اللهم ان الامر امرك والحكم حكمك والسماء سماء والارض ارضك ضيق اللهم السماء بما وسعت والارض بما رحبت والشرق شرقك والغرب غربك والقبلى قبلى والبحرى بحرى والسهل سهلك والجبال جبالك والبر بر والبحار بحارك فضيق السماء والارض والشرق والغرب والقبلى والبحرى والسهل والجبال والبر والبحر على قلب فلان ابن فلانة اضيق من بطن امة واضيق من خز الغيرة وضيق الدنيا بما رحبت وخيرة فى نفسة واتنافسة وهيج اللهم روحانية حتى الى فلانة بنت فلانة الى هذا المكان بحق او ظلمات فى بحر لجى يغشاه موج من موج من فوقة سحاب ظلمات بعضها فوق بعض اذا اخرج يده لم يكد يراها حتى ياتى كذا والى هذا المكان يامن رد يوسف على ابية يعقوب والعافية على جسد ايوب ورد سليمان بعد زولة ورد موسى الى امة رد فلان ابن فلان الى فلانة بنت فلانة حيران عى رجعة لقادر ووكلت علية خدام الايام السبعة العلوية والارضية وخدام الملوك المختصون بالجهات الاربعة وخدام الساعات النهارية والليلية وخدام الطبائع الاربعة والحروف وجميع الملوك الموكلة العلوية والارضية توكلو يامن دعوتكم فى", "Da‘wati ista’dzantu min ‘ammar... tawakkalu ‘ala fulan hatta la yahna’a akle syurbe... Al-Waha — tulisan Yasin ‘Ya Sin... tas‘a...’ + ‘Allahumma innal amra amruk... dhayyiq sama’ wa ardh... akhnak min bathni ummih...’ + ‘aw zhulumatin fi bahr lujjiyyin...’ + ‘ya man radda Yusuf...’ + tawkil khuddam 7 hari, 4 penjuru, sa‘at, thaba’i’...")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 51 — Wafaq Yasin + Mahabbah Abu Makanan — Picture 025 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "دعوتى واستاذنو من عمار مكانى حتى يساعدونى فى قضاء حاجتى وتوكلو على فلان ابن فلانة حتى لا يتهنا فى اكل ولا شرب ولا يتهنا فى عيش ولا نوم حتى ياتى اى فلانة بنت فلانة الوحا العجل الساعة وهذا الوفق محبة يوضع فى الطعام يكتب هذا الطلسم فى كاغد بمسك وزعفران وتحرقة وتاخذ رماد الطلسم واوضعة فى الطعام الذى ياكلة فانة لا ياخذة اصطبار ويصير مشغوفا دائما بمحبة الطالب وهذا ما تكتب ا١١ ط طع ٤ ١١١ هـ / ١١ هـ واهمء ١٢ ع اح امراح // ٧٧ امراح ١٢ ع اح ط ١١٥ ١١ ٢٢ ١١ ٨ ع ١١ ١١ ن خجج ٤٨٨ ن خجج // ٣١١١١٣٣ انسكا ٩ ١١ ١١١ ل ١٨ توكلو يا خدام هذة الطلاسم والاسماء والقوا محبة كذا فى قلب كذا واحرقو قلبة بالمحبة القاطعة بحق اطلموش 2همحوش 2غلبوش 2هملوش 2ملوش 2علوش 2فلوش 2", "Tawkil da‘wati... wafaq murabba‘ ditunjukkan dulu. Mahabbah makanan: kertas misk+za‘faran dibakar ambil abu masuk makanan — maka tak sabar, majnun cinta — tulisan 2 baris `ا11 ط طع 4 111هـ ...` + `ط115...` + tawkil Athlamusy Hamhush Ghalbush Hamlush Malush ‘Alush Falush 2x.")
add_rajah(RAJAH_51W, "Halaman 51 Atas — Wafaq Yasin Murabba", "Wafaq persegi 4 border melingkar + isi 4 baris — Yasin tadhyiq digantung. HANYA kotak (915KB, 3180x2300 px, 4x putih).")
add_rajah(RAJAH_51B, "Halaman 51 Bawah — Thilasm Abu Makanan", "2 baris + bawah `9 11 111 ل 18` — `ا11 ط طع...` + `ط115...` — bakar abu makanan. HANYA thilasm (221KB, 3108x924 px, 4x).")

# ========== BATCH 11: Hal052-056 (Picture 026-028) 6 Rajah ==========
pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 52 — Thilasm Ahmar 49x + Harf Ha — Picture 026 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "هاموش 2 باروش 2 عالوش 2 بابوش 2 قالوش 2 قروش 2 اجيبو والقوا كذا محبة كذا بالمحبة والهيام توكلو والا تكونو كالذين قالو سمعنا وهم لا يسمعون الوحا العجل الساعة والعمل في ساعة سعيدة هوانية طلسم الاحمر يعمل به الطالب كل شياء يكتب على قماش حمراء ويسرج او على 7 ورقات واطلق البخور وهو كندر وقلفل عليهم الاسماء حتى تنقطع الدخان واحدة بعد واحدة والعمل في اى وقت من الساعات الخاصة بالمحبة والتهييج ومقابلة الملوك والسلاطين وقضاء الحوائج وهذا الطلسم اليها و وهذة الاسماء التى تعزم بيهاو عدد التلاوة 49 مرة على كل ورة 7 مرات وهما ما تقر يشبوش 2 جلشبوش 2 وكشبوش 2 توكلو بجلب كذا الى كذا بحق تعليخ 2 فليخ 2 شليخ شلشليخ 2 اجب يا احمر وتوكل على كذا ولا تترك حتى ياتى كذا بحق هذة الاسماء عليكم وطاعتها لديكم الوحا العجل الساعة دعوة حرف الهاء للجلب", "Thilasm Ahmar: kain merah + siraj atau 7 kertas, kundur+qulqul, azimah Hamush... Qurush 2x ... wa illa takunu ka-alladzina qalu sami‘na... Al-Waha. Thilasm Ahmar untuk segala hajat mahabbah/tahyij/muqabalat muluk — thilasm lihat Rajah — azimah Yasybush Jalshabush Kasybush Ta‘likh Falaikh Syalaikh Syalsyalaikh — ajib ya Ahmar 49x (7x tiap warq) — Harf Ha da‘wah.")
add_rajah(RAJAH_52, "Halaman 52 — Thilasm Ahmar", "2 baris + garis bawah `و — / وـا لح` + `411S 899...` — kain merah/7 kertas kundur. HANYA thilasm 341K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 53 — Harf Ha Diamond 21/45x + Muluk — Picture 026 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "يكتب ويحمل هو ان تكتب الخاتم وحولة العزيمة دائرة ويتلى علية العزيمة 21 مرة وان كان 45 مرة كان اجود ويعطى للطالب يحمله على زراعة اليمنى واحدة تعلق فى الهواء اتجاء شرق وهذة العزيمة المشار اليها بطريابل اليها 2بطريابل 2طفيابل 2هبيابل 2زريابل 2 جريابل 2 فنيابل 2 ابل 2 جريابل 2 فنيابل 2 ابل 2 اجيبو ايتها الحروف الثمانية واتونى بما اكل اخيكم التاسع الذاھب عنكم وهو حرف الهاء بحق السر الذى اودعة الله فيكم وهو البارى الطاهر الدائم الزكى الجواد الودود الواحد الحى الا ما هيجتم قلب وعقل كذا الى كذا بحق هذة الاسماء عليكم وبحق انة من سليمان واتة بسم الله الرحمن الرحيم الا تعلو على واتونى مسلمين طائعين لله رب العالمين مجيبين ومنفذين لطال ب وجلب كذا الى كذا اسرع من البرق الخاطف الوحا العجل الساعة محبة خاصة بالملوك والحكام والاكابر وهيبة يكتب هذا الطلسم على كاغد احمر او كاغد مصبوغ بزعفران وزنجبيل وكركم وماء ورد فى شرف الشمس وطالع الاسد من البروج ويبخر بجاوى وليان وتفاح الجان والعزيمة سورة النمل المباركة 3 مرات ثم تنجمة ثم توكل بما تريد ثم تنجمة 3 ليالى وتشمعة ويحمل على طهارة", "Harf Ha: tulis khatam + azimah melingkar, baca 21x (45x lebih baik), bawa di lengan kanan + gantung timur menghadap syarq — Bathrayabil ilaiha... Ajibu 8 huruf bawa Ha’ bi-sirr Bari... hayyijtum qalba... bi-haqqi Innahu min Sulaiman... asra‘ min barq — Rajah diamond. Mahabbah Muluk: kertas merah/za‘faran jahe kunyit mawar, syaraf Syams thali‘ Asad, jawi luban tufah jann, NAML 3x tanjim 3 malam.")
add_rajah(RAJAH_53, "Halaman 53 — Diamond Harf Ha", "Diamond wajik berangka tengah + tulisan pinggir — harf Ha gantung timur. HANYA khatam 581K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 54 — Lion Sun + Mahabbah Hawa — Picture 027 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "وهذا الطلسم المشار الية - صورة أسد سيف شمس وجه - مجربات شيخ الروحانين الشيخ عطية 00201062022238 محبة تعلق فى الهواء يكتب هذا الطلسم بزعفران ومسك ودم حمام ابيض يكتب نسختين ويبخرين بكزبرة ويعزم عليهم بسورة القارعة المباركة 11 مرة مع التوكيل كل مرة وصرف العمار قبل الشروع فى العمل وتحرق واحدة والاخرى تعلق فى الهواء بخيط حرير احمر ويكون العمل ساعة هوانية وهذا الطلسم المشار الية هوائية", "Lion thilasm — sharf Syams+Asad — Mujarrabat Athiyah telp. Mahabbah hawa: za‘faran misk dam hamam abyadh 2 salinan, kuzbarah, QARI‘AH 11x + tawkil tiap, sharf, bakar 1 gantung 1 sutra merah jam hawa’iyyah — hawa’iyyah.")
add_rajah(RAJAH_54, "Halaman 54 — Singa Matahari", "Singa pedang + matahari berwajah + tulisan badan `شجرة طيبة` + keliling — syaraf Syams/Asad. HANYA singa 809K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 55 — Mizan Yusuf Kulit Ular — Picture 027 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "محبة وطاعة - تكتب هذا الطلسم على ورقة بزعفران وماء ورد ويبخر بكزبرة وجاوى وتقر علية سورة يوسف 3 مرات ويوضع فى جلد ثعبان اسود ويلف بخيط احمر وينجم تحت القمر 3 ليالى ويكون القمر ليلة 12 فى الشهر ويظل التنجيم حتى يوم 15 فى الشهر ويكون التنجيم فى اناء نحاس اصفر وتوقد شمعة خضراء اللون كل ليلة من التنجيم وكل ليلة فى التنجيم تقر سورة يوسف مرة وتوكل بالمحبة فلان ابن فلانة الى فلان ابن فلانة بحق فاتة الحب الخير لشديد وما ذلك على الله بعزيز توكلو بحق هذة السورة المباركة وهذا الطلسم وما فية من الاسرار بجلب ومحبة وطاعة فلان ابن فلانة على فلان ابن فلانة الوحا العجل الساعة بارك الله فيكم", "Mahabbah Tha‘ah: kertas za‘faran mawar kuzbarah jawi Yusuf 3x → kulit ular hitam benang merah tanjim 3 malam (12-15 Hijri) bejana kuningan + lilin hijau tiap malam Yusuf 1x + tawkil ‘bi-haqqi innahu li-hubbil khair lasyadid...’ Al-Waha.")
add_rajah(RAJAH_55, "Halaman 55 — Mizan Yusuf", "Mizan timbangan + sosok pedang + tabel angka — kulit ular tanjim. HANYA mizan 553K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 56 — Qulub Rahman Star Wafaq — Picture 028 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "ح ب ش ى د ى د و ر ى ا ح ع س ى ن هـيـب ش دى و زخج ع س ك دى لا كس - محبة وطاعة القلوب - يكتب هذا الطلسم ويحرز بجلد غزال بالحبر الروحانى الاصفر على كاغد اخضر بالبان التننية والميعة السائلة وجوز عجم وتقرء علية سورة الرحمن سبع مرات تقر بعد كل مرة توكلو يا روحانية هذة السورة المباركة وهذا الطلسم الشريف بجلب ومحبة قلوب اولاد ادم وبنات حواء الى محبة وطاعة حامل هذا الحرز بعزة الله الودود القدير وهذا الطلسم المشار اليه", "Grid huruf `ح ب ش ى د ى...` + atas `هيب شدى...` — Mahabbah Qulub: jilid ghazal hibr kuning kertas hijau luban mi‘ah walnut, Rahman 7x tiap ‘tawakkalu ya ruhaniyyah...’ — Star wafaq")
add_rajah(RAJAH_56T, "Halaman 56 Atas — Grid Huruf", "Grid 3 baris huruf + angka + `×××` — `ح ب ش ى...` — jilid ghazal. HANYA grid 406K 4× putih.")
add_rajah(RAJAH_56B, "Halaman 56 Bawah — Star 6 + Wafaq", "Bintang 6/segitiga + wafaq 3×3 tengah + sigil keliling — Rahman 7x qulub. HANYA bintang 615K 4× putih.")


pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 57 — Mahabbah Zawjain 3+1 Waraq Kahfi 2x — Picture 028 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "محبة بين الزوجين\\nتكتب هذا الطلسم على 3 اوراق بمسك وزعفران وصغار البيض ودم الاخوين وتبخرهن بميعة سائلة وسندروس وتحرق يوميا وقت الغروب واحدة لمدة 3 ايام وطبعا لا تكتب الايات التي مع الطلسم في هذه الاوراق والورقة الرابعة تكتب فيها الايات والطلسم ونفس الشروط الـ 3 ينجرقن بالنستلينبور والمواد الكتابة ولكن هذه الورقة تدفن تحت فراش الزوجين والعزيمة واحدة على الاربعة ورقات وهي سورة الكهف مرتين مع التوكيل بعد كل مرة فاعلم انهم لا يفترقون مادام هذا الحجاب تحتهم طول عمرهم وهذا الطلسم المشار اليه\\nللمحبة القاطعة والجلب\\nيرسم هذا الطلسم ويحرق بعد كتابته بزعفران وحليب غنم وعسل ويبخر بعود هندي وتقرء البسملة الشريفة عددها بالجمل الكبير وتتوكل يا خدام هذا الطلسم اجلبوا وهيجوا", "Mahabbah Zawjain: 3 kertas misk za‘faran puth telur dam akhawain may‘ah sandarus bakar ghurub 3 hari tanpa ayat, lembar 4 ayat+thilasm kubur bawah ranjang — Kahfi 2x + tawkil tiap — tidak cerai selama hijab di bawah. Lil qati‘ah: za‘faran susu kambing madu ‘ud hindi Basmalah Jumal Kabir — ya khuddam ijlibu.")
add_rajah(RAJAH_57, "Halaman 57 — Couple Wafaq Zawjain", "Pasangan peluk atas jadwal 3x6 `د ي د ش ب ح / ز و ت ب / يد ع س ح` + ular hati panah — 3 lembar bakar+1 tanam Kahfi2x. HANYA rajah 423K 4x putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 58 — Ruh Mahabbah + Shabaz Barhatiyyah 21/45x — Picture 029 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "روح وروحانية فلان ابن فلانة على محبة وعشق وطاعة فلان ابن فلانة بارك الله الا الوحا العجل الساعة\\nوصرف العمار قبل البدء في العمل وهذا الطلسم المشار اليه\\nمحبة قوية ومجربة\\nتكتب دعوة البرهتية حول هذا الشعباذ وتصرف العمار بالزلزلة 7 مرات وتكرر اشتاتا 7 ثم تعلق الورقة في سبية من الرمان او الزيتون وتطلق البخور ثم تشرع في قرائة العزيمة ولا يشغلك الا عملك في وقت العمل وخذ المطلوب في حين وتتو الدعوة 21 مرة وان اتممت 45 مرة كان اجود واسرع بالاجابة العمل ساعة الزهرة وبعد اتمام العمل ادفن العمل بجوار نار او كانون", "Ruh Fulan — sharaf ‘ammar sebelum amal — Barhatiyyah keliling shabaz, zalzalah 7x asytatan 7x, gantung ranting delima/zaitun, azimah 21x (45x lebih baik) jam Zuhrah, kubur dekat api.")
add_rajah(RAJAH_58, "Halaman 58 — Couple Sitting Shabaz", "Duduk bersila peluk bintang dada + pita paha `XP9A...` — Barhatiyyah 21/45x gantung delima. HANYA rajah 534K clean 4x putih (iklan cetak dibersihkan).")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 59 — Bab Jalb Qawathi Yasin 11x — Picture 029 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "باب جلب شرب من القواطع\\nتكتب هذه الطلاسم ومن حولها سورة يس والكتابة في ساعة سعيدة والبخور يكون وقت الكتابة وساعة العمل وساعة العمل يكون الطالع سعيد اول الشهر العربي والعزيمة سورة يس والتوكيل عند كل مبين وتقرء السورة على العمل بهذه الكيفية 11 مرة وهذا العمل لا يخطئ في الحلال وهذه الطلاسم المشار اليه", "Jalp Qawathi Yasin 11x — tulis thalasim+ Yasin keliling jam sa‘idah awal bulan, tawkil tiap mubin, 11x tidak meleset halal.")
add_rajah(RAJAH_59, "Halaman 59 — Bust Qawathi", "Bust mata besar dada wadah `السهام...` + `1912` — Yasin keliling 11x awal bulan halal. HANYA rajah 480K 4x putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 60 — Bab Shabaz Jaljalutiyah 21/49x — Picture 030 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "ع ع ع ع ب ع ع ع د د د س م ٥١٢٨ آلباب دد و و و و و و و ضـ ف ـض ف ف ف ف ف × × × × × ع ع ع ع ع... هـ هـ هـ هـ هـ هط هط هط هط х هطلمط хمسق хمسق لما لما\\nباب محبة من الاسرار\\nهذا الباب من القواطع واسرار الحكماء\\nترسم الشعباذ في ورقة حمراء او مصبوغة وتكتب التوكيل في ظهر الشعباذ وتقرء عليها دعوة الجلجلوتية الصغرى 21 مرة وان عزمت عليها بالدعوة 49 مرة اقوى واسرع بالاجابة في يومه والبخور لهذا العمل اللبان والعود والجاوي ولادن والجميع بالمسك ويخفو في الظل لوقت الحاجة وهذا هو الشعباذ وهذا العمل بعد التم منة اعمل على حسب طبيعة المطلوب ان كان ناري او ترابي او هوائي او مائي", "Shabaz script `ع ع... آلباب... هط...` — Bab Asrar Qawathi — kertas merah belakang tawkil Jaljalutiyah 21x (49x lebih kuat) luban ‘ud jawi ladzan misk simpan teduh sesuai tabi‘ah nari/turabi/hawa’i/ma’i.")
add_rajah(RAJAH_60, "Halaman 60 — Script Shabaz Jaljalutiyah", "Dua gugus `ع ع... آلباب دد... ف ف...` + `هـ هـ... هط... хمسق لما...` — shabaz Jajalutiyah. HANYA script 480K 4x putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 61 — Wajah Shabaz + Mahabbah Mujarrabah 2 Shabaz — Picture 030 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli', "محبة مجربة وصحيحة\\nارسم ايها الطالب لهذا العلم الجليل هذان الشعباذ كل شعباذ في جهة من الورقة والتوكيل يكون نفسة بمعنى التوكيل الذي تكتبه حول الشعباذ الاول يكون هو نفسه بدون نقصان او زيادة حول الثاني وتقرء دعوة خلخلة الهوه الكبرى على عملك وبعد الانتهاء يدفن في طريق المعمول له كلما مر عليه ازداد حب وعشق لطالبة واذا كتب على اثر المعمول له كان له كا السم في الطعام بمعنى يكون قوى الفعل والتسليط عليه ولا يتركه خدام الدعوة والشعباذ حتى ياتي طالبة بالحضور الية واليك ايها الطالب الشعباذ المطلوب في العمل وهذا الشعباذ الاول", "Mahabbah mujarrabah 2 shabaz — tiap sisi kertas, tawkil sama tak kurang tambah, Khalkhalah Hawah Kubra, kubur jalan tiap lewat tambah cinta, atsar seperti racun makanan kuat — shabaz pertama (bersambung 062).")
add_rajah(RAJAH_61, "Halaman 61 — Wajah Shabaz", "Wajah besar dada tulisan `احرقت قلبه على محبة... 189... السبل المسل... ه ه` — 2 shabaz Khalkhalah. HANYA wajah 392K 4x putih.")


pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 62 — Bab Mahabbah Shabaz Ats-Thani 2 Figur — Picture 031 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Shabaz', "وهذا الشعباذ الثانى - 2 figur dada ganda 18918912 + pita 8912912 - باب محبة", "Dua shabaz Hal.62: Atas dada ganda angka 18918912 + 5 tusukan, bawah profil pita 8912912 — Bab Mahabbah, tulis di raq‘ah/kulit, detail di Rajah.")
add_rajah(RAJAH_62, "Halaman 62 — Shabaz Pair 2 Figur", "2 Shabaz `18918912` dada kembar 5 paku + `8912912` pita lengan — Bab Mahabbah tulis di raq‘ah. HANYA rajah 761K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 63 — Hadid + Hawa Zuwadah + Turabiyyah — Picture 031 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Hadid', "اذا اردت ان يحبك احد ليس له قرار من محبتك تنقش على حديد هذا الطلسم وتضعه فى موقد النار فان المطلوب يأتيك ولو بينك وبينه بحر يأتيك باذن الله وهذا الطلسم موقد النار ويكون زيادة النور اول ساعة من يوم الاثنين [thilasm 4 H] تمم بالخير عمم", "Ukir di besi taruh di tungku api jam 1 Senin ziyadah nur mathlub datang walau bahr. Thilasm 4 H lihat Rajah.")
add_rajah(RAJAH_63, "Halaman 63 — Thilasm 4 Hadid", "4 simbol `H` silang + `111 99812` + `wa 319` — ukir di besi tungku Senin jam1. HANYA thilasm 126K 4× putih.")
add_block_box('Teks Arab Asli - Hawa & Turab', "فائدة محبة تكتب يوم الاربعاء وقت الظهر نظيف الثياب وتعلق في الهواء بشعر المطلوب وتعزم بعزيمة الهواء وهذا ما تكتب اول الشهر [هو هو... كهيعص...] فائدة ترابية تكتب في اثر المطلوب وتدفن في عتبة وتعزم بسورة الجن 21 ويبخر لبان وعود رصد مناسب", "Rabu Zhuhur gantung hawa + rambut + azimah Hawa + Hu Hu Kahya‘ash — Turabiyyah: tanah jejak kubur ‘atabah Jinn 21x luban ‘ud rashi.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 64 — Wafaq Jalb Fatilah + Zuhrah Sabasib — Picture 032 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Fatilah', "فائدة محبة وجاب وتهييج وعطف واحضار من اراد جلب احد يكتب على اثر المطلوب وافتله فتيلة وسرجه في مظلمة ويبخر لبان وجاوى ليلة الاحد او الاربعاء اول الشهر والعزيمة المريخ 11 وهذا ما تكتب ساعة سعيدة [ع ل ع... + ارقام] فائدة محبة تكتب ساعة الزهرة بماء ورد وكافور تبخر عنبر مسك كافور بدعوة السباسب الكبرى 7", "Wafaq besar Hal.64: atsar pilin sumbu gelap luban jawi Ahad/Rabu awal Mirrikh 11x jam sa‘idah — Zuhrah mawar kafur ‘anbar Sabasib 7x.")
add_rajah(RAJAH_64, "Halaman 64 — Wafaq Fatilah 7×6", "Wafaq 7 baris `1 2 wa 888 30... / 8 1089...` — atsar sumbu gelap Ahad/Rabu Mirrikh 11x. HANYA wafaq 373K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 65 — Figur Bertopi + 2 Wafaq 382 & Mukhammas — Picture 032 kiri', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Figur', "[Figur 2 bertopi 8911...] فائدة محبة تكتب هذا الوفق حوله البرهتية وبها تعزم يبخر لبان نتاية وصندل احمر رصد مناسب 11 وتعلق في الهواء اتجاه المطلوب [wafaq 4×4 جـ 38 382 س / 284 ت نو / 389 بـ م 388] [wafaq 5×5 40- 284 331 الله 330 / ... الرحيم الرحمن 431 381 ب] فائدة محبة", "2 figur topi angka 8911 — wafaq 4×4 382 + 5×5 Mukhammas Allah 330 R-Rahim 431 — Barhatiyyah keliling 11x luban nataya shandal ahmar gantung hadap target.")
add_rajah(RAJAH_65T, "Halaman 65 Atas — 2 Figur Topi", "2 figur bertopi `8911` + angka keliling — Barhatiyyah 11x gantung. HANYA figur 303K 4× putih.")
add_rajah(RAJAH_65B, "Halaman 65 Bawah — 2 Wafaq 4×4 & 5×5", "4×4 `جـ 38 382 س` + 5×5 `الله 330 / الرحيم 381` — 382-396 khadam. HANYA wafaq 510K 4× putih.")

pdf.set_font('DejaVu', 'B', 12)
pdf.set_text_color(124,45,18)
pdf.cell(0, 7, 'HALAMAN 66 — Thilasm 3 Baris + Qarurah 35x + Baidah — Picture 033 kanan', new_x="LMARGIN", new_y="NEXT")
add_block_box('Teks Arab Asli - Atas', "يكتب بالحبر الروحاني رصد اول الشهر جلّب صغرى 21 ويدفن بيت المطلوب جمعة اجود [ثم ثلسم اهمر 111 همو 988 وا لسم كاسحروزااطا # اا ع ه ع 11111 سم 88 تمت] فائدة محبة في قارورة يكتب في قارورة او ورقة بماء في القارورة على نار دعوة النار 35 وان كتب في القارورة ضف ماء لا تراه الشمس [ثم جرجر طع طم... مصاصع...] فائدة محبة على بيضة سبيتية تكتب وتعزم بعزيمة البيض مجمرة هادئة ما استوت امامك لبان كسبرة", "Hibr ruhaniyyah Jand Sughra 21x kubur Jum‘at thilasm Ahmar 111 humu 988 — Qarurah kertas/botol air + Da‘wah Nar 35x air la tarahu shams `جرجر طع طم مسوم...` — Baidah sabtiyyah majmarah hadiah luban kusbarah.")
add_rajah(RAJAH_66T, "Halaman 66 Atas — Thilasm 3 Baris", "Ahmar 111 humu 988 `# اا ع ه ع 11111 سم 88` — hibr ruhaniyyah 21x. HANYA thilasm 173K 4× putih.")
add_rajah(RAJAH_66M, "Halaman 66 Tengah — Jar Jar Nar", "Jarjar tha‘ tham masum `جرجر طع طم... / مصاصع...` — Qarurah 35x Nar. HANYA script 205K 4× putih.")

pdf.ln(4)
pdf.set_font('DejaVu', 'I', 7)
pdf.set_text_color(100,116,139)
pdf.multi_cell(0, 4, 'Sumber & Verifikasi: Transkrip manual per huruf. Batch 10: Hal47-51 6 Rajah (48×2,49×2,51×2). Batch 11: Hal52-56 6 Rajah (52,53,54,55,56×2) — Picture 026-028. Batch 12: Hal57-61 5 Rajah. Batch 13: Hal62-66 7 Rajah (62,63,64,65×2,66×2) — Picture 031-033. Total 38 Rajah HQ. Untuk Batch 14-30 (hal.67-selesai), PDF FULL akan di-append otomatis per 5 hal. Generate 23 Sep 2026 - Arena. Preview: http-server 8000 5-menit AUTO', align='L', new_x="LMARGIN", new_y="NEXT")

# Output
pdf.output(PDF_OUT)
print(f"PDF B01-B13 generated: {PDF_OUT}")

# Also copy to FULL for now (will be appended later)
import shutil
shutil.copy(PDF_OUT, PDF_FULL)
print(f"FULL PDF (sementara B01-B13) also at {PDF_FULL}")