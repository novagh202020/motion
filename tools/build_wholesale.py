import os, pathlib, shutil, re, sys
from playwright.sync_api import sync_playwright
root=pathlib.Path('.'); src=pathlib.Path('catalog/catalog.html').read_text(encoding='utf8')
head,body=src.split('<div class="wrap">',1)
def doc(b): return ('<!doctype html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  +head.strip()+'\n</head>\n<body>\n<div class="wrap">'+b.replace('</script>\n','</script>\n</body>\n</html>\n',1))
# 1) PDF
tmp=pathlib.Path('catalog/_print.html'); tmp.write_text(doc(body),encoding='utf8')
out=pathlib.Path('out/final'); out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
  br=p.chromium.launch(executable_path=os.environ.get('CHROME_PATH'))
  pg=br.new_page(viewport={'width':900,'height':1200}); pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(2000)
  pg.emulate_media(media='print'); pg.pdf(path=str(out/'cardiag_wholesale_catalog.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
  br.close()
tmp.unlink()
# 2) site package
site=pathlib.Path('out/site/cardiag-wholesale'); shutil.rmtree(site.parent,ignore_errors=True); site.mkdir(parents=True)
dl=('\n <section class="sec screen-only" id="downloads">\n  <header><p class="eyebrow">دریافت</p><h2>نسخه PDF کاتالوگ</h2></header>\n'
    '  <p><a class="dl" href="downloads/cardiag_wholesale_catalog.pdf" download>دریافت فایل PDF کاتالوگ</a></p>\n </section>\n</div>\n\n<script>')
b2=body.replace('\n</div>\n\n<script>',dl,1); assert b2!=body
h2=doc(b2).replace('</style>','.dl{display:inline-flex;align-items:center;gap:10px;font-weight:800;font-size:18px;color:#fff;background:var(--blue);border-radius:999px;padding:14px 28px;text-decoration:none}\n.dl:focus-visible{outline:3px solid var(--deep);outline-offset:3px}\n</style>',1)
(site/'index.html').write_text(h2,encoding='utf8')
shutil.copytree('catalog/media',site/'media')
(site/'downloads').mkdir(); shutil.copy(out/'cardiag_wholesale_catalog.pdf',site/'downloads')
v=site.parent/'videos'; v.mkdir()
for f in ['cardiag_wholesale_music.mp4','cardiag_wholesale_sfx.mp4']: shutil.copy(out/f,v/f)
print('ok')
