# Renderer Cetak n179 — BETA TERBATAS

**Satu APK**. Tiga paket unduhan **DATA** (`.n179r`) berisi pengaturan layout yang dikonsumsi oleh mesin Kotlin dasar **di APK utama**. Paket bukan `.apk`, `.dex`, `.jar`, maupun `.so`, dan tidak menjalankan kode dari jaringan.

- Document: baru `.docx`, paragraf/tabel/gambar sederhana. **BUKAN** layout Word kompleks.
- Spreadsheet: baru `.xlsx`, nilai sel/sheet sederhana, belum setara Excel untuk merge/print titles/chart/fit kompleks.
- Presentation: baru `.pptx`, teks dan gambar dasar, belum master/theme/notes/handout.

Format `.doc/.xls/.ppt` lama dan ODF **belum didukung**. Fidelity diberi label **LIMITED**, bukan NATIVE.

GitHub Actions membangun ulang ketiga paket, memeriksa hash yang dipin di katalog, kemudian memublikasikan **pre-release BETA**, bukan release stabil. Status `BETA_STAGING_NOT_VERIFIED_ON_PHONE` wajib dipertahankan hingga pengujian fisik lolos.

Terbitnya Release **belum berarti** Cetak n179 di HP berhasil mengunduh atau merender. GitHub Actions untuk APK utama dan uji HP harus dipisahkan.

JANGAN mengganti repository utama menjadi publik atau mengunggah signing key.
