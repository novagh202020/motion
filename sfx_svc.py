"""SFX + mixes for svc_motion.html (periodic service reminder, 30 s). Writes sfx_svc_full.wav (no-music version),
sfx_svc_light.wav (UI layer) and, if song/song_cut.wav exists, mix_svc.wav (song + UI layer)."""
import numpy as np, os
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, hp_fast, rng
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
T_PH, T_TILE, T_ADD = 138, BT(0), BT(2)
T_FLD = [BT(3), BT(3.75), BT(4.5), BT(5.25)]
T_TYPE0, T_TYPE1, T_SAVE = BT(6), BT(8), BT(8.75)
T_U = [BT(10.5), BT(14.5), BT(18.5)]; T_NOTIF = BT(24)   # three manual km entries (no GPS on a phone)
T_RECAP, T_END = B(8), 817.5; T_LIST = T_RECAP - 12


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def notif():                                        # two-note phone notification
    out = np.zeros(int(0.7 * SR))
    for i, f in enumerate((1318.5, 1975.5)):
        s = chime((f,), 0.0, 0.45); j = int(i * 0.13 * SR); out[j:j + len(s)] += s
    return out


def warn2():
    out = np.zeros(int(0.42 * SR))
    for i, f in enumerate((659.3, 523.3)):
        s = beep(f, 0.18); j = int(i * 0.16 * SR); out[j:j + len(s)] += s
    return out


def build(full):
    b = np.zeros((N, 2))
    # --- hook: odometer rolling, sticky note, oil lamp
    for i in range(40): add(b, tick(2800 + 400 * (i % 2), 0.02), F(2 + i * 3), 0.05)
    add(b, pop(500, 0.14), F(16), 0.25)
    add(b, zap(0.3, 900, 300), F(62), 0.1)                    # the note fades away
    for k in range(4): add(b, beep(988, 0.10), F(96 + 19 * k), 0.09)
    add(b, whoosh(0.6, 200, 2500), F(T_PH), 0.3)
    # --- quick access -> periodic service -> add service dialog
    tap(b, T_TILE); add(b, whoosh(0.35, 500, 5000), F(T_TILE + 3), 0.18)
    tap(b, T_ADD); add(b, pop(700, 0.12), F(T_ADD + 5), 0.22)
    for t in T_FLD: add(b, pop(900, 0.07), F(t), 0.14)
    n = 24
    for i in range(n): add(b, tick(3200 + 300 * (i % 3), 0.02), F(T_TYPE0 + i * (T_TYPE1 - T_TYPE0) / n), 0.07)
    tap(b, T_SAVE); add(b, chime((1568, 2093), 0.05, 0.6), F(T_SAVE + 8), 0.26)
    # --- days pass; the user enters the km three times; green -> amber on the third
    for t in T_U:
        add(b, whoosh(0.25, 800, 6000), F(t - 6), 0.12)              # calendar flips
        tap(b, t); add(b, pop(700, 0.1), F(t + 5), 0.18)
        for i in range(6): add(b, tick(3200 + 300 * (i % 3), 0.02), F(t + 8 + i * 2), 0.08)
        tap(b, t + 22, 0.3)
        for i in range(6): add(b, tick(4200, 0.02), F(t + 28 + i * 2), (1.6 if full else 1) * 0.06)
    add(b, warn2(), F(T_U[2] + 38), 0.26); add(b, thump(0.3), F(T_U[2] + 38), 0.25)
    # --- notification
    add(b, notif(), F(T_NOTIF), 0.4); add(b, pop(820, 0.12), F(T_NOTIF + 8), 0.2)
    # --- more services
    for i in range(1, 4): add(b, pop(700 + 100 * i, 0.1), F(T_LIST + i * 6), 0.2)
    # --- end card
    add(b, shimmer(0.9), F(846), 0.40); add(b, pop(900, 0.12), F(848), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
        for n in range(0, 33, 4): add(b, thump(0.25), F(BT(n)), 0.18)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_svc_full.wav', full); write('sfx_svc_light.wav', light)
if os.path.exists('song/song_cut.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_cut.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_svc.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
