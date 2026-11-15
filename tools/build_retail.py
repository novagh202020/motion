import os, pathlib, shutil
from playwright.sync_api import sync_playwright
src=pathlib.Path('catalog/retail.html').read_text(encoding='utf8')
head,body=src.split('<div class="wrap">',1)
def doc(b): return ('<!doctype html>\n<html lang="fa" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  +head.strip()+'\n</head>\n<body>\n<div class="wrap">'+b.replace('</script>\n','</script>\n</body>\n</html>\n',1))
out=pathlib.Path('out/final'); out.mkdir(parents=True,exist_ok=True)
PDF=out/'cardiag_catalog.pdf'
tmp=pathlib.Path('catalog/_print_r.html'); tmp.write_text(doc(body),encoding='utf8')
with sync_playwright() as p:
  br=p.chromium.launch(executable_path=os.environ.get('CHROME_PATH'))
  pg=br.new_page(viewport={'width':900,'height':1200}); pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(2000)
  pg.emulate_media(media='print'); pg.pdf(path=str(PDF),format='A4',print_background=True,prefer_css_page_size=True)
  br.close()
tmp.unlink()
root=pathlib.Path('out/site_retail'); shutil.rmtree(root,ignore_errors=True); site=root/'cardiag-catalog'; (site/'media').mkdir(parents=True)
dl=('\n <section class="sec screen-only" id="downloads">\n  <header><p class="eyebrow">دریافت</p><h2>نسخه PDF کاتالوگ</h2></header>\n'
    '  <p><a class="buy" href="downloads/cardiag_catalog.pdf" download>دریافت فایل PDF کاتالوگ</a></p>\n </section>\n</div>\n\n<script>')
b2=body.replace('\n</div>\n\n<script>',dl,1); assert b2!=body
(site/'index.html').write_text(doc(b2),encoding='utf8')
for f in ['retail.mp4','retail.jpg','diag_plug.png']+[f'clip_{n}.{e}' for n in ['ecu','ai','trip','bat','km','mon','svc'] for e in ['mp4','jpg']]:
  shutil.copy('catalog/media/'+f,site/'media'/f)
(site/'downloads').mkdir(); shutil.copy(PDF,site/'downloads')
v=root/'videos'; v.mkdir()
for f in ['cardiag_retail_music.mp4','cardiag_retail_sfx.mp4']: shutil.copy(out/f,v/f)
(root/'README.txt').write_text('''کاتالوگ محصول کاردیاگ (مشتریان خرد) - راهنمای فایل‌ها

cardiag-catalog/     پوشه سایت؛ کل پوشه را روی هاست آپلود کنید (مثلاً cardiag.ir/catalog/)
  index.html         صفحه کاتالوگ (فونت وزیرمتن داخل خود صفحه قرار دارد)
  media/             ویدیوی معرفی و ویدیوهای کوتاه بخش‌ها
  downloads/         نسخه PDF کاتالوگ
videos/
  cardiag_retail_music.mp4   موشن ۳۰ ثانیه‌ای معرفی با موزیک کاردیاگ (۱۰۸۰×۱۹۲۰)
  cardiag_retail_sfx.mp4     همان موشن فقط با افکت صوتی (برای آهنگ‌های اینستاگرام)

ویدیوهای آپارات:
در فایل index.html، بخش «const APARAT» را پیدا کنید و لینک هر ویدیو را جلوی کلید آن بگذارید:
  hero = ویدیوی معرفی (۱)، ecu، ai، trip، bat، km، mon، svc = ویدیوهای ۲ تا ۸
تا زمانی که لینکی وارد نشده باشد، ویدیوی معرفی و کلیپ‌های کوتاه فعلی نمایش داده می‌شوند.
''',encoding='utf8')
print('ok')
