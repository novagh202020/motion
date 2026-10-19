"""Full-length song for the 1-minute launch motion (motion60.html): the stretched track from motion 0 to its end.
Same alignment as song_cut.wav (motion bar m downbeat 0.25+2.25m = song bar m+1), no edits, so every section
change, both breaks (motion bars 10, 24) and the final hit (motion 61.0 s) come straight from the song."""
import numpy as np, soundfile as sf
P, B0 = np.load('grid.npy'); k = 4 * P / 2.25
x, sr = sf.read('suno_st.wav')
bar_s = lambda n: (B0 + n * 4 * P) / k
off = bar_s(4) - 7.0
DUR = 62.2; N = int(DUR * sr)
y = x[int(off * sr): int(off * sr) + N].copy()
if len(y) < N: y = np.vstack([y, np.zeros((N - len(y), 2))])
n = int(0.12 * sr); y[-n:] *= np.linspace(1, 0, n)[:, None] ** 2
sf.write('song_full.wav', y, sr)
print('off', round(off, 3), 'final hit motion', round(bar_s(28) - off, 3), 'end', round(len(x) / sr - off, 3))
