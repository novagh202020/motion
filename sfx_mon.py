"""SFX + mixes for mon_motion.html (live monitoring, 36.75 s). Writes sfx_mon_full.wav (no-music version),
sfx_mon_light.wav (UI layer) and, if song/song_buy.wav exists (song/extend.py 3), mix_mon.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "36.75")
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write
F = lambda f: f / 30
B = lambda k: 210 + 67.5 * k
BT = lambda n: 210 + 16.875 * n
BEAT, UPD = 16.875, 709 / 1000 * 30
T_PH, T_HOME = 196, 244
T_CONN, T_SEARCH = BT(2.75), BT(3.5)
T_DEV = [BT(4), BT(4.15), BT(4.3), BT(4.45), BT(4.6)]
T_PICK = BT(5); T_BACK = T_PICK + 4
T_STEP = [T_BACK + 6, BT(5.75), BT(6.25)]; T_OK = BT(6.75)
T_MON, T_MS = BT(7.25), BT(9)
T_SCAN, T_FOUND, T_LIST1 = BT(10), BT(11.25), BT(12)
T_TICK1 = [BT(12.75) + i * BEAT / 2 for i in range(13)]
T_OK1, T_START1, T_STOP, T_RESCAN, T_LIST2 = BT(20), BT(21), BT(29), BT(30), BT(31.5)
T_TICK2 = [BT(32.25), BT(34), BT(34.5)]
T_OK2, T_START2 = BT(35.5), BT(36.5)
T_EX = B(11); T_END = T_EX + 67.5


def tap(b, t, g=0.35):
    add(b, tick(), F(t), g)


def build(full):
    b = np.zeros((N, 2))
    # hook: the driver's questions pop up
    add(b, pop(600, 0.1), F(12), 0.18)
    for i in range(3): add(b, pop(820 + 120 * i, 0.12), F(22 + i * 22), 0.28, 0.3 * (-1) ** i)
    add(b, zap(0.3, 1400, 500), F(92), 0.18); add(b, thump(0.35), F(94), 0.35)
    add(b, whoosh(0.5, 300, 4000), F(132), 0.35); add(b, whoosh(0.5, 250, 3000, False), F(150), 0.25)
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
    # long press on the monitoring tile, release -> page
    tap(b, T_MON, 0.4); add(b, beep(880, 0.25), F(T_MON + 2), 0.05)
    add(b, pop(760, 0.1), F(T_MS - 4), 0.22); add(b, whoosh(0.35, 500, 5000), F(T_MS), 0.18)
    for a, z in ((T_SCAN, T_FOUND), (T_RESCAN, T_LIST2 - 6)):        # scan: radar ticks, found chime
        tap(b, a); t = a + 4
        while t < z: add(b, tick(3600, 0.03), F(t), 0.07); t += 3.2
    add(b, chime((1568, 2093), 0.05, 0.6), F(T_FOUND), 0.24)
    for lst, ticks, ok in ((T_LIST1, T_TICK1, T_OK1), (T_LIST2, T_TICK2, T_OK2)):
        add(b, whoosh(0.35, 400, 4500), F(lst), 0.18)
        for i, t in enumerate(ticks): add(b, tick(2600 + 90 * (i % 5), 0.04), F(t), 0.22, 0.2 * (-1) ** i)
        tap(b, ok); add(b, chime((1318.5, 1760), 0.05, 0.5), F(ok + 2), 0.2); add(b, whoosh(0.3, 500, 5000, False), F(ok + 4), 0.14)
    # reading: start, one soft blip per refresh (709 ms), stop
    for a, z, k in ((T_START1, T_STOP, 13), (T_START2, T_EX - 4, 3)):
        tap(b, a); add(b, shimmer(0.5), F(a + 3), 0.22)
        for i in range(k): add(b, pop(640 + 25 * i, 0.08), F(a + 2 + i * 2.2), 0.12)
        t = a + 2 + UPD
        while t < z: add(b, beep(1760, 0.05), F(t), 0.035); t += UPD
    tap(b, T_STOP); add(b, zap(0.2, 900, 400), F(T_STOP + 1), 0.12)
    add(b, whoosh(0.4, 400, 4500), F(T_START2 + 12), 0.16)
    # break: "what it does" card, one row per beat
    add(b, whoosh(0.4, 400, 4500), F(T_EX - 8), 0.18)
    for i in range(3): add(b, pop(700 + 110 * i, 0.11), F(T_EX + i * BEAT), 0.26, 0.25 * (i - 1))
    # end card
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        add(b, beep(1046.5, 0.18), F(T_END + 50.5), 0.22); add(b, thump(0.4), F(T_END + 50.5), 0.40)
        add(b, beep(1046.5, 0.18), F(T_END + 67.5), 0.30); add(b, thump(0.4), F(T_END + 67.5), 0.60)
        for n in range(16, int((T_EX - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(BT(n)), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx_mon_full.wav', full); write('sfx_mon_light.wav', light)
if os.path.exists('song/song_buy.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_buy.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix_mon.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
