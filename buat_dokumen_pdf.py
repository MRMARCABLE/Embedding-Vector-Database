"""
buat_dokumen_pdf.py
Script untuk membuat 3 PDF pedoman akademik teks (bukan scan)
untuk keperluan pengujian RAG dan Vector Database P-10.
"""
from pathlib import Path

def buat_pdf_sederhana(filepath, judul, paragraf_list):
    """
    Menghasilkan file PDF standar (PDF-1.4) berbasis teks murni tanpa library eksternal.
    Teks tersimpan di text stream agar dapat diekstrak 100% sempurna oleh pypdf.
    """
    lines = []
    lines.append(f"BT")
    lines.append(f"/F1 16 Tf")
    lines.append(f"50 740 Td")
    lines.append(f"({judul}) Tj")
    lines.append(f"ET")

    y = 700
    for p in paragraf_list:
        lines.append("BT")
        lines.append("/F1 11 Tf")
        lines.append(f"50 {y} Td")
        lines.append(f"14 TL") # line leading
        words = p.split()
        cur_line = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + 1 > 75:
                baris_str = " ".join(cur_line).replace("(", "\\(").replace(")", "\\)")
                lines.append(f"({baris_str}) '")
                cur_line = [w]
                cur_len = len(w)
                y -= 14
            else:
                cur_line.append(w)
                cur_len += len(w) + 1
        if cur_line:
            baris_str = " ".join(cur_line).replace("(", "\\(").replace(")", "\\)")
            lines.append(f"({baris_str}) '")
            y -= 14
        lines.append("ET")
        y -= 15 # space between paragraphs
        if y < 80:
            break

    stream_content = "\n".join(lines).encode("latin1", "replace")
    stream_len = len(stream_content)

    objects = []
    # 1: Catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2: Pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # 3: Page
    objects.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 595 842] /Contents 5 0 R >>\nendobj\n")
    # 4: Font
    objects.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    # 5: Stream
    objects.append(f"5 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("latin1") + stream_content + b"\nendstream\nendobj\n")

    # Header
    pdf_bytes = bytearray(b"%PDF-1.4\n")
    xref = [0]
    for obj in objects:
        xref.append(len(pdf_bytes))
        pdf_bytes.extend(obj)

    xref_pos = len(pdf_bytes)
    pdf_bytes.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin1"))
    for pos in xref[1:]:
        pdf_bytes.extend(f"{pos:010d} 00000 n \n".encode("latin1"))

    pdf_bytes.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin1"))

    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(pdf_bytes)
    print(f"✓ Berhasil membuat: {filepath}")

def main():
    folder = Path("dokumen")
    folder.mkdir(exist_ok=True)

    # 1. Pedoman Cuti dan Masa Studi
    buat_pdf_sederhana(
        folder / "pedoman_akademik_ukwms.pdf",
        "PEDOMAN AKADEMIK DAN ATURAN CUTI KULIAH UKWMS",
        [
            "Pasal 1 Ketentuan Cuti Akademik: Mahasiswa diperbolehkan mengajukan cuti akademik setelah menempuh minimal dua semester berturut-turut pada program sarjana. Permohonan cuti diajukan selambat-lambatnya dua minggu sebelum perkuliahan semester baru dimulai dengan persetujuan Dosen Wali dan Dekan Fakultas.",
            "Pasal 2 Durasi Cuti: Jangka waktu cuti akademik yang diizinkan adalah maksimal dua semester berturut-turut atau total empat semester kumulatif selama masa studi. Masa cuti akademik tidak diperhitungkan dalam evaluasi batas maksimal masa studi.",
            "Pasal 3 Batas Masa Studi: Batas maksimal masa studi untuk program Sarjana (S1) adalah 14 semester atau 7 tahun kalender. Mahasiswa yang melewati batas waktu tanpa menyelesaikan skripsi atau tugas akhir akan dinyatakan drop out (DO).",
            "Pasal 4 Kartu Rencana Studi (KRS): Setiap mahasiswa wajib melakukan pengisian kartu rencana studi (KRS) online sesuai kalender akademik. Mahasiswa dengan IPK minimal 3.00 berhak mengambil beban maksimal hingga 24 SKS.",
            "Pasal 5 Pengajuan Skripsi: Prosedur pengajuan skripsi atau tugas akhir mensyaratkan mahasiswa telah lulus minimal 120 SKS dan mata kuliah metodologi penelitian dengan nilai minimal C."
        ]
    )

    # 2. Peraturan Ujian dan Kehadiran
    buat_pdf_sederhana(
        folder / "peraturan_ujian_dan_kehadiran.pdf",
        "PERATURAN KEHADIRAN KULIAH DAN TATA TERTIB UJIAN",
        [
            "Pasal 1 Batas Kehadiran Mahasiswa: Mahasiswa wajib memenuhi batas kehadiran perkuliahan tatap muka minimal 75 persen dari total pertemuan terjadwal untuk setiap mata kuliah agar berhak mengikuti Ujian Akhir Semester (UAS).",
            "Pasal 2 Dispensasi Kehadiran: Ketidakhadiran karena sakit yang disertai surat keterangan dokter resmi dapat diberikan dispensasi kehadiran maksimal dua kali pertemuan dan wajib dilaporkan kepada dosen pengampu.",
            "Pasal 3 Tata Tertib Ruang Ujian: Mahasiswa wajib hadir 15 menit sebelum ujian dimulai, mengenakan pakaian rapi berkerah, dan membawa kartu tanda mahasiswa (KTM) atau kartu ujian resmi yang telah divalidasi.",
            "Pasal 4 Larangan dan Sanksi Kecurangan: Segala bentuk kecurangan seperti mencontek, menggunakan joki ujian, atau membuka gadget tanpa izin akan dikenakan sanksi tegas berupa pembatalan nilai mata kuliah menjadi E serta skorsing akademik.",
            "Pasal 5 Ujian Susulan: Ujian susulan hanya dapat diselenggarakan bagi mahasiswa yang berhalangan hadir dengan alasan force majeure yang disetujui oleh ketua program studi."
        ]
    )

    # 3. SOP Keuangan dan Pembayaran
    buat_pdf_sederhana(
        folder / "sop_keuangan_administrasi.pdf",
        "SOP PEMBAYARAN KULIAH DAN ADMINISTRASI KEUANGAN",
        [
            "Pasal 1 Pembayaran Biaya Kuliah: Pembayaran uang kuliah tunggal (UKT) atau SPP semesteran dilakukan melalui virtual account bank mitra universitas paling lambat tanggal 10 sebelum periode pengisian KRS dimulai.",
            "Pasal 2 Denda Keterlambatan: Keterlambatan pembayaran biaya kuliah setelah tanggal jatuh tempo akan dikenakan sanksi denda administratif sebesar dua persen per bulan dan penangguhan akses portal akademik.",
            "Pasal 3 Mahasiswa Cuti Kuliah: Mahasiswa yang disetujui permohonan cuti akademiknya tetap diwajibkan membayar biaya administrasi her-registrasi cuti sebesar sepuluh persen dari total SPP pokok per semester.",
            "Pasal 4 Dispensasi Pembayaran: Pengajuan dispensasi pembayaran cicilan uang kuliah dapat diajukan kepada biro administrasi keuangan dengan melampirkan surat permohonan dari orang tua atau wali mahasiswa.",
            "Pasal 5 Pengembalian Biaya: Biaya kuliah yang telah dibayarkan tidak dapat ditarik kembali apabila mahasiswa mengundurkan diri setelah semester perkuliahan berjalan."
        ]
    )

if __name__ == "__main__":
    main()
