"""
indeks.py
Membangun Indeks Dokumen ke ChromaDB (Langkah 2 & Langkah 3 Praktik P-10)
"""
from pathlib import Path
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions

def baca_pdf(path):
    """Mengekstrak teks dari seluruh halaman file PDF."""
    reader = PdfReader(path)
    return "\n".join((p.extract_text() or "") for p in reader.pages)

def potong(teks, ukuran=800, tumpang=100):
    """
    Pemotongan ukuran tetap dengan overlap.
    ukuran: panjang karakter per chunk
    tumpang: jumlah karakter tumpang tindih (overlap)
    """
    hasil, mulai = [], 0
    while mulai < len(teks):
        hasil.append(teks[mulai:mulai + ukuran])
        mulai += ukuran - tumpang
    return [h for h in hasil if h.strip()]

def potong_rekursif(teks, ukuran=800, tumpang=100):
    """
    Alternatif pemotongan rekursif (LangChain) yang menjaga batas alami teks.
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(chunk_size=ukuran, chunk_overlap=tumpang)
        return splitter.split_text(teks)
    except ImportError:
        # Fallback ke potong standar jika library belum terpasang
        return potong(teks, ukuran, tumpang)

def bangun_indeks(folder_dokumen="dokumen", ukuran_chunk=800, overlap=100, nama_koleksi="pedoman", gunakan_rekursif=True):
    print(f"\n[1/3] Menyiapkan model embedding multilingual lokal...")
    # Model embedding multilingual (jalan lokal di PyTorch, tanpa API key)
    emb = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )

    print(f"[2/3] Membuka database vektor ChromaDB (folder: ./chroma_db)...")
    client = chromadb.PersistentClient(path="./chroma_db")
    koleksi = client.get_or_create_collection(
        name=nama_koleksi,
        embedding_function=emb,
        metadata={"hnsw:space": "cosine"} # Ukuran jarak: Cosine Similarity
    )

    pdf_files = sorted(list(Path(folder_dokumen).glob("*.pdf")))
    if not pdf_files:
        print(f"⚠️ Peringatan: Tidak ditemukan file PDF di folder '{folder_dokumen}/'")
        return koleksi

    print(f"[3/3] Memproses {len(pdf_files)} dokumen PDF...")
    total_chunk_keseluruhan = 0

    for pdf in pdf_files:
        teks = baca_pdf(pdf)
        if gunakan_rekursif:
            chunks = potong_rekursif(teks, ukuran=ukuran_chunk, tumpang=overlap)
        else:
            chunks = potong(teks, ukuran=ukuran_chunk, tumpang=overlap)

        if not chunks:
            print(f"⚠️ File '{pdf.name}' kosong atau tidak ada teks yang terbaca.")
            continue

        # Upsert: aman dijalankan ulang (menimpa jika id sudah ada)
        stem_bersih = pdf.stem.replace(" ", "_")
        koleksi.upsert(
            ids=[f"{stem_bersih}-{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"sumber": pdf.name, "chunk": i} for i in range(len(chunks))],
        )
        print(f"   ✓ {pdf.name} → {len(chunks)} chunk tersimpan")
        total_chunk_keseluruhan += len(chunks)

    print(f"\n🎉 Berhasil! Sebanyak {total_chunk_keseluruhan} chunk telah diindeks ke koleksi '{nama_koleksi}'.")
    return koleksi

if __name__ == "__main__":
    bangun_indeks()
