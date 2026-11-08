"""Sound for dgpay_motion.html (30 s Digipay ad). Writes mix_dgpay.wav = song/song_ad.wav + an Apple-clean UI layer.
In the song cut, bar k starts at frame 67.5*k (beat 16.875); the final hit lands on bar 13."""
import numpy as np, soundfile as sf
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, thump, norm, softclip, write, lp_fast
F = lambda f: f / 30
BAR, BEAT = 67.5, 16.875
Bk = lambda k: BAR * k
Bt = lambda k, b: BAR * k + BEAT * b
rng = np.random.default_rng(5)


def tap(b, t, g=0.4): add(b, tick(), F(t), g)


b = np.zeros((N, 2))
H_END = Bt(2, 1); T_SW = Bt(0, 2); T_PAID = [Bt(1, 1), Bt(1, 2), Bt(1, 3), Bk(2)]
add(b, thump(0.4), F(0), 0.8); add(b, pop(520, 0.14), F(4), 0.4)                                # the switch appears
add(b, tick(1500, 0.05), F(T_SW), 0.9); add(b, pop(380, 0.1), F(T_SW + 1), 0.6)                  # click: on
add(b, shimmer(1.0), F(T_SW + 5), 0.45); add(b, chime((1318.5, 1661.2, 1975.5), 0.05, 0.9), F(T_SW + 6), 0.3)
add(b, whoosh(0.4, 300, 5000), F(Bk(1) - 6), 0.25)
for i in range(4): add(b, pop(700 + 120 * i, 0.11), F(Bk(1) - 2 + i * 2), 0.3, 0.4 * (1.5 - i) / 1.5)
for i, t0 in enumerate(T_PAID):                                                              # paid, month by month
    add(b, chime((1046.5 * 2 ** (i * 2 / 12), 1318.5 * 2 ** (i * 2 / 12)), 0.04, 0.5), F(t0), 0.3); add(b, tick(2400, 0.04), F(t0), 0.3)
for t in (H_END, Bt(3, 2), Bk(5), Bk(7), Bk(9), Bk(11)): add(b, whoosh(0.4, 300, 5000), F(t - 6), 0.22)
add(b, shimmer(1.0), F(H_END + 6), 0.32)                                                     # the product's light sweep
add(b, whoosh(0.35, 700, 3000), F(Bt(3, 3)), 0.25)                                           # strike
t = Bk(4)
while t < Bk(4) + 12: add(b, tick(2800 + 300 * np.sin(t), 0.02), F(t), 0.14); t += 1.2
add(b, pop(980, 0.12), F(Bk(4) + 12), 0.34); add(b, thump(0.3), F(Bk(4) + 12), 0.5)
add(b, pop(820, 0.12), F(Bk(5) + 10), 0.3)
for i in range(4): add(b, pop(760 + 90 * i, 0.1), F(Bt(6, i)), 0.3)                           # four installments
tap(b, Bt(7, 2)); add(b, pop(900, 0.1), F(Bt(7, 2) + 2), 0.22)
tap(b, Bt(8, 1)); add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.9), F(Bt(8, 2)), 0.36)
for i in range(4): add(b, thump(0.25), F(Bt(9, i)), 0.5); add(b, tick(2200, 0.04), F(Bt(9, i)), 0.35)   # montage
add(b, pop(600, 0.12), F(Bk(10)), 0.2); add(b, pop(800, 0.12), F(Bt(10, 2)), 0.24)
t = Bt(11, 2) + 4
while t < Bt(11, 4): add(b, tick(4200, 0.02), F(t), 0.16); t += (Bt(11, 4) - Bt(11, 2) - 4) / 10
add(b, pop(1000, 0.12), F(Bk(12)), 0.3)
add(b, shimmer(1.2), F(Bk(13) - 2), 0.4); add(b, thump(0.5), F(Bk(13)), 0.6)
def punch(x, drive=3.5, bass=1.0):
    y = np.tanh(x * drive) / np.tanh(drive); return y + bass * np.stack([lp_fast(y[:, c], 160) for c in range(2)], 1)
ui = norm(punch(norm(b, -1)), -1)
song, sr = sf.read('song/song_ad.wav'); mus = np.zeros((N, 2)); m = min(N, len(song)); mus[:m] = song[:m]
write('mix_dgpay.wav', norm(softclip(norm(mus, -1) * 0.8 + ui * 0.7), -1)); print('ok')
