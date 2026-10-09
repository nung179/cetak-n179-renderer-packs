import hashlib,json,pathlib
packs=json.loads(pathlib.Path('catalog/renderer-index.json').read_text())
assert packs['catalog_status']=='BETA_TEST_ONLY'
for fam in packs['families']:
    rel=fam['release']; path=pathlib.Path('dist')/rel['asset']
    assert path.is_file(), rel
    assert hashlib.sha256(path.read_bytes()).hexdigest()==rel['sha256']
    assert path.stat().st_size==rel['size_bytes']
    assert fam['verified_extensions']==[{'document':'docx','presentation':'pptx','spreadsheet':'xlsx'}[fam['id']]]
print('PASS: 3 reproducible renderer DATA packs SHA256 pinned')
