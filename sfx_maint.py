"""Sound for maint_motion.html (service reminder on the car's Android monitor, 47 s). Writes mix_maint.wav.
Hook (no music): the engine spins up, the timing belt squeals and snaps, the gears shatter and blow apart, then a heart
monitor beeps twice and goes flat on a D (the song is in G). One bar before the light comes back the flat tone is remixed:
it is chopped on the 16ths into a G-major arpeggio while the song's last intro bar opens up under it, and the groove
lands on the reveal. The song (song/song_travel.wav) is delayed by D frames so its bars line up with the motion."""
import numpy as np, soundfile as sf
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, beep, thump, norm, softclip, write, lp_fast, hp_fast
F = lambda f: f / 30
D = 90
MB = lambda m: 7.5 + 67.5 * m + D
BEAT = 16.875
T_SNAP, T_BOOM, T_DARK, T_BEAT, T_FLAT, T_REMIX, T_LIGHT = 80, 94, 118, (132, 152), 170, MB(2), MB(3)
T_S1, T_S2, T_S3, T_S4, T_S5, T_CTA, T_END = MB(4), MB(6), MB(9), MB(12), MB(15), MB(16), MB(18)
T_NAME, T_KM, T_SAVE1 = (T_S1 + 18, T_S1 + 46), (T_S1 + 76, T_S1 + 100), T_S1 + 112
T_ADD, T_DLG, T_DROP, T_PICK, T_INT, T_SAVE2, T_CARD1, T_CARD2 = T_S2 + 12, T_S2 + 16, T_S2 + 36, T_S2 + 62, (T_S2 + 78, T_S2 + 100), T_S2 + 118, T_S2 + 126, T_S2 + 168
T_GPS, T_DRIVE, T_NOTI = T_S3 + 22, (T_S3 + 64, T_S3 + 182), T_S4 + 4
G5, B5, D6, G6 = 783.99, 987.77, 1174.66, 1567.98
rng = np.random.default_rng(7)


def tap(b, t, g=0.35): add(b, tick(), F(t), g)


def typing(b, a, z, g=0.12):
    t = a
    while t < z: add(b, tick(4200, 0.02), F(t), g); t += 2.6


def tone(f, dur, a=0.004, r=0.01):           # the monitor's beep: a sine with a little odd harmonic, hard edges
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 3 * f * t)
    e = np.minimum(1, np.minimum(t / a, (dur - t) / r)); return x * np.clip(e, 0, 1)


def metal(f0, dur):                           # a struck piece of metal: inharmonic partials, fast decay
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for k, (m, g) in enumerate(((1, 1), (2.76, .6), (5.4, .4), (8.9, .25))):
        x += g * np.sin(2 * np.pi * f0 * m * t + k) * np.exp(-t * (6 + 4 * k))
    return x * np.exp(-t * 3)


b = np.zeros((N, 2))
# --- spin-up: engine pitch and belt whine climb, rattles get denser
n = int(F(T_SNAP) * SR); t = np.arange(n) / SR; u = t / t[-1]
f_eng = 42 + 30 * u ** 2; ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (0.55 * np.sin(ph) + 0.3 * np.sin(2 * ph + .4) + 0.2 * np.sin(3 * ph)) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
eng += 0.25 * lp_fast(rng.standard_normal(n), 700)
f_wh = 1500 + 1100 * u ** 2; whine = np.sin(2 * np.pi * np.cumsum(f_wh) / SR) * (0.05 + 0.5 * u ** 3) * (0.8 + 0.2 * np.sin(2 * np.pi * 23 * t))
add(b, (eng * np.minimum(1, t / 0.4) + whine) * 0.6, 0, 0.5)
tt = 30.0
while tt < T_SNAP: add(b, tick(900 + rng.integers(0, 900), 0.02), F(tt), 0.08 + 0.2 * (tt - 30) / 50, rng.uniform(-.6, .6)); tt += max(1.0, 6 - (tt - 30) / 10)
# --- the snap: a whip crack and a ringing ping
nn = int(0.3 * SR); whip = rng.standard_normal(nn) * np.exp(-np.arange(nn) / (0.03 * SR))
add(b, whip, F(T_SNAP), 0.9); add(b, metal(1830, 0.7), F(T_SNAP), 0.5); add(b, thump(0.5), F(T_SNAP), 0.8)
# --- free-running overspeed + grinding between snap and boom
n = int(F(T_BOOM - T_SNAP) * SR); t = np.arange(n) / SR; u = t / t[-1]
grind = hp_fast(rng.standard_normal(n), 1500) * (0.2 + 0.8 * u ** 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 37 * t))
over = np.sin(2 * np.pi * np.cumsum(2600 + 1600 * u ** 2) / SR) * 0.4 * u
add(b, grind * 0.35 + over * 0.3, F(T_SNAP + 1), 0.8)
# --- the gears let go: boom, sub drop, a shower of metal, debris tinkles
nb = int(2.4 * SR); tb = np.arange(nb) / SR
boom = lp_fast(rng.standard_normal(nb), 380) * np.exp(-tb / 0.55) * 3
sub = np.sin(2 * np.pi * np.cumsum(70 * np.exp(-tb / 0.5) + 28) / SR) * np.exp(-tb / 0.8)
add(b, boom + 1.2 * sub, F(T_BOOM), 1.0); add(b, zap(0.4, 3000, 120), F(T_BOOM), 0.4)
for k in range(26):
    add(b, metal(rng.uniform(700, 3400), rng.uniform(0.15, 0.45)), F(T_BOOM + rng.uniform(0, 18)), rng.uniform(0.15, 0.4), rng.uniform(-.8, .8))
for k in range(30):
    add(b, tick(rng.uniform(3000, 7000), 0.02), F(T_BOOM + 8 + rng.uniform(0, 26)), rng.uniform(0.04, 0.12), rng.uniform(-.9, .9))
# --- heart monitor: two beeps, then flat on D6 until the remix bar
for t0 in T_BEAT: add(b, tone(D6, 0.13), F(t0 + 1), 0.32)
flat = tone(D6, F(T_REMIX - T_FLAT), a=0.004, r=0.003); add(b, flat, F(T_FLAT + 2), 0.30)
# --- the remix bar: the flat tone chopped on the 16ths, climbing a G-major arpeggio, song opening underneath
pat = [D6, D6, D6, D6, G5, B5, D6, G6, G5, B5, D6, G6, B5, D6, G6, D6 * 2]
for i, fq in enumerate(pat):
    st = T_REMIX + i * BEAT / 4; gate = 0.12 - 0.04 * (i / 16)
    add(b, tone(fq, gate, 0.003, 0.02), F(st), 0.30 - 0.1 * (i / 16), 0.25 * np.sin(i * 1.3))
add(b, whoosh(F(T_LIGHT - T_REMIX - 30) + 0.4, 300, 6000), F(T_LIGHT - 40), 0.4)
add(b, thump(0.6), F(T_LIGHT), 0.7); add(b, shimmer(1.2), F(T_LIGHT + 2), 0.35)
# --- the rest of the motion
for i in range(2): add(b, pop(820 + 120 * i, 0.12), F(T_LIGHT + 24 + i * 16), 0.24)
typing(b, *T_NAME); typing(b, *T_KM); tap(b, T_SAVE1); add(b, whoosh(0.3, 600, 5000), F(T_SAVE1 + 4), 0.12)
tap(b, T_ADD); add(b, pop(640, 0.12), F(T_DLG), 0.22); tap(b, T_DROP); tap(b, T_PICK); typing(b, *T_INT)
tap(b, T_SAVE2); add(b, pop(900, 0.12), F(T_CARD1), 0.26); add(b, pop(980, 0.12), F(T_CARD2), 0.26)
tap(b, T_GPS); add(b, chime((1568, 2093), 0.05, 0.5), F(T_GPS + 4), 0.2)
tt = T_DRIVE[0]
while tt < T_DRIVE[1]: add(b, tick(3000, 0.02), F(tt), 0.04); tt += 4
add(b, beep(659.3, 0.18), F(T_DRIVE[1] - 20), 0.14)
add(b, chime((1046.5, 1318.5, 1568), 0.09, 1.0), F(T_NOTI), 0.38); add(b, chime((1046.5, 1318.5, 1568), 0.09, 1.0), F(T_NOTI + 60), 0.2)
add(b, whoosh(0.5, 300, 5000), F(T_S5 - 4), 0.26)
for i in range(2): add(b, pop(820 + 120 * i, 0.12), F(T_S5 + 12 + i * 16), 0.24)
add(b, whoosh(0.5, 3000, 300, False), F(T_CTA - 4), 0.22); typing(b, T_CTA + 16, T_CTA + 44, 0.14)
tap(b, T_CTA + 54, 0.4); add(b, pop(900, 0.12), F(T_CTA + 56), 0.24); add(b, chime((1568, 2093), 0.05, 0.5), F(T_CTA + 70), 0.26)
add(b, shimmer(0.9), F(T_END + 6), 0.36)
fx = norm(b, -1)

# --- the song, delayed by D; silent through the hook, its last intro bar opens up from a low-pass under the remix
song, sr = sf.read('song/song_travel.wav'); off = int(F(D) * SR)
mus = np.zeros((N, 2)); m = min(N - off, len(song)); mus[off:off + m] = song[:m]
i0, i1 = int(F(T_REMIX) * SR), int(F(T_LIGHT) * SR)
seg_ = mus[i0:i1].copy(); low = np.stack([lp_fast(seg_[:, c], 350) for c in range(2)], 1)
w = np.linspace(0, 1, i1 - i0) ** 2
mus[i0:i1] = (low * (1 - w)[:, None] + seg_ * w[:, None]) * np.linspace(0.25, 1, i1 - i0)[:, None]
mus[:i0] = 0
mix = norm(mus, -1) * 0.95 + fx * 0.6
write('mix_maint.wav', norm(softclip(mix), -1)); print('ok')
