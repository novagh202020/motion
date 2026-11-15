"""Sound for batend_motion.html (10 s end card of the battery-test teaser). No music, only real-sounding effects.
Writes mix_batend.wav."""
import numpy as np
from audio import N, SR, add, norm, write, lp_fast, hp_fast
F = lambda f: f / 30
rng = np.random.default_rng(11)
T = lambda d: np.arange(int(d * SR)) / SR


def bandnoise(d, lo, hi): x = rng.standard_normal(int(d * SR)); return hp_fast(lp_fast(x, hi), lo)


def key():                                    # a phone keyboard tap: a short plastic click with a little body
    t = T(0.05); n = len(t)
    click = bandnoise(0.05, 1800, 6000) * np.exp(-t / 0.004)
    body = np.sin(2 * np.pi * rng.uniform(170, 230) * t) * np.exp(-t / 0.018)
    return (click * 0.9 + body * 0.35) * rng.uniform(0.75, 1.0)


def tapf():                                   # a finger tap on glass
    t = T(0.08); return bandnoise(0.08, 300, 3000) * np.exp(-t / 0.008) * 0.8 + np.sin(2 * np.pi * 140 * t) * np.exp(-t / 0.02) * 0.5


def whoosh(d, f0, f1, g=1.0):                 # moving air: noise through a sweeping band, swelling then fading
    x = rng.standard_normal(int(d * SR)); t = np.linspace(0, 1, len(x)); out = np.zeros_like(x); seg = 2048
    for i in range(0, len(x), seg):
        c = f0 + (f1 - f0) * t[i]; out[i:i + seg] = hp_fast(lp_fast(x[i:i + seg], c * 1.6), c * 0.5)
    return out * np.sin(np.pi * t) ** 1.5 * g


def ding(f=1318.5, d=1.4):                    # a struck bell: inharmonic partials, long decay
    t = T(d); s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * k) for m, a, k in ((1, 1, 3.2), (2.76, .45, 6), (5.4, .25, 10), (8.9, .12, 16)))
    return s * np.minimum(1, t / 0.002)


def boom(d=1.6):                              # a deep cinematic impact
    t = T(d); sub = np.sin(2 * np.pi * np.cumsum(60 * np.exp(-t / 0.3) + 32) / SR) * np.exp(-t / 0.7)
    return sub * 1.3 + lp_fast(rng.standard_normal(len(t)), 250) * np.exp(-t / 0.25) * 1.6 + bandnoise(d, 2000, 8000) * np.exp(-t / 0.03) * 0.4


b = np.zeros((N, 2))
# battery: power-on thunk, then a rising electric charge with crackle, a relay click and a ding when full
t = T(0.12); add(b, np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.05) + bandnoise(0.12, 800, 4000) * np.exp(-t / 0.006), 0, 0.8)
d = F(40 - 8); t = T(d); u = t / d
hum = sum(np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.6 * u ** 1.4)) / SR * h) / h for f0 in (100,) for h in (1, 2, 3, 5))
crk = bandnoise(d, 2500, 9000) * (rng.random(len(t)) < 0.002 + 0.01 * u).astype(float)
add(b, (hum * 0.35 * (0.3 + 0.7 * u) + crk * 0.8) * np.minimum(1, t / 0.05), F(8), 0.8)
t = T(0.04); add(b, bandnoise(0.04, 1500, 7000) * np.exp(-t / 0.004), F(40), 0.9)
add(b, ding(1567.98), F(41), 0.5)
add(b, whoosh(0.7, 300, 3000), F(46), 0.9)                                   # the battery opens into the scene
add(b, whoosh(0.5, 2500, 500, 0.6), F(55), 0.6)                              # diag and phone land
add(b, tapf(), F(88), 0.8); add(b, ding(2093, 0.5), F(89), 0.15)              # the battery tile lights
add(b, whoosh(0.6, 400, 2500), F(146), 0.7)                                  # the comment sheet slides up
for k in range(17): add(b, key(), F(164 + k * 36 / 17 + rng.uniform(-0.5, 0.5)), 0.75, rng.uniform(-.2, .2))
add(b, tapf(), F(206), 0.8); add(b, whoosh(0.35, 800, 5000, 0.8), F(207), 0.6)  # send
add(b, ding(1318.5, 1.0), F(220), 0.35); add(b, ding(1760, 0.8), F(223), 0.25)  # the reply notification
add(b, whoosh(0.6, 300, 3000), F(232), 0.7)                                  # to the site
for k in range(10): add(b, key(), F(250 + k * 22 / 10 + rng.uniform(-0.5, 0.5)), 0.75, rng.uniform(-.2, .2))
add(b, boom(), F(276), 1.0); add(b, ding(1046.5, 2.0) * 0.6 + ding(1567.98, 2.0) * 0.4, F(277), 0.25)
write('mix_batend.wav', norm(b, -1)); print('ok')
