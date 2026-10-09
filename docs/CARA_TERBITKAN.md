# SOP Penerbitan Renderer

Repository distribusi: `https://github.com/nung179/cetak-n179-renderer-packs` (PUBLIC). Source aplikasi: `nung179/cetak-n179` (PRIVATE).

1. **Tuntaskan engine sungguhan** untuk keluarga format tertentu. Uji file nyata (tabel/gambar/font/multipage/cetak) dan catat fidelity `HIGH_FIDELITY`/`COMPATIBLE`/`LIMITED` yang terbukti. Jangan promosikan DOC/XLS/PPT lama hanya karena DOCX/XLSX/PPTX bisa dibuka.
2. Tentukan bentuk paket **yang aman dan benar-benar dapat dimuat** n179; siapkan aturan lisensi, metadata, dan bukti uji.
3. Bangun arsip paket lengkap `manifest.json`, `payload/`, setiap file punya hash; jalankan `python tools/validate_pack.py <path.zip>`.
4. Rilis hanya artefak yang selesai ke **GitHub Releases** (tag versi unik). Jangan menaruh file rilis besar langsung ke cabang `main`.
5. Catat `tag`, URL aset yang nyata, ukuran tepat, hash ZIP, signature + identitas trusted key, kompatibilitas, dan verified extensions pada `catalog/renderer-index.json`.
6. Jalankan `python tools/validate_catalog.py` dan `python -m unittest discover -s tests -v` sebelum push. Workflow harus hijau. Periksa URL dan signature agar APK konsumen tidak gagal.
7. Uji lewat aplikasi Cetak n179: membuka sumber → prompt unduh sekali → verifikasi → simpan private → render → pratinjau → cetak. Uji perubahan Page Setup dan rollback paket. **Baru tandai AVAILABLE** setelah kontrak berjalan.
8. Saat uji fisik gagal, turunkan status paket menjadi `NOT_AVAILABLE` atau `BLOCKED` dan jelaskan, bukan fallback ke aplikasi eksternal secara diam-diam.

**Saat ini: tidak ada release dan semua paket NOT_AVAILABLE.** Langkah berikutnya adalah membuat mesin dan loader sesuai kontrak; repository ini hanya jalur distribusi.
