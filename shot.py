import os, sys, pathlib
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]; q = sys.argv[3] if len(sys.argv) > 3 else ""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto(pathlib.Path(src).resolve().as_uri() + q); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    pg.screenshot(path=out); b.close()
