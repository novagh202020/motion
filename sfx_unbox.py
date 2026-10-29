"""UI layer + music mix for unbox_motion.html (box to first scan + 3-day offer, 44 s). Writes mix_unbox.wav (song/song_travel.wav + UI layer).
Music version only."""
import numpy as np, soundfile as sf
from audio import N, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write
F = lambda f: f / 30
MB = lambda m: 7.5 + 67.5 * m
BT = lambda n: 210 + 16.875 * n
BEAT = 16.875
T_S1, T_S2, T_S3 = MB(2), BT(4), BT(9)
T_INST, T_DL1, T_RUN, T_ACT, T_CODE0, T_CODE1, T_ACTB, T_GOLD = BT(10), BT(12.25), BT(12.75), BT(13.75), BT(14), BT(15.25), BT(15.5), BT(16)
T_S4, T_CONN, T_SEARCH, T_DEV0, T_PICK = BT(17), BT(17.5), BT(18), BT(18.5), BT(19.5)
T_BACK = T_PICK + 4; T_STEP = [T_BACK + 6, BT(20.25), BT(20.6)]; T_OK = BT(21)
T_S5, T_ECU, T_ESCAN = BT(22), BT(22.25), BT(23)
T_LAP, T_DONE = [BT(3), BT(8), BT(16.5), BT(21.5), BT(26)], BT(26.5)
T_OFF, T_STRIKE, T_ROLL, T_ROLL1, T_SAVE, T_GIFT, T_CAL, T_CTA, T_TAPC = MB(11), BT(34), BT(35), BT(37.5), BT(38), BT(40), BT(42), BT(46), BT(48)
T_RECAP, T_END = MB(16), MB(17)
PLUG = T_S2 + 32                                  # dash(): the diag seats at 168 - 136 after the scene starts


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


OK3 = lambda: chime((1318.5, 1661.2, 1975.5), 0.06, 0.8)
b = np.zeros((N, 2))
add(b, whoosh(0.5, 3000, 300, False), F(8), 0.25); add(b, thump(0.3), F(28), 0.4)          # the case drops in
t = T_S1 + 4                                                                               # zipper
while t < T_S1 + 52: add(b, tick(5200, 0.015), F(t), 0.08, 0.6 * np.sin(t / 7)); t += 1.2
add(b, whoosh(0.4, 400, 3500), F(T_S1 + 52), 0.25); add(b, pop(500, 0.12), F(T_S1 + 74), 0.25)
for i, t in enumerate(T_LAP):                                                              # laps: a bright ding + hit
    add(b, chime((1568 * 2 ** (i / 12), 2093 * 2 ** (i / 12)), 0.05, 0.6), F(t), 0.3); add(b, thump(0.25), F(t), 0.3)
for t in (T_S2, T_S3, T_OFF): add(b, whoosh(0.4, 300, 6000), F(t - 3), 0.3); add(b, zap(0.2, 2400, 600), F(t), 0.1)
add(b, tick(1800, 0.06), F(PLUG), 0.6); add(b, pop(300, 0.12), F(PLUG), 0.5); add(b, chime(), F(PLUG + 8), 0.28)
tap(b, T_INST); t = T_INST + 3
while t < T_DL1: add(b, tick(3600, 0.02), F(t), 0.05); t += 3
add(b, pop(820, 0.1), F(T_DL1), 0.22); tap(b, T_RUN); add(b, shimmer(0.6), F(T_RUN + 6), 0.25)
add(b, whoosh(0.45, 300, 3000), F(T_ACT - 8), 0.2); add(b, zap(0.25, 3000, 1500), F(T_ACT + 4), 0.1)   # card flies in, foil scratch
for k in range(6): add(b, tick(4200, 0.025), F(T_CODE0 + k * (T_CODE1 - T_CODE0) / 6), 0.14)
tap(b, T_ACTB); add(b, shimmer(0.9), F(T_GOLD), 0.32)
tap(b, T_CONN); tap(b, T_SEARCH); add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV0), 0.2)
tap(b, T_PICK); add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
add(b, OK3(), F(T_OK), 0.3)
tap(b, T_ECU, 0.4); tap(b, T_ESCAN); t = T_ESCAN + 4
while t < T_ESCAN + 16: add(b, tick(3600, 0.03), F(t), 0.07); t += 3.0
add(b, OK3(), F(T_ESCAN + 16), 0.3)
add(b, thump(0.4), F(T_DONE), 0.5); add(b, tick(1200, 0.06), F(T_DONE), 0.4)
add(b, whoosh(0.4, 600, 3000), F(T_STRIKE), 0.22)
t = T_ROLL                                                                                 # rolling digits
while t < T_ROLL1 + 6: add(b, tick(2800 + 400 * np.sin(t), 0.02), F(t), 0.09 * (1 - (t - T_ROLL) / (T_ROLL1 + 6 - T_ROLL)) + 0.02); t += 1.5
add(b, pop(980, 0.12), F(T_ROLL1 + 6), 0.25)
add(b, pop(820, 0.12), F(T_SAVE), 0.26); add(b, shimmer(0.8), F(T_GIFT), 0.3)
add(b, whoosh(0.35, 800, 4000), F(T_CAL + 10), 0.22); add(b, pop(640, 0.12), F(T_CAL), 0.24)
add(b, pop(900, 0.12), F(T_CTA), 0.25); tap(b, T_TAPC, 0.45)
add(b, whoosh(0.4, 400, 4500), F(T_RECAP - 8), 0.18)
for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_RECAP + i * BEAT), 0.26, 0.25 * (i - 1))
add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
light = norm(b, -1)
song, sr = sf.read('song/song_travel.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_unbox.wav', norm(softclip(norm(song, -1) + light * 0.55), -1)); print('ok')
