"""SFX + mixes for buy_motion.html (pre-purchase check with the AI troubleshooter, 36.75 s). Writes sfx_buy_full.wav
(no-music version), sfx_buy_light.wav (UI layer) and, if song/song_buy.wav exists, mix_buy.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "36.75")          # 3 extra groove bars (song/extend.py 3)
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, hp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV = [BT(4), BT(4.15), BT(4.3), BT(4.45), BT(4.6)]
T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_ECU, T_TRIP, T_AI, T_BUY, T_REP = BT(7.75), BT(9.5), BT(12), BT(15), BT(18)
T_RECAP = B(11); T_END = T_RECAP + 67.5
T_DOC0 = T_REP + 22; T_DOC = lambda i: T_DOC0 + i * (T_RECAP - 62 - T_DOC0) / 6


def warn2():
    out = np.zeros(int(0.42 * SR))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * SR); out[j:j + len(s)] += s
    return out


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def build(full):
    b = np.zeros((N, 2))
    # --- hook: the seller's chat bubbles, then a question mark
    add(b, pop(600, 0.1), F(12), 0.18)
    for i in range(3): add(b, pop(820 + 120 * i, 0.12), F(22 + i * 22), 0.28, 0.3 * (-1) ** i)
    add(b, zap(0.3, 1400, 500), F(92), 0.18); add(b, thump(0.35), F(94), 0.35); add(b, beep(392, 0.2), F(96), 0.12)
    add(b, whoosh(0.5, 300, 4000), F(132), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
    add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25)
    # --- splash -> home -> very fast connect
    add(b, shimmer(0.8), F(T_PH + 8), 0.30); add(b, whoosh(0.35, 500, 5000), F(T_HOME), 0.15)
    tap(b, T_CONN); add(b, whoosh(0.3, 500, 5000), F(T_CONN + 3), 0.16)
    tap(b, T_SEARCH); add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV[0]), 0.22)
    tap(b, T_PICK); add(b, whoosh(0.3, 500, 5000, False), F(T_BACK), 0.16)
    add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
    for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
    # --- montage: ECU scan (0 faults), 20-minute trip (68%)
    tap(b, T_ECU); add(b, pop(760, 0.1), F(T_ECU + 4), 0.2)
    for i in range(8): add(b, tick(3600, 0.03), F(T_ECU + 9 + i * 3), 0.07)
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_ECU + 32), 0.22)
    tap(b, T_TRIP); add(b, pop(820, 0.1), F(T_TRIP + 6), 0.2)
    t, gap = T_TRIP + 10, 4.0
    while t < T_TRIP + 40: add(b, tick(4200, 0.025), F(t), 0.08); t += gap; gap = max(1.4, gap * 0.85)
    add(b, pop(640, 0.13), F(T_TRIP + 42), 0.22)
    # --- AI troubleshooter, gold badge, "I want to buy this car", typing
    tap(b, T_AI); add(b, whoosh(0.35, 500, 5000), F(T_AI + 3), 0.18)
    add(b, shimmer(0.6), F(T_AI + 22), 0.3); add(b, chime((1975.5, 2637), 0.05, 0.6), F(T_AI + 24), 0.18)   # gold
    tap(b, T_BUY); add(b, whoosh(0.35, 500, 5000), F(T_BUY + 3), 0.18)
    add(b, pop(900, 0.1), F(T_BUY + 12), 0.2)
    for i in range(int((T_REP - 14 - T_BUY - 22) / 5)): add(b, tick(2400 + 300 * (i % 3), 0.03), F(T_BUY + 24 + i * 5), 0.06)
    # --- the answer grows out of the phone and scrolls section by section
    add(b, whoosh(0.5, 300, 5000), F(T_REP), 0.24); add(b, shimmer(0.8), F(T_REP + 10), 0.26)
    for k in range(1, 6): add(b, whoosh(0.28, 600, 5000), F(T_DOC(k) - 14), 0.08, 0.3 * (-1) ** k)
    add(b, warn2(), F(T_DOC(1) + 4), 0.2)                                   # money issues
    add(b, pop(520, 0.14), F(T_DOC(2) + 2), 0.26); add(b, beep(784, 0.12), F(T_DOC(2) + 6), 0.1)   # negotiation tip
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_DOC(3) + 4), 0.2)            # mileage matches
    for i in range(4): add(b, pop(700 + 90 * i, 0.1), F(T_DOC(5) + 2 + i * 8), 0.2)
    # --- recap checklist + gold capsule
    add(b, whoosh(0.5, 300, 3500, False), F(T_RECAP - 4), 0.25)
    for i in range(5): add(b, tick(3000, 0.04), F(T_RECAP + 6 + i * 6), 0.18); add(b, beep(1318.5 + 120 * i, 0.08), F(T_RECAP + 7 + i * 6), 0.06)
    add(b, shimmer(0.7), F(T_RECAP + 38), 0.35); add(b, chime((1975.5, 2637), 0.05, 0.7), F(T_RECAP + 40), 0.22)
    # --- end card
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 50.5), 0.22); add(b, thump(0.4), F(T_END + 50.5), 0.40)
        add(b, beep(1046.5, 0.18), F(T_END + 67.5), 0.30); add(b, thump(0.4), F(T_END + 67.5), 0.60)
        for n in range(16, int((T_RECAP - 210) / 16.875) + 1, 4): add(b, thump(0.25), F(BT(n)), 0.18)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_buy_full.wav', full); write('sfx_buy_light.wav', light)
if os.path.exists('song/song_buy.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_buy.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_buy.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
