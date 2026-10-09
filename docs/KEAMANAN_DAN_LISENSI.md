# Keamanan, lisensi, dan tata kelola

1. **Jangan rilis apa pun yang belum boleh didistribusikan.** Simpan catatan atribusi, lisensi dependency, dan bukti hak redistribusi. Kode/proyek privat, token, credential, key signing, EULA vendor yang membatasi distribusi tidak boleh ada di repo publik.
2. **SHA-256 bukan pengganti autentikasi.** SHA harus dicek dengan manifest yang ditandatangani atau channel tepercaya dan kunci publik yang di-pin di n179. Selagi signature belum diterapkan, seluruh paket tetap `NOT_AVAILABLE`.
3. **Pertahanan ZIP:** cegah zip-slip, symlink, duplicate entry, zip bomb, nested code yang belum disetujui. Verifikasi hash dan ukuran sebelum dipakai; extraction atomic di app-private, data sementara dibersihkan bila gagal.
4. **Android security/Google Play:** mengunduh arsip dan menyimpannya tidak berarti kontennya dapat dieksekusi dengan aman/diizinkan. Tentukan jenis payload dan metode loader berdasarkan ketentuan Android serta kanal distribusi yang digunakan. Tetap satu APK secara UX dan instalasi.
5. **Privacy:** dokumen pengguna tidak boleh diunggah ke GitHub/Drive untuk dirender; pemrosesan dilakukan di HP. Source asli jangan ditimpa. Preview PDF hanya cache sementara.
6. **Status bukti:** CI katalog hijau = metadata valid; compile APK hijau = build; tes di HP = runtime; tes dengan printer fisik = physical verification. Jangan menyamakan keempatnya.
7. **Rollback:** client boleh menyimpan versi lama yang valid dan sesuai kompatibilitas, jangan downgrade otomatis tanpa validasi/konfirmasi.
