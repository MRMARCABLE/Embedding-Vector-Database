"""
lab_terbimbing.py
Menjalankan Seluruh Modul Lab Terbimbing (Lab 1, Lab 2, dan Lab 3)
Sesuai Silabus Pertemuan 10 AI UKWMS
"""
import sys
import random
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

from indeks import baca_pdf, potong, potong_rekursif, bangun_indeks
from evaluasi_retrieval import UJI, hit_at_k, mrr

def jalankan_lab1():
    print("\n" + "=" * 70)
    print("🧪 LAB 1: EKSPERIMEN CHUNKING (500, 1000, 1500 KARAKTER)")
    print("=" * 70)

    pdf_files = list(Path("dokumen").glob("*.pdf"))
    if not pdf_files:
        print("❌ Tidak ada file PDF di folder dokumen/.")
        return

    sample_pdf = pdf_files[0]
    teks = baca_pdf(sample_pdf)
    print(f"File sampel: {sample_pdf.name} (Total panjang teks: {len(teks)} karakter)")
    print("\n--- 500 Karakter Pertama Dokumen ---")
    print(teks[:500])
    print("------------------------------------")

    pengaturan = [
        {"ukuran": 500, "overlap": 100},
        {"ukuran": 1000, "overlap": 150},
        {"ukuran": 1500, "overlap": 200},
    ]

    print("\nHasil Pemotongan (Chunking):")
    for cfg in pengaturan:
        u, o = cfg["ukuran"], cfg["overlap"]
        chunks = potong(teks, ukuran=u, tumpang=o)
        print(f"\n▶ Ukuran: {u} karakter | Overlap: {o} karakter → Menghasilkan {len(chunks)} chunk")
        
        # Ambil sampel chunk acak
        sampel_idx = min(len(chunks) - 1, 1)
        print(f"  Sampel Chunk #{sampel_idx + 1}:")
        cuplikan = chunks[sampel_idx].strip().replace("\n", " ")
        if len(cuplikan) > 180:
            cuplikan = cuplikan[:180] + "..."
        print(f"  \"{cuplikan}\"")

def jalankan_lab2():
    print("\n" + "=" * 70)
    print("🧪 LAB 2: BANGUN INDEKS & PENCARIAN SEMANTIK (QUERY & PARAFRASE)")
    print("=" * 70)

    # 1. Bangun indeks
    koleksi = bangun_indeks(folder_dokumen="dokumen", nama_koleksi="pedoman")

    # 2. Ajukan pertanyaan langsung & parafrase
    pertanyaan_uji = [
        ("Apa syarat cuti akademik?", "Pertanyaan eksplisit (kata sama persis)"),
        ("Berapa batas kehadiran agar boleh mengikuti ujian?", "Pertanyaan eksplisit"),
        ("Bagaimana sanksi jika mahasiswa mencontek?", "Pertanyaan eksplisit"),
        ("Boleh berhenti kuliah sementara?", "Parafrase makna: Cuti Akademik"),
        ("Absen kuliah maksimal berapa kali boleh bolos?", "Parafrase makna: Batas Kehadiran Ujian"),
    ]

    print("\nMenguji 5 Kueri Semantik:")
    for query, tipe in pertanyaan_uji:
        print(f"\n[Uji] \"{query}\" ({tipe})")
        hasil = koleksi.query(query_texts=[query], n_results=1)
        if hasil["documents"] and hasil["documents"][0]:
            doc = hasil["documents"][0][0].replace("\n", " ").strip()
            meta = hasil["metadatas"][0][0]
            jarak = hasil["distances"][0][0]
            if len(doc) > 180:
                doc = doc[:180] + "..."
            print(f"   ✓ Ditemukan di: {meta['sumber']} (chunk {meta['chunk']}) | Jarak Cosine: {jarak:.4f}")
            print(f"   Kutipan: \"{doc}\"")

def jalankan_lab3():
    print("\n" + "=" * 70)
    print("🧪 LAB 3: UKUR PERBANDINGAN RETRIEVAL HIT@k PADA UKURAN CHUNK BERBEDA")
    print("=" * 70)

    # Membangun 2 koleksi uji untuk membandingkan chunk 500 vs 1000
    pdf_files = list(Path("dokumen").glob("*.pdf"))
    if not pdf_files:
        print("❌ Dokumen PDF tidak ditemukan.")
        return

    emb = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )
    client = chromadb.PersistentClient(path="./chroma_db")

    eksperimen = [
        {"nama": "koleksi_chunk_500", "ukuran": 500, "overlap": 100},
        {"nama": "koleksi_chunk_1000", "ukuran": 1000, "overlap": 150},
    ]

    for eksp in eksperimen:
        nama = eksp["nama"]
        u = eksp["ukuran"]
        o = eksp["overlap"]
        print(f"\n▶ Mengindeks dengan chunk_size={u}, overlap={o} ke '{nama}'...")
        koleksi_uji = client.get_or_create_collection(name=nama, embedding_function=emb, metadata={"hnsw:space": "cosine"})

        for pdf in pdf_files:
            teks = baca_pdf(pdf)
            chunks = potong(teks, ukuran=u, tumpang=o)
            koleksi_uji.upsert(
                ids=[f"{pdf.stem}-{i}" for i in range(len(chunks))],
                documents=chunks,
                metadatas=[{"sumber": pdf.name, "chunk": i} for i in range(len(chunks))]
            )

        print(f"  Hasil Evaluasi untuk {nama}:")
        for k in (1, 3, 5):
            skor = hit_at_k(koleksi_uji, UJI, k=k)
            print(f"    - Hit@{k}: {skor:.2f} ({int(skor * len(UJI))}/{len(UJI)})")
        skor_mrr = mrr(koleksi_uji, UJI)
        print(f"    - MRR   : {skor_mrr:.3f}")

    print("\n💡 Kesimpulan Lab 3:")
    print("Perbandingan menunjukkan ukuran chunk yang moderat (~800–1000 karakter) umumnya memberikan keseimbangan")
    print("terbaik antara konteks yang utuh dan presisi semantik vektor dibandingkan chunk yang terlalu sempit.")

def main():
    print("╔══════════════════════════════════════════════════════════════════════════════════╗")
    print("║     LAB TERBIMBING PRAKTIK P-10: EMBEDDING & VECTOR DATABASE (AI UKWMS)          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════╝")

    jalankan_lab1()
    jalankan_lab2()
    jalankan_lab3()

if __name__ == "__main__":
    main()
