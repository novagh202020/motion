"""Render motion.html frames.
usage: python render.py frames 0,30,60 outdir     -> PNG keyframes
       python render.py video out.mp4 [start end]  -> silent H.264 via ffmpeg pipe
       VW=1920 VH=1080 PAGE=... for landscape wrappers
"""
import os, sys, subprocess, pathlib, time
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
URL = (HERE / os.environ.get("PAGE", "motion.html")).as_uri()


def page_ctx(p):
    b = p.chromium.launch(args=["--disable-web-security", "--allow-file-access-from-files", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": int(os.environ.get("VW", 1080)), "height": int(os.environ.get("VH", 1920))}, device_scale_factor=1)
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL)
    pg.evaluate("window.READY")
    pg.wait_for_timeout(300)
    return b, pg, errs


def main():
    mode = sys.argv[1]
    with sync_playwright() as p:
        b, pg, errs = page_ctx(p)
        if mode == "frames":
            frames = [int(x) for x in sys.argv[2].split(",")]
            out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
            for f in frames:
                pg.evaluate(f"render({f})")
                pg.screenshot(path=str(out / f"f{f:04d}.png"))
        else:
            dst = sys.argv[2]
            a, z = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 900)
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", "30",
                                   "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                                   "-pix_fmt", "yuv420p", "-r", "30", dst], stdin=subprocess.PIPE)
            t0 = time.time()
            for f in range(a, z):
                pg.evaluate(f"render({f})")
                ff.stdin.write(pg.screenshot(type="png"))
                if f % 100 == 0:
                    print(f"frame {f}  {time.time()-t0:.0f}s", flush=True)
            ff.stdin.close(); ff.wait()
        if errs:
            print("PAGE ERRORS:", errs[:10])
        b.close()


if __name__ == "__main__":
    main()
