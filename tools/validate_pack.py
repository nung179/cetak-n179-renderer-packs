#!/usr/bin/env python3
"""Periksa ZIP paket renderer dan manifest; belum memverifikasi signature publik."""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

FORBIDDEN = {'.apk','.aab','.dex','.jar','.aar','.so','.keystore','.jks','.pem','.key','.p12','.pfx'}
SHA=re.compile(r'^[0-9a-f]{64}$')
FAMILIES={'document','presentation','spreadsheet'}
MAX_FILE=150*1024*1024
MAX_TOTAL=500*1024*1024
MAX_ENTRIES=2000


def validate(path):
    errors=[]
    try:
        with zipfile.ZipFile(path) as archive:
            infos=archive.infolist()
            if len(infos)>MAX_ENTRIES: errors.append('terlalu banyak file')
            seen=set()
            files={}
            total=0
            for info in infos:
                name=info.filename
                parts=PurePosixPath(name).parts
                if name.startswith('/') or '\\' in name or ':' in name or '..' in parts or not parts or name.startswith('./'):
                    errors.append(f'path berbahaya: {name}'); continue
                if name in seen: errors.append(f'duplicate zip member: {name}')
                seen.add(name)
                if ((info.external_attr>>16)&0o170000)==0o120000:
                    errors.append(f'symlink dilarang: {name}')
                if info.flag_bits & 1: errors.append(f'encrypted file dilarang: {name}')
                if info.is_dir(): continue
                if info.file_size>MAX_FILE: errors.append(f'file terlalu besar: {name}')
                total += info.file_size
                if PurePosixPath(name).suffix.lower() in FORBIDDEN:
                    errors.append(f'binary executable / key dilarang: {name}')
                files[name]=info
            if total>MAX_TOTAL:errors.append('ukuran unpacked melebihi batas')
            if 'manifest.json' not in files: return errors+['manifest.json wajib']
            if not any(k.startswith('payload/') for k in files): errors.append('payload/ harus berisi file')
            try: meta=json.loads(archive.read('manifest.json'))
            except Exception as exc: return errors+[f'manifest.json tidak valid: {exc}']
            if meta.get('schema_version')!=1:errors.append('schema_version paket bukan 1')
            family=meta.get('family')
            if family not in FAMILIES:errors.append('family paket salah')
            if meta.get('package_id')!=f'org.n179.renderer.{family}':errors.append('package_id salah')
            if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.\-]+)?',meta.get('version','')):
                errors.append('version bukan semver')
            exts=meta.get('verified_extensions')
            if not isinstance(exts,list) or not exts:errors.append('verified_extensions paket harus tidak kosong')
            if not meta.get('min_core_version'):errors.append('min_core_version wajib')
            declared=meta.get('files')
            if not isinstance(declared,dict): return errors+['files hash map wajib']
            actual=set(files)-{'manifest.json'}
            if set(declared)!=actual:errors.append('daftar file manifest != isi ZIP')
            for fname,expected in declared.items():
                if not fname.startswith('payload/') or not SHA.fullmatch(str(expected)):
                    errors.append(f'path/hash invalid: {fname}');continue
                if fname not in files:continue
                # read dengan batasan: jangan dialokasikan tanpa batas
                h=hashlib.sha256()
                with archive.open(files[fname]) as src:
                    while True:
                        chunk=src.read(256*1024)
                        if not chunk:break
                        h.update(chunk)
                if h.hexdigest()!=expected:errors.append(f'hash mismatch: {fname}')
            return errors
    except (OSError,zipfile.BadZipFile,RuntimeError,ValueError) as exc:
        return [f'gagal memeriksa ZIP: {exc}']


def main():
    if len(sys.argv)!=2:
        print('Usage: python tools/validate_pack.py <renderer-pack.zip>');return 2
    errors=validate(Path(sys.argv[1]))
    for e in errors:print('ERROR:',e)
    if errors:return 1
    print('PASS: zip safety + per-file SHA-256 + manifest contract')
    print('WARNING: tanda tangan publik dan kompatibilitas Android tetap harus diuji di aplikasi')
    return 0


if __name__=='__main__':sys.exit(main())
