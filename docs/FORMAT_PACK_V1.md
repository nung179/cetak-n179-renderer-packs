# Kontrak Paket Renderer V1 — Cetak n179

## Rantai distribusi

`GitHub Release publik → katalog → paket → verifikasi SHA-256 + tanda tangan tepercaya → app-private storage → loader yang kompatibel → renderer internal → PDF spool → Phoenix Preview → Print Rule Center/Capability Bridge → cetak`.

**Catatan:** ini spesifikasi distribusi, **belum implementasi loader Android**. ZIP **tidak** secara otomatis dapat dieksekusi Android. Sebelum rilis nyata, pilih bentuk engine yang aman dan didukung Android/kanal distribusi. Untuk modul kode atau native, desain loader, verifikasi, dan kebijakan distribusi wajib ditinjau terpisah. Jangan diam-diam memasang APK kedua.

## Keluarga format

| ID | Ekstensi calon | Keterangan |
|---|---|---|
| `document` | DOC/DOCX/ODT/RTF | Hanya ekstensi yang sudah diuji masuk `verified_extensions` |
| `presentation` | PPT/PPTX/ODP | Notes/outline/handout adalah mode output berbeda |
| `spreadsheet` | XLS/XLSX/ODS/CSV | Print area sumber → used-range fallback → override job |

## Arsip rilis (jika mesin nyata telah dibuat)

Nama aset: `n179-renderer-<family>-<version>.zip`.

Root ZIP harus memiliki berkas `manifest.json` **dan** direktori `payload/`. Contoh bentuk metadata, BUKAN file yang sudah tersedia:

```json
{
  "schema_version": 1,
  "package_id": "org.n179.renderer.document",
  "family": "document",
  "version": "1.0.0",
  "engine_kind": "HOST_COMPATIBLE_ASSETS",
  "verified_extensions": ["docx"],
  "min_core_version": "0.1.103",
  "files": {
    "payload/runtime/example.dat": "<64-lowercase-hex-sha256>"
  }
}
```

- `manifest.json` tidak boleh menyatakan format didukung hanya karena ekstensinya dikenali.
- `files` memuat path relatif payload dan SHA-256 hasil byte sebenarnya.
- Tidak ada path traversal (`../`), nama file ganda, symlink, arsip terenkripsi, nested APK, private key, DEX/JAR, atau pustaka native yang dimuat tanpa mekanisme yang disetujui.
- SHA-256 melindungi integritas byte **hanya jika** nilai acuannya tepercaya; untuk saluran publik, pin kunci verifikasi publik dalam APK dan gunakan signature yang diverifikasi. `security.signature_mode=NOT_CONFIGURED` berarti **jangan aktifkan download runtime di client**.
- `min_core_version` mengacu kontrak host yang nyata, bukan nilai promosi.

## Katalog aktif (belum berlaku)

Setelah rilis yang benar-benar verified, satu entri `release` harus mencakup:

`tag`, `asset_name`, `url`, `size_bytes`, `sha256`, `signature`, `compatibility`, serta `verified_extensions`. URL wajib menuju GitHub Releases repository ini. Semua nilai berasal dari artefak, bukan contoh.

## Page Setup universal

Renderer mengambil sumber asli dan `PageSetupState` dari Cetak n179. Hasil spool/page cache hanyalah disposable. Jika pilihan cetak memerlukan reflow/rerender, renderer harus mengerjakannya tanpa menyunting file sumber. Renderer tidak tahu printer Epson/Brother/driver.
