"""UI layer + music mix for unbox_motion.html (box to first scan + 3-day offer, 62 s). Writes mix_unbox.wav (song/song_full.wav + UI layer).
Music version only."""
import numpy as np, soundfile as sf
from audio import N, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write
F = lambda f: f / 30
MB = lambda m: 7.5 + 67.5 * m
T_S1 = MB(3); T_ZIP, T_LID, T_LIFT = T_S1 + 24, T_S1 + 84, T_S1 + 108
T_S2 = MB(6); T_PLUG = T_S2 + 78
T_S3 = MB(9); T_INST = T_S3 + 44; T_DL1 = T_INST + 96; T_RUN = T_S3 + 156
T_S4 = MB(12); T_CONN = T_S4 + 52; T_STEP = [T_S4 + 60, T_S4 + 84, T_S4 + 108]; T_OK = T_S4 + 132
T_S5 = MB(15); T_ECU, T_ESCAN = T_S5 + 40, T_S5 + 84; T_RES = T_ESCAN + 30
T_DONE = MB(18)
T_OA = MB(19); T_STRIKE = T_OA + 30; T_ROLL = MB(20); T_ROLL1 = T_ROLL + 40; T_SAVE = T_ROLL + 52
T_OB, T_OC, T_OD, T_TAPC, T_END = MB(21), MB(22), MB(23), MB(24) + 20, MB(25)


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


OK3 = lambda: chime((1318.5, 1661.2, 1975.5), 0.06, 0.8)
b = np.zeros((N, 2))
add(b, whoosh(0.5, 3000, 300, False), F(8), 0.25); add(b, thump(0.3), F(28), 0.4)          # the case drops in
t = T_ZIP                                                                                  # zipper
while t < T_ZIP + 56: add(b, tick(5200, 0.015), F(t), 0.08, 0.6 * np.sin(t / 7)); t += 1.2
add(b, whoosh(0.4, 400, 3500), F(T_LID), 0.25); add(b, whoosh(0.5, 300, 4000), F(T_LIFT), 0.22); add(b, shimmer(0.7), F(T_LIFT + 30), 0.25)
for t in (MB(6), MB(9), MB(19), MB(21), MB(22), MB(23)): add(b, whoosh(0.35, 300, 6000), F(t - 3), 0.26); add(b, zap(0.2, 2400, 600), F(t), 0.08)
add(b, tick(1800, 0.06), F(T_PLUG), 0.6); add(b, pop(300, 0.12), F(T_PLUG), 0.5); add(b, chime(), F(T_PLUG + 8), 0.28)
tap(b, T_INST); t = T_INST + 4
while t < T_DL1: add(b, tick(3600, 0.02), F(t), 0.05); t += 4
add(b, pop(820, 0.1), F(T_DL1), 0.22); tap(b, T_RUN); add(b, shimmer(0.7), F(T_RUN + 8), 0.25)
tap(b, T_CONN); add(b, pop(700, 0.12), F(T_CONN + 4), 0.2)
for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
add(b, OK3(), F(T_OK), 0.32)
tap(b, T_ECU, 0.4); tap(b, T_ESCAN); t = T_ESCAN + 4
while t < T_RES: add(b, tick(3600, 0.03), F(t), 0.07); t += 3.0
add(b, OK3(), F(T_RES), 0.32)
add(b, thump(0.4), F(T_DONE), 0.5); add(b, tick(1200, 0.06), F(T_DONE), 0.4)
add(b, whoosh(0.4, 600, 3000), F(T_STRIKE), 0.22)
t = T_ROLL
while t < T_ROLL1 + 9: add(b, tick(2800 + 400 * np.sin(t), 0.02), F(t), 0.09 * (1 - (t - T_ROLL) / (T_ROLL1 + 9 - T_ROLL)) + 0.02); t += 1.5
add(b, pop(980, 0.12), F(T_ROLL1 + 9), 0.25); add(b, pop(820, 0.12), F(T_SAVE), 0.26)
add(b, shimmer(0.9), F(T_OB + 22), 0.32)
add(b, pop(640, 0.12), F(T_OC + 4), 0.24); add(b, whoosh(0.35, 800, 4000), F(T_OC + 16), 0.22); add(b, pop(900, 0.1), F(T_OC + 28), 0.2)
add(b, pop(820, 0.1), F(T_OD + 4), 0.2); add(b, pop(900, 0.1), F(T_OD + 14), 0.2); add(b, pop(1000, 0.12), F(T_OD + 26), 0.26); tap(b, T_TAPC, 0.45)
add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
light = norm(b, -1)
song, sr = sf.read('song/song_full.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_unbox.wav', norm(softclip(norm(song, -1) + light * 0.55), -1)); print('ok')
