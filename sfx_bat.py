"""SFX + mixes for bat_motion.html (battery & alternator test). Writes sfx_bat_full.wav (no-music version),
sfx_bat_light.wav (UI layer) and, if song/song_cut.wav exists, mix_bat.wav (song + UI layer)."""
import numpy as np, os
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, hp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
CR0, CR1 = 50, 124
CRANK = []
t, p = CR0, 5.2
while t < CR1 - 3:
    CRANK.append(t); t += p; p += 0.22
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(3), BT(4)
T_DEV = [BT(4.75), BT(5), BT(5.25), BT(5.5), BT(5.75)]
T_PICK = BT(6.25); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(7.25), BT(7.75)]; T_OK = BT(8.25)
T_TILE, T_START = BT(9.25), BT(11)
T_R = [BT(14), BT(17), BT(20), BT(23)]; T_RES = T_R[3] + 4
T_RECAP, T_END = B(8), 817.5


def starter(t0, t1, strokes, f_hi=105, f_lo=68):
    """Weak-battery starter motor: buzzy whine whose pitch sags on every compression stroke and drags
    lower over time ("کش اومدن"), plus a dull thud per stroke."""
    n = int((t1 - t0) / 30 * SR); tt = np.arange(n) / SR + t0 / 30
    base = np.interp(tt, [t0 / 30, t1 / 30], [f_hi, f_lo])
    sag = np.zeros(n)
    for s in strokes:
        d = tt - s / 30
        sag += np.where(d >= 0, np.exp(-d / 0.06), 0) * 0.32
    fi = base * (1 - np.clip(sag, 0, 0.55))
    ph = 2 * np.pi * np.cumsum(fi) / SR
    x = sum(np.sin(k * ph) / k ** 0.8 for k in range(1, 14))       # saw-like buzz
    x = lp_fast(x, 1600) + 0.25 * hp_fast(lp_fast(rng.standard_normal(n), 2500), 600)  # gear whir
    am = 0.55 + 0.45 * (1 - np.clip(sag * 2, 0, 1))                 # louder when spinning freely
    a = np.clip((tt - t0 / 30) / 0.04, 0, 1) * np.clip((t1 / 30 - tt) / 0.06, 0, 1)
    out = x * am * a
    for s in strokes:                                               # compression thuds
        j = int((s - t0) / 30 * SR)
        if 0 <= j < n:
            k = min(int(0.12 * SR), n - j); e = np.exp(-np.arange(k) / SR * 30)
            out[j:j + k] += lp_fast(rng.standard_normal(k), 180)[:k] * e * 1.6
    return out / (np.max(np.abs(out)) + 1e-9)


def engine(dur, flare=True):
    """Engine catches and settles to a rough idle."""
    n = int(dur * SR); t = np.arange(n) / SR
    rpm = 14 + (22 * np.exp(-t / 0.35) if flare else 0)             # firing freq (Hz)
    ph = 2 * np.pi * np.cumsum(rpm) / SR
    pulses = (0.5 + 0.5 * np.sin(ph)) ** 6
    body = lp_fast(rng.standard_normal(n), 260) * (0.4 + 0.9 * pulses) + 0.5 * np.sin(ph * 2.0) * pulses
    a = np.clip(t / 0.03, 0, 1) * np.clip((dur - t) / 0.6, 0, 1)
    return body * a / (np.max(np.abs(body)) + 1e-9)


def warn2():                                         # soft two-tone warning (problem found)
    out = np.zeros(int(0.42 * SR))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * SR); out[j:j + len(s)] += s
    return out


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def build(full):
    b = np.zeros((N, 2))
    # --- hook: new-battery card, key on, slow dragging crank, engine catches, battery light stays on
    add(b, pop(700, 0.12), F(5), 0.25)
    add(b, pop(1100, 0.1), F(24), 0.28); add(b, beep(880, 0.12), F(25), 0.10)        # key on, lamps
    add(b, starter(CR0, CR1, CRANK), F(CR0), 0.5 if full else 0.7)
    add(b, engine(3.0), F(CR1), 0.35 if full else 0.45)
    add(b, pop(520, 0.14), F(CR0 + 30), 0.3)                                         # "!" on the new-battery card
    for k in range(3): add(b, beep(988, 0.10), F(CR1 + 6 + 11 * k), 0.08)           # battery lamp nag
    add(b, whoosh(0.5, 300, 4000), F(134), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
    add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25)
    # --- splash -> home -> fast connect
    add(b, shimmer(0.8), F(T_PH + 8), 0.30); add(b, whoosh(0.35, 500, 5000), F(T_HOME), 0.15)
    tap(b, T_CONN); add(b, whoosh(0.3, 500, 5000), F(T_CONN + 3), 0.16)
    tap(b, T_SEARCH)
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV[0]), 0.24)
    for i in range(1, 5): add(b, pop(640 + 90 * i, 0.08), F(T_DEV[i]), 0.16, 0.3 * (-1) ** i)
    tap(b, T_PICK); add(b, whoosh(0.3, 500, 5000, False), F(T_BACK), 0.16)
    add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
    for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
    # --- battery test
    tap(b, T_TILE); add(b, whoosh(0.35, 500, 5000), F(T_TILE + 3), 0.18)
    tap(b, T_START); add(b, pop(820, 0.1), F(T_START + 8), 0.2)
    add(b, starter(T_R[1] - 14, T_R[1] + 4, [T_R[1] - 13, T_R[1] - 8, T_R[1] - 3], 120, 100), F(T_R[1] - 14), 0.35)
    add(b, engine(1.6, False), F(T_R[1] + 4), 0.22)
    for i, t in enumerate(T_R):
        tap(b, t); add(b, pop(900 if i < 2 else 620, 0.1), F(t + 2), 0.24)
    for t in range(int(T_START + 10), int(T_RES), 6): add(b, tick(4200, 0.02), F(t), 0.035)   # live data
    add(b, zap(0.25, 900, 300), F(T_R[1] - 12), 0.10)                                         # voltage dip
    # --- result: two greens, then the alternator warning
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_RES + 8), 0.22); add(b, chime((1568, 2093), 0.05, 0.5), F(T_RES + 17), 0.20)
    add(b, warn2(), F(T_RES + 26), 0.26); add(b, thump(0.3), F(T_RES + 26), 0.22)
    add(b, pop(640, 0.13), F(T_RES + 16), 0.22)
    # --- recap: battery light still on, "it's the alternator"
    add(b, whoosh(0.5, 300, 3500, False), F(T_RECAP - 4), 0.25)
    add(b, warn2(), F(T_RECAP + 14), 0.2); add(b, pop(700, 0.12), F(T_RECAP + 16), 0.22)
    # --- end card
    add(b, shimmer(0.9), F(846), 0.40); add(b, pop(900, 0.12), F(848), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(16, 33, 4): add(b, thump(0.25), F(BT(n)), 0.18)      # soft bar pulse under the UI
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_bat_full.wav', full); write('sfx_bat_light.wav', light)
if os.path.exists('song/song_cut.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_cut.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    # duck the song under the crank so the dragging starter is clearly heard
    tt = np.arange(N) / SR
    duck = 1 - 0.55 * np.clip((tt - F(CR0 - 6)) / 0.2, 0, 1) * np.clip((F(CR1 + 20) - tt) / 0.4, 0, 1)
    write('mix_bat.wav', norm(softclip(norm(song, -1) * duck[:, None] + light * 0.6), -1))
print('ok')
