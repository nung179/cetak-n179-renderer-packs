#!/usr/bin/env python3
"""Validator katalog distribusi publik. Stdlib-only, exit code !=0 untuk metadata tidak aman."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'catalog' / 'renderer-index.json'
FAMILIES = {'document', 'presentation', 'spreadsheet'}
SHA = re.compile(r'^[0-9a-f]{64}$')
ASSET = re.compile(r'^n179-renderer-(document|presentation|spreadsheet)-[0-9A-Za-z.+_-]+\.zip$')


def validate(data):
    errors = []
    if data.get('schema_version') != 1: errors.append('schema_version harus 1')
    if data.get('catalog_id') != 'org.n179.renderer.public.v1': errors.append('catalog_id salah')
    if data.get('channel') != 'stable': errors.append('channel belum didukung')
    security = data.get('security', {})
    if not isinstance(security, dict): security = {}; errors.append('security bukan object')
    mode = security.get('signature_mode')
    if mode not in ('NOT_CONFIGURED', 'ED25519_PINNED_V1'): errors.append('signature_mode tak dikenal')
    if security.get('distribution_host') != 'github.com': errors.append('host tak dikenal')
    if mode == 'ED25519_PINNED_V1' and not security.get('trusted_key_id'):
        errors.append('pinned signing key id wajib')
    families = data.get('families')
    if not isinstance(families, list): return errors + ['families harus array']
    ids = [f.get('id') for f in families if isinstance(f, dict)]
    if len(ids) != 3 or set(ids) != FAMILIES: errors.append('wajib tepat 3 family id unik')
    active = 0
    for family in families:
        if not isinstance(family, dict): errors.append('family bukan object'); continue
        fid = family.get('id')
        planned, verified = family.get('planned_extensions'), family.get('verified_extensions')
        if not isinstance(planned, list) or not planned or not all(isinstance(x, str) for x in planned):
            errors.append(f'{fid}: planned_extensions tidak valid'); continue
        if not isinstance(verified, list) or not all(isinstance(x, str) for x in verified):
            errors.append(f'{fid}: verified_extensions tidak valid'); continue
        if len(planned)!=len(set(planned)) or len(verified)!=len(set(verified)):
            errors.append(f'{fid}: ekstensi duplikat')
        if not set(verified).issubset(set(planned)):
            errors.append(f'{fid}: verified_extensions bukan subset planned')
        status, rel = family.get('status'), family.get('release')
        if status not in ('NOT_AVAILABLE', 'AVAILABLE', 'BLOCKED'):
            errors.append(f'{fid}: status salah'); continue
        if status == 'NOT_AVAILABLE':
            if rel is not None or verified: errors.append(f'{fid}: NOT_AVAILABLE harus release null dan verified kosong')
            continue
        if status == 'BLOCKED':
            if not family.get('reason'): errors.append(f'{fid}: BLOCKED harus punya alasan')
            continue
        active += 1
        if mode != 'ED25519_PINNED_V1': errors.append(f'{fid}: AVAILABLE dilarang tanpa signature mode dan pinned key')
        if not verified: errors.append(f'{fid}: AVAILABLE wajib verified_extensions')
        if not isinstance(rel, dict): errors.append(f'{fid}: release metadata wajib'); continue
        name = rel.get('asset_name', '')
        if not ASSET.fullmatch(name) or not name.startswith(f'n179-renderer-{fid}-'):
            errors.append(f'{fid}: asset_name salah')
        url = rel.get('url', '')
        p=urlparse(url)
        prefix='/nung179/cetak-n179-renderer-packs/releases/download/'
        if p.scheme!='https' or p.netloc!='github.com' or not p.path.startswith(prefix) or not p.path.endswith('/'+name) or p.query or p.fragment:
            errors.append(f'{fid}: URL bukan asset release resmi')
        if not isinstance(rel.get('size_bytes'), int) or rel.get('size_bytes')<=0:
            errors.append(f'{fid}: ukuran paket salah')
        if not SHA.fullmatch(rel.get('sha256','')): errors.append(f'{fid}: SHA-256 ZIP tidak valid')
        if not rel.get('signature') or not rel.get('key_id') or rel.get('key_id')!=security.get('trusted_key_id'):
            errors.append(f'{fid}: signature/pinned key wajib dan cocok')
        if not isinstance(rel.get('compatibility'),dict) or not rel['compatibility'].get('min_core_version'):
            errors.append(f'{fid}: compatibility wajib')
    expected = 'PACKS_PUBLISHED' if active else 'NO_PUBLISHED_PACKS'
    if data.get('catalog_status') != expected: errors.append('catalog_status tidak sesuai ketersediaan')
    return errors


def main():
    try: data=json.loads(INDEX.read_text(encoding='utf-8'))
    except Exception as exc: print('ERROR membaca index:',exc); return 2
    errors=validate(data)
    if errors:
        for err in errors: print('ERROR:',err)
        return 1
    print('PASS: catalog schema, family, status, security, URL/hash metadata')
    print('PACKS AVAILABLE:',sum(x['status']=='AVAILABLE' for x in data['families']))
    return 0


if __name__=='__main__': sys.exit(main())
