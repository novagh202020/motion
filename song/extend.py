"""Lengthen song_cut.wav for longer motions by repeating groove bars.
usage: python3 extend.py BARS OUT.wav  -> inserts BARS groove bars (motion bars 4.. copied) at motion bar 9 (= frame 615),
so everything from the recap on moves BARS*2.25 s later (recap frame 750 -> 750 + 67.5*BARS)."""
import numpy as np, soundfile as sf, sys
bars, out = int(sys.argv[1]), sys.argv[2]
x, sr = sf.read('song_cut.wav')
mb = lambda n: 0.25 + 2.25 * n                    # motion bar downbeat (s)
PRE, XF = 0.012, 0.010                            # cut just before the transient, short crossfade
cut, a = mb(9) - PRE, mb(4) - PRE
ins = x[int((a - XF) * sr): int((a + 2.25 * bars) * sr)]   # starts XF early: the crossfade eats it
n = int(XF * sr); w = np.linspace(0, np.pi / 2, n)[:, None]
head, tail = x[:int(cut * sr)].copy(), x[int(cut * sr):].copy()
def join(A, Bv):
    A = A.copy(); Bv = Bv.copy()
    mix = A[-n:] * np.cos(w) + Bv[:n] * np.sin(w)
    return np.vstack([A[:-n], mix, Bv[n:]])
y = join(join(head, np.vstack([ins, x[int((a + 2.25 * bars) * sr): int((a + 2.25 * bars) * sr) + n]])), tail)
sf.write(out, y, sr); print(out, round(len(y) / sr, 3), 's')
