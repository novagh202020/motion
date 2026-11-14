"""SFX + mixes for wholesale_motion.html (30 s wholesale teaser on the song/song_cut.wav grid: bar m = 7.5 + 67.5m,
groove from 210, recap 750, end card 817.5, heartbeats 868 / 885).
Writes sfx_wh_full.wav (no-music version) and mix_wh.wav (CarDiag song + light UI layer)."""
import numpy as np, soundfile as sf
from audio import N, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write

F = lambda fr: fr / 30.0
BAR, BEAT = 67.5, 16.875
B = lambda m: 7.5 + BAR * m
T_APP, T_CHIP, T_TRUST, T_PRICE, T_TERMS, T_PROF, T_PROF2, T_REC, T_END = B(3), B(4), B(5), B(7), B(8), B(9), B(10), B(11), B(12)


def build(full):
    b = np.zeros((N, 2))
    # intro: line draws, the diag drops on the heartbeat spike, sales counter
    add(b, whoosh(0.5, 300, 5000), F(4), 0.28)
    add(b, whoosh(0.4, 200, 2500, False), F(10), 0.26)
    if full:
        for fr in (7.5, 41.25, 75): add(b, thump(0.3), F(fr), 0.25)
        add(b, beep(1046.5, 0.22), F(24.4), 0.32); add(b, thump(0.5), F(24.4), 0.85)
    add(b, shimmer(0.7), F(30), 0.30)
    add(b, pop(820, 0.12), F(103), 0.30)
    for i in range(10): add(b, tick(3200 + 120 * i, 0.03), F(110 + i * 3.6), 0.10)
    add(b, chime((1568, 2093), 0.06, 0.6), F(150), 0.22)
    # app: phone rises, Bluetooth link, chips
    add(b, whoosh(0.45, 300, 4000), F(T_APP), 0.28)
    add(b, zap(0.22), F(T_APP + 16), 0.22); add(b, chime(), F(T_APP + 22), 0.26)
    for i in range(3): add(b, pop(640 + 90 * i, 0.12), F(T_CHIP + i * BEAT * 1.2 + 3), 0.30, 0.2 * (i - 1))
    # trust cards
    add(b, whoosh(0.4, 400, 4500, False), F(T_TRUST - 4), 0.24)
    for i in range(4): add(b, pop(700 + 80 * i, 0.11), F(T_TRUST + 6 + i * BEAT * 2 + 3), 0.30, 0.25 * (-1) ** i)
    add(b, shimmer(0.6), F(T_TRUST + 6 + 6 * BEAT + 6), 0.25)
    # price counts up, terms
    add(b, whoosh(0.5, 300, 3500), F(T_PRICE - 6), 0.26)
    for i in range(14): add(b, tick(3000 + 90 * i, 0.025), F(T_PRICE + 6 + i * 3.3), 0.09)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_PRICE + 52), 0.26)
    for i in range(2): add(b, pop(760 + 120 * i, 0.11), F(T_TERMS + i * 2 * BEAT), 0.28)
    # profit cards
    add(b, whoosh(0.4, 400, 4500), F(T_PROF - 6), 0.24)
    add(b, pop(700, 0.12), F(T_PROF + 4), 0.28); add(b, pop(860, 0.12), F(T_PROF + 2 * BEAT + 2), 0.30)
    for i in range(10): add(b, tick(3400 + 100 * i, 0.025), F(T_PROF + 2 * BEAT + 4 + i * 3.4), 0.08)
    add(b, pop(1000, 0.12), F(T_PROF2 + 2), 0.30); add(b, chime((1568, 2093), 0.06, 0.6), F(T_PROF2 + 10), 0.24)
    # recap + end card
    add(b, whoosh(0.5, 300, 3500, False), F(T_REC - 4), 0.25); add(b, shimmer(0.8), F(T_REC + 10), 0.30)
    add(b, pop(900, 0.12), F(T_END + 10), 0.26); add(b, shimmer(0.9), F(T_END + 16), 0.30)
    add(b, tick(), F(T_END + 10 + 2 * BEAT), 0.30)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(0, int((T_REC - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(210 + BEAT * n), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_wh_full.wav', full)
song, sr = sf.read('song/song_cut.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_wh.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
