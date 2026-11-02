# Praktikum Pertemuan 10: RAG Part 1 — Embedding & Vector Database
**Mata Kuliah:** Kecerdasan Buatan (UKWMS)  
**Tujuan:** Membangun separuh pertama sistem RAG (Indexing, Chunking, Embedding Semantik, Vector Database ChromaDB, dan Evaluasi Retrieval).

---

## 📂 Struktur Proyek

```
p10-rag-embedding-vectordb/
├── .venv/                                      # Virtual environment Python (uv)
├── chroma_db/                                  # Persistent storage database vektor ChromaDB
├── dokumen/                                    # Dataset dokumen PDF akademik
│   └── 2025 Pedoman Akademik-FT-S1 Informatika.pdf  # (Dokumen resmi UKWMS, 135 hal, 317 chunk)
├── indeks.py                                   # Alur Indexing (Load -> Split -> Embed -> Store)
├── cari.py                                     # Alur Query semantik top-k dari ChromaDB
├── evaluasi_retrieval.py                       # Evaluasi akurasi retrieval (Hit@k & MRR)
├── lab_terbimbing.py                           # Skrip eksekusi terpadu Lab 1, Lab 2, & Lab 3
├── buat_laporan_docx.py                        # Generator dokumen laporan Word (.docx)
├── Dokumentasi_Praktikum_AI_P10.docx           # File dokumentasi laporan resmi praktikum
├── requirements.txt                            # Dependensi pustaka Python
└── README.md                                   # Panduan & dokumentasi proyek
```

---

## 🚀 Cara Menjalankan

### 1. Aktivasi Virtual Environment
Buka terminal di dalam **Antigravity IDE** (`Ctrl` + `~`) atau terminal Linux:
```bash
cd /home/mrmarc/MATKUL-AI/p10-rag-embedding-vectordb
source .venv/bin/activate
```

### 2. Membangun Indeks Dokumen (Indexing)
Membaca PDF dari folder `dokumen/`, memotong teks, menghitung vektor embedding dengan model multilingual lokal (`paraphrase-multilingual-MiniLM-L12-v2`), dan menyimpannya ke ChromaDB:
```bash
python indeks.py
```
> Menghasilkan **317 chunk teks** yang tersimpan di koleksi vektor persisten `./chroma_db`.

### 3. Melakukan Pencarian Semantik (Query)
Menguji retrieval dengan berbagai kueri (baik kueri spesifik pedoman UKWMS maupun kueri parafrase makna):
```bash
# Kueri spesifik pedoman akademik Informatika UKWMS
python cari.py "Berapa batas maksimal nilai D untuk program studi Informatika?"
python cari.py "Apa saja syarat kelulusan tahap akhir S1 Informatika?"

# Kueri uji parafrase makna
python cari.py "Boleh berhenti kuliah sementara?"
python cari.py "Batas minimal presensi kehadiran kuliah?"
```

### 4. Evaluasi Kualitas Retrieval
Mengukur performa retrieval secara objektif sebelum menghubungkan ke LLM:
```bash
python evaluasi_retrieval.py
```
* **Hit@1:** 0.87 (86.7% kueri langsung berada di peringkat teratas)
* **Hit@3:** 0.93 (93.3% kueri terjawab di 3 hasil teratas)
* **Hit@5:** 1.00 (100.0% kueri terjawab di 5 hasil teratas)
* **MRR (Mean Reciprocal Rank):** 0.913

### 5. Menjalankan Seluruh Modul Lab Terbimbing
Menjalankan otomatis **Lab 1 (Eksperimen Chunking Dokumen 135 Hal)**, **Lab 2 (Indeks & Parafrase)**, dan **Lab 3 (Komparasi Hit@k)**:
```bash
python lab_terbimbing.py
```

### 6. Membangun Ulang Dokumen Laporan (.docx)
```bash
python buat_laporan_docx.py
```
File dokumen otomatis tersimpan di:
* `/home/mrmarc/MATKUL-AI/Dokumentasi_Praktikum_AI_P10.docx`
* `/home/mrmarc/MATKUL-AI/p10-rag-embedding-vectordb/Dokumentasi_Praktikum_AI_P10.docx`

---

## 🧠 Konsep Penting & Best Practices

1. **Aturan Emas Model Embedding:** Model embedding pada saat proses *indexing* dokumen dan saat *query* pencarian harus selalu menggunakan model yang sama persis (`paraphrase-multilingual-MiniLM-L12-v2`).
2. **Karakteristik Metrik Jarak (Distance):** ChromaDB menggunakan jarak kosinus (*cosine distance*), di mana skor yang semakin kecil (mendekati 0.0) menandakan tingkat kemiripan makna yang semakin tinggi.
3. **Pemisahan Evaluasi:** Evaluasi retrieval dilakukan terpisah dari LLM untuk memastikan masalah akurasi jawaban berasal dari retrieval atau generasi model.
