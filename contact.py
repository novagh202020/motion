"""Contact sheet of key frames for cheap QA (one image instead of many).
usage: PAGE=km_motion.html python3 contact.py 0,150,300,450,600,750,870 out.png [cols=4] [thumb_w=360]
Renders the frames via render.py, tiles them with a frame-number label.
"""
import os, sys, subprocess, tempfile, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).resolve().parent
frames, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
tw = int(sys.argv[4]) if len(sys.argv) > 4 else 360
tmp = tempfile.mkdtemp()
subprocess.run([sys.executable, str(HERE / "render.py"), "frames", frames, tmp], check=True)
files = sorted(pathlib.Path(tmp).glob("f*.png"))
ims = [Image.open(f).convert("RGB") for f in files]
th = int(tw * ims[0].height / ims[0].width)
rows = -(-len(ims) // cols)
sheet = Image.new("RGB", (cols * tw, rows * th), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for i, (f, im) in enumerate(zip(files, ims)):
    x, y = (i % cols) * tw, (i // cols) * th
    sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
    d.rectangle([x, y, x + 70, y + 22], fill=(0, 0, 0))
    d.text((x + 4, y + 4), f.stem, fill=(255, 255, 255))
sheet.save(out)
print(out, sheet.size)
