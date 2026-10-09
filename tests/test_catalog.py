import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_catalog import validate
from validate_pack import validate as validate_pack

class RendererRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'catalog'/'renderer-index.json').read_text(encoding='utf-8'))

    def test_current_catalog_is_valid(self):
        self.assertEqual(validate(self.data),[])

    def test_no_fake_available_without_signed_manifest(self):
        self.data['families'][0]['status']='AVAILABLE'
        self.assertTrue(validate(self.data))

    def test_bad_catalog_family(self):
        self.data['families'][0]['id']='unknown'
        self.assertTrue(validate(self.data))

    def test_cannot_claim_formats_as_verified_if_unavailable(self):
        self.data['families'][0]['status']='NOT_AVAILABLE'
        self.assertTrue(validate(self.data))

    def test_candidate_release_url_requires_known_origin(self):
        self.data['security']['signature_mode']='ED25519_PINNED_V1'
        self.data['security']['trusted_key_id']='KEY1'
        self.data['catalog_status']='PACKS_PUBLISHED'
        f=self.data['families'][0]
        f['status']='AVAILABLE'
        f['verified_extensions']=['docx']
        f['release']={'asset_name':'n179-renderer-document-1.0.0.zip',
          'url':'https://attacker.invalid/file.zip','size_bytes':100,'sha256':'a'*64,
          'signature':'BASE64','key_id':'KEY1','compatibility':{'min_core_version':'0.1.103'}}
        self.assertIn('document: URL bukan asset release resmi',validate(self.data))

    def _pack(self, bad_path=None, bad_sha=False):
        content=b'RENDERER-TEST-FIXTURE-NOT-A-REAL-ENGINE'
        path=bad_path or 'payload/runtime/example.dat'
        man={'schema_version':1,'family':'document','package_id':'org.n179.renderer.document',
             'version':'1.0.0','min_core_version':'0.1.103','verified_extensions':['docx'],
             'files':{path: ('0'*64 if bad_sha else hashlib.sha256(content).hexdigest())}}
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
            z.writestr('manifest.json',json.dumps(man))
            z.writestr(path,content)
        tmp=tempfile.NamedTemporaryFile(suffix='.zip',delete=False)
        tmp.write(buf.getvalue());tmp.close()
        return Path(tmp.name)

    def test_valid_synthetic_pack_manifest(self):
        p=self._pack()
        try:self.assertEqual(validate_pack(p),[])
        finally:p.unlink()

    def test_reject_bad_pack_hash(self):
        p=self._pack(bad_sha=True)
        try:self.assertTrue(any('hash mismatch' in e for e in validate_pack(p)))
        finally:p.unlink()

    def test_reject_zip_path_traversal(self):
        p=self._pack(bad_path='payload/../../sneaky.dat')
        try:self.assertTrue(any('path berbahaya' in e for e in validate_pack(p)))
        finally:p.unlink()

    def test_reject_executable_in_pack(self):
        p=self._pack(bad_path='payload/test.apk')
        try:self.assertTrue(any('dilarang' in e for e in validate_pack(p)))
        finally:p.unlink()


class RendererBetaExtraTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'catalog'/'renderer-index.json').read_text(encoding='utf-8'))
    def test_beta_catalog_pinned_urls(self):
        self.assertEqual(validate(self.data), [])
    def test_block_arbitrary_download_host(self):
        self.data['families'][0]['release']['url']='https://evil.example/a.n179r'
        self.assertTrue(any('URL beta tidak aman' in x for x in validate(self.data)))
    def test_beta_cannot_pretend_native(self):
        self.data['families'][0]['release']['fidelity']='NATIVE'
        self.assertTrue(validate(self.data))

if __name__=='__main__':unittest.main()
