"""SFX + mixes for box_motion.html (what ships with CarDiag, 53.2 s). Writes sfx_box_full.wav (no-music version),
sfx_box_light.wav (UI layer) and, if song/song_box.wav exists (song/box_cut.py), mix_box.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "53.2")
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, rng
F = lambda f: f / 30
HALF, BEAT = 67.5, 16.875
B = lambda m: 7.5 + HALF * m
T_DIAG, T_PLUG, T_CARD, T_PH, T_FREE, T_PAID = B(3), B(5), B(6), B(7), B(8), B(10)
T_CRED, T_MIX, T_PLANS, T_TRUST, T_COMP, T_END = B(12), B(13), B(15), B(17), B(19), B(21)
F_HIT = B(23)


def zipper(d=2.2):
    n = int(d * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n) * (0.5 + 0.5 * (np.sin(2 * np.pi * 38 * t) > 0.6))
    return lp_fast(x, 3500) * np.sin(np.pi * np.linspace(0, 1, n)) ** 0.5 * 0.8


def scratch(d=0.6):
    n = int(d * SR); x = rng.standard_normal(n) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * np.arange(n) / SR))
    return lp_fast(x, 6000) * np.sin(np.pi * np.linspace(0, 1, n))


def coin():
    s = np.zeros(int(0.5 * SR))
    for f0, d in ((2637, 0), (3520, 0.05)):
        b = beep(f0, 0.3); i = int(d * SR); s[i:i + len(b)] += b
    return s


def build(full):
    b = np.zeros((N, 2))
    # the zip case: pops in, zip runs round, lid flips, items lift
    add(b, pop(500, 0.12), F(10), 0.3); add(b, zipper(), F(38), 0.32)
    add(b, whoosh(0.4, 300, 3000), F(104), 0.24); add(b, thump(0.25), F(122), 0.2)
    add(b, shimmer(0.7), F(128), 0.3); add(b, whoosh(0.5, 400, 5000), F(132), 0.2, 0.4)
    # 1. diag: chips on the beats, plug in, connected
    for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_DIAG + 6 + i * 2 * BEAT), 0.26, 0.25 * (i - 1))
    add(b, whoosh(0.4, 300, 3000, False), F(T_PLUG), 0.2); add(b, tick(1800, 0.06), F(T_PLUG + 22), 0.6); add(b, pop(300, 0.12), F(T_PLUG + 22), 0.45)
    add(b, chime(), F(T_PLUG + 30), 0.3)
    # 2. activation card: scratch, phone, code, activate, gold plan
    add(b, whoosh(0.5, 300, 4000), F(T_CARD - 6), 0.24); add(b, scratch(), F(T_CARD + 2 * BEAT), 0.3)
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_CARD + 3 * BEAT + 6), 0.2)
    add(b, whoosh(0.4, 200, 2500), F(T_PH), 0.22); add(b, whoosh(0.3, 600, 5000, False), F(T_PH + 10), 0.16)
    for i in range(6): add(b, tick(2600 + 200 * i, 0.03), F(T_PH + 24 + i * 1.8), 0.08)
    add(b, tick(), F(T_PH + 40), 0.4); add(b, shimmer(0.7), F(T_PH + 46), 0.3); add(b, chime((1975.5, 2637), 0.05, 0.7), F(T_PH + 50), 0.24)
    # free list, paid list with coins
    add(b, whoosh(0.4, 400, 4500), F(T_FREE - 6), 0.18)
    for i in range(4): add(b, pop(640 + 80 * i, 0.11), F(T_FREE + 10 + i * 2 * BEAT), 0.24, 0.3)
    add(b, whoosh(0.4, 400, 4500), F(T_PAID - 4), 0.16)
    for i in range(2): add(b, pop(700, 0.11), F(T_PAID + 10 + i * 2 * BEAT), 0.24, 0.3); add(b, coin(), F(T_PAID + 22 + i * 2 * BEAT), 0.18)
    # 72 credits: stack, two coins spent, the mix bar
    add(b, shimmer(0.6), F(T_CRED + 2), 0.26)
    for t in (T_CRED + 0.5 * BEAT, T_CRED + 2 * BEAT): add(b, whoosh(0.3, 800, 5000), F(t), 0.14); add(b, coin(), F(t + 10), 0.2)
    for i in range(5): add(b, pop(900 + 60 * i, 0.08), F(T_CRED + 1.1 * BEAT + i * 3), 0.14)
    add(b, whoosh(0.5, 300, 4000), F(T_MIX + BEAT + 6), 0.16); add(b, whoosh(0.5, 300, 4000), F(T_MIX + 2 * BEAT + 6), 0.16)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_MIX + 3.5 * BEAT + 6), 0.26)
    # plans, peace of mind, compatibility
    for i in range(2): add(b, whoosh(0.35, 500, 5000), F(T_PLANS + 4 + i * 2 * BEAT), 0.16)
    for i in range(4): add(b, tick(3000, 0.04), F(T_TRUST + 8 + i * 1.4 * BEAT), 0.2); add(b, beep(1318.5 + 120 * i, 0.08), F(T_TRUST + 9 + i * 1.4 * BEAT), 0.06)
    for i in range(2): add(b, whoosh(0.5, 300, 4000), F(T_COMP + 8 + i * 2 * BEAT), 0.14)
    add(b, pop(820, 0.1), F(T_COMP + 5 * BEAT), 0.2); add(b, pop(900, 0.1), F(T_COMP + 6 * BEAT), 0.2)
    # end card
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 50.5), 0.22); add(b, thump(0.4), F(T_END + 50.5), 0.40)
        add(b, beep(1046.5, 0.18), F(T_END + 67.5), 0.30); add(b, thump(0.4), F(T_END + 67.5), 0.60)
        add(b, beep(1046.5, 0.18), F(F_HIT - 17), 0.22); add(b, thump(0.4), F(F_HIT - 17), 0.40)
        add(b, beep(1046.5, 0.18), F(F_HIT), 0.30); add(b, thump(0.4), F(F_HIT), 0.60)
        for n in range(0, int((B(20) - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(210 + BEAT * n), 0.16)
        for k in (7.5, 41.25, 75, 108.75): add(b, thump(0.3), F(k), 0.22)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_box_full.wav', full); write('sfx_box_light.wav', light)
if os.path.exists('song/song_box.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_box.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_box.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
