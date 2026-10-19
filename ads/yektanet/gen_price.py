"""Price campaign: «عیب‌یاب هوش مصنوعی خودرو» + ۱٬۴۹۰٬۰۰۰ (was ۲٬۱۰۰٬۰۰۰). Writes price_<W>x<H>.html."""
from gen import phone, card, bt, diag, ring, brand, write

OLD, NEW, OFF = '۲٬۱۰۰٬۰۰۰', '۱٬۴۹۰٬۰۰۰', '۳۰٪ تخفیف'  # exact (2.1M − 1.49M) / 2.1M is 29%; rounded to 30% at the owner's request


def title(sep='<br>'):
    return (f'<div id="title" class="a h">عیب‌یاب <span class="ai">هوش مصنوعی<span class="shine" data-t0="0.3"></span></span>'
            f'{sep}خودرو</div>')


def sub(text='برای خودروهای ایرانی و خارجی'):
    return f'<div id="sub" class="a">{text}</div>'


def price(stack_tm=False):
    new = (f'<div class="r"><span class="new">{NEW}</span></div><div class="r"><span class="tm">تومان</span></div>' if stack_tm
           else f'<div class="r"><span class="new">{NEW}</span> <span class="tm">تومان</span></div>')
    return (f'<div id="price" class="a"><div class="r"><span class="old">{OLD}</span><span id="badge">{OFF}</span></div>{new}'
            '<span class="shine" data-t0="1.4"></span></div>')


def tag():  # compact P0301 card for the phone
    return card(full=True).replace('<div class="s">احتراق ناقص سیلندر ۱</div>', '').replace('<i></i>', '') \
        .replace('</div><div id="ok">', '</div><br><div id="ok">')


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
    "#brand{right:26px;top:26px;height:36px;padding:0 18px;border-radius:18px;font-size:19px;box-shadow:0 6px 14px rgba(20,40,80,.25)}"
    "#title{right:26px;top:80px;font-size:35px;line-height:1.45}"
    "#sub{right:26px;top:190px;font-size:18px}"
    "#price{right:26px;top:238px;padding:10px 18px 8px;border-radius:18px}"
    "#price .r{gap:10px}#price .old{font-size:17px}#badge{font-size:13px;padding:2px 9px;border-radius:9px}"
    "#price .new{font-size:38px;line-height:1.15}#price .tm{font-size:18px;margin-right:6px}",
    ring(-70, 10, 430) + ring(0, 80, 290) + ph + bt(600, 400, 196, 276, 14, 72, 4) + diag(152, 266, 134, 3) + card() +
    brand() + title() + sub() + price())

# ---- 300x250 ----
pc, ph = phone(62, 16, 80)
SIZES[(300, 250)] = (
    "#c{background:radial-gradient(circle at 25% 65%,#4AACFA 0%,rgba(74,172,250,0) 45%),#2793eb}" + pc +
    "#title{left:0;top:9px;width:300px;text-align:center;font-size:20.5px;line-height:1.3}"
    "#sub{left:0;top:42px;width:300px;text-align:center;font-size:12.5px}"
    "#card{left:6px;top:116px;width:84px;padding:4px 4px 5px;border-radius:8px}"
    "#card .t{font-size:7px;margin-bottom:3px}#card .code{border-radius:5px;padding:0 5px;font-size:12px}"
    "#ok{margin-top:3px;height:12px;padding:0 4px;border-radius:6px;font-size:6px}"
    "#price{right:10px;top:92px;padding:8px 11px 6px;border-radius:13px}"
    "#price .r{gap:6px}#price .old{font-size:12px}#badge{font-size:9.5px;padding:1px 6px;border-radius:6px}"
    "#price .new{font-size:25px;line-height:1.15}#price .tm{font-size:12px;margin-right:4px}"
    "#brand{left:0;top:212px;width:300px;height:38px;font-size:21px;box-shadow:0 -4px 12px rgba(20,40,80,.18)}",
    ring(-40, 70, 200) + ph + bt(300, 250, 108, 168, 6, 34, 2.2) + diag(76, 150, 84) + tag() +
    title(sep=' ') + sub() + price() + brand())

# ---- 728x90 ----
SIZES[(728, 90)] = (
    "#c{background:radial-gradient(ellipse at 28% 50%,#4AACFA 0%,rgba(74,172,250,0) 40%),#2793eb}"
    "#brand{left:12px;top:25px;height:40px;padding:0 16px;border-radius:20px;font-size:20px;box-shadow:0 6px 14px rgba(20,40,80,.25)}"
    "#title{right:14px;top:9px;font-size:25px;line-height:1.35}"
    "#sub{right:14px;top:52px;font-size:14px}"
    "#price{left:232px;top:13px;padding:6px 11px 4px;border-radius:12px}"
    "#price .r{gap:7px}#price .old{font-size:12px}#badge{font-size:10px;padding:1px 6px;border-radius:6px}"
    "#price .new{font-size:24px;line-height:1.1}#price .tm{font-size:12px;margin-right:4px}",
    ring(130, -60, 210) + diag(140, 14, 86) + brand() + title(sep=' ') + sub() + price())

# ---- 468x60 ----
SIZES[(468, 60)] = (
    "#c{background:radial-gradient(ellipse at 18% 50%,#4AACFA 0%,rgba(74,172,250,0) 40%),#2793eb}"
    "#title{right:8px;top:4px;font-size:19.5px;line-height:1.35}"
    "#sub{right:8px;top:36px;font-size:11px}"
    "#price{left:74px;top:6px;padding:4px 8px 3px;border-radius:9px}"
    "#price .r{gap:5px}#price .old{font-size:9px}#badge{font-size:7.5px;padding:0 4px;border-radius:4px}"
    "#price .new{font-size:19px;line-height:1.1}#price .tm{font-size:9px;margin-right:3px}",
    diag(5, 7, 64, 1) + title(sep=' ') + sub() + price())

# ---- 300x100 ----
SIZES[(300, 100)] = (
    "#c{background:radial-gradient(ellipse at 18% 45%,#4AACFA 0%,rgba(74,172,250,0) 50%),#2793eb}"
    "#brand{left:8px;top:74px;height:21px;padding:0 10px;border-radius:11px;font-size:13px;box-shadow:0 4px 10px rgba(20,40,80,.25)}"
    "#title{right:8px;top:5px;font-size:15px;line-height:1.35}"
    "#sub{right:8px;top:29px;font-size:9.5px}"
    "#price{right:8px;top:47px;padding:4px 9px 3px;border-radius:9px}"
    "#price .r{gap:5px}#price .old{font-size:9px}#badge{font-size:7.5px;padding:0 4px;border-radius:4px}"
    "#price .new{font-size:20px;line-height:1.1}#price .tm{font-size:9.5px;margin-right:3px}",
    ring(-40, -30, 170) + diag(6, 6, 88, 1) + brand() + title(sep=' ') + sub() + price())

# ---- 120x600 ----
pc, ph = phone(80, 16, 176)
SIZES[(120, 600)] = (
    "#c{background:radial-gradient(ellipse at 50% 52%,#4AACFA 0%,rgba(74,172,250,0) 45%),#2793eb}" + pc +
    "#title{left:0;top:16px;width:120px;text-align:center;font-size:24px;line-height:1.42}#title .ai{font-size:.74em;padding:0 .25em}"
    "#sub{left:0;top:128px;width:120px;text-align:center;font-size:11px;line-height:1.5;white-space:normal}"
    "#card{left:8px;top:236px;width:104px;padding:6px 5px 7px;border-radius:10px}"
    "#card .t{font-size:9px;margin-bottom:4px}#card .code{border-radius:6px;padding:0 7px;font-size:16px}"
    "#ok{margin-top:4px;height:14px;padding:0 5px;border-radius:7px;font-size:7.4px}"
    "#price{left:8px;top:436px;width:104px;padding:8px 6px 7px;border-radius:14px;text-align:center}"
    "#price .r{gap:5px;justify-content:center}#price .old{font-size:12px}#badge{font-size:9px;padding:1px 5px;border-radius:5px}"
    "#price .new{font-size:19px;line-height:1.25}#price .tm{font-size:12px}"
    "#brand{left:0;top:548px;width:120px;height:52px;font-size:19px;box-shadow:0 -4px 12px rgba(20,40,80,.18)}",
    ring(-60, 170, 240) + ph + bt(120, 600, 64, 356, 8, 44, 2.6) + diag(14, 340, 98) + tag() +
    title().replace('عیب‌یاب <span', 'عیب‌یاب<br><span') + sub('برای خودروهای<br>ایرانی و خارجی') + price(stack_tm=True) + brand())

if __name__ == '__main__':
    write(SIZES, 'price')
