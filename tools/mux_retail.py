"""Composite the app clips (out/clip_*.mp4, rendered from the existing motions) into the feature card of
retail_motion.html, one per bar on the song_cut grid. Input: out/rt_base.mp4 (silent render). Output: out/rt_silent.mp4."""
import subprocess
from PIL import Image, ImageDraw
B = lambda m: (7.5 + 67.5 * m) / 30.0
X, Y, W, H, R = 180, 330, 720, 1067, 38
SPEED = 1.6
# (clip, start second inside the clip) in feature order
CLIPS = [('ecu', 1.67), ('ai', 4.8), ('trip', 1.5), ('bat', 1.67), ('km', 3.5), ('mon', 0.3), ('svc', 4.0)]
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), R, fill=255); m.save('out/rt_mask.png')
inp = ['-i', 'out/rt_base.mp4', '-loop', '1', '-i', 'out/rt_mask.png']
fl, last = [], '0:v'
for k, (n, ss) in enumerate(CLIPS):
    a = B(3 + k) + (10 / 30 if k == 0 else 0); b = B(4 + k) - (6 / 30 if k == 6 else 0)
    dur = b - a
    inp += ['-ss', f'{ss:.3f}', '-t', f'{dur * SPEED + 0.2:.3f}', '-i', f'out/clip_{n}.mp4']
    i = k + 2
    fl.append(f'[{i}:v]crop=1080:1600:0:300,scale={W}:{H},setpts=PTS/{SPEED}+{a:.4f}/TB,format=rgba[c{k}]')
    fl.append(f'[1:v]trim=duration={dur + 1:.3f},setpts=PTS+{a:.4f}/TB,format=gray[m{k}]')
    fl.append(f'[c{k}][m{k}]alphamerge,fade=t=in:st={a:.4f}:d=0.12:alpha=1,fade=t=out:st={b - 0.12:.4f}:d=0.12:alpha=1[a{k}]')
    fl.append(f"[{last}][a{k}]overlay={X}:{Y}:eof_action=pass:enable='between(t,{a:.4f},{b:.4f})'[v{k}]")
    last = f'v{k}'
cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fl), '-map', f'[{last}]', '-t', '30',
       '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '30', 'out/rt_silent.mp4']
subprocess.run(cmd, check=True); print('ok')
