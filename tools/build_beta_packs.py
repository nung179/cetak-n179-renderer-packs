from pathlib import Path
import hashlib, json, zipfile
root=Path('.')
pub=root
repo=root
for p in ['tools','catalog','.github/workflows']:(pub/p).mkdir(parents=True,exist_ok=True)
# Build deterministic DATA-only profiles and match the pinned catalog SHA256
families = {
 'document': {'verified_extensions':['docx'], 'layout':{'family':'document','layout_version':1,'margin_pt':42.0,'body_font_pt':10.7,'max_pages':500},'fidelity':'LIMITED'},
 'spreadsheet':{'verified_extensions':['xlsx'], 'layout':{'family':'spreadsheet','layout_version':1,'margin_pt':25.0,'row_height_pt':22.0,'max_pages':500},'fidelity':'LIMITED'},
 'presentation':{'verified_extensions':['pptx'],'layout':{'family':'presentation','layout_version':1,'slide_background':'WHITE','max_pages':150},'fidelity':'LIMITED'},
}
tag='beta-v0.1.0'
assets=root/'dist';assets.mkdir(exist_ok=True)
catalog=json.loads((repo/'catalog/renderer-index.json').read_text())
catalog['catalog_status']='BETA_TEST_ONLY'
catalog['core_note']='R116 beta: CORE memiliki parser OOXML dasar, pack berupa profil DATA; BUKAN Office full fidelity. Periksa tes HP sebelum produksi.'
catalog['security']={'distribution_host':'github.com','signature_mode':'SHA256_PINNED_IN_APK','trusted_key_id':None}
sha={}
for f in catalog['families']:
 family=f['id'];d=families[family];fname=f'renderer-{family}-v0.1.0-beta.1.n179r'
 payload=json.dumps(d['layout'],indent=2,ensure_ascii=False,sort_keys=True).encode()+b'\n'
 manifest={'schema_version':1,'family':family,'package_id':f'org.n179.renderer.{family}','version':'0.1.0-beta.1','verified_extensions':d['verified_extensions'],'min_core_version':'0.1.104','fidelity':'LIMITED','kind':'DECLARATIVE_RENDER_PROFILE','files':{'payload/layout.json':hashlib.sha256(payload).hexdigest()}}
 m=json.dumps(manifest,sort_keys=True,indent=2,ensure_ascii=False).encode()+b'\n'
 with zipfile.ZipFile(assets/fname,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,blob in [('manifest.json',m),('payload/layout.json',payload)]:
   info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,blob)
 h=hashlib.sha256((assets/fname).read_bytes()).hexdigest();sha[family]=h
 f['verified_extensions']=d['verified_extensions'];f['status']='BETA_STAGING_NOT_VERIFIED_ON_PHONE'
 f['release']={'tag':tag,'asset':fname,'url':f'https://github.com/nung179/cetak-n179-renderer-packs/releases/download/{tag}/{fname}','sha256':h,'size_bytes':(assets/fname).stat().st_size,'fidelity': 'LIMITED'}

print('built:', *(str(p) for p in sorted(assets.glob('*.n179r'))))
for f in catalog['families']:
    if f['release']['sha256'] != sha[f['id']]: raise SystemExit(f"Mismatch catalogue: {f['id']}")
