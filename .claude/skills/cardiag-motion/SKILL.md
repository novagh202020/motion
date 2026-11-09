---
name: cardiag-motion
description: Build, render and QA a new CarDiag brand motion (1080x1920, 30fps, HTML frame-by-frame). Use when asked for a new motion/ad/cover in the CarDiag series.
---

# CarDiag motion workflow (token-cheap)

Rules live in `CLAUDE.md` (colors, Vazirmatn FD, RTL, max 5-word titles). Technical commands live in `README.md`. Do not re-read them in full; use this checklist.

1. **Propose first**: idea + timed storyboard (frame/second table) + style; wait for approval.
2. **Start from the closest existing page** (`*_motion.html`, same series) instead of writing from scratch; reuse `endcard.js` and the sfx_* script of the nearest motion.
3. **Check keyframes with a contact sheet, not single full-size frames**:
   `PAGE=x_motion.html python3 contact.py 0,60,150,... /tmp/sheet.png 4 360` then view one image. Zoom into single frames (`render.py frames`) only for problems.
4. **Render only the changed range** while iterating (`render.py video silent.mp4 A Z`); full render only after approval.
5. **Audio**: build sfx with the matching `sfx_*.py`; produce both versions: with music (mix) and SFX-only (no music, for trending audio).
6. **Mux**: `ffmpeg -i silent.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-2 -c:a aac -b:a 192k out.mp4`
7. **QA checklist before delivery**: >=1 brand-blue element in every key frame; orange only for problems, green only for healthy, gold only for subscription; Persian digits, «٫» and «٪»; correct half-spaces; titles fixed, centred, y~185-230, <=5 words; shadows use Shadow Navy not black; ffprobe: 1080x1920, 30fps, h264, aac 192k; page console has no errors.
