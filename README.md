# Praktikum Pertemuan 10: RAG Part 1 — Embedding & Vector Database
**Mata Kuliah:** Kecerdasan Buatan (UKWMS)  
**Tujuan:** Membangun separuh pertama sistem RAG (Indexing, Chunking, Embedding Semantik, Vector Database ChromaDB, dan Evaluasi Retrieval).

---

## 📂 Struktur Proyek

```
p10-rag-embedding-vectordb/
├── .venv/                         # Virtual environment Python (uv)
├── chroma_db/                     # Persistent storage database vektor ChromaDB
├── dokumen/                       # Kumpulan file PDF berbasis teks
│   ├── pedoman_akademik_ukwms.pdf
│   ├── peraturan_ujian_dan_kehadiran.pdf
│   └── sop_keuangan_administrasi.pdf
├── buat_dokumen_pdf.py            # Generator PDF dokumen uji akademik
├── indeks.py                      # Alur Indexing (Load -> Split -> Embed -> Store)
├── cari.py                        # Alur Query semantik top-k dari ChromaDB
├── evaluasi_retrieval.py          # Evaluasi akurasi retrieval (Hit@k & MRR)
├── lab_terbimbing.py              # Skrip eksekusi terpadu Lab 1, Lab 2, & Lab 3
├── requirements.txt               # Dependensi pustaka Python
└── README.md                      # Dokumentasi & panduan
```

---

## 🚀 Cara Menjalankan

### 1. Aktivasi Virtual Environment
Buka terminal di dalam **Antigravity IDE** (`Ctrl` + `~`) atau terminal biasa:
```bash
cd /home/mrmarc/MATKUL-AI/p10-rag-embedding-vectordb
source .venv/bin/activate
```

### 2. Membangun Indeks Dokumen (Indexing)
Membaca PDF dari folder `dokumen/`, memotong menjadi chunk, menghitung vektor dengan model multilingual (`paraphrase-multilingual-MiniLM-L12-v2`), dan menyimpannya ke ChromaDB:
```bash
python indeks.py
```

### 3. Melakukan Pencarian Semantik (Query)
Menguji retrieval dengan berbagai variasi kueri (baik kata kunci langsung maupun parafrase makna):
```bash
# Kueri default (Syarat cuti akademik)
python cari.py

# Kueri kustom via argumen
python cari.py "Boleh berhenti kuliah sementara?"
python cari.py "Berapa minimal kehadiran agar boleh ikut ujian?"
python cari.py "Apakah ada dispensasi cicilan SPP?"
```

### 4. Evaluasi Kualitas Retrieval
Mengukur performa retrieval secara objektif sebelum menghubungkan ke LLM:
```bash
python evaluasi_retrieval.py
```
Metrik yang dihitung:
* **Hit@1, Hit@3, Hit@5**: Proporsi kueri uji yang berhasil menemukan potongan jawaban di $k$ peringkat teratas.
* **MRR (Mean Reciprocal Rank)**: Rata-rata bobot peringkat jawaban benar pertama.

### 5. Menjalankan Seluruh Modul Lab Terbimbing
Menjalankan otomatis **Lab 1 (Eksperimen Chunking)**, **Lab 2 (Indeks & Parafrase)**, dan **Lab 3 (Komparasi Hit@k Chunk 500 vs 1000)**:
```bash
python lab_terbimbing.py
```

---

## 🧠 Konsep Penting & Best Practices

1. **Aturan Emas Model Embedding:** Model embedding pada saat proses *indexing* dokumen dan saat *query* pencarian harus selalu menggunakan model yang sama persis (`paraphrase-multilingual-MiniLM-L12-v2`).
2. **Karakteristik Metrik Jarak (Distance):** ChromaDB menggunakan jarak kosinus (*cosine distance*), di mana skor yang semakin kecil (mendekati 0.0) menandakan tingkat kemiripan makna yang semakin tinggi.
3. **Pentingnya Metadata:** Menyimpan metadata (`sumber`, `chunk_id`) krusial agar pada tahap generasi jawaban (P-11), LLM dapat menyertakan sitasi sumber rujukan yang valid dan transparan.
