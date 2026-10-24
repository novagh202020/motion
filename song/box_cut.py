"""Song for box_motion.html: the whole track (song_full.wav), no repeated bars. One 4-bar phrase of groove B
(motion bars 15-18) is taken out at a phrase boundary, so every part keeps its natural order:
intro 0-2, groove A 3-9, break 10, groove B 11-19, break 20, outro 21-22, final hit bar 23 (frame 1560). 53.2 s."""
import numpy as np, soundfile as sf
x, sr = sf.read('song_full.wav')
mb = lambda n: 0.25 + 2.25 * n
cut0, cut1 = mb(15), mb(19)              # remove [34.0, 43.0)
PRE, XF = 0.012, 0.030
a = x[:int((cut0 - PRE + XF) * sr)].copy(); b = x[int((cut1 - PRE) * sr):].copy()
n = int(XF * sr); w = np.linspace(0, np.pi / 2, n)[:, None]
mix = a[-n:] * np.cos(w) + b[:n] * np.sin(w)
y = np.vstack([a[:-n], mix, b[n:]])
sf.write('song_box.wav', y, sr); print('song_box.wav', round(len(y) / sr, 3), 's')
