"""Generates banner_<W>x<H>.html for every Yektanet size (shared look in common.css, motion in anim.js)."""
import pathlib

ICON = ('<svg width="{w}" height="{h}" viewBox="0 0 24 18" fill="none" stroke="#F28012" stroke-width="2.8" '
        'stroke-linejoin="round" stroke-linecap="round"><path d="M5 5h3V2h7v3h3l2 3h2v5h-2l-2 3H8L5 13H2V7h3z"/></svg>')


def chip(icon, text='چراغ چک روشن شده؟'):
    return f'<div id="chip" class="a h"><i><span id="halo"></span>{ICON.format(w=icon, h=round(icon * .78))}</i><span>{text}</span><span id="shine"></span></div>'


def title(sep='<br>', l1='قبل از تعمیرگاه،', l2a='علتش رو'):
    return f'<div id="title" class="a h">{l1}{sep}{l2a} <u>خودت ببین<b id="ul"></b></u></div>'


def phone(S, left, top, statusbar=False):
    k = S / 154
    pad = max(3, round(7 * k))
    h = round(S * 338 / 154)
    css = (f"#phone{{left:{left}px;top:{top}px;width:{S + 2 * pad}px;height:{h + 2 * pad}px;border-radius:{30 * k:.1f}px}}"
           f"#scr{{left:{pad}px;top:{pad}px;width:{S}px;height:{h}px;border-radius:{24 * k:.1f}px}}"
           f"#scr img{{top:{10 * k:.1f}px;width:{S}px}}"
           f"#isl{{left:{55 * k:.1f}px;top:{5 * k:.1f}px;width:{44 * k:.1f}px;height:{12 * k:.1f}px;border-radius:{7 * k:.1f}px}}"
           f"#st{{left:{91 * k:.1f}px;top:{56 * k:.1f}px;width:{24 * k:.1f}px;height:{10 * k:.1f}px;font-size:{7.4 * k:.2f}px;line-height:{10 * k:.1f}px}}")
    sb = ''
    if statusbar:
        css += "#sb{left:0;top:0;width:%dpx;height:18px;font:700 7px V;color:#10203C;display:flex;justify-content:space-between;align-items:center;padding:3px 16px 0}" % S
        sb = '<div id="sb" class="a"><span>۱۲:۳۴</span><span>۱۰۰٪</span></div>'
    html = (f'<div id="phone" class="a"><div id="scr" class="a"><img src="app_home.jpg" alt="">{sb}'
            '<div id="isl" class="a"></div><div id="st" class="a">متصل</div></div></div>')
    return css, html


def card(full=True, ok='✓ علت و راه‌حل آماده‌ست', dy=12):
    if full:
        inner = ('<div class="t"><i></i>کد خطا پیدا شد</div><div class="code">P0301</div>'
                 '<div class="s">احتراق ناقص سیلندر ۱</div><div id="ok">' + ok + '</div>')
    else:
        inner = f'<div class="code">P0301</div><div id="ok">{ok}</div>'
    return f'<div id="card" class="a" data-dy="{dy}">{inner}</div>'


def bt(W, H, ox, oy, r0, r1, w):
    return f'<svg id="bt" class="a" style="left:0;top:0;overflow:visible" width="{W}" height="{H}" data-ox="{ox}" data-oy="{oy}" data-r0="{r0}" data-r1="{r1}" data-w="{w}"></svg>'


def diag(left, top, w, amp=2):
    return f'<img id="diag" class="a" src="diag.png" alt="" style="left:{left}px;top:{top}px;width:{w}px" data-amp="{amp}">'


def ring(l, t, d):
    return f'<div class="a ring" style="left:{l}px;top:{t}px;width:{d}px;height:{d}px"></div>'


def brand(): return '<div id="brand" class="a">CarDiag AI</div>'


SIZES = {}

# ---- 600x400 ----
pc, ph = phone(154, 46, 24, statusbar=True)
SIZES[(600, 400)] = (
    "#c{background:radial-gradient(circle at 24% 55%,#4AACFA 0%,rgba(74,172,250,0) 48%),#2793eb}" + pc +
    "#card{left:34px;top:140px;width:168px;padding:9px 11px 10px;border-radius:16px;text-align:right}"
    "#card .t{font-size:12px;display:flex;align-items:center;gap:6px}"
    "#card .t i{width:16px;height:16px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#FFC446,#F28012)}"
    "#card .code{margin-top:7px;border-radius:9px;padding:1px 10px;font-size:21px}"
    "#card .s{margin-top:5px;font:500 11px V;color:#6E7D96}"
    "#ok{margin-right:0;margin-top:7px;height:22px;padding:0 10px;border-radius:11px;font-size:11px}"
    "#chip{right:26px;top:50px;height:44px;padding:0 7px 0 18px;border-radius:22px;gap:9px;font-size:21px}"
    "#chip i{width:32px;height:32px}"
    "#title{right:26px;top:110px;font-size:35px;line-height:1.35}#title u b{bottom:4px;height:5px}"
    "#sub{right:26px;top:226px;width:285px;font:500 16px/1.7 V;color:#E6F3FF;direction:rtl}"
    "#brand{right:26px;top:310px;height:50px;padding:0 28px;border-radius:25px;font-size:26px;box-shadow:0 8px 18px rgba(20,40,80,.25)}",
    ring(-70, 10, 430) + ring(0, 80, 290) + ph + bt(600, 400, 196, 276, 14, 72, 4) + diag(152, 266, 134, 3) + card() +
    chip(17) + title() +
    '<div id="sub" class="a">دیاگ بلوتوثی کاردیاگ رو وصل کن؛ کد خطا و راه‌حل رو فارسی، روی گوشیت ببین.</div>' + brand())

# ---- 300x250 ----
pc, ph = phone(80, 12, 30)
SIZES[(300, 250)] = (
    "#c{background:radial-gradient(circle at 22% 50%,#4AACFA 0%,rgba(74,172,250,0) 50%),#2793eb}" + pc +
    "#card{left:6px;top:110px;width:98px;padding:5px 5px 6px;border-radius:10px}"
    "#card .t{font-size:8.5px;margin-bottom:4px}#card .code{border-radius:6px;padding:0 7px;font-size:15px}#card .s{display:none}"
    "#ok{margin-top:4px;height:14px;padding:0 5px;border-radius:7px;font-size:7px}"
    "#chip{right:10px;top:10px;height:30px;padding:0 5px 0 11px;border-radius:15px;gap:6px;font-size:15px}#chip i{width:22px;height:22px}"
    "#title{right:10px;top:48px;font-size:22px;line-height:1.38}#title u b{bottom:3px;height:3.5px}"
    "#brand{left:0;top:212px;width:300px;height:38px;font-size:21px;box-shadow:0 -4px 12px rgba(20,40,80,.18)}",
    ring(-50, 10, 230) + ph + bt(300, 250, 196, 150, 8, 48, 2.6) + diag(176, 126, 104) +
    card(full=True).replace('<div class="s">احتراق ناقص سیلندر ۱</div>', '').replace('<i></i>', '').replace('</div><div id="ok">', '</div><br><div id="ok">') + chip(14) + title() + brand())

# ---- 728x90 ----
SIZES[(728, 90)] = (
    "#c{background:radial-gradient(ellipse at 28% 50%,#4AACFA 0%,rgba(74,172,250,0) 40%),#2793eb}"
    "#brand{left:12px;top:24px;height:42px;padding:0 18px;border-radius:21px;font-size:21px;box-shadow:0 6px 14px rgba(20,40,80,.25)}"
    "#card{left:226px;top:14px;padding:4px 6px 5px;border-radius:9px;display:flex;flex-direction:column;align-items:center}"
    "#card .code{border-radius:5px;padding:0 6px;font-size:13px}"
    "#ok{margin-top:3px;height:14px;padding:0 6px;border-radius:7px;font-size:8px}"
    "#chip{right:14px;top:8px;height:28px;padding:0 4px 0 11px;border-radius:14px;gap:6px;font-size:14.5px}#chip i{width:20px;height:20px}"
    "#title{right:14px;top:42px;font-size:25px;line-height:1.4}#title u b{bottom:3px;height:3.5px}",
    ring(130, -60, 210) + diag(150, 12, 92) + card(full=False, ok='✓ علت پیدا شد', dy=8) + brand() + chip(12) + title(sep=' '))

# ---- 468x60 ----
SIZES[(468, 60)] = (
    "#c{background:radial-gradient(ellipse at 26% 50%,#4AACFA 0%,rgba(74,172,250,0) 40%),#2793eb}"
    "#brand{left:7px;top:15px;height:30px;padding:0 11px;border-radius:15px;font-size:15px;box-shadow:0 4px 10px rgba(20,40,80,.25)}"
    "#card{left:136px;top:7px;padding:3px 4px 4px;border-radius:6px;display:flex;flex-direction:column;align-items:center}"
    "#card .code{border-radius:4px;padding:0 4px;font-size:9.5px}"
    "#ok{margin-top:2px;height:10px;padding:0 4px;border-radius:5px;font-size:6.5px}"
    "#chip{right:8px;top:4px;height:22px;padding:0 3px 0 9px;border-radius:11px;gap:5px;font-size:12px}#chip i{width:16px;height:16px}"
    "#title{right:8px;top:28px;font-size:17.5px;line-height:1.4}#title u b{bottom:2px;height:2.5px}",
    diag(108, 7, 64, 1) + card(full=False, ok='✓ علت پیدا شد', dy=5) + brand() + chip(10) + title(sep=' '))

# ---- 300x100 ----
SIZES[(300, 100)] = (
    "#c{background:radial-gradient(ellipse at 22% 45%,#4AACFA 0%,rgba(74,172,250,0) 50%),#2793eb}"
    "#brand{left:8px;top:74px;height:21px;padding:0 10px;border-radius:11px;font-size:13px;box-shadow:0 4px 10px rgba(20,40,80,.25)}"
    "#card{left:62px;top:28px;padding:3px 4px 4px;border-radius:7px;display:flex;flex-direction:column;align-items:center}"
    "#card .code{border-radius:4px;padding:0 5px;font-size:11px}"
    "#ok{margin-top:2px;height:11px;padding:0 4px;border-radius:6px;font-size:6.5px}"
    "#chip{right:8px;top:7px;height:24px;padding:0 3px 0 9px;border-radius:12px;gap:5px;font-size:13px}#chip i{width:18px;height:18px}"
    "#title{right:8px;top:36px;font-size:18px;line-height:1.3}#title u b{bottom:2px;height:2.5px}",
    ring(-40, -30, 170) + diag(6, 2, 98, 1) + card(full=False, ok='✓ علت پیدا شد', dy=5) + brand() + chip(11) + title())

# ---- 120x600 ----
pc, ph = phone(88, 12, 262)
SIZES[(120, 600)] = (
    "#c{background:radial-gradient(ellipse at 50% 62%,#4AACFA 0%,rgba(74,172,250,0) 45%),#2793eb}" + pc +
    "#chip{left:9px;top:14px;width:102px;flex-direction:column;justify-content:center;padding:9px 4px 10px;border-radius:18px;gap:6px;"
    "font-size:16px;line-height:1.3;white-space:normal;text-align:center}#chip i{width:30px;height:30px}"
    "#title{left:0;top:128px;width:120px;text-align:center;font-size:22px;line-height:1.32}#title u b{bottom:3px;height:3.5px}"
    "#card{left:8px;top:322px;width:104px;padding:6px 5px 7px;border-radius:10px}"
    "#card .t{font-size:9px;margin-bottom:4px}#card .code{border-radius:6px;padding:0 7px;font-size:16px}"
    "#ok{margin-top:4px;height:14px;padding:0 5px;border-radius:7px;font-size:7.4px}"
    "#brand{left:0;top:548px;width:120px;height:52px;font-size:19px;box-shadow:0 -4px 12px rgba(20,40,80,.18)}",
    ring(-60, 250, 240) + ph + bt(120, 600, 64, 448, 8, 46, 2.6) + diag(14, 432, 98) +
    card(full=True).replace('<div class="s">احتراق ناقص سیلندر ۱</div>', '').replace('<i></i>', '').replace('</div><div id="ok">', '</div><br><div id="ok">') +
    chip(18, 'چراغ چک<br>روشن شده؟') + title(l1='قبل از<br>تعمیرگاه،<br>', sep='', l2a='علتش رو<br>').replace('علتش رو<br> <u>', 'علتش رو<br><u>') + brand())

TPL = '''<!doctype html>
<html lang="fa"><head><meta charset="utf-8"><title>CarDiag Yektanet {W}x{H}</title>
<link rel="stylesheet" href="common.css">
<style>html,body{{width:{W}px;height:{H}px}}#c{{width:{W}px;height:{H}px}}
{css}</style></head><body>
<div id="c">{html}</div>
<script src="anim.js"></script>
</body></html>
'''

here = pathlib.Path(__file__).parent
for (W, H), (css, html) in SIZES.items():
    (here / f'banner_{W}x{H}.html').write_text(TPL.format(W=W, H=H, css=css.replace('}', '}\n'), html=html))
print('ok', len(SIZES))
