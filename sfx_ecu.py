"""SFX + mixes for ecu_motion.html. Writes sfx_ecu_full.wav (no-music version), sfx_ecu_light.wav (UI layer)
and, if song/song_cut.wav exists, mix_ecu.wav (song + UI layer)."""
import numpy as np, os
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
KICK = (7.5, 24.4, 41.25, 75, 91.9, 108.75, 125.6); STALL = 58.1
T_PH, T_HOME, T_CONN, T_SEARCH, T_ALLOW = 196, 244, BT(4), BT(6), BT(8)
T_DEV = [BT(12), BT(12.5), BT(13), BT(13.5), BT(14)]
T_PICK = BT(15); T_BACK = T_PICK + 4
T_STEP = [BT(16) - 4, BT(17), BT(18)]; T_OK = BT(19)
T_TILE, T_SCAN, T_DTC, T_CLEAR = BT(20), BT(22), B(6), BT(28)
T_RECAP, T_OFF, T_END = B(8), BT(34), 817.5


def cough(dur=0.16, mag=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    return lp_fast(rng.standard_normal(n), 420) * np.exp(-t * 22) * mag


def sputter():
    out = np.zeros(int(0.9 * SR))
    for d, a in [(0, 1), (0.09, .7), (0.2, .9), (0.33, .5), (0.5, .35)]:
        c = cough(0.16, a); j = int(d * SR); out[j:j + len(c)] += c
    return out


def error_buzz():                                   # short two-tone "fault found"
    out = np.zeros(int(0.42 * SR))
    for i, f in enumerate((523.3, 392.0)):
        s = beep(f, 0.18); j = int(i * 0.16 * SR); out[j:j + len(s)] += s
    return out


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def build(full):
    b = np.zeros((N, 2))
    # --- intro: idling engine misfires, check-engine light, diag plugs in
    for k in KICK: add(b, cough(), F(k), 0.55, 0.3)
    add(b, sputter(), F(STALL - 2), 0.9, 0.3)
    add(b, pop(1100, 0.1), F(22), 0.28); add(b, beep(880, 0.12), F(23), 0.10)
    add(b, whoosh(0.5, 300, 4000), F(134), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
    add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25)
    # --- splash -> home
    add(b, shimmer(0.8), F(T_PH + 8), 0.30); add(b, whoosh(0.35, 500, 5000), F(T_HOME), 0.15)
    # --- connect page, permission, scan
    tap(b, T_CONN); add(b, whoosh(0.35, 500, 5000), F(T_CONN + 3), 0.18)
    tap(b, T_SEARCH); add(b, pop(800, 0.1), F(T_SEARCH + 5), 0.25)
    tap(b, T_ALLOW)
    for i in range(3): add(b, beep(1318.5, 0.10), F(T_ALLOW + 8 + 20 * i), 0.07)
    add(b, chime((1568, 2093), 0.06, 0.6), F(T_DEV[0]), 0.26)
    for i in range(1, 5): add(b, pop(640 + 90 * i, 0.1), F(T_DEV[i]), 0.20, 0.3 * (-1) ** i)
    tap(b, T_PICK); add(b, whoosh(0.35, 500, 5000, False), F(T_BACK), 0.18)
    # --- connecting popup
    add(b, pop(700, 0.12), F(T_BACK + 6), 0.25)
    for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.18)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
    add(b, pop(900, 0.1), F(T_OK + 12), 0.15)
    # --- ECU scan, fault, clear
    tap(b, T_TILE); add(b, whoosh(0.35, 500, 5000), F(T_TILE + 3), 0.18)
    tap(b, T_SCAN)
    for i in range(12): add(b, tick(3600, 0.03), F(T_SCAN + 3 + i * 2.6), 0.08)
    add(b, error_buzz(), F(T_DTC), 0.26); add(b, thump(0.3), F(T_DTC), 0.25)
    add(b, pop(640, 0.13), F(T_DTC + 6), 0.25)
    tap(b, T_CLEAR); add(b, whoosh(0.4, 300, 4500, False), F(T_CLEAR + 3), 0.25)
    add(b, chime((1568, 1975.5, 2349.3), 0.06, 0.8), F(T_CLEAR + 10), 0.32)
    add(b, pop(800, 0.12), F(T_CLEAR + 18), 0.22)
    # --- recap: light goes off
    add(b, whoosh(0.5, 300, 3500, False), F(T_RECAP - 4), 0.25)
    add(b, zap(0.25, 1200, 300), F(T_OFF), 0.16); add(b, chime((1568, 2093), 0.06, 0.6), F(T_OFF + 2), 0.26)
    add(b, pop(700, 0.12), F(T_OFF + 6), 0.22)
    # --- end card
    add(b, shimmer(0.9), F(846), 0.40); add(b, pop(900, 0.12), F(848), 0.25)
    if full:
        for k in KICK: add(b, thump(0.3), F(k), 0.3)
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(16, 33, 4): add(b, thump(0.25), F(BT(n)), 0.18)      # soft bar pulse under the UI
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_ecu_full.wav', full); write('sfx_ecu_light.wav', light)
if os.path.exists('song/song_cut.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_cut.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_ecu.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
