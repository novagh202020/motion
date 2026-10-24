"""Build the Elementor data for the CarDiag product page.

template_3124.json -> Elementor Pro product template (hero, buy box, section chips, product content)
product_2560.json  -> the product's own Elementor content (all sections below the hero)

Text lives in normal Elementor widgets so it can be edited in the editor; assets.html (CSS, sticky bar,
added-to-cart popup) goes into one HTML widget in the template. Text from the old page is reused verbatim
where possible (backup/2560_elementor_data.json)."""
import json, re, hashlib, pathlib, urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
OLD = json.loads((HERE.parent / 'backup' / '2560_elementor_data.json').read_text())[0]['elements'][0]['settings']['editor']
FA = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
fa = lambda s: re.sub(r'(?<![A-Za-z\d])\d+(?![A-Za-z\d])', lambda m: m.group(0).translate(FA), s)

_n = [0]
def nid(seed):
    _n[0] += 1
    return hashlib.md5(f'cdp{seed}{_n[0]}'.encode()).hexdigest()[:8]

Z = {"unit": "px", "top": 0, "right": 0, "bottom": 0, "left": 0, "isLinked": True}
gap = lambda px: {"unit": "px", "size": px, "column": str(px), "row": str(px), "isLinked": True}

def C(cls, kids, direction='column', g=14, anchor=None, **extra):
    s = {"content_width": "full", "flex_direction": direction, "flex_gap": gap(g), "padding": Z, "css_classes": cls}
    if anchor: s["_element_id"] = anchor
    s.update(extra)
    return {"id": nid(cls), "elType": "container", "settings": s, "elements": kids, "isInner": False}

def W(kind, cls='', **settings):
    if cls: settings["_css_classes"] = cls
    return {"id": nid(kind), "elType": "widget", "widgetType": kind, "settings": settings, "elements": []}

def heading(html, cls='', size='h2', **kw): return W('heading', cls, title=html, header_size=size, **kw)
def text(html, cls=''): return W('text-editor', cls, editor=html)
def icon(v): return {"value": v, "library": "fa-brands" if v.startswith("fab ") else "fa-solid"}
def ibox(ic, title, desc, cls='', link=None):
    s = dict(selected_icon=icon(ic), title_text=title, description_text=desc, position='right', title_size='h3')
    if link: s['link'] = {"url": link, "is_external": "", "nofollow": ""}
    return W('icon-box', cls, **s)
def ilist(items, cls='', inline=False):
    rows = []
    for it in items:
        t, ic, link = (it + (None, None))[:3] if isinstance(it, tuple) else (it, None, None)
        r = {"_id": nid('li')[:7], "text": t, "selected_icon": icon(ic) if ic else {"value": "", "library": ""}}
        if link: r["link"] = {"url": link, "is_external": "", "nofollow": ""}
        rows.append(r)
    s = {"icon_list": rows}
    if inline: s["view"] = "inline"
    return W('icon-list', cls, **s)
def accordion(items, cls='cdp-acc', faq=False):
    s = {"tabs": [{"_id": nid('ac')[:7], "tab_title": t, "tab_content": c} for t, c in items],
         "selected_icon": icon("fas fa-chevron-down"), "selected_active_icon": icon("fas fa-chevron-up"), "title_html_tag": "h3"}
    if faq: s["faq_schema"] = "yes"
    return W('accordion', cls, **s)
def price_tag(fmt):
    tag = urllib.parse.quote(json.dumps({"format": fmt}, separators=(',', ':')))
    return f'[elementor-tag id="{nid("t")[:7]}" name="woocommerce-product-price-tag" settings="{tag}"]'

# ---------------------------------------------------------------- template 3124 (hero)
assets = (HERE / 'assets.html').read_text()
buy_form = ('<form class="cdp-cart" method="post" enctype="multipart/form-data">'
            '<div class="cdp-qty"><button type="button" data-q="-1" aria-label="کم کردن">−</button>'
            '<input type="number" name="quantity" value="1" min="1" max="99" inputmode="numeric" aria-label="تعداد">'
            '<button type="button" data-q="1" aria-label="زیاد کردن">+</button></div>'
            '<button type="submit" name="add-to-cart" value="" class="cdp-btn">افزودن به سبد خرید</button></form>')

template = [
    W('html', 'cdp-assets', html=assets),
    C('cdp cdp-wrap cdp-crumbs', [W('woocommerce-breadcrumb')]),
    C('cdp cdp-wrap cdp-hero', [
        C('cdp cdp-gal', [W('html', '', html='<span class="cdp-badge"></span>'),
                          W('theme-post-featured-image', '', image_size='large', __dynamic__={"image": f'[elementor-tag id="{nid("t")[:7]}" name="post-featured-image" settings="%7B%7D"]'})],
          g=0, width={"unit": "%", "size": 50}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100}),
        C('cdp cdp-info', [
            heading('', 'cdp-title', 'h1', __dynamic__={"title": f'[elementor-tag id="{nid("t")[:7]}" name="post-title" settings="%7B%7D"]'}),
            text('<p>مدل شخصی · برای خودروهای ایرانی و خارجی</p>', 'cdp-model'),
            text('<p><span class="in">● موجود در انبار</span><span class="out">ناموجود</span></p>', 'cdp-stock'),
            C('cdp cdp-buybox', [
                C('cdp cdp-prices', [
                    C('cdp', [heading('', 'cdp-old', 'div', __dynamic__={"title": price_tag('original')}),
                              heading('', 'cdp-now', 'div', __dynamic__={"title": price_tag('sale')})], g=0),
                    W('html', '', html='<span class="cdp-save"></span>')], direction='row', g=12,
                  flex_justify_content='space-between', flex_align_items='flex-end',
                  flex_direction_mobile='row', flex_direction_tablet='row'),
                ibox('fas fa-gift', 'اشتراک طلایی اپ، رایگان و همیشگی', 'تعمیرکار هوش مصنوعی و همه‌ی امکانات حرفه‌ای', 'cdp-gift'),
                W('html', 'cdp-buy', html=buy_form),
            ], anchor='cdp-buy'),
            ilist([('۶ ماه گارانتی تعویض', 'fas fa-shield-alt'), ('۵ روز مرجوعی اگر وصل نشد', 'fas fa-undo'),
                   ('ارسال به سراسر کشور', 'fas fa-truck'), ('اپلیکیشن کاملاً فارسی', 'fas fa-language')], 'cdp-trust'),
            ibox('fas fa-car', 'به ماشین من وصل می‌شه؟', 'حدود ۹۰٪ خودروهای ایرانی و همه‌ی خارجی‌ها · دیدن لیست', 'cdp-fit', '#cars'),
            W('theme-post-excerpt', 'cdp-lead', __dynamic__={"excerpt": f'[elementor-tag id="{nid("t")[:7]}" name="post-excerpt" settings="%7B%7D"]'}),
        ], width={"unit": "%", "size": 50}, width_tablet={"unit": "%", "size": 100}, width_mobile={"unit": "%", "size": 100}),
    ], direction='row', g=40, flex_direction_tablet='column', flex_direction_mobile='column', flex_gap_mobile=gap(16),
       flex_gap_tablet=gap(20), flex_align_items='flex-start', flex_wrap='nowrap'),
    C('cdp cdp-snav', [ilist([('امکانات', None, '#app'), ('راه‌اندازی', None, '#setup'), ('مقایسه', None, '#vs'),
                              ('مشخصات', None, '#spec'), ('خودروها', None, '#cars'), ('سوالات', None, '#faq')], inline=True)]),
    C('cdp cdp-body', [W('woocommerce-product-content')]),
]

# ---------------------------------------------------------------- product 2560 (content)
paras = re.findall(r'<p dir="rtl">(.*?)</p>', OLD)[:4]
aparat = re.search(r'<div id="\d+"><script.*?</script></div>', OLD).group(0)
gift_p = re.search(r'<h2>هدیه ویژه خرید.*?</h2>(<p>.*?</p>)', OLD).group(1)

cars = []
for brand, ul in re.findall(r'<p><strong>([^<]+)</strong></p><ul>(.*?)</ul>', OLD):
    if 'پراید' in brand: continue
    rows = []
    for li in re.findall(r'<li>(.*?)</li>', ul):
        mm = re.match(r'(.*?)\s*\(سال‌های\s*(.*?)\)$', li)
        model, years = (mm.group(1), mm.group(2)) if mm else (li, '')
        rows.append(f'<li>{fa(model)}<span>{fa(years)}</span></li>')
    cars.append((f'{fa(brand)} <small>· {fa(str(len(rows)))} مدل</small>', '<ul>' + ''.join(rows) + '</ul>'))

faq = [(q, a) for q, a in re.findall(r'<h3>(.*?)</h3><p>(.*?)</p>', OLD)]
faq = [(fa(q.replace('عیب یاب', 'عیب‌یاب')), fa(a).replace('میتوانید', 'می‌توانید').replace('می شود', 'می‌شود').replace('نمی کنند', 'نمی‌کنند')) for q, a in faq]

sec = lambda anchor, kids, **kw: C('cdp-sec', kids, anchor=anchor, **kw)
product = [C('cdp-body-inner', [
    sec('app', [
        heading('روی گوشی‌ات <span>چی می‌بینی؟</span>'),
        C('cdp-show', [
            W('image', '', image={"url": "https://www.cardiag.ir/wp-content/uploads/2026/10/cardiag-app-ecu-errors.webp", "id": 3104,
                                   "alt": "نمایش کد خطای P0420 با علل احتمالی در اپلیکیشن کاردیاگ", "source": "library"},
              image_size='medium_large', _flex_size='none'),
            C('cdp-feat', [
                ibox('fas fa-exclamation-triangle', 'خطایابی ایسیو', 'کدهای خطا به فارسی، علت احتمالی و پاک کردن خطا و چراغ چک'),
                ibox('fas fa-robot', 'تعمیرکار هوش مصنوعی', 'عیب‌یابی به زبان ساده و جواب هر سؤالی درباره ماشینت'),
                ibox('fas fa-route', 'گزارش سفر', 'ثبت داده‌ها حین رانندگی و گزارش کامل در پایان مسیر'),
                ibox('fas fa-heartbeat', 'مانیتورینگ زنده', 'دمای موتور، دور موتور، ولتاژ باتری و دینام، بار موتور'),
            ], g=12, _flex_size='grow'),
        ], direction='row', g=16, flex_direction_mobile='row', flex_wrap='nowrap'),
        W('html', 'cdp-video', html=aparat),
    ]),
    sec('why', [
        heading('چرا <span>کاردیاگ؟</span>'),
        C('cdp-tiles', [
            ibox('fas fa-car-side', 'بیش از ۵۰ مدل خودرو', 'پژو، سمند، تیبا، دنا، تارا، شاهین و همه‌ی چینی و خارجی‌ها'),
            ibox('fab fa-bluetooth-b', 'اتصال بلوتوثی سریع', 'بدون کابل، اتصال خودکار در چند ثانیه'),
            ibox('fas fa-shield-alt', 'کاملاً ایمن', 'فقط اطلاعات را می‌خواند و تنظیمات خودرو را تغییر نمی‌دهد'),
            ibox('fas fa-language', 'بدون دانش فنی', 'رابط ساده و فارسی برای همه‌ی رانندگان'),
        ], g=10),
    ]),
    sec('about', [heading('کاردیاگ <span>چه می‌کند؟</span>'), text(''.join(f'<p>{p}</p>' for p in paras) + gift_p)]),
    sec('setup', [heading('راه‌اندازی در <span>۳ قدم</span>'), text(
        '<ol class="cdp-steps">'
        '<li><b>دستگاه را وصل کنید</b>کاردیاگ را به سوکت OBD2 زیر داشبورد، کنار فرمان بزنید. ابزار یا تخصصی لازم نیست.</li>'
        '<li><b>اپلیکیشن را نصب کنید</b>اپ را رایگان از سایت دانلود کنید؛ اشتراک طلایی خودکار فعال می‌شود.</li>'
        '<li><b>بلوتوث را روشن کنید</b>اپ را باز کنید؛ اتصال در کمتر از ۳۰ ثانیه برقرار می‌شود.</li></ol>')]),
    sec('vs', [heading('کاردیاگ یا <span>تعمیرگاه؟</span>'), text(
        '<table class="cdp-vs"><thead><tr><th></th><th>تعمیرگاه</th><th>کاردیاگ</th></tr></thead><tbody>'
        '<tr><td>هزینه‌ی هر بار دیاگ</td><td>۲۰۰ تا ۴۰۰ هزار تومان</td><td><span>رایگان</span></td></tr>'
        '<tr><td>زمان</td><td>نوبت، رفت‌وآمد و انتظار</td><td><span>کمتر از ۱ دقیقه</span></td></tr>'
        '<tr><td>دسترسی</td><td>فقط در تعمیرگاه</td><td><span>هر جا، هر وقت</span></td></tr>'
        '<tr><td>شفافیت</td><td>وابسته به تعمیرکار</td><td><span>روی گوشی خودت</span></td></tr>'
        '<tr><td>هزینه‌ی سالانه</td><td>۶۰۰ هزار تا ۲٫۴ میلیون تومان</td><td><span>یک بار خرید</span></td></tr></tbody></table>')]),
    sec('spec', [heading('مشخصات فنی'), text(
        '<table class="cdp-spec"><tbody>'
        '<tr><td>پروتکل‌ها</td><td dir="ltr">CAN · KWP2000 · ISO 9141 · J1850 PWM/VPW</td></tr>'
        '<tr><td>نوع اتصال</td><td>بلوتوث ۴٫۰</td></tr><tr><td>سیستم‌عامل</td><td>اندروید ۵ به بالا</td></tr>'
        '<tr><td>خودروها</td><td>بیش از ۵۰ مدل ایرانی، مونتاژی و وارداتی</td></tr><tr><td>زبان اپ</td><td>فارسی</td></tr>'
        '<tr><td>جنس</td><td>پلاستیک باکیفیت</td></tr><tr><td>هدیه</td><td>اشتراک طلایی مادام‌العمر + ۷۲ اعتبار هوش مصنوعی و سفر</td></tr>'
        '<tr><td>گارانتی</td><td>۶ ماه تعویض + پشتیبانی فارسی</td></tr></tbody></table>')]),
    sec('who', [heading('مناسب چه کسانی است؟'), ilist([
        ('می‌خواهید قبل از تعمیرگاه، دلیل روشن شدن چراغ چک را بدانید', 'fas fa-check'),
        ('قصد خرید خودروی کارکرده دارید و وضعیت فنی‌اش برایتان مهم است', 'fas fa-check'),
        ('نمی‌خواهید هزینه‌ی تعمیرات غیرضروری بدهید', 'fas fa-check'),
        ('می‌خواهید همیشه از سلامت ماشین‌تان باخبر باشید', 'fas fa-check')], 'cdp-who')]),
    sec('cars', [heading('خودروهای <span>تست‌شده</span>'),
                 text('<p>همه‌ی خودروهای چینی و خارجی بدون محدودیت وصل می‌شوند. از خودروهای داخلی حدود ۹۰٪ پشتیبانی می‌شوند؛ '
                      'اگر خودروی شما وصل نشد، تا ۵ روز می‌توانید مرجوع کنید. فهرست زیر بخشی از خودروهای تست‌شده است.</p>', 'cdp-note'),
                 accordion(cars)]),
    sec('faq', [heading('سوالات متداول'), accordion(faq, faq=True)]),
    C('cdp-final', [heading('مکانیکِ تو جیبت', '', 'h2'), text('<p>با خرید دیاگ، اشتراک طلایی اپ را هدیه بگیر</p>'),
                    W('button', '', text='خرید با تخفیف', link={"url": "#cdp-buy", "is_external": "", "nofollow": ""}, align='justify')],
      g=12, flex_align_items='stretch'),
], g=0)]

# ---------------------------------------------------------------- app guide page (free / paid / credits / cars)
_css = re.search(r'<style>(.*?)</style>', assets, re.S).group(1).splitlines()
_keep = ('.cdp,', '.cdp *', '.cdp-sec', '.cdp-feat', '.cdp-tiles', 'ol.cdp-steps', 'table.cdp', '.cdp-who', '.cdp-note', '.cdp-acc', '.cdp-final')
guide_css = '\n'.join(l for l in _css if l.startswith(_keep) and 'elementor-3124' not in l)
guide_css += """
.cdp-guide{max-width:100%;overflow-x:clip;font-family:Vazirmatn,inherit}
.cdp-guide.e-con,.cdp-guide .cdp-sec.e-con,.cdp-guide .cdp-final.e-con{--padding-left:0px;--padding-right:0px}
.cdp-guide .e-con,.cdp-guide .elementor-widget,.cdp-guide .elementor-widget-container{min-width:0!important;max-width:100%}
.cdp-guide table{width:100%!important;table-layout:fixed!important}
.cdp-guide .cdp-sec{padding:28px 0 4px!important}
.cdp-lead-g p{font-size:14.5px;line-height:2;color:#33415C;margin:0}
.cdp-free .elementor-icon{background:var(--gt)!important;color:var(--g)!important}
.cdp-plans{display:grid!important;grid-template-columns:1fr;gap:10px}
.cdp-plans>.elementor-widget{background:#fff;border:1px solid var(--l);border-radius:18px;padding:14px;margin:0!important;width:auto!important}
.cdp-plans .elementor-icon-box-wrapper{display:flex!important;gap:10px;text-align:right!important;align-items:flex-start}
.cdp-plans .elementor-icon-box-icon{margin:0!important}
.cdp-plans .elementor-icon{width:40px;height:40px;border-radius:12px;background:var(--s);color:var(--b)!important;font-size:18px!important;display:flex!important;align-items:center;justify-content:center;padding:0!important}
.cdp-plans .cdp-gold .elementor-icon{background:linear-gradient(90deg,#F6CD5C,#FFEA9C,#E0A82C);color:var(--ink)!important}
.cdp-plans .elementor-icon-box-title{margin:0!important;font-size:14.5px!important;font-weight:800!important;color:var(--n)!important}
.cdp-plans .elementor-icon-box-description{margin:0!important;font-size:13px!important;color:var(--sl)!important;line-height:1.7}
.cdp-guide .cdp-sec h1.elementor-heading-title{font-size:24px!important;font-weight:900!important;line-height:1.5!important;color:var(--n)!important;margin:0 0 6px}
.cdp-guide .cdp-sec h1 span{color:var(--b)}
@media (min-width:768px){.cdp-plans{grid-template-columns:repeat(3,1fr)}.cdp-tiles{grid-template-columns:repeat(3,1fr)}.cdp-guide .cdp-sec h1.elementor-heading-title{font-size:30px!important}.cdp-guide .cdp-sec h2.elementor-heading-title{font-size:24px!important}}
"""
BUY = {"url": "/product/cardiag/", "is_external": "", "nofollow": ""}
guide = [C('cdp-guide', [
    W('html', 'cdp-assets', html='<style>' + guide_css + '</style>'),
    sec('guide-top', [
        heading('اپ کاردیاگ؛ <span>چی رایگانه، چی پولیه؟</span>', size='h1'),
        text('<p>اپ کاردیاگ را رایگان از سایت دانلود می‌کنی. بعضی بخش‌هایش همیشه رایگانه و بعضی‌ها با اعتبار یا اشتراک کار می‌کنند. اینجا ساده توضیح دادیم کدوم کدومه، ۷۲ اعتبار یعنی چی، و با خرید دیاگ چی می‌گیری.</p>', 'cdp-lead-g'),
    ]),
    sec('free', [
        heading('بخش‌های <span>رایگان</span>'),
        text('<p>این بخش‌ها اعتبار مصرف نمی‌کنند و هر چند بار خواستی می‌تونی ازشون استفاده کنی:</p>'),
        C('cdp-feat cdp-free', [
            ibox('fas fa-exclamation-triangle', 'خطایابی ایسیو', 'کدهای خطا به فارسی، علت احتمالی و پاک کردن خطا و چراغ چک'),
            ibox('fas fa-heartbeat', 'مانیتورینگ زنده', 'دمای موتور، دور موتور، ولتاژ باتری و دینام، بار موتور'),
            ibox('fas fa-car-battery', 'تست باتری و دینام', 'سالم بودن باتری و شارژ دینام را بسنج'),
            ibox('fas fa-chart-line', 'روند سلامت خودرو', 'سلامت ماشین را در گذر زمان ببین'),
        ], g=12),
    ]),
    sec('paid', [
        heading('بخش‌های <span>پولی</span>'),
        text('<p>این دو بخش با اعتبار کار می‌کنند. <b>هر بار استفاده، یک اعتبار</b> کم می‌کند:</p>'),
        C('cdp-feat', [
            ibox('fas fa-robot', 'تعمیرکار هوش مصنوعی', 'عیب‌یابی به زبان ساده، جواب هر سؤالی درباره ماشینت و بررسی خودرو قبل از خرید'),
            ibox('fas fa-route', 'گزارش سفر', 'ثبت داده‌ها حین رانندگی و گزارش کامل در پایان مسیر'),
        ], g=12),
    ]),
    sec('credits', [
        heading('۷۲ اعتبار <span>یعنی چی؟</span>'),
        text('<p>اعتبار، شارژ مصرفیِ بخش‌های پولی اپه. هر بار که از تعمیرکار هوش مصنوعی یا گزارش سفر استفاده کنی، یک اعتبار از حسابت کم می‌شه. با خرید دیاگ، ۷۲ اعتبار هدیه می‌گیری؛ یعنی ۷۲ بار استفاده، در هر ترکیبی که دوست داری.</p>'),
        text('<table class="cdp-spec"><tbody>'
             '<tr><td>یک پرسش از هوش مصنوعی</td><td>۱ اعتبار</td></tr>'
             '<tr><td>یک سفر</td><td>۱ اعتبار</td></tr>'
             '<tr><td>خطایابی، مانیتورینگ، تست باتری، روند سلامت</td><td>رایگان</td></tr>'
             '<tr><td>هدیه‌ی خرید دیاگ</td><td>۷۲ اعتبار</td></tr></tbody></table>'),
        text('<p>مثلاً ۴۰ بار از هوش مصنوعی بپرسی و ۳۲ سفر ثبت کنی. اعتبارت که تموم شد، می‌تونی اشتراک بگیری.</p>', 'cdp-note'),
    ]),
    sec('plans', [
        heading('اشتراک <span>برنزی، نقره‌ای، طلایی</span>'),
        text('<p>از داخل اپ، بخش «اشتراک»، یکی از سه اشتراک را بخر. با خرید دیاگ هم اشتراک طلایی رایگان و همیشگی هدیه می‌گیری.</p>'),
        C('cdp-plans', [
            ibox('fas fa-medal', 'اشتراک برنزی', 'از بخش اشتراک اپ'),
            ibox('fas fa-medal', 'اشتراک نقره‌ای', 'از بخش اشتراک اپ'),
            ibox('fas fa-medal', 'اشتراک طلایی', 'هدیه‌ی خرید دیاگ، رایگان و همیشگی', 'cdp-gold'),
        ], g=10),
    ]),
    sec('gets', [
        heading('با خرید کاردیاگ <span>چی می‌گیری؟</span>'),
        ilist([('دیاگ بلوتوثی کاردیاگ (مدل شخصی، بلوتوث ۴٫۰)', 'fas fa-check'),
               ('اشتراک طلایی اپ، رایگان و همیشگی', 'fas fa-check'),
               ('۷۲ اعتبار هوش مصنوعی و سفر', 'fas fa-check'),
               ('۶ ماه گارانتی تعویض و پشتیبانی فارسی', 'fas fa-check'),
               ('۵ روز مرجوعی اگر به ماشینت وصل نشد', 'fas fa-check')], 'cdp-who'),
    ]),
    sec('gear', [
        heading('به <span>تجهیزات دیگه</span> هم نیاز دارم؟'),
        text('<p><b>نه.</b> فقط این سه تا لازمه:</p>'
             '<ol class="cdp-steps">'
             '<li><b>دیاگ کاردیاگ</b>به سوکت OBD2 زیر داشبورد، کنار فرمان وصل می‌شه. ابزار یا تخصص لازم نیست.</li>'
             '<li><b>گوشی اندروید ۵ به بالا</b>فعلاً اپ فقط برای اندرویده.</li>'
             '<li><b>اپ کاردیاگ و بلوتوث روشن</b>اپ رایگانه و اتصال در کمتر از ۳۰ ثانیه برقرار می‌شه.</li></ol>'
             '<p>کابل و لپ‌تاپ نمی‌خوای. کاردیاگ فقط اطلاعات را می‌خونه و تنظیمات خودرو را تغییر نمی‌ده.</p>'),
    ]),
    sec('cars', [
        heading('چه <span>خودروهایی</span> می‌تونن استفاده کنن؟'),
        text('<p>همه‌ی خودروهای چینی و خارجی بدون محدودیت وصل می‌شوند. از خودروهای داخلی حدود ۹۰٪ پشتیبانی می‌شوند؛ '
             'اگر خودروی شما وصل نشد، تا ۵ روز می‌توانید مرجوع کنید و مبلغ دستگاه برمی‌گردد. فهرست زیر بخشی از خودروهای تست‌شده است.</p>', 'cdp-note'),
        accordion(cars),
    ]),
    C('cdp-final', [heading('مکانیکِ تو جیبت', '', 'h2'), text('<p>دیاگ رو بخر، اشتراک طلایی هدیه بگیر</p>'),
                    W('button', '', text='مشاهده و خرید دیاگ', link=BUY, align='justify')],
      g=12, flex_align_items='stretch'),
], g=0)]

for name, data in (('template_3124', template), ('product_2560', product), ('app_guide', guide)):
    out = HERE / f'{name}.json'
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    print(name, len(out.read_text()), 'chars')
print('cars', len(cars), 'faq', len(faq), 'paras', len(paras))
