"""SFX + mixes for tg_motion.html (Telegram channel promo, 30 s, song/song_cut.wav grid). Writes sfx_tg_full.wav
(no-music version), sfx_tg_light.wav (UI layer) and mix_tg.wav (song + UI layer)."""
import numpy as np, os
from audio import N, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write
F = lambda fr: fr / 30.0
HALF, BEAT = 67.5, 16.875
B = lambda m: 7.5 + HALF * m
T_PH, T_LAND = 100, 122
T_EX, T_JOIN, T_NTF, T_OUT, T_END = B(7), B(9) + 8, B(10), B(11), B(12)


def build(full):
    b = np.zeros((N, 2))
    # intro: heartbeat line, the paper plane takes off and dives into the phone
    add(b, whoosh(0.5, 300, 5000), F(9), 0.30)
    if full:
        for fr in (7.5, 41.25, 75): add(b, thump(0.3), F(fr), 0.25)
        add(b, beep(1046.5, 0.22), F(24.4), 0.32); add(b, thump(0.5), F(24.4), 0.85)
    add(b, shimmer(0.6), F(46), 0.35)
    add(b, whoosh(0.9, 300, 6000), F(90), 0.40, 0.3)               # take-off
    add(b, whoosh(0.4, 200, 2500), F(T_PH), 0.28, -0.1)            # phone up (fast)
    add(b, pop(900, 0.12), F(T_LAND - 2), 0.35); add(b, chime(), F(T_LAND + 2), 0.30)
    # one post per bar
    for i in range(4):
        add(b, whoosh(0.3, 500, 5000), F(B(3 + i)) - 0.12, 0.18, 0.2 * (-1) ** i)
        add(b, pop(620 + 70 * i, 0.12), F(B(3 + i) + 2), 0.30)
    # "what you get": one row every two beats
    add(b, whoosh(0.4, 400, 4500), F(T_EX - 8), 0.18)
    for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_EX + i * 2 * BEAT), 0.26, 0.25 * (i - 1))
    # join, bell, notification
    add(b, tick(), F(T_JOIN), 0.45); add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_JOIN + 2), 0.32)
    add(b, bell(1.0), F(T_JOIN + 12), 0.22)
    add(b, whoosh(0.3, 600, 5000, False), F(T_NTF), 0.16); add(b, chime((1568, 2093), 0.05, 0.5), F(T_NTF + 6), 0.22)
    # break: the plane in the blue circle; outro: @cardiagai
    add(b, whoosh(0.5, 300, 3500, False), F(T_OUT - 4), 0.25); add(b, shimmer(0.8), F(T_OUT + 8), 0.35)
    add(b, pop(900, 0.12), F(T_END + 2), 0.28); add(b, shimmer(0.9), F(T_END + 18), 0.30)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(0, int((T_OUT - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(210 + BEAT * n), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_tg_full.wav', full); write('sfx_tg_light.wav', light)
import soundfile as sf
song, sr = sf.read('song/song_cut.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_tg.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
