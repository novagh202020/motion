"""Synthesize SFX + music for the 30s CarDiag Series C motion. Writes sfx.wav, music_mix.wav."""
import numpy as np, wave

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
F = lambda fr: fr / 30.0                       # frame -> seconds
FS = lambda k: F(210 + 67.5 * k)               # feature start


def env(n, a=0.005, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    dec = np.exp(-np.maximum(t - a, 0) * curve / max(d, 1e-4))
    return att * dec


def add(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * gain * l * 1.414
    buf[i:i + len(sig), 1] += sig * gain * r * 1.414


def sine(f, dur, phase=0):
    t = np.arange(int(dur * SR)) / SR
    return np.sin(2 * np.pi * f * t + phase)


def lp(x, cutoff):  # one-pole lowpass
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y


def lp_fast(x, cutoff):
    # vectorised-ish via FFT brickwall-ish soft filter
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (fr / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cutoff):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (fr / cutoff) ** 2 / np.sqrt(1 + (fr / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


# ---------------- SFX ----------------
def beep(f=1046.5, dur=0.16):
    s = sine(f, dur) * env(int(dur * SR), 0.003, dur, 5)
    s += 0.25 * sine(f * 2, dur) * env(int(dur * SR), 0.003, dur * .5, 6)
    return s


def thump(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 55 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, dur, 6)


def whoosh(dur=0.45, f0=400, f1=4000, rising=True):
    n = int(dur * SR); x = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    # sweep band by mixing lowpassed versions
    lo, hi = lp_fast(x, f0), lp_fast(x, f1)
    m = t if rising else 1 - t
    y = lo * (1 - m) + hi * m
    shape = np.sin(np.pi * t) ** 1.6
    return hp_fast(y * shape, 180) * 0.9


def tick(f=2600, dur=0.05):
    n = int(dur * SR); x = rng.standard_normal(n) * env(n, 0.0005, dur, 9)
    return hp_fast(x, 1500) * 0.6 + sine(f, dur) * env(n, 0.0005, dur, 12) * 0.5


def pop(f=700, dur=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = f * (1 + 0.8 * np.exp(-t * 40))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, 0.002, dur, 7)


def chime(notes=(1318.5, 1661.2, 1975.5), gap=0.07, dur=0.9):
    out = np.zeros(int((gap * len(notes) + dur) * SR))
    for i, f in enumerate(notes):
        s = (sine(f, dur) + 0.3 * sine(f * 2.01, dur) + 0.12 * sine(f * 3, dur)) * env(int(dur * SR), 0.004, dur, 5)
        j = int(i * gap * SR); out[j:j + len(s)] += s / 1.4
    return out


def zap(dur=0.22, f0=300, f1=2400):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    fr = f0 * (f1 / f0) ** t
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t) ** 0.8 * 0.6


def shimmer(dur=0.8):
    n = int(dur * SR); x = hp_fast(rng.standard_normal(n), 6000)
    t = np.linspace(0, 1, n)
    return x * np.sin(np.pi * t) ** 2 * 0.35


def bell(dur=1.0):
    s = np.zeros(int(dur * SR))
    for f, a in ((1568, 1), (1568 * 2.76, .35), (1568 * 5.4, .12)):
        s += a * sine(f, dur) * env(len(s), 0.002, dur, 6)
    # quick tremolo for "ring"
    t = np.arange(len(s)) / SR
    return s * (0.75 + 0.25 * np.sin(2 * np.pi * 14 * t)) * 0.5


def build_sfx():
    b = np.zeros((N, 2))
    # --- S1 reveal
    for fr in (0, 15):
        add(b, beep(880, 0.10), F(fr), 0.10)                 # faint monitor beeps on the line
    add(b, whoosh(0.5, 300, 5000), F(14), 0.30)
    add(b, beep(1046.5, 0.22), F(30), 0.32)                   # the heartbeat spike
    add(b, thump(0.5), F(30), 0.85)
    add(b, shimmer(0.8), F(52), 0.45)
    # --- S2 connection
    add(b, whoosh(0.6, 250, 3000, False), F(104), 0.28)
    add(b, whoosh(0.7, 200, 2500), F(108), 0.25, 0.1)
    for fr in range(124, 196, 18):
        add(b, pop(1500, 0.08), F(fr), 0.10, -0.2)            # BT ring blips
    add(b, tick(), F(140), 0.45)                              # tap
    add(b, zap(0.2), F(141), 0.30)                            # link shoots down (fast)
    add(b, chime(), F(150), 0.38)                             # connected
    add(b, whoosh(0.6, 300, 4000), F(194), 0.28)
    # --- features: identical cue set for every feature
    for k in range(8):
        a = FS(k)
        if k > 0:
            add(b, whoosh(0.35, 500, 5000), a - 0.18, 0.20, 0.15 * (-1) ** k)
        add(b, pop(640, 0.13), a + F(9), 0.32)                # floating card lands
        add(b, tick(3000, 0.04), a + F(3), 0.16)              # title tick
    # small in-feature details (kept quiet so the rhythm stays uniform)
    a = FS(0); add(b, tick(), a + F(4), 0.30); add(b, tick(), a + F(36), 0.30)
    add(b, whoosh(0.3, 800, 6000, False), a + F(38), 0.15); add(b, chime((1568, 2093), 0.06, 0.6), a + F(44), 0.22)
    a = FS(1)
    for i in range(8): add(b, tick(3600, 0.03), a + F(4 + i * 4.2), 0.08)
    a = FS(3)
    a = FS(4)
    for i in range(14): add(b, tick(4200 + 300 * (i % 3), 0.025), a + F(2 + i * 1.6), 0.07)
    add(b, tick(), a + F(29), 0.30); add(b, chime((1318.5, 1760), 0.06, 0.5), a + F(47), 0.18)
    a = FS(5); add(b, chime((1568, 2093), 0.06, 0.6), a + F(32), 0.20)
    a = FS(6); add(b, tick(), a + F(5), 0.30); add(b, chime((1568, 2093), 0.06, 0.6), a + F(34), 0.20)
    a = FS(7); add(b, bell(1.0), a + F(30), 0.22)
    # --- recap
    add(b, whoosh(0.5, 300, 3500, False), F(748), 0.25)
    for k in range(8): add(b, pop(520 + 60 * k, 0.1), F(754 + k * 2.2), 0.18, 0.4 * (-1) ** k)
    add(b, whoosh(0.5, 300, 5000), F(788), 0.25)
    # --- end card
    add(b, thump(0.5), F(800), 0.7); add(b, beep(1046.5, 0.2), F(800), 0.18)
    add(b, shimmer(0.9), F(830), 0.40)
    add(b, pop(900, 0.12), F(832), 0.25)
    add(b, beep(1046.5, 0.18), F(862), 0.30); add(b, thump(0.4), F(862), 0.55)
    add(b, beep(1046.5, 0.18), F(884), 0.22); add(b, thump(0.4), F(884), 0.40)
    return b


# ---------------- music ----------------
BEAT = 2.25 / 4          # 106.67 BPM, 1 bar = one feature
T0 = 0.25                # bar grid so bars land on 7.0s, 9.25s, ...
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)
# chord per bar: C  G  Am  F  (I V vi IV)
PROG = [(48, (60, 64, 67)), (43, (59, 62, 67)), (45, (60, 64, 69)), (41, (60, 65, 69))]


def saw(f, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for h in range(1, 12):
        s += ((-1) ** (h + 1)) * np.sin(2 * np.pi * f * h * t) / h
    return s * 0.6


def build_music():
    b = np.zeros((N, 2))
    nbars = int((DUR - T0) / 2.25) + 1
    for bar in range(nbars):
        t = T0 + bar * 2.25
        root, ch = PROG[bar % 4]
        sec = t
        intro = sec < 4.7; build = 4.7 <= sec < 7.0; outro = sec >= 27.0
        # pad (whole bar)
        pad = sum(saw(NOTE(m), 2.4) for m in ch)
        pad = lp_fast(pad, 1400 if intro else 2400) * env(len(pad), 0.25, 2.4, 1.2) * 0.10
        add(b, pad, t, 0.9, -0.3); add(b, pad, t + 0.012, 0.9, 0.3)
        if intro and bar == 0:
            continue
        # bass (8ths from build on)
        if not intro:
            for i in range(8 if not build else 4):
                step = 0.5 if not build else 1.0
                bt = t + i * BEAT * step
                f = NOTE(root - 12 if i % 2 == 0 else root)
                s = (sine(f, 0.26) + 0.3 * sine(f * 2, 0.26)) * env(int(0.26 * SR), 0.004, 0.26, 3)
                add(b, s, bt, 0.22)
        # pluck arpeggio 16ths-ish (8ths)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
        for i in range(8):
            if intro and i % 2: continue
            m = arp[i % 4]
            s = lp_fast(saw(NOTE(m), 0.22), 3500) * env(int(0.22 * SR), 0.002, 0.22, 7)
            add(b, s, t + i * BEAT / 2, 0.10 if not intro else 0.07, 0.35 * (-1) ** i)
        # drums
        if not intro:
            for i in range(4):
                bt = t + i * BEAT
                if not build or i % 2 == 0:
                    add(b, thump(0.3), bt, 0.55)
                if not build:
                    hh = hp_fast(rng.standard_normal(int(0.06 * SR)), 7000) * env(int(0.06 * SR), 0.001, 0.06, 8)
                    add(b, hh, bt + BEAT / 2, 0.10, 0.25)
                    if i in (1, 3):
                        sn = hp_fast(rng.standard_normal(int(0.18 * SR)), 1200) * env(int(0.18 * SR), 0.002, 0.18, 6)
                        add(b, sn, bt, 0.16)
            if build:  # riser into the feature section
                n = int(2.25 * SR); x = hp_fast(rng.standard_normal(n), 2000) * np.linspace(0, 1, n) ** 2
                add(b, x, t, 0.12)
    # final sustained chord + fade
    t = 27.25
    ch = (60, 64, 67, 72)
    pad = sum(saw(NOTE(m), 2.75) for m in ch)
    add(b, lp_fast(pad, 2600) * env(len(pad), 0.05, 2.7, 1.5) * 0.10, t, 1.0)
    fade = np.ones(N); fade[int(29.2 * SR):] = np.linspace(1, 0, N - int(29.2 * SR))
    b *= fade[:, None]
    return b


def norm(x, peak_db=-1.0):
    p = np.max(np.abs(x)) + 1e-9
    return x / p * 10 ** (peak_db / 20)


def softclip(x):
    return np.tanh(x * 1.2) / np.tanh(1.2)


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    sfx = build_sfx(); mus = build_music()
    mus = norm(mus, -1) * 0.42
    write("sfx.wav", norm(softclip(norm(sfx, -1)), -1.0))
    write("music_mix.wav", norm(softclip(mus + norm(sfx, -1) * 0.75), -1.0))
    print("ok")
