"""
evaluasi_retrieval.py
Evaluasi Kualitas Retrieval Sebelum Menambah LLM (Langkah 7 Praktik P-10)
Menghitung Metrik Hit@k dan Mean Reciprocal Rank (MRR)
"""
import chromadb
from chromadb.utils import embedding_functions

# Dataset uji: pasangan (pertanyaan, kata kunci/frasa yang harus ada di chunk jawaban)
UJI = [
    ("Apa syarat cuti akademik?", "cuti akademik"),
    ("Berapa batas kehadiran untuk boleh ujian?", "75 persen"),
    ("Apakah boleh berhenti kuliah sementara?", "cuti akademik"),
    ("Berapa minimal kehadiran tatap muka kuliah?", "kehadiran"),
    ("Apa konsekuensi jika terlambat membayar biaya kuliah?", "denda"),
    ("Berapa lama batas maksimal masa studi S1?", "masa studi"),
    ("Bagaimana tata tertib selama ujian berlangsung?", "ujian"),
    ("Berapa lama maksimal izin cuti yang diberikan?", "semester"),
    ("Apakah mahasiswa cuti tetap membayar biaya her-registrasi?", "biaya"),
    ("Apa sanksi bila kedapatan berbuat curang saat ujian?", "sanksi"),
    ("Bagaimana prosedur pengajuan skripsi atau tugas akhir?", "skripsi"),
    ("Berapa IPK minimal untuk mengambil 24 SKS?", "ipk"),
    ("Apakah ada dispensasi pembayaran uang kuliah?", "dispensasi"),
    ("Kapan batas akhir pengisian kartu rencana studi (KRS)?", "krs"),
    ("Siapa yang berhak menandatangani persetujuan cuti kuliah?", "dekan"),
]

def hit_at_k(koleksi, uji, k=3):
    """
    Hit@k: Proporsi pertanyaan uji di mana chunk relevan
    ditemukan di antara k hasil teratas.
    """
    benar = 0
    for pertanyaan, kunci in uji:
        res = koleksi.query(query_texts=[pertanyaan], n_results=k)
        docs = res["documents"][0] if res["documents"] else []
        if any(kunci.lower() in d.lower() for d in docs):
            benar += 1
    return benar / len(uji)

def mrr(koleksi, uji, max_k=10):
    """
    Mean Reciprocal Rank (MRR): Rata-rata dari 1/peringkat pertama chunk benar.
    Semakin tinggi nilai MRR (mendekati 1.0), semakin konsisten chunk yang tepat
    berada di peringkat teratas (rank 1).
    """
    total_rr = 0.0
    for pertanyaan, kunci in uji:
        res = koleksi.query(query_texts=[pertanyaan], n_results=max_k)
        docs = res["documents"][0] if res["documents"] else []
        rank_ditemukan = 0
        for idx, doc in enumerate(docs, 1):
            if kunci.lower() in doc.lower():
                rank_ditemukan = idx
                break
        if rank_ditemukan > 0:
            total_rr += 1.0 / rank_ditemukan
    return total_rr / len(uji)

def evaluasi_retrieval(nama_koleksi="pedoman"):
    print("=" * 65)
    print("  EVALUASI KUALITAS RETRIEVAL (SEBELUM MENAMBAH LLM)")
    print("=" * 65)
    print(f"Dataset Evaluasi: {len(UJI)} pasangan (pertanyaan, kata kunci jawaban)")
    print(f"Target Koleksi  : {nama_koleksi}")
    print("-" * 65)

    emb = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        koleksi = client.get_collection(name=nama_koleksi, embedding_function=emb)
    except Exception as e:
        print(f"❌ Error membuka koleksi '{nama_koleksi}': {e}")
        print("Pastikan Anda sudah menjalankan 'python indeks.py' terlebih dahulu.")
        return

    print("Hasil Pengukuran:")
    for k in (1, 3, 5):
        skor = hit_at_k(koleksi, UJI, k=k)
        jumlah_benar = int(round(skor * len(UJI)))
        persen = skor * 100
        print(f"  • Hit@{k:<2} = {skor:.2f} ({persen:5.1f}%) — {jumlah_benar}/{len(UJI)} pertanyaan terjawab di top-{k}")

    skor_mrr = mrr(koleksi, UJI)
    print(f"  • MRR    = {skor_mrr:.3f} (Mean Reciprocal Rank)")
    print("-" * 65)

    if skor >= 0.8:
        print("💡 Analisis: Kualitas retrieval sangat baik untuk diteruskan ke LLM (P-11).")
    else:
        print("💡 Analisis: Pertimbangkan penyesuaian ukuran chunk atau overlap untuk meningkatkan akurasi.")

if __name__ == "__main__":
    evaluasi_retrieval()
