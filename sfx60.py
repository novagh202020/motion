"""SFX + mixes for motion60.html (1-minute app tour, 10 sections x 2 bars, 62.2 s). Writes sfx60_full.wav (no-music
version), sfx60_light.wav (UI layer) and, if song/song_full.wav exists (song/full.py), mix60.wav (song + UI layer)."""
import numpy as np, os
os.environ.setdefault("CARDIAG_DUR", "62.2")
from audio import N, SR, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write
F = lambda fr: fr / 30.0
HALF, BEAT = 67.5, 16.875
FS = lambda k: 210 + 135 * k                      # section start frame (bar downbeat)
T_RECAP = FS(10); T_END = T_RECAP + 135; F_HIT = T_END + 135
io = lambda t: 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def inv_io(y):                                    # t with io(t) = y (bisection)
    a, b = 0.0, 1.0
    for _ in range(30):
        m = (a + b) / 2; a, b = (m, b) if io(m) < y else (a, m)
    return a


def build(full):
    b = np.zeros((N, 2))
    # intro: reveal + connect (same as the 30 s launch)
    add(b, whoosh(0.5, 300, 5000), F(9), 0.30)
    if full:
        for fr in (7.5, 41.25, 75, 91.9): add(b, thump(0.3), F(fr), 0.25)
        add(b, beep(1046.5, 0.22), F(24.4), 0.32); add(b, thump(0.5), F(24.4), 0.85)
    add(b, shimmer(0.8), F(46), 0.45)
    add(b, whoosh(0.6, 250, 3000, False), F(104), 0.28)
    add(b, whoosh(0.7, 200, 2500), F(108), 0.25, 0.1)
    for fr in range(124, 196, 18): add(b, pop(1500, 0.08), F(fr), 0.10, -0.2)
    add(b, tick(), F(142.5), 0.45); add(b, zap(0.2), F(143), 0.30); add(b, chime(), F(151), 0.38)
    add(b, whoosh(0.6, 300, 4000), F(194), 0.28)
    # sections: bar 1 = screen (+ floating card), bar 2 = "what it does" card, one row per beat
    for k in range(10):
        a = F(FS(k))
        if k > 0: add(b, whoosh(0.35, 500, 5000), a - 0.18, 0.20, 0.15 * (-1) ** k)
        add(b, pop(640, 0.13), a + F(9), 0.32); add(b, tick(3000, 0.04), a + F(3), 0.16)
        add(b, whoosh(0.4, 400, 4500), a + F(HALF - 8), 0.16, -0.15 * (-1) ** k)
        for i in range(3): add(b, pop(700 + 110 * i, 0.11), a + F(HALF + i * BEAT), 0.26, 0.25 * (i - 1))
    a = F(FS(0)); add(b, tick(), a + F(4), 0.30); add(b, tick(), a + F(36), 0.30)
    add(b, whoosh(0.3, 800, 6000, False), a + F(38), 0.15); add(b, chime((1568, 2093), 0.06, 0.6), a + F(44), 0.22)
    a = F(FS(1))
    for i in range(8): add(b, tick(3600, 0.03), a + F(4 + i * 4.2), 0.08)
    a = F(FS(4))
    for i in range(14): add(b, tick(4200 + 300 * (i % 3), 0.025), a + F(2 + i * 1.6), 0.07)
    add(b, tick(), a + F(29), 0.30); add(b, chime((1318.5, 1760), 0.06, 0.5), a + F(47), 0.18)
    a = F(FS(5)); add(b, chime((1568, 2093), 0.06, 0.6), a + F(32), 0.20)
    a = F(FS(6)); add(b, tick(), a + F(5), 0.30); add(b, chime((1568, 2093), 0.06, 0.6), a + F(34), 0.20)
    a = F(FS(7)); add(b, bell(1.0), a + F(30), 0.22)
    a = F(FS(8))                                   # health trend: one tick per scan point, rising
    for i in range(6): add(b, beep(880 * 2 ** (i / 12 * 2), 0.09), a + F(6 + 38 * inv_io(i / 5)), 0.08)
    add(b, chime((1568, 2093), 0.06, 0.6), a + F(44), 0.22)
    a = F(FS(9))                                   # pre-purchase: gold badge, question, typing, verdict
    add(b, shimmer(0.6), a + F(2), 0.28); add(b, chime((1975.5, 2637), 0.05, 0.6), a + F(4), 0.16)
    add(b, pop(900, 0.1), a + F(5), 0.2)
    for i in range(4): add(b, tick(2400 + 300 * (i % 3), 0.03), a + F(14 + i * 3), 0.06)
    for i in range(5): add(b, tick(3000, 0.04), a + F(26 + i * 7), 0.12)
    # recap: one tile per eighth note, both break beats flash
    add(b, whoosh(0.5, 300, 3500, False), F(T_RECAP - 4), 0.25)
    for k in range(12): add(b, pop(520 + 45 * k, 0.1), F(T_RECAP + 4 + k * BEAT / 2), 0.17, 0.4 * (-1) ** k)
    for n in (2, 3): add(b, shimmer(0.4), F(T_RECAP + HALF + n * BEAT), 0.18)
    add(b, whoosh(0.5, 300, 5000), F(T_END - 11), 0.25)
    # end card on the outro, last heartbeat on the song's final hit
    add(b, shimmer(0.9), F(T_END + 28.5), 0.40); add(b, pop(900, 0.12), F(T_END + 30.5), 0.25)
    if full:
        add(b, thump(0.5), F(T_END), 0.7); add(b, beep(1046.5, 0.2), F(T_END), 0.18)
        for fr, g in ((T_END + 50.5, .6), (T_END + 67.5, 1), (F_HIT - 17, .6), (F_HIT, 1)):
            add(b, beep(1046.5, 0.18), F(fr), 0.22 + 0.08 * g); add(b, thump(0.4), F(fr), 0.4 * g + 0.2 * (g == 1))
        for n in range(0, int((T_RECAP - 210) / BEAT) + 1, 4): add(b, thump(0.25), F(210 + BEAT * n), 0.16)
    return b


full, light = norm(softclip(norm(build(True), -1)), -1), norm(build(False), -1)
write('sfx60_full.wav', full); write('sfx60_light.wav', light)
if os.path.exists('song/song_full.wav'):
    import soundfile as sf
    song, sr = sf.read('song/song_full.wav'); song = song[:N]
    if len(song) < N: song = np.vstack([song, np.zeros((N - len(song), 2))])
    write('mix60.wav', norm(softclip(norm(song, -1) + light * 0.55), -1))
print('ok')
