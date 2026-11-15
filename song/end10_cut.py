"""10 s end-card song: song_full.wav from the last groove bar (23) through the break (24), the outro (25-26) and the
final hit (27). In the cut, bar k starts at frame 67.5*k; the final hit lands on frame 270 (9.0 s)."""
import numpy as np, soundfile as sf
x, sr = sf.read('song_full.wav')
mb = lambda n: 0.25 + 2.25 * n
y = x[int(mb(23) * sr):int((mb(23) + 10.0) * sr)].copy()
fi = int(0.006 * sr); y[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(0.4 * sr); y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
sf.write('song_end10.wav', y, sr); print('song_end10.wav', round(len(y) / sr, 2), 's')
