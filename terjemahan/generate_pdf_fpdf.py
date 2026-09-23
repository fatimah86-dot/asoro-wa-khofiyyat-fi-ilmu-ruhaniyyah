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
AMIRI_REG = "/tmp/amiri/fonts/Amiri-Regular.ttf"
AMIRI_BOLD = "/tmp/amiri/fonts/Amiri-Bold.ttf"
RAJAH_05 = str(BASE / "assets/rajah-hal-005-wafaq-tehij.jpg")
RAJAH_07 = str(BASE / "assets/rajah-hal-007-khatam-7waraq.jpg")
RAJAH_12 = str(BASE / "assets/rajah-hal-012-thilasm-final.jpg")
RAJAH_13 = str(BASE / "assets/rajah-hal-013-thilasm-final.jpg")
RAJAH_14 = str(BASE / "assets/rajah-hal-014-tilasm-final.jpg")
RAJAH_16 = str(BASE / "assets/rajah-hal-016-khatam-besar.jpg")
RAJAH_19 = str(BASE / "assets/rajah-hal-019-khatam-4x4.jpg")
PDF_OUT = str(BASE / "Asrar-wa-Khofayyat-Terjemahan-Lengkap-B01-B04.pdf")
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
        self.cell(0, 6, 'كتاب أسرار و خفايات في علم الروحانيات - Terjemahan Lengkap Indonesia (Batch 01-04)', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, 5, 'Batch 01–04 (Halaman 001–021) • Versi PDF • 23 Sep 2026', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, 7, 'Daftar Isi - Batch 01–04', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 8)
pdf.set_text_color(15,23,42)
pdf.multi_cell(0, 4.5,
'Batch 01 (Hal. 001–005): Cover, Fasal 1 Mahabbah/Jalb/Tahyij, Mas-alah 1 (Alfah 20 daun lemon), Mas-alah 2 (72x), Mas-alah 3 (Syaqfah Selasa), Rajah Hal.05 Wafaq, Mas-alah 4 (7 lembar)\n'
'Batch 02 (Hal. 006–011): Lanjutan Mas-alah 4, Khatam 7 Waraq Hal.07, Mas-alah 5 (400x/300x), Al-Humazah lilin, Mas-alah 7 (Maimun Thayyar), Mas-alah 8 (Harut-Marut lampu hijau), Mas-alah 9 (Mahmala, Ahya Syarahya 31x)\n'
'Batch 03 (Hal. 012–016): Mas-alah 10 (Malam Ahad, Rajah Hal.12), Mas-alah 12 Susi (Rajah Hal.13 tinta rambut/kuku), Mas-alah 13 Qallama (Rajah Hal.14), Mas-alah 14 awal + Khatam Sulaiman (Hal.15)\n'
'Batch 04 (Hal. 016–021): Lanjutan Khatam Sulaiman Hal.16 (Rajah Besar 8x8 Hal.16), Mas-alah 14 Da`wah Fatihah (Hal.17-19, Rajah 4x4 Hal.19 837x), Mas-alah 15 Tahyij 7 kertas Sabtu jam 11 (Hal.20-21, azimah Harut-Marut), Mas-alah 16 Mahabbah adonan faras (Hal.21)\n'
'Batch 05–30 (Hal. 022–~300) - menyusul per 5 hal., PDF FULL akan di-append otomatis', new_x="LMARGIN", new_y="NEXT")
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

# FOOTER FOR PDF
pdf.ln(4)
pdf.set_font('DejaVu', 'I', 7)
pdf.set_text_color(100,116,139)
pdf.multi_cell(0, 4, 'Sumber & Verifikasi: Transkrip manual per huruf dari scan asli. Sumber Batch 04: Picture 008 (hal.16-17), Picture 009 (hal.18-19), Picture 010 (hal.20-21). Rajah Hal.16 (8x8) & Hal.19 (4x4) crop presisi HANYA kotak, putih bersih 4x. Untuk Batch 05-30 (hal.22-selesai), PDF FULL akan di-append otomatis per 5 hal. Generate 23 Sep 2026 - Arena.', align='L', new_x="LMARGIN", new_y="NEXT")

# Output
pdf.output(PDF_OUT)
print(f"PDF B01-B04 generated: {PDF_OUT}")

# Also copy to FULL for now (will be appended later)
import shutil
shutil.copy(PDF_OUT, PDF_FULL)
print(f"FULL PDF (sementara B01-B04) also at {PDF_FULL}")
