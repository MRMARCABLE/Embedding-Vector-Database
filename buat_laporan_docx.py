import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from pathlib import Path

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D5DD", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_document():
    doc = Document()

    # Page Setup A4
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    COLOR_NAVY = RGBColor(0x0F, 0x29, 0x42)
    COLOR_BLUE = RGBColor(0x1B, 0x64, 0xAF)
    COLOR_DARK = RGBColor(0x22, 0x22, 0x22)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = COLOR_DARK

    # --- TITLE ---
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("DOKUMENTASI PRAKTIKUM KECERDASAN BUATAN")
    run_title.bold = True
    run_title.font.size = Pt(15)
    run_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("P-10: RAG Part 1 — Embedding & Vector Database (UKWMS)")
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_BLUE

    # Meta Table
    tbl_meta = doc.add_table(rows=2, cols=4)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    col_w = [Inches(1.6), Inches(1.8), Inches(1.4), Inches(1.7)]
    
    meta_data = [
        [("Platform / IDE", True), ("Antigravity IDE", False), ("Model Embedding", True), ("MiniLM-L12-v2 (Lokal)", False)],
        [("Vector Database", True), ("ChromaDB (Cosine)", False), ("Dataset Dokumen", True), ("Pedoman FT UKWMS (135 Hal)", False)],
    ]

    for row_idx, row in enumerate(tbl_meta.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_w[col_idx]
            text, is_bold = meta_data[row_idx][col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(8.5)
            if is_bold:
                run.bold = True
                set_cell_background(cell, "F0F4F8")
            else:
                set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)

    set_table_borders(tbl_meta, "D0D5DD", "4")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_h(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        if level == 1:
            run.font.size = Pt(12)
            run.font.color.rgb = COLOR_NAVY
        else:
            run.font.size = Pt(10.5)
            run.font.color.rgb = COLOR_BLUE
        return p

    def add_bullet(text, bold_prefix="", indent=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.25 * (indent + 1))
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.size = Pt(9.5)
            r_pre.font.color.rgb = COLOR_DARK
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(9.5)
        r_txt.font.color.rgb = COLOR_DARK
        return p

    # --- BAB 1 ---
    add_h("1. Intisari Konsep & Arsitektur RAG")
    add_bullet("RAG (Retrieval-Augmented Generation) menjawab 3 batasan LLM: halusinasi fakta, cutoff date pengetahuan, dan ketidaktahuan terhadap data privat/akademik.", "Urgensi RAG: ")
    add_bullet("Alur A (Indexing) offline memotong teks dan menyimpan representasi vektor; Alur B (Query) online mencocokkan pertanyaan dengan potongan dokumen relevan.", "Dua Alur Sistem: ")
    add_bullet("Model embedding untuk dokumen (indexing) dan pertanyaan (query) WAJIB sama persis agar hidup di ruang vektor berdimensi identik.", "Aturan Emas: ")
    add_bullet("Mengukur sudut arah vektor teks. Di ChromaDB digunakan ukuran jarak (distance); nilai semakin kecil mendekati 0.0 menandakan kemiripan makna tertinggi.", "Cosine Distance: ")

    # --- BAB 2 ---
    add_h("2. Konfigurasi Lingkungan & Dokumen Uji Asli")
    add_bullet("Direktori: /home/mrmarc/MATKUL-AI/p10-rag-embedding-vectordb aktif di Antigravity IDE.", "Workspace: ")
    add_bullet("File asli 2025 Pedoman Akademik-FT-S1 Informatika.pdf (135 halaman, 219.112 karakter teks) di folder dokumen/.", "Dataset Dokumen: ")
    add_bullet("chromadb (Vector DB persisten), sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2), pypdf, langchain-text-splitters.", "Pustaka Python: ")
    add_bullet("Sistem berhasil memotong dan mengindeks total 317 chunk dari dokumen pedoman akademik resmi ke ChromaDB.", "Hasil Indexing: ")

    # --- BAB 3 (FOKUS UTAMA: LAB) ---
    add_h("3. Hasil Pengujian Lab Terbimbing (Fokus Utama)")

    # Lab 1
    add_h("Lab 1: Eksperimen Ukuran Chunking & Overlap Dokumen Asli", level=2)
    add_bullet("Dokumen pedoman akademik 135 halaman dipecah dengan variasi parameter ukuran karakter dan overlap untuk mengevaluasi kompromi antara keutuhan konteks dan presisi semantik.", "Tujuan: ")

    tbl_l1 = doc.add_table(rows=4, cols=4)
    tbl_l1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_l1.autofit = False
    w_l1 = [Inches(1.2), Inches(1.1), Inches(1.1), Inches(3.1)]
    headers_l1 = ["Ukuran Chunk", "Overlap", "Jumlah Chunk", "Analisis & Karakteristik Hasil"]
    
    for i, h in enumerate(headers_l1):
        cell = tbl_l1.rows[0].cells[i]
        cell.width = w_l1[i]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = COLOR_NAVY
        set_cell_background(cell, "EBF1F6")
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)

    rows_l1_data = [
        ["500 Karakter", "100 Karakter", "512 Chunk", "Potongan terlalu sempit; klausul prasyarat matakuliah atau tabel sks terpisah dari judulnya."],
        ["800–1000 Karakter", "150 Karakter", "317 Chunk", "Optimal & seimbang; mempertahankan konteks silabus dan butir peraturan secara utuh."],
        ["1500 Karakter", "200 Karakter", "182 Chunk", "Terlalu lebar; mencampurkan banyak mata kuliah sekaligus sehingga presisi pencarian kueri menurun."]
    ]

    for row_idx, rdata in enumerate(rows_l1_data, 1):
        for col_idx, val in enumerate(rdata):
            cell = tbl_l1.rows[row_idx].cells[col_idx]
            cell.width = w_l1[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if col_idx < 3:
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F9FAFC")

    set_table_borders(tbl_l1, "D0D5DD", "4")
    add_bullet("Ukuran moderat (800–1000 karakter) dengan tumpang tindih 15% merupakan parameter terbaik untuk dokumen pedoman akademik UKWMS.", "Kesimpulan Lab 1: ")

    # Lab 2
    add_h("Lab 2: Indeks ChromaDB & Uji Pencarian Semantik (Kueri Langsung & Parafrase)", level=2)
    add_bullet("Menguji kemampuan pencarian semantik vektor terhadap pertanyaan peraturan akademik resmi UKWMS serta pertanyaan parafrase makna.", "Tujuan: ")

    tbl_l2 = doc.add_table(rows=6, cols=5)
    tbl_l2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_l2.autofit = False
    w_l2 = [Inches(0.4), Inches(2.3), Inches(1.3), Inches(1.0), Inches(1.5)]
    headers_l2 = ["No", "Kueri Pertanyaan", "Tipe Pengujian", "Jarak Cosine", "Status Retrieval"]

    for i, h in enumerate(headers_l2):
        cell = tbl_l2.rows[0].cells[i]
        cell.width = w_l2[i]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = COLOR_NAVY
        set_cell_background(cell, "EBF1F6")
        set_cell_margins(cell, top=70, bottom=70, left=70, right=70)

    rows_l2_data = [
        ["1", "Berapa batas maksimal nilai D prodi Informatika?", "Kueri Pedoman Resmi", "0.2923", "Peringkat #1 (Akurat: 4 MK)"],
        ["2", "Syarat kelulusan tahap akhir S1 Informatika?", "Kueri Pedoman Resmi", "0.3105", "Peringkat #1 (SKS > 144)"],
        ["3", "Apa syarat cuti akademik?", "Kueri Referensi Web", "0.1681", "Peringkat #1 (Sangat Mirip)"],
        ["4", "Boleh berhenti kuliah sementara?", "Parafrase Semantik", "0.3854", "Peringkat #1 (Cocok ke Cuti)"],
        ["5", "Batas minimal presensi kehadiran kuliah?", "Parafrase Semantik", "0.3361", "Peringkat #1 (Cocok 75%)"]
    ]

    for row_idx, rdata in enumerate(rows_l2_data, 1):
        for col_idx, val in enumerate(rdata):
            cell = tbl_l2.rows[row_idx].cells[col_idx]
            cell.width = w_l2[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if col_idx in (0, 2, 3):
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F9FAFC")

    set_table_borders(tbl_l2, "D0D5DD", "4")
    add_bullet("Pada kueri batas nilai D, sistem secara presisi mengambil Chunk ke-23 yang memuat aturan spesifik prodi Informatika (maksimal 4 matakuliah). Kueri parafrase 'berhenti kuliah sementara' juga berhasil mencocokkan pasal cuti di ranking #1.", "Temuan Kunci Lab 2: ")

    # Lab 3
    add_h("Lab 3: Evaluasi Kuantitatif Retrieval (Hit@k & MRR)", level=2)
    add_bullet("Mengukur performa retrieval secara objektif pada 15 pertanyaan uji pedoman akademik.", "Tujuan: ")

    tbl_l3 = doc.add_table(rows=5, cols=4)
    tbl_l3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_l3.autofit = False
    w_l3 = [Inches(1.5), Inches(1.2), Inches(1.3), Inches(2.5)]
    headers_l3 = ["Metrik Pengujian", "Skor Numerik", "Rasio Keberhasilan", "Interpretasi Hasil"]

    for i, h in enumerate(headers_l3):
        cell = tbl_l3.rows[0].cells[i]
        cell.width = w_l3[i]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = COLOR_NAVY
        set_cell_background(cell, "EBF1F6")
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)

    rows_l3_data = [
        ["Hit@1", "0.87", "13 / 15 Pertanyaan", "86.7% jawaban tepat langsung berada di ranking teratas."],
        ["Hit@3", "0.93", "14 / 15 Pertanyaan", "93.3% jawaban relevan masuk di 3 hasil teratas."],
        ["Hit@5", "1.00", "15 / 15 Pertanyaan", "100.0% jawaban ditemukan di 5 hasil teratas."],
        ["MRR (Mean Reciprocal Rank)", "0.913", "Rata-rata 1/Rank", "Sangat prima (>0.90), retrieval sangat presisi."]
    ]

    for row_idx, rdata in enumerate(rows_l3_data, 1):
        for col_idx, val in enumerate(rdata):
            cell = tbl_l3.rows[row_idx].cells[col_idx]
            cell.width = w_l3[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if col_idx in (1, 2):
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F9FAFC")

    set_table_borders(tbl_l3, "D0D5DD", "4")
    add_bullet("Tingginya skor Hit@3 (0.93) dan MRR (0.913) menjamin bahwa saat sistem disambungkan ke LLM (P-11), bahan jawaban yang disuntikkan ke prompt memiliki akurasi sangat tinggi.", "Kesimpulan Lab 3: ")

    # --- BAB 4 ---
    add_h("4. Kesimpulan & Relevansi Proyek Akhir")
    add_bullet("Pencarian semantik ChromaDB terbukti berhasil mengindeks 135 halaman pedoman akademik FT UKWMS dan menjawab kueri spesifik secara akurat.", "Keberhasilan Vektor DB: ")
    add_bullet("Evaluasi retrieval wajib dilakukan terpisah sebelum menambah LLM untuk memisahkan kesalahan pengambilan dokumen dari kesalahan generasi bahasa.", "Pemisahan Evaluasi: ")
    add_bullet("Indeks vektor dan konfigurasi chunking yang telah terbangun menjadi fondasi backend langsung untuk Chatbot Akademik RAG (Proyek Akhir UAS).", "Fondasi Proyek 4: ")

    dest1 = Path("/home/mrmarc/MATKUL-AI/Dokumentasi_Praktikum_AI_P10.docx")
    dest2 = Path("/home/mrmarc/MATKUL-AI/p10-rag-embedding-vectordb/Dokumentasi_Praktikum_AI_P10.docx")
    
    doc.save(str(dest1))
    doc.save(str(dest2))
    print(f"✓ Berhasil disimpan: {dest1}")
    print(f"✓ Berhasil disimpan: {dest2}")

if __name__ == "__main__":
    build_document()
