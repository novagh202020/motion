"""SFX on the retimed motion. Writes sfx.wav (full, for the no-music version) and sfx_light.wav (UI layer under the song)."""
import numpy as np
from audio import (N, add, beep, thump, whoosh, tick, pop, chime, zap, shimmer, bell, norm, softclip, write)
F = lambda fr: fr / 30.0
FS = lambda k: F(210 + 67.5 * k)

def build(full):
    b = np.zeros((N, 2))
    # S1 reveal (spike on song kick at frame 24.4)
    add(b, whoosh(0.5, 300, 5000), F(9), 0.30)
    if full:
        for fr in (7.5, 41.25, 75, 91.9): add(b, thump(0.3), F(fr), 0.25)
        add(b, beep(1046.5, 0.22), F(24.4), 0.32); add(b, thump(0.5), F(24.4), 0.85)
    add(b, shimmer(0.8), F(46), 0.45)
    # S2 connection (tap on bar downbeat 142.5)
    add(b, whoosh(0.6, 250, 3000, False), F(104), 0.28)
    add(b, whoosh(0.7, 200, 2500), F(108), 0.25, 0.1)
    for fr in range(124, 196, 18): add(b, pop(1500, 0.08), F(fr), 0.10, -0.2)
    add(b, tick(), F(142.5), 0.45)
    add(b, zap(0.2), F(143), 0.30)
    add(b, chime(), F(151), 0.38)
    add(b, whoosh(0.6, 300, 4000), F(194), 0.28)
    # features
    for k in range(8):
        a = FS(k)
        if k > 0: add(b, whoosh(0.35, 500, 5000), a - 0.18, 0.20, 0.15 * (-1) ** k)
        add(b, pop(640, 0.13), a + F(9), 0.32)
        add(b, tick(3000, 0.04), a + F(3), 0.16)
    a = FS(0); add(b, tick(), a + F(4), 0.30); add(b, tick(), a + F(36), 0.30)
    add(b, whoosh(0.3, 800, 6000, False), a + F(38), 0.15); add(b, chime((1568, 2093), 0.06, 0.6), a + F(44), 0.22)
    a = FS(1)
    for i in range(8): add(b, tick(3600, 0.03), a + F(4 + i * 4.2), 0.08)
    a = FS(4)
    for i in range(14): add(b, tick(4200 + 300 * (i % 3), 0.025), a + F(2 + i * 1.6), 0.07)
    add(b, tick(), a + F(29), 0.30); add(b, chime((1318.5, 1760), 0.06, 0.5), a + F(47), 0.18)
    a = FS(5); add(b, chime((1568, 2093), 0.06, 0.6), a + F(32), 0.20)
    a = FS(6); add(b, tick(), a + F(5), 0.30); add(b, chime((1568, 2093), 0.06, 0.6), a + F(34), 0.20)
    a = FS(7); add(b, bell(1.0), a + F(30), 0.22)
    # recap
    add(b, whoosh(0.5, 300, 3500, False), F(748), 0.25)
    for k in range(8): add(b, pop(520 + 60 * k, 0.1), F(754 + k * 2.2), 0.18, 0.4 * (-1) ** k)
    add(b, whoosh(0.5, 300, 5000), F(806), 0.25)
    # end card (re-entry 817.5, final hit 885)
    if full:
        add(b, thump(0.5), F(817.5), 0.7); add(b, beep(1046.5, 0.2), F(817.5), 0.18)
        add(b, beep(1046.5, 0.18), F(868), 0.22); add(b, thump(0.4), F(868), 0.40)
        add(b, beep(1046.5, 0.18), F(885), 0.30); add(b, thump(0.4), F(885), 0.60)
    add(b, shimmer(0.9), F(846), 0.40)
    add(b, pop(900, 0.12), F(848), 0.25)
    return b

write('sfx.wav', norm(softclip(norm(build(True), -1)), -1.0))
write('sfx_light.wav', norm(build(False), -1.0))
print('ok')
