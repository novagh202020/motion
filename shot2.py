import os, sys, pathlib
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
from playwright.sync_api import sync_playwright
src, out, w, h, dpr = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=dpr)
    pg.goto(pathlib.Path(src).resolve().as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    pg.screenshot(path=out); b.close()
