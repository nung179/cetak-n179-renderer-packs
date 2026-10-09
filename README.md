# Cetak n179 — Gudang Renderer Publik

**Repositori distribusi paket renderer on-demand resmi untuk Cetak n179**. Repository ini **bukan** source code aplikasi utama. Source code utama tetap di repository privat `nung179/cetak-n179`.

> **STATUS SEKARANG: BELUM ADA RENDERER SIAP DIUNDUH.** Tidak ada release, URL paket, hash atau tanda tangan yang boleh dikarang. Katalog [renderer-index.json](catalog/renderer-index.json) masih menandai tiga keluarga paket sebagai `NOT_AVAILABLE`.

## Satu aplikasi, paket sesuai kebutuhan

- **Cetak n179** adalah **SATU APK**, SATU UI Phoenix, SATU Print Rule Center.
- Saat membuka DOC/DOCX/ODT/RTF, PPT/PPTX/ODP, atau XLS/XLSX/ODS/CSV, n179 memeriksa paket renderer yang diperlukan. Unduh paket **sekali** jika dan ketika tersedia, verifikasi, simpan di ruang privat aplikasi, lalu render di dalam n179.
- **Tidak ada APK kedua**, tidak ada editor dokumen, tidak membuka Word/Excel/PowerPoint sebagai jalur utama.
- Source file tetap utuh; **BACA SUMBER → PAGE SETUP → RENDER → PRATINJAU → CETAK**.
- PDF/foto/web memakai jalur core aplikasi sebagaimana baseline, bukan paket yang dikelola repo ini.
- Driver printer berada di gudang terpisah dan tidak bergantung pada format renderer.

## Isi repositori

| Lokasi | Fungsi |
|---|---|
| `catalog/renderer-index.json` | Status dan alamat paket yang **benar-benar** dirilis |
| `packs/document/` | Kontrak keluarga DOC/DOCX/ODT/RTF |
| `packs/presentation/` | Kontrak keluarga PPT/PPTX/ODP |
| `packs/spreadsheet/` | Kontrak keluarga XLS/XLSX/ODS/CSV |
| `docs/FORMAT_PACK_V1.md` | Format paket dan kontrak kompatibilitas |
| `docs/KEAMANAN_DAN_LISENSI.md` | Integritas, keamanan, dan hak distribusi |
| `docs/CARA_TERBITKAN.md` | SOP produksi/publikasi setelah paket nyata ada |
| `tools/` dan `tests/` | Pemeriksaan katalog dan arsip paket sebelum penerbitan |

## Larangan rilis palsu

Status `NOT_AVAILABLE` **bukan** berarti paket rusak; paket memang **belum ada**. Status hanya boleh diubah setelah mesin nyata tersedia, lisensi terverifikasi, artefak dirilis, hash/tanda tangan benar, pemuatan di Android terbukti, dan tes render/paging terdokumentasi. GitHub Actions hijau pada repo ini hanya membuktikan **validitas metadata**, bukan kualitas renderer ataupun uji cetak fisik.

**Baseline core saat pembuatan katalog:** R113A `v0.1.103 (105)` (build GitHub Actions dilaporkan hijau). Core **belum** dinyatakan mempunyai loader renderer siap produksi.
