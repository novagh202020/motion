"""UI layer + music mix for travel_motion.html (pre-trip check, 44 s). Writes mix_travel.wav (song/song_travel.wav + UI layer).
Music version only."""
import numpy as np, soundfile as sf
from audio import N, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write
F = lambda f: f / 30
MB = lambda m: 7.5 + 67.5 * m
BT = lambda n: 210 + 16.875 * n
BEAT = 16.875
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV0 = BT(4); T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_BAT, T_BGO, T_BROW, T_BB = BT(7.5), BT(8.25), [BT(8.75), BT(9.25), BT(9.75), BT(10.25)], BT(12)
T_ECU, T_EB = BT(12.75), BT(15.5); T_ESCAN = T_ECU + 12
T_TRIP, T_TB = BT(16.25), BT(23.5); T_HOT = T_TRIP + 82
T_AI, T_OPT, T_TYPE1, T_INSP, T_REP = BT(24.25), BT(25.5), BT(27.5), BT(28), BT(30)
T_TYPE0 = T_OPT + 8
T_ROW, T_TIP, T_STAMP, T_FLIP = [BT(31.5), BT(32.5), BT(33.5), BT(34.5)], BT(35.5), BT(37), BT(38.5)
T_CK, T_BULB = [BT(40.5), BT(41.5), BT(42.5), BT(43.5)], BT(45)
T_SCN, T_RECAP, T_END = MB(15), MB(16), MB(17)


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


def warn2():
    out = np.zeros(int(0.42 * 48000))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * 48000); out[j:j + len(s)] += s
    return out


OK3 = lambda: chime((1318.5, 1661.2, 1975.5), 0.06, 0.8)
b = np.zeros((N, 2))
add(b, pop(600, 0.1), F(52), 0.2)                                   # doubt bubble
for i, t in enumerate((58, 75, 92)): add(b, pop(820 + 120 * i, 0.12), F(t), 0.28, 0.3 * (i - 1))
add(b, whoosh(0.5, 300, 4000), F(136), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)   # iris
add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.28); add(b, shimmer(0.8), F(T_PH + 8), 0.30)
tap(b, T_CONN); add(b, whoosh(0.3, 600, 5000), F(T_CONN + 3), 0.12); tap(b, T_SEARCH)
add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV0), 0.22)
tap(b, T_PICK); add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
add(b, OK3(), F(T_OK), 0.32)
for t in (T_BAT, T_ECU, T_TRIP, T_AI):                              # tile taps + zoom + card flip + route car
    tap(b, t, 0.4); add(b, whoosh(0.3, 600, 5000), F(t + 3), 0.14); add(b, whoosh(0.35, 400, 3500), F(t + 8), 0.14)
for t in (T_BB, T_EB, T_TB): add(b, whoosh(0.3, 5000, 600, False), F(t), 0.1)
tap(b, T_BGO)
for i, t in enumerate(T_BROW): add(b, pop(760 + 90 * i, 0.1), F(t), 0.2)
add(b, OK3(), F(T_BROW[3] + 8), 0.28)
tap(b, T_ESCAN); t = T_ESCAN + 4
while t < T_ESCAN + 14: add(b, tick(3600, 0.03), F(t), 0.07); t += 3.0
add(b, OK3(), F(T_ESCAN + 14), 0.3)
add(b, warn2(), F(T_HOT), 0.2)
tap(b, T_OPT); t = T_TYPE0
while t < T_TYPE1: add(b, tick(4200, 0.02), F(t), 0.06); t += 2.2
tap(b, T_INSP); add(b, pop(760, 0.1), F(T_INSP + 12), 0.2)
add(b, whoosh(0.6, 300, 4500), F(T_REP), 0.3); add(b, pop(900, 0.12), F(T_REP + 16), 0.25)
for i, t in enumerate(T_ROW): add(b, pop(820 + 80 * i, 0.1), F(t + 4), 0.22, 0.2 * (i - 1.5))
add(b, warn2(), F(T_TIP), 0.18)
add(b, thump(0.35), F(T_STAMP), 0.45); add(b, tick(1200, 0.06), F(T_STAMP), 0.4)
add(b, whoosh(0.6, 300, 4000), F(T_FLIP), 0.3)
for i, t in enumerate(T_CK): add(b, tick(2400, 0.05), F(t + 2), 0.3); add(b, pop(900 + 70 * i, 0.08), F(t + 2), 0.15)
add(b, chime((1568, 2093), 0.05, 0.5), F(T_BULB), 0.2)
add(b, whoosh(0.7, 200, 3500), F(T_SCN - 16), 0.32)
add(b, whoosh(0.4, 400, 4500), F(T_RECAP - 8), 0.18)
for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_RECAP + i * BEAT), 0.26, 0.25 * (i - 1))
add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
light = norm(b, -1)
song, sr = sf.read('song/song_travel.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_travel.wav', norm(softclip(norm(song, -1) + light * 0.55), -1)); print('ok')
