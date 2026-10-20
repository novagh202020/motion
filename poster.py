# A1 poster render: python3 poster.py [out_dir] [dpi]   (coupon QR target: QR_URL env, default https://www.cardiag.ir/?coupon=IRAN)
# -> poster_a1.pdf (print), poster_a1_<dpi>dpi.jpg, poster_a1_preview.jpg
import os, sys, pathlib
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
import segno
from PIL import Image
from playwright.sync_api import sync_playwright

Image.MAX_IMAGE_PIXELS = None
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 300
out.mkdir(parents=True, exist_ok=True)
W, H = 2245, 3179                      # 594 x 841 mm at 96 px/in
segno.make(os.environ.get("QR_URL", "https://www.cardiag.ir/?coupon=IRAN"), error="q").save("assets/qr_coupon.svg", scale=10, border=0, dark="#10203C")
page = pathlib.Path("poster_a1.html").resolve().as_uri()

def shot(pg, q, path, scale):
    pg.goto(page + q); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    png = str(path.with_suffix(".png")); pg.screenshot(path=png)
    Image.open(png).convert("RGB").save(path, quality=95, dpi=(dpi, dpi)); os.remove(png)

with sync_playwright() as p:
    exe = "/opt/pw-browsers/chromium"
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb"], executable_path=exe if os.path.exists(exe) else None)
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto(page); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    pg.pdf(path=str(out / "poster_a1.pdf"), width="594mm", height="841mm", print_background=True, prefer_css_page_size=True)
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=dpi / 96)
    shot(pg, "", out / f"poster_a1_{dpi}dpi.jpg", dpi / 96)
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=0.5)
    shot(pg, "", out / "poster_a1_preview.jpg", 0.5)
    b.close()
