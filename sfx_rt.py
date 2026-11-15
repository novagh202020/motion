"""SFX + mixes for retail_motion.html (30 s, song/song_cut.wav grid: bar m = 7.5 + 67.5m; features bars 3-9, recap 682.5,
break 750, end card 817.5, heartbeats 868 / 885). Writes sfx_rt_full.wav (no music) and mix_rt.wav (song + light UI layer)."""
import numpy as np, soundfile as sf
from audio import N, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write
F = lambda fr: fr / 30.0
BAR, BEAT = 67.5, 16.875
B = lambda m: 7.5 + BAR * m
T_F, T_REC, T_BRK, T_END = B(3), B(10), B(11), B(12)


def build(full):
    b = np.zeros((N, 2))
    add(b, whoosh(0.5, 300, 5000), F(4), 0.28); add(b, whoosh(0.4, 200, 2500, False), F(10), 0.26)
    if full:
        for fr in (7.5, 41.25, 75): add(b, thump(0.3), F(fr), 0.25)
        add(b, beep(1046.5, 0.22), F(24.4), 0.32); add(b, thump(0.5), F(24.4), 0.85)
    add(b, shimmer(0.7), F(30), 0.30)
    add(b, whoosh(0.4, 300, 4000), F(40), 0.24); add(b, pop(760, 0.12), F(52), 0.30)        # price strip lands
    add(b, chime((1568, 2093), 0.06, 0.6), F(60), 0.20)
    add(b, whoosh(0.5, 300, 4500, False), F(T_F - 10), 0.26)
    for k in range(7):                                                                    # one feature per bar
        a = B(3 + k)
        if k: add(b, whoosh(0.3, 500, 5000), F(a) - 0.12, 0.18, 0.2 * (-1) ** k)
        add(b, pop(640 + 50 * k, 0.12), F(a + 3), 0.28); add(b, tick(3000, 0.04), F(a + 2), 0.14)
    add(b, whoosh(0.4, 400, 4500, False), F(T_REC - 4), 0.24)
    for i in range(7): add(b, pop(600 + 70 * i, 0.10), F(T_REC + 4 + i * 8.4), 0.22, 0.3 * (-1) ** i)
    add(b, whoosh(0.5, 300, 3500, False), F(T_BRK - 4), 0.25)
    for i in range(3): add(b, pop(760 + 120 * i, 0.11), F(T_BRK + 4 + i * BEAT), 0.28)
    add(b, shimmer(0.6), F(T_BRK + 8), 0.25)
    add(b, pop(900, 0.12), F(T_END + 10), 0.26); add(b, shimmer(0.9), F(T_END + 16), 0.30); add(b, tick(), F(T_END + 10 + BEAT), 0.30)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(0, int((T_REC - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(210 + BEAT * n), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_rt_full.wav', full)
song, sr = sf.read('song/song_cut.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_rt.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
