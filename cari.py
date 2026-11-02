"""
cari.py
Pencarian Dokumen Semantik via Query ChromaDB (Langkah 4 Praktik P-10)
"""
import sys
import chromadb
from chromadb.utils import embedding_functions

def cari_dokumen(query="Apa syarat cuti akademik?", n_results=3, nama_koleksi="pedoman"):
    print(f"\n" + "=" * 65)
    print(f"🔎 QUERY SEMANTIK: \"{query}\"")
    print("=" * 65)

    # 1. Inisialisasi embedding function yang persis sama dengan saat indexing
    emb = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

    # 2. Hubungkan ke ChromaDB persistent client
    client = chromadb.PersistentClient(path="./chroma_db")
    koleksi = client.get_or_create_collection(
        name=nama_koleksi,
        embedding_function=emb,
        metadata={"hnsw:space": "cosine"}
    )

    # 3. Eksekusi query
    hasil = koleksi.query(query_texts=[query], n_results=n_results)

    if not hasil["documents"] or not hasil["documents"][0]:
        print("❌ Tidak ada dokumen yang ditemukan di database vektor.")
        return

    # 4. Tampilkan dokumen hasil retrieval
    docs = hasil["documents"][0]
    metas = hasil["metadatas"][0]
    jaraks = hasil["distances"][0]

    for rank, (doc, meta, jarak) in enumerate(zip(docs, metas, jaraks), 1):
        # Kemiripan: semakin kecil jarak kosinus (distance), semakin dekat maknanya
        # Nilai kemiripan aproksimasi = 1 - jarak
        skor_kemiripan = max(0.0, 1.0 - jarak)
        print(f"\n[HASIL #{rank}] 📄 {meta.get('sumber', 'Unknown')} (Chunk ke-{meta.get('chunk', 0)})")
        print(f"Jarak Cosine (Distance) : {jarak:.4f} (Makin kecil makin identik)")
        print(f"Estimasi Kemiripan       : {skor_kemiripan * 100:.1f}%")
        print("-" * 65)
        cuplikan = doc.strip().replace("\n", " ")
        if len(cuplikan) > 280:
            cuplikan = cuplikan[:280] + "..."
        print(f"Kutipan Teks:\n\"{cuplikan}\"")
        print("=" * 65)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pertanyaan = " ".join(sys.argv[1:])
    else:
        pertanyaan = "Apa syarat cuti akademik?"
    cari_dokumen(pertanyaan)
