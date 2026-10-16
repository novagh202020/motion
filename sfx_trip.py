"""SFX + mixes for trip_motion.html (20-minute trip analysis). Writes sfx_trip_full.wav (no-music version),
sfx_trip_light.wav (UI layer) and, if song/song_cut.wav exists, mix_trip.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "41.25")          # 5 extra groove bars (song/extend.py)
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, hp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV = [BT(4), BT(4.15), BT(4.3), BT(4.45), BT(4.6)]
T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_TILE, T_SCAN, T_GO, T_FIN, T_REP = BT(9), BT(13), BT(17), BT(29), BT(31)
T_RECAP = B(13); T_END = T_RECAP + 67.5
T_DOC0 = T_REP + 22; T_DOC = lambda i: T_DOC0 + i * (T_RECAP - 62 - T_DOC0) / 10
T_PULL, T_BACKIN = T_GO + 26, T_FIN - 16


def drive(dur):
    """Car passing on the road: engine hum + tyre/road noise."""
    n = int(dur * SR); t = np.arange(n) / SR
    fr = 38 + 4 * np.sin(2 * np.pi * 0.3 * t)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    hum = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)) * (0.8 + 0.2 * np.sin(2 * np.pi * 7 * t))
    road = lp_fast(rng.standard_normal(n), 900) * 0.6 + hp_fast(lp_fast(rng.standard_normal(n), 4000), 1500) * 0.12
    a = np.clip(t / 0.4, 0, 1) * np.clip((dur - t) / 0.5, 0, 1)
    y = (lp_fast(hum, 400) * 0.7 + road) * a
    return y / (np.max(np.abs(y)) + 1e-9)


def riser(dur, f0=300, f1=7000):
    n = int(dur * SR); x = rng.standard_normal(n); t = np.linspace(0, 1, n)
    y = lp_fast(x, f0) * (1 - t) + lp_fast(x, f1) * t
    tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (t * 1.5)) / SR) * 0.25
    y = hp_fast((y + tone) * t ** 2.2, 150)
    return y / (np.max(np.abs(y)) + 1e-9)


def warn2():
    out = np.zeros(int(0.42 * SR))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * SR); out[j:j + len(s)] += s
    return out


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def build(full):
    b = np.zeros((N, 2))
    # --- hook: car on the road, sensor chips pop in and link to the car
    add(b, drive(5.0), 0, 0.3)
    for i in range(4):
        a = 22 + i * 14
        add(b, pop(760 + 80 * i, 0.12), F(a), 0.26, 0.4 * (-1) ** i)
        add(b, beep(1568 + 200 * i, 0.08), F(a + 16), 0.07, 0.4 * (-1) ** i)
    add(b, whoosh(0.5, 300, 4000), F(132), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
    add(b, tick(1800, 0.06), F(168), 0.6); add(b, pop(300, 0.12), F(168), 0.5); add(b, chime(), F(176), 0.30)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.25)
    # --- splash -> home -> very fast connect
    add(b, shimmer(0.8), F(T_PH + 8), 0.30); add(b, whoosh(0.35, 500, 5000), F(T_HOME), 0.15)
    tap(b, T_CONN); add(b, whoosh(0.3, 500, 5000), F(T_CONN + 3), 0.16)
    tap(b, T_SEARCH)
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_DEV[0]), 0.22)
    tap(b, T_PICK); add(b, whoosh(0.3, 500, 5000, False), F(T_BACK), 0.16)
    add(b, pop(700, 0.12), F(T_BACK + 6), 0.22)
    for t in T_STEP[1:]: add(b, tick(3000, 0.04), F(t), 0.16)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_OK), 0.32)
    # --- trip screen: scan -> 13 PID cards, start trip
    tap(b, T_TILE); add(b, whoosh(0.35, 500, 5000), F(T_TILE + 3), 0.18)
    tap(b, T_SCAN)
    for i in range(13): add(b, pop(600 + 45 * i, 0.07), F(T_SCAN + 6 + i * 2.6), 0.14, 0.5 * np.sin(i))
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_SCAN + 40), 0.22)
    tap(b, T_GO); add(b, beep(880, 0.12), F(T_GO + 1), 0.14); add(b, beep(1318.5, 0.16), F(T_GO + 5), 0.14)
    # --- 20-minute time-lapse: ticks speed up, riser, cards pulled out of the phone
    t, gap = T_GO + 6, 7.0
    while t < T_FIN - 2:
        add(b, tick(4200, 0.025), F(t), (1.8 if full else 1) * (0.06 + 0.05 * (t - T_GO) / (T_FIN - T_GO))); t += gap; gap = max(1.6, gap * 0.93)
    add(b, riser((T_FIN - T_GO - 8) / 30), F(T_GO + 8), 0.45 if full else 0.22)
    for i in range(6): add(b, whoosh(0.35, 400, 5000), F(T_PULL + i * 4), 0.12, 0.5 * (-1) ** i)
    add(b, pop(820, 0.1), F(T_PULL + 12), 0.15)
    for i in range(6): add(b, whoosh(0.3, 400, 4000, False), F(T_BACKIN + i * 3), 0.09)
    add(b, chime((1318.5, 1661.2, 1975.5), 0.06, 0.8), F(T_FIN + 2), 0.34); add(b, thump(0.4), F(T_FIN + 2), 0.3)
    for i in range(8): add(b, tick(3400, 0.03), F(T_FIN + 12 + i * 2.5), 0.06)
    # --- report document grows out of the phone and scrolls through every section
    add(b, whoosh(0.5, 300, 5000), F(T_REP), 0.24); add(b, shimmer(0.8), F(T_DOC(0)), 0.28)
    add(b, chime((1568, 2093), 0.05, 0.5), F(T_DOC(0) + 26), 0.2)
    for k in range(1, 11): add(b, whoosh(0.28, 600, 5000), F(T_DOC(k) - 14), 0.07, 0.3 * (-1) ** k)
    add(b, warn2(), F(T_DOC(3) + 10), 0.22)                     # fuel system: urgent
    add(b, warn2(), F(T_DOC(7) + 10), 0.18)                     # fault list
    for i in range(14): add(b, tick(3200 if i not in (2, 6) else 1600, 0.03), F(T_DOC(8) + i * 1.6), 0.08)
    for i in range(3): add(b, pop(700 + 120 * i, 0.12), F(T_DOC(10) + 4 + i * 5), 0.22)
    # --- recap: PDF pages fan out
    add(b, whoosh(0.5, 300, 3500, False), F(T_RECAP - 4), 0.25)
    for i in range(5): add(b, whoosh(0.18, 800, 6000), F(T_RECAP + 8 + i * 3), 0.12, 0.4 * (i - 2) / 2); add(b, tick(2200, 0.03), F(T_RECAP + 10 + i * 3), 0.10)
    add(b, pop(900, 0.12), F(T_RECAP + 30), 0.25)
    # --- end card
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 50.5), 0.22); add(b, thump(0.4), F(T_END + 50.5), 0.40)
        add(b, beep(1046.5, 0.18), F(T_END + 67.5), 0.30); add(b, thump(0.4), F(T_END + 67.5), 0.60)
        for n in range(16, int((T_RECAP - 210) / 16.875) + 1, 4): add(b, thump(0.25), F(BT(n)), 0.18)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_trip_full.wav', full); write('sfx_trip_light.wav', light)
if os.path.exists('song/song_trip.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_trip.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_trip.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
