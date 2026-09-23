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
PDF_OUT = str(BASE / "Asrar-wa-Khofayyat-Terjemahan-Lengkap-B01-B02.pdf")
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
        self.cell(0, 6, 'كتاب أسرار و خفايات في علم الروحانيات - Terjemahan Lengkap Indonesia (Batch 01-02)', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, 5, 'Batch 01–02 (Halaman 001–011) • Versi PDF • 23 Sep 2026', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, 7, 'Daftar Isi - Batch 01–02', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('DejaVu', '', 8)
pdf.set_text_color(15,23,42)
pdf.multi_cell(0, 4.5,
'Batch 01 (Hal. 001–005): Cover, Fasal 1 Mahabbah/Jalb/Tahyij, Mas-alah 1 (Alfah suami-istri, 20 daun lemon), Mas-alah 2 (Mahabbah 72x), Mas-alah 3 (Tahyij di Syaqfah Selasa pagi), Rajah Hal.05 Wafaq Tahyij 4 baris, Mas-alah 4 (7 lembar)\n'
'Batch 02 (Hal. 006–011): Lanjutan Mas-alah 4 (2 luban + 3x2 kuzbarah, 21x), Azimah Bismillahil Azhim, Khatam 7 Waraq Rajah Hal.07, Mas-alah 5 (Tahyij 400x/300x), Mas-alah 5 duplikat (Al-Humazah di lilin Iskandari), Mas-alah 7 (Maimun Thayyar, Rabu di pohon timur), Mas-alah 8 (Harut-Marut, lampu hijau), Mas-alah 9 (Mahabbah Jalb, minyak Yasamin, Thilasm Mahmala...), Azimah Ahya Syarahya 31x\n'
'Batch 03–30 (Hal. 012–~300) - akan menyusul otomatis per 5 halaman, PDF ini akan di-update ke versi FULL', new_x="LMARGIN", new_y="NEXT")
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

# FOOTER FOR PDF
pdf.ln(4)
pdf.set_font('DejaVu', 'I', 7)
pdf.set_text_color(100,116,139)
pdf.multi_cell(0, 4, 'Sumber & Verifikasi: Transkrip manual per huruf dari scan asli. Bandingkan dengan file sumber: 1.jpg, Picture 001.jpg (hal.2–3), Picture 002.jpg (hal.4–5), Picture 003.jpg (hal.6–7), Picture 004.jpg (hal.8–9), Picture 005.jpg (hal.10–11). Rajah Hal.05 & Hal.07 - crop presisi HANYA kotak, putih bersih, 4x. Untuk Batch 03–30 (hal.12–selesai), PDF FULL akan di-append otomatis per 5 halaman. Generate 23 Sep 2026 - Arena. Jika butuh cetak jilid, gunakan PDF ini (A4, margin 18/16mm, font Amiri).', align='L', new_x="LMARGIN", new_y="NEXT")

# Output
pdf.output(PDF_OUT)
print(f"PDF B01-B02 generated: {PDF_OUT}")

# Also copy to FULL for now (will be appended later)
import shutil
shutil.copy(PDF_OUT, PDF_FULL)
print(f"FULL PDF (sementara B01-B02) also at {PDF_FULL}")
