"""Song for dgpay_motion.html (30 s ad): song_full.wav starting straight on the groove, phrases joined at bar lines,
nothing repeated: groove A bars 3-9, groove B 11-13, break 24, outro 25-26, final hit bar 27 (+0.7 s tail).
In the cut, bar k starts at frame 67.5*k: 0-6 groove A, 7-9 groove B, 10 break, 11-12 outro, final hit bar 13 (877.5)."""
import numpy as np, soundfile as sf
x, sr = sf.read('song_full.wav')
mb = lambda n: 0.25 + 2.25 * n
PRE, XF = 0.012, 0.030
segs = [(mb(3), mb(10)), (mb(11), mb(14)), (mb(24), mb(27) + 0.7)]
n = int(XF * sr); w = np.linspace(0, np.pi / 2, n)[:, None]
y = x[int(segs[0][0] * sr):int((segs[0][1] - PRE + XF) * sr)].copy()
for a, b in segs[1:]:
    s = x[int((a - PRE) * sr):int((b - PRE + XF) * sr)].copy()
    y = np.vstack([y[:-n], y[-n:] * np.cos(w) + s[:n] * np.sin(w), s[n:]])
y = y[:-n]
f = int(0.6 * sr); y[-f:] *= np.linspace(1, 0, f)[:, None] ** 2           # tail fades out under 30 s
fi = int(0.004 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
sf.write('song_ad.wav', y, sr); print('song_ad.wav', round(len(y) / sr, 3), 's')
