# Shine car-wash wall banner, 100 x 200 cm: python3 banner.py [out_dir] [dpi]
# (coupon QR target: QR_URL env, default https://www.cardiag.ir/?coupon=SHINE)
# -> banner_shine.pdf (print, 1000 x 2000 mm), banner_shine_<dpi>dpi.jpg, banner_shine_preview.jpg
import os, sys, pathlib
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

Image.MAX_IMAGE_PIXELS = None
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 150   # 100-150 dpi is the norm for a 2 m banner
out.mkdir(parents=True, exist_ok=True)
W, H = 2245, 4490                      # design px; 1000 mm = 3780 px at 96 px/in
segno.make(os.environ.get("QR_URL", "https://www.cardiag.ir/?coupon=SHINE"), error="q").save("assets/qr_shine.svg", scale=10, border=0, dark="#10203C")
page = pathlib.Path("banner_shine.html").resolve().as_uri()

def shot(pg, path, scale):
    pg.goto(page); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    png = str(path.with_suffix(".png")); pg.screenshot(path=png)
    Image.open(png).convert("RGB").save(path, quality=93, dpi=(round(W * scale / (1000 / 25.4)),) * 2); os.remove(png)

with sync_playwright() as p:
    exe = "/opt/pw-browsers/chromium"
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb"], executable_path=exe if os.path.exists(exe) else None)
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto(page); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    pg.pdf(path=str(out / "banner_shine.pdf"), width="1000mm", height="2000mm", scale=3780 / W, print_background=True)
    s = dpi * 1000 / 25.4 / W
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=s)
    shot(pg, out / f"banner_shine_{dpi}dpi.jpg", s)
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=0.4)
    shot(pg, out / "banner_shine_preview.jpg", 0.4)
    b.close()
