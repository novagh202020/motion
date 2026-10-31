"""UI layer + music mix for maint_motion.html (service reminder on the car's Android monitor, 44 s).
Writes mix_maint.wav (song/song_travel.wav + UI layer). The song stays silent through the hook (belt snaps,
blackout) and swells in as the light comes back."""
import numpy as np, soundfile as sf
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast
F = lambda f: f / 30
MB = lambda m: 7.5 + 67.5 * m
T_SNAP, T_DARK, T_LIGHT = 40, 50, MB(2)
T_S1, T_S2, T_S3, T_S4, T_S5, T_CTA, T_END = MB(3), MB(5), MB(9), MB(12), MB(15), MB(16), MB(18)
T_NAME, T_KM, T_SAVE1 = (T_S1 + 18, T_S1 + 46), (T_S1 + 76, T_S1 + 100), T_S1 + 112
T_ADD, T_DLG, T_DROP, T_PICK, T_INT, T_SAVE2, T_CARD1, T_CARD2 = T_S2 + 14, T_S2 + 18, T_S2 + 44, T_S2 + 76, (T_S2 + 96, T_S2 + 124), T_S2 + 146, T_S2 + 154, T_S2 + 206
T_GPS, T_DRIVE, T_NOTI = T_S3 + 22, (T_S3 + 64, T_S3 + 182), T_S4 + 4


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


def typing(b, a, z, g=0.12):
    t = a
    while t < z: add(b, tick(4200, 0.02), F(t), g); t += 2.6


rng = np.random.default_rng(3)
b = np.zeros((N, 2))
# engine hum under the spinning belt, cut dead at the snap
n = int(F(T_SNAP + 2) * SR); t = np.arange(n) / SR
hum = 0.5 * np.sin(2 * np.pi * 48 * t) + 0.3 * np.sin(2 * np.pi * 96 * t + 0.4) + 0.15 * lp_fast(rng.standard_normal(n), 900)
hum *= (0.6 + 0.4 * np.sin(2 * np.pi * 12 * t)) * np.minimum(1, t / 0.3)
hum[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
add(b, hum, 0, 0.35)
whip = rng.standard_normal(int(0.25 * SR)) * np.exp(-np.arange(int(0.25 * SR)) / (0.04 * SR))       # the snap
add(b, whip, F(T_SNAP), 0.9); add(b, thump(0.6), F(T_SNAP), 0.9); add(b, zap(0.3, 2600, 200), F(T_SNAP), 0.4)
add(b, thump(0.5), F(T_DARK + 2), 0.35); add(b, beep(392, 0.3), F(T_DARK + 40), 0.12)         # dark title + «late»
add(b, whoosh(0.8, 200, 4000), F(T_LIGHT - 6), 0.35); add(b, shimmer(1.0), F(T_LIGHT + 6), 0.3)
for i in range(2): add(b, pop(820 + 120 * i, 0.12), F(T_LIGHT + 24 + i * 16), 0.24)
typing(b, *T_NAME); typing(b, *T_KM); tap(b, T_SAVE1); add(b, whoosh(0.3, 600, 5000), F(T_SAVE1 + 4), 0.12)
tap(b, T_ADD); add(b, pop(640, 0.12), F(T_DLG), 0.22); tap(b, T_DROP); tap(b, T_PICK); typing(b, *T_INT)
tap(b, T_SAVE2); add(b, pop(900, 0.12), F(T_CARD1), 0.26); add(b, pop(980, 0.12), F(T_CARD2), 0.26)
tap(b, T_GPS); add(b, chime((1568, 2093), 0.05, 0.5), F(T_GPS + 4), 0.2)
t = T_DRIVE[0]
while t < T_DRIVE[1]: add(b, tick(3000, 0.02), F(t), 0.04); t += 4
add(b, beep(659.3, 0.18), F(T_DRIVE[1] - 20), 0.14)
add(b, chime((1046.5, 1318.5, 1568), 0.09, 1.0), F(T_NOTI), 0.38); add(b, chime((1046.5, 1318.5, 1568), 0.09, 1.0), F(T_NOTI + 60), 0.2)
add(b, whoosh(0.5, 300, 5000), F(T_S5 - 4), 0.26)
for i in range(2): add(b, pop(820 + 120 * i, 0.12), F(T_S5 + 12 + i * 16), 0.24)
add(b, whoosh(0.5, 3000, 300, False), F(T_CTA - 4), 0.22); typing(b, T_CTA + 16, T_CTA + 44, 0.14)
tap(b, T_CTA + 54, 0.4); add(b, pop(900, 0.12), F(T_CTA + 56), 0.24); add(b, chime((1568, 2093), 0.05, 0.5), F(T_CTA + 70), 0.26)
add(b, shimmer(0.9), F(T_END + 6), 0.36)
light = norm(b, -1)
song, sr = sf.read('song/song_travel.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
g = np.ones(N); i0, i1 = int(F(T_SNAP) * SR), int(F(T_LIGHT - 6) * SR); g[:i1] = 0; g[i1:int(F(T_LIGHT + 6) * SR)] = np.linspace(0, 1, int(F(T_LIGHT + 6) * SR) - i1)
g[:i0] = 0.35                                                                          # music low under the engine, gone at the snap
song = song * g[:, None]
write('mix_maint.wav', norm(softclip(norm(song, -1) + light * 0.55), -1)); print('ok')
