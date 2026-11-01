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
T_SNAP, T_BOOM, T_DARK, T_BEAT, T_FLAT, T_DEATH, T_REMIX, T_LIGHT = 90, 100, 118, (132, 152), 170, 176, MB(2), MB(3)
T_S1, T_S2, T_S3, T_S4, T_S5, T_CTA, T_END = MB(4), MB(6), MB(9), MB(12), MB(14), MB(16), MB(18)
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
# --- spin-up: engine climbs; the belt squeals, flaps faster and groans as it stretches (loud: this is the story)
n = int(F(T_SNAP) * SR); t = np.arange(n) / SR; u = t / t[-1]
f_eng = 42 + 30 * u ** 2; ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (0.55 * np.sin(ph) + 0.3 * np.sin(2 * ph + .4) + 0.2 * np.sin(3 * ph)) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
eng += 0.25 * lp_fast(rng.standard_normal(n), 700)
add(b, eng * np.minimum(1, t / 0.4) * 0.35, 0, 0.5)
ramp = seg = np.clip((t - F(36)) / (F(T_SNAP) - F(36)), 0, 1)
f_sq = 1900 + 900 * ramp ** 1.5 + 140 * np.sin(2 * np.pi * 13 * t)                       # rubber squeal: wobbling, rising
squeal = np.sin(2 * np.pi * np.cumsum(f_sq) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f_sq * 1.51) / SR)
squeal += 0.8 * hp_fast(lp_fast(rng.standard_normal(n), 4200), 1800)
squeal *= (0.15 + ramp ** 1.3) * (0.75 + 0.25 * np.sin(2 * np.pi * 23 * t))
add(b, squeal * 0.55, 0, 1.0)
groan = np.sin(2 * np.pi * np.cumsum(110 - 45 * ramp) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t)) * ramp ** 1.2   # the belt stretching
add(b, groan * 0.7, 0, 1.0)
tt = 46.0
while tt < T_SNAP - 1:                                                                  # flapping: thwap-thwap, faster and harder
    k = (tt - 46) / (T_SNAP - 46); nb_ = int(0.06 * SR)
    th = lp_fast(rng.standard_normal(nb_), 900) * np.exp(-np.arange(nb_) / (0.012 * SR))
    add(b, th, F(tt), 0.5 + 0.9 * k, rng.uniform(-.3, .3)); tt += max(1.6, 5.5 - 4.5 * k)
tt = 40.0
while tt < T_SNAP: add(b, tick(900 + rng.integers(0, 900), 0.02), F(tt), 0.1 + 0.25 * (tt - 40) / 50, rng.uniform(-.6, .6)); tt += max(1.0, 6 - (tt - 40) / 10)
add(b, pop(260, 0.18), F(58), 0.5); add(b, pop(200, 0.16), F(63), 0.4)                      # the car gulps
# --- the snap: very loud whip crack, a ringing ping, a rubber twang
nn = int(0.35 * SR); whip = rng.standard_normal(nn) * np.exp(-np.arange(nn) / (0.035 * SR))
add(b, whip * 1.6, F(T_SNAP), 1.0); add(b, metal(1830, 0.9), F(T_SNAP), 0.8); add(b, thump(0.6), F(T_SNAP), 1.0)
nt = int(0.5 * SR); tw_ = np.arange(nt) / SR; twang = np.sin(2 * np.pi * np.cumsum(220 * np.exp(-tw_ / 0.12) + 70) / SR) * np.exp(-tw_ / 0.18)
add(b, twang, F(T_SNAP), 0.9)
# --- free-running overspeed + grinding between snap and boom
n = int(F(T_BOOM - T_SNAP) * SR); t = np.arange(n) / SR; u = t / t[-1]
grind = hp_fast(rng.standard_normal(n), 1500) * (0.2 + 0.8 * u ** 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 37 * t))
over = np.sin(2 * np.pi * np.cumsum(2600 + 1600 * u ** 2) / SR) * 0.4 * u
add(b, grind * 0.45 + over * 0.35, F(T_SNAP + 1), 0.9)

# --- horror score under the hook (0 .. the snap): drone, a dissonant tremolo cluster, a speeding heartbeat kick,
#     a riser and «braam» hits; it cuts dead at the snap
hz = np.zeros((N, 2)); n = int(F(T_SNAP) * SR); t = np.arange(n) / SR; u = t / t[-1]
def sawp(fr):                                                                            # band-limited-ish saw from a frequency curve
    ph = 2 * np.pi * np.cumsum(fr) / SR; return sum(((-1) ** (h + 1)) * np.sin(h * ph) / h for h in range(1, 9))
drone = sawp(np.full(n, 49.0)) + sawp(np.full(n, 49.4)) + 0.8 * sawp(np.full(n, 69.3))       # G1 against D♭2 (tritone)
drone = lp_fast(drone, 320) * (0.5 + 0.5 * u)
clus = sum(np.sin(2 * np.pi * fq * t + k) for k, fq in enumerate((196.0, 207.65, 277.18, 293.66, 415.3)))  # G3 A♭3 D♭4 D4 A♭4
clus *= (0.55 + 0.45 * np.sin(2 * np.pi * (6 + 6 * u) * t)) * u ** 1.4                    # tremolo speeds up as it swells
riser = sawp(200 + 1300 * u ** 2) * u ** 2.2; riser = lp_fast(riser, 3500)
screech = np.sin(2 * np.pi * np.cumsum(1400 + 900 * u ** 3 + 30 * np.sin(2 * np.pi * 7 * t)) / SR) * np.clip((u - 0.55) / 0.45, 0, 1) ** 2
bed = drone * 0.9 + clus * 0.35 + riser * 0.35 + screech * 0.25
bed[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
add(hz, bed, 0, 1.0)
tt = 6.0
while tt < T_SNAP - 2:                                                                  # heartbeat kick: lub-dub, faster and faster
    k = tt / T_SNAP; add(hz, thump(0.35), F(tt), 0.9); add(hz, thump(0.25), F(tt + 6 - 3 * k), 0.6); tt += max(9, 26 - 18 * k)
for t0, g in ((0, 1.0), (44, 1.0)):                                                      # braams
    nb_ = int(1.8 * SR); tb_ = np.arange(nb_) / SR
    br = (sawp(np.full(nb_, 49.0)) + sawp(np.full(nb_, 98.0)) + 0.7 * sawp(np.full(nb_, 146.8)) + 0.6 * sawp(np.full(nb_, 138.6)))
    br = lp_fast(br, 900) * np.minimum(1, tb_ / 0.04) * np.exp(-tb_ / 0.9)
    add(hz, br, F(t0), g)
nr = int(F(T_SNAP - 60) * SR); rv = lp_fast(rng.standard_normal(nr), 6000) * np.linspace(0, 1, nr) ** 3   # reverse-cymbal swell into the snap
add(hz, rv, F(60), 0.6)
# --- the gears let go: a bomb, not a crack. A dull impact, a long sub boom falling in pitch, a rolling rumble;
#     the metal is low and quiet underneath
nb = int(3.2 * SR); tb = np.arange(nb) / SR
hit = lp_fast(rng.standard_normal(nb), 600) * np.exp(-tb / 0.05) * 2.2                     # the punch
sub = np.sin(2 * np.pi * np.cumsum(55 * np.exp(-tb / 0.35) + 24) / SR) * np.minimum(1, tb / 0.006) * np.exp(-tb / 1.1)
rumble = lp_fast(rng.standard_normal(nb), 140) * np.exp(-tb / 1.0) * 4.0
rumble *= 0.7 + 0.3 * np.sin(2 * np.pi * 3 * tb)
body = lp_fast(rng.standard_normal(nb), 320) * np.exp(-tb / 0.35) * 2.5
add(b, (hit + 2.2 * sub + rumble + body) * 1.6, F(T_BOOM), 1.0)
add(b, thump(0.8), F(T_BOOM), 1.0)
for k in range(10):
    add(b, lp_fast(metal(rng.uniform(250, 700), rng.uniform(0.2, 0.4)), 1500), F(T_BOOM + rng.uniform(2, 16)), rng.uniform(0.08, 0.16), rng.uniform(-.8, .8))
for k in range(14):
    nd = int(0.05 * SR); add(b, lp_fast(rng.standard_normal(nd), 900) * np.exp(-np.arange(nd) / (0.01 * SR)), F(T_BOOM + 10 + rng.uniform(0, 26)), rng.uniform(0.1, 0.25), rng.uniform(-.9, .9))
# --- heart monitor: two beeps, then flat on D6 until the remix bar
for t0 in T_BEAT: add(b, tone(D6, 0.13), F(t0 + 1), 0.5)
flat = tone(D6, F(T_REMIX - T_FLAT), a=0.004, r=0.003); add(b, flat, F(T_FLAT + 2), 0.45)
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
add(b, pop(900, 0.12), F(T_S5 + 20), 0.26); add(b, tick(2400, 0.05), F(T_S5 + 70), 0.35)        # robot's bubble, the wink
for i in range(2): add(b, pop(820 + 120 * i, 0.12), F(T_S5 + 40 + i * 14), 0.24)
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
# effects up front: compress the layer so the quiet UI sounds come up, then a low boost for weight
def punch(x, drive=3.0, bass=1.0):
    y = np.tanh(x * drive) / np.tanh(drive)
    return y + bass * np.stack([lp_fast(y[:, c], 160) for c in range(2)], 1)
cut = int(F(T_LIGHT - 8) * SR)
hk = b.copy(); hk[cut:] = 0; ui = b.copy(); ui[:cut] = 0                              # the hook and the UI get their own levels
hk = norm(punch(norm(hk, -1), 3.0, 1.1), -1); ui = norm(punch(norm(ui, -1), 4.0, 1.2), -1)
hz = norm(punch(norm(hz, -1), 1.8, 0.8), -1)
mix = norm(mus, -1) * 0.7 + hk * 1.0 + ui * 0.85 + hz * 0.9
write('mix_maint.wav', norm(softclip(mix), -1)); print('ok')
