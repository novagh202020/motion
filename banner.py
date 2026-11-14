# Car-wash wall banners: python3 banner.py [out_dir] [dpi]
# banner_shine.html 100 x 200 cm (code shine), banner_azadi.html 120 x 150 cm (code azadi),
# banner_mehdi.html 100 x 150 cm (code mehdi), banner_azaran.html 100 x 200 cm (code azaran); QR -> https://www.cardiag.ir/?coupon=<CODE>
# -> <name>.pdf (print, exact size), <name>_<dpi>dpi.jpg, <name>_preview.jpg
import os, sys, pathlib
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

Image.MAX_IMAGE_PIXELS = None
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 150   # 100-150 dpi is the norm for wall banners
out.mkdir(parents=True, exist_ok=True)
W = 2245                               # design width in px for every banner
BANNERS = [("banner_shine", 1000, 2000, "SHINE"), ("banner_azadi", 1200, 1500, "AZADI"),
           ("banner_mehdi", 1000, 1500, "MEHDI"),
           ("banner_azaran", 1000, 2000, "AZARAN")]

def shot(pg, page, path, dpi_out):
    pg.goto(page); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    png = str(path.with_suffix(".png")); pg.screenshot(path=png)
    Image.open(png).convert("RGB").save(path, quality=93, dpi=(dpi_out, dpi_out)); os.remove(png)

with sync_playwright() as p:
    exe = "/opt/pw-browsers/chromium"
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb"], executable_path=exe if os.path.exists(exe) else None)
    for name, wmm, hmm, code in BANNERS:
        segno.make(f"https://www.cardiag.ir/?coupon={code}", error="q").save(f"assets/qr_{code.lower()}.svg", scale=10, border=0, dark="#10203C")
        page = pathlib.Path(f"{name}.html").resolve().as_uri()
        H = round(W * hmm / wmm)
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(page); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        k = wmm / 25.4 * 96 / W                # PDF scale to the real size; Chromium caps it at 2, CSS zoom covers the rest
        if k > 2: pg.add_style_tag(content=f"html{{zoom:{k / 2}}}")
        pg.pdf(path=str(out / f"{name}.pdf"), width=f"{wmm}mm", height=f"{hmm}mm", scale=min(k, 2), print_background=True)
        s = dpi * wmm / 25.4 / W
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=s)
        shot(pg, page, out / f"{name}_{dpi}dpi.jpg", dpi)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=0.4)
        shot(pg, page, out / f"{name}_preview.jpg", round(dpi * 0.4 / s))
    b.close()
