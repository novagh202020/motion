"""SFX + mixes for insp_motion.html (technical-inspection check, 41.25 s). Writes sfx_insp_full.wav (no-music version),
sfx_insp_light.wav (UI layer) and, if song/song_trip.wav exists (song/extend.py 5), mix_insp.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "41.25")
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
BEAT = 16.875
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV = [BT(4), BT(4.15), BT(4.3), BT(4.45), BT(4.6)]
T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_ECU, T_EB = BT(7.5), BT(11); T_ESCAN = T_ECU + 12
T_TRIP, T_TB = BT(11.75), BT(17.5)
T_AI, T_OPT, T_INSP, T_REP = BT(18.25), BT(20), BT(21.5), BT(24)
T_FIX, T_GATE, T_STAMP = BT(41), BT(45), BT(47)
T_RECAP = B(13); T_END = T_RECAP + 67.5
T_DOC0 = T_REP + 22; T_DOC = lambda i: T_DOC0 + i * (T_FIX - 26 - T_DOC0) / 6


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def stamp():
    n = int(0.3 * SR); x = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 30)
    return lp_fast(x, 1800) * 1.4 + thump(0.3) * 0.8


def puff(d=0.5):
    n = int(d * SR); t = np.linspace(0, 1, n); x = rng.standard_normal(n) * np.sin(np.pi * t) ** 2
    return lp_fast(x, 700) * 1.2


def build(full):
    b = np.zeros((N, 2))
    # hook: queue, smoke puffs, «مردود» stamp on the kick, rewind
    for t in (12, 40, 68): add(b, puff(), F(t), 0.22, 0.5)
    add(b, whoosh(0.3, 3000, 600, False), F(86), 0.18); add(b, stamp(), F(91.5), 0.6); add(b, beep(392, 0.22), F(93), 0.12)
    add(b, whoosh(0.7, 4000, 300, False), F(112), 0.30, -0.3)                                   # rewind
    add(b, whoosh(0.5, 300, 4000), F(134), 0.32); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.22)
    add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25)
    # splash -> home -> very fast connect
    add(b, shimmer(0.8), F(T_PH + 8), 0.30); add(b, whoosh(0.35, 500, 5000), F(T_HOME), 0.15)
    tap(b, T_CONN); add(b, whoosh(0.3, 500, 5000), F(T_CONN + 3), 0.16)
    tap(b, T_SEARCH); add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV[0]), 0.22)
    tap(b, T_PICK); add(b, whoosh(0.3, 500, 5000, False), F(T_BACK), 0.16)
    add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
    for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
    # step 1: ECU scan -> P0420 (warning, not a crash)
    for t in (T_ECU, T_TRIP, T_AI): add(b, pop(980, 0.1), F(t + 3), 0.22)                     # step strip
    tap(b, T_ECU); add(b, whoosh(0.3, 500, 5000), F(T_ECU + 3), 0.16); tap(b, T_ESCAN)
    for i in range(5): add(b, tick(3600, 0.03), F(T_ESCAN + 3 + i * 2.6), 0.07)
    add(b, beep(659.3, 0.16), F(T_ESCAN + 14), 0.14); add(b, beep(523.3, 0.18), F(T_ESCAN + 19), 0.14)
    add(b, whoosh(0.3, 500, 5000, False), F(T_EB), 0.14)
    # step 2: trip time-lapse, bumps and exhaust puffs
    tap(b, T_TRIP); add(b, whoosh(0.3, 500, 5000), F(T_TRIP + 3), 0.16); add(b, pop(820, 0.1), F(T_TRIP + 6), 0.18)
    t, gap = T_TRIP + 10, 4.0
    while t < T_TB - 20: add(b, tick(4200, 0.025), F(t), 0.07); t += gap; gap = max(1.4, gap * 0.88)
    for t in range(int(T_TRIP + 8), int(T_TB), 40): add(b, thump(0.18), F(t), 0.12); add(b, puff(0.4), F(t + 2), 0.10, 0.4)
    add(b, pop(640, 0.13), F(T_TB - 18), 0.22); add(b, whoosh(0.3, 500, 5000, False), F(T_TB), 0.14)
    # step 3: AI troubleshooter, inspection option, typing
    tap(b, T_AI); add(b, whoosh(0.35, 500, 5000), F(T_AI + 3), 0.18)
    tap(b, T_OPT); add(b, chime((1568, 2093), 0.05, 0.5), F(T_OPT + 2), 0.18)
    add(b, pop(700, 0.1), F(T_OPT + 10), 0.18); add(b, pop(780, 0.1), F(T_OPT + 16), 0.18)
    tap(b, T_INSP); add(b, whoosh(0.35, 500, 5000), F(T_INSP + 3), 0.18); add(b, pop(900, 0.1), F(T_INSP + 12), 0.2)
    for i in range(int((T_REP - 14 - T_INSP - 22) / 5)): add(b, tick(2400 + 300 * (i % 3), 0.03), F(T_INSP + 24 + i * 5), 0.06)
    # the answer grows and scrolls
    add(b, whoosh(0.5, 300, 5000), F(T_REP), 0.24); add(b, shimmer(0.8), F(T_REP + 10), 0.22)
    add(b, beep(392, 0.2), F(T_DOC(0) + 8), 0.12)
    for k in range(1, 6): add(b, whoosh(0.28, 600, 5000), F(T_DOC(k) - 14), 0.08, 0.3 * (-1) ** k)
    for i in range(5): add(b, pop(700 + 90 * i, 0.1), F(T_DOC(3) + 2 + i * 6), 0.16)
    # repair, gauge 20 -> 85, gate, «قبول»
    add(b, whoosh(0.5, 300, 4000), F(T_FIX - 8), 0.24); add(b, pop(820, 0.12), F(T_FIX + 4), 0.24)
    for i in range(10): add(b, tick(2200 + 160 * i, 0.03), F(T_FIX + 18 + i * 2.2), 0.08)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.9), F(T_FIX + 42), 0.30)
    add(b, whoosh(0.5, 300, 4000), F(T_GATE - 16), 0.22)
    add(b, stamp(), F(T_STAMP - 0.5), 0.55); add(b, chime((1568, 2093, 2637), 0.05, 0.8), F(T_STAMP + 2), 0.28)
    add(b, zap(0.25, 600, 1200), F(T_STAMP + 8), 0.10); add(b, whoosh(0.8, 300, 3500), F(T_STAMP + 22), 0.24, -0.4)
    # break: what it does
    add(b, whoosh(0.4, 400, 4500), F(T_RECAP - 8), 0.18)
    for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_RECAP + i * BEAT), 0.26, 0.25 * (i - 1))
    # end card
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 50.5), 0.22); add(b, thump(0.4), F(T_END + 50.5), 0.40)
        add(b, beep(1046.5, 0.18), F(T_END + 67.5), 0.30); add(b, thump(0.4), F(T_END + 67.5), 0.60)
        for n in range(16, int((T_RECAP - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(BT(n)), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_insp_full.wav', full); write('sfx_insp_light.wav', light)
if os.path.exists('song/song_trip.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_trip.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_insp.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
