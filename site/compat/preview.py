"""Writes preview.html (checker + local fonts + local CSV) for checking in a browser."""
import pathlib
h=pathlib.Path(__file__).parent
snip=(h/'checker.html').read_text(encoding='utf-8').replace('data-csv="/wp-content/uploads/cardiag-compat.csv"','data-csv="cardiag-compat.csv"')
ff=''.join(f'@font-face{{font-family:Vazirmatn;font-weight:{w};src:url(../../fonts/Vazirmatn-FD-{n}.ttf)}}' for w,n in [(500,'Medium'),(700,'Bold'),(800,'ExtraBold'),(900,'Black')])
(h/'preview.html').write_text(f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>بررسی سازگاری کاردیاگ</title><style>{ff}body{{margin:0;background:#F4F8FD}}</style></head><body>{snip}</body></html>',encoding='utf-8')
