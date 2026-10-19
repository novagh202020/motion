# A1 poster render: python3 poster.py [out_dir] [dpi]   (QR target: QR_URL env, default https://cardiag.ir)
# -> poster_a1.pdf (print), poster_a1_<dpi>dpi.jpg, poster_a1_guide.jpg (box zone outlined),
#    poster_a1_mock.jpg (box + card preview), box_front_14x7.pdf / _<dpi>dpi.jpg (box face print)
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
segno.make(os.environ.get("QR_URL", "https://cardiag.ir"), error="h").save("assets/qr_cardiag.svg", scale=10, border=0, dark="#10203C")
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
    shot(pg, "?guide=1", out / "poster_a1_guide.jpg", 0.5)
    shot(pg, "?mock=1", out / "poster_a1_mock.jpg", 0.5)
    # business-card box face, 14 x 7 cm
    pg = b.new_page(viewport={"width": 529, "height": 265}, device_scale_factor=dpi / 96)
    shot(pg, "?box=1", out / f"box_front_14x7_{dpi}dpi.jpg", dpi / 96)
    pg.pdf(path=str(out / "box_front_14x7.pdf"), width="140mm", height="70mm", print_background=True, prefer_css_page_size=False)
    b.close()
