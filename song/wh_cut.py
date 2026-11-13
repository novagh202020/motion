"""Song for wholesale_motion.html (21 s wholesale teaser): song_full.wav from the groove, phrases joined at bar lines.
groove A bars 3-6, groove B 11-12, break 24, outro 25-26, final hit bar 27 (+0.7 s tail).
In the cut, bar k starts at frame 67.5*k: 0-3 groove A, 4-5 groove B, 6 break, 7-8 outro, final hit bar 9 (607.5)."""
import numpy as np, soundfile as sf
x, sr = sf.read('song_full.wav')
mb = lambda n: 0.25 + 2.25 * n
PRE, XF = 0.012, 0.030
segs = [(mb(3), mb(7)), (mb(11), mb(13)), (mb(24), mb(27) + 0.7)]
n = int(XF * sr); w = np.linspace(0, np.pi / 2, n)[:, None]
y = x[int(segs[0][0] * sr):int((segs[0][1] - PRE + XF) * sr)].copy()
for a, b in segs[1:]:
    s = x[int((a - PRE) * sr):int((b - PRE + XF) * sr)].copy()
    y = np.vstack([y[:-n], y[-n:] * np.cos(w) + s[:n] * np.sin(w), s[n:]])
y = y[:-n]
N = int(21.0 * sr)
y = y[:N] if len(y) >= N else np.vstack([y, np.zeros((N - len(y), 2))])
f = int(0.5 * sr); y[-f:] *= np.linspace(1, 0, f)[:, None] ** 2
fi = int(0.004 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
sf.write('song_wh.wav', y, sr); print('song_wh.wav', round(len(y) / sr, 3), 's')
