"""SFX + mixes for wholesale_motion.html (21 s wholesale teaser, song/song_wh.wav grid: bar k = frame 67.5k).
Writes sfx_wh_full.wav (no-music version, with heartbeat kicks) and mix_wh.wav (song + light UI layer)."""
import os
os.environ.setdefault("CARDIAG_DUR", "21")
import numpy as np, soundfile as sf
from audio import N, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write

F = lambda fr: fr / 30.0
BAR, BEAT = 67.5, 16.875
B = lambda k: BAR * k
T_APP, T_CHIP, T_TRUST, T_PRICE, T_TERMS, T_END, T_HIT = B(2), B(3), B(4), B(6), B(7), B(8), B(9)


def build(full):
    b = np.zeros((N, 2))
    # scene 1: line draws, the diag drops in and lands, sales counter
    add(b, whoosh(0.5, 300, 5000), F(2), 0.28)
    add(b, whoosh(0.4, 200, 2500, False), F(14), 0.30)
    add(b, thump(0.45), F(26), 0.75 if full else 0.45); add(b, shimmer(0.7), F(30), 0.30)
    add(b, pop(820, 0.12), F(B(1) - 4), 0.30)
    for i in range(10): add(b, tick(3200 + 120 * i, 0.03), F(B(1) + 2 + i * 3.6), 0.10)
    add(b, chime((1568, 2093), 0.06, 0.6), F(B(1) + 40), 0.22)
    # scene 2: diag slides, phone rises, BT link, chips on the beats
    add(b, whoosh(0.45, 300, 4000), F(T_APP), 0.28)
    add(b, zap(0.22), F(T_APP + 16), 0.22); add(b, chime(), F(T_APP + 22), 0.26)
    for i in range(3): add(b, pop(640 + 90 * i, 0.12), F(T_CHIP + i * BEAT * 1.2 + 3), 0.30, 0.2 * (i - 1))
    # scene 3: trust cards
    add(b, whoosh(0.4, 400, 4500, False), F(T_TRUST - 4), 0.24)
    for i in range(4): add(b, pop(700 + 80 * i, 0.11), F(T_TRUST + 6 + i * BEAT * 1.6 + 3), 0.30, 0.25 * (-1) ** i)
    add(b, shimmer(0.6), F(T_TRUST + 6 + 3 * BEAT * 1.6 + 6), 0.25)           # gold capsule
    # scene 4: price counts up on the break, terms on the outro
    add(b, whoosh(0.5, 300, 3500), F(T_PRICE - 6), 0.26); add(b, thump(0.4), F(T_PRICE + 2), 0.5 if full else 0.3)
    for i in range(14): add(b, tick(3000 + 90 * i, 0.025), F(T_PRICE + 6 + i * 3.3), 0.09)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_PRICE + 52), 0.28)
    for i in range(2): add(b, pop(760 + 120 * i, 0.11), F(T_TERMS + i * 2 * BEAT), 0.28)
    # end card
    add(b, whoosh(0.5, 300, 5000, False), F(T_END - 6), 0.25)
    add(b, pop(900, 0.12), F(T_END + 10), 0.26); add(b, shimmer(0.9), F(T_END + 14), 0.30)
    add(b, tick(), F(T_END + 10 + 2 * BEAT), 0.30)
    if full:
        add(b, thump(0.5), F(T_END), 0.65); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 2 * BEAT), 0.22); add(b, thump(0.4), F(T_END + 2 * BEAT), 0.40)
        add(b, beep(1046.5, 0.2), F(T_HIT), 0.32); add(b, thump(0.5), F(T_HIT), 0.75)
        for n in range(0, int(T_END / BEAT), 4): add(b, thump(0.25), F(BEAT * n), 0.14)   # soft pulse on the bars
    fade = np.ones(N); i0 = int(20.4 * 48000); fade[i0:] = np.linspace(1, 0, N - i0)
    return b * fade[:, None]


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_wh_full.wav', full)
song, sr = sf.read('song/song_wh.wav'); song = song[:N]
if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
write('mix_wh.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
