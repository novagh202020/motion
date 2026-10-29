"""Song for travel_motion.html: the whole track (song_full.wav) with two groove-B phrases (motion bars 15-22) taken out
at phrase boundaries, nothing repeated: intro 0-2, groove A 3-9, break 10, groove B 11-15, break 16, outro 17-18,
final hit bar 19 (frame 1290). 44.2 s."""
import numpy as np, soundfile as sf
x, sr = sf.read('song_full.wav')
mb = lambda n: 0.25 + 2.25 * n
cut0, cut1 = mb(15), mb(23)
PRE, XF = 0.012, 0.030
a = x[:int((cut0 - PRE + XF) * sr)].copy(); b = x[int((cut1 - PRE) * sr):].copy()
n = int(XF * sr); w = np.linspace(0, np.pi / 2, n)[:, None]
y = np.vstack([a[:-n], a[-n:] * np.cos(w) + b[:n] * np.sin(w), b[n:]])
sf.write('song_travel.wav', y, sr); print('song_travel.wav', round(len(y) / sr, 3), 's')
