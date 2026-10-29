"""UI layer + music mix for km_motion.html (mileage check, 30 s). Writes mix_km.wav (song/song_cut.wav + UI layer).
Music version only."""
import numpy as np, soundfile as sf
from audio import N, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
BEAT = 16.875
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV0 = BT(4); T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_KM, T_KS, T_CHK, T_CMP, T_C1R = BT(7.25), BT(9), BT(10), BT(11), BT(14)
T_C2, T_CHK2, T_C2R = BT(20), BT(20.5), BT(24)
T_RECAP, T_END = B(8), 817.5


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


def warn2():
    out = np.zeros(int(0.42 * 48000))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * 48000); out[j:j + len(s)] += s
    return out


b = np.zeros((N, 2))
add(b, pop(600, 0.1), F(12), 0.18)
for i in range(3): add(b, pop(820 + 120 * i, 0.12), F(22 + i * 22), 0.28, 0.3 * (-1) ** i)
add(b, zap(0.3, 1400, 500), F(92), 0.18); add(b, thump(0.35), F(94), 0.35)
add(b, whoosh(0.5, 300, 4000), F(132), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25); add(b, shimmer(0.8), F(T_PH + 8), 0.30)
tap(b, T_CONN); tap(b, T_SEARCH); add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV0), 0.22)
tap(b, T_PICK); add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
tap(b, T_KM, 0.4); add(b, pop(760, 0.1), F(T_KS - 4), 0.22); add(b, whoosh(0.35, 500, 5000), F(T_KS), 0.18)
for a, z in ((T_CHK, T_C1R), (T_CHK2, T_C2R)):
    tap(b, a); t = a + 6
    while t < z - 4: add(b, tick(3600, 0.03), F(t), 0.07); t += 3.0
add(b, whoosh(0.4, 400, 4500), F(T_CMP - 4), 0.18)
add(b, warn2(), F(T_C1R), 0.24); add(b, thump(0.3), F(T_C1R), 0.3)
add(b, whoosh(0.4, 600, 5000), F(T_C2 - 6), 0.16); add(b, pop(820, 0.1), F(T_C2 + 4), 0.2)
add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_C2R), 0.3)
add(b, whoosh(0.4, 400, 4500), F(T_RECAP - 8), 0.18)
for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_RECAP + i * BEAT), 0.26, 0.25 * (i - 1))
add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
light = norm(b, -1)
song, sr = sf.read('song/song_cut.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_km.wav', norm(softclip(norm(song, -1) + light * 0.55), -1)); print('ok')
