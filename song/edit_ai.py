"""Cut the Suno track to the 30 s motion on the bar grid.
Motion grid: bar = 2.25 s, bar downbeats at 0.25 + 2.25*n (features start 7.0 = bar 3).
Song grid (raw): beat P, bar b0 + 4P*n.  Song is time-stretched by k = 4P/2.25 first (inaudible, ~0.66%).
Edit (song bars -> motion):  1..10 -> 0..22.75 (intro, build, groove A)
                             24     -> 22.75   (last feature)
                             25     -> 25.00   (break -> recap)
                             27     -> 27.25   (outro groove -> end card)
                             28     -> 29.50   (final hit -> last heartbeat)"""
import numpy as np, soundfile as sf, subprocess, sys
NUDGE_B = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
OUT = sys.argv[2] if len(sys.argv) > 2 else 'song_ai.wav'

P, B0 = np.load('grid.npy')
BAR_M = 2.25
k = 4 * P / BAR_M
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'suno.wav', '-af', f'rubberband=tempo={k:.6f}:transients=crisp',
                '-ar', '48000', 'suno_st.wav'], check=True)
x, sr = sf.read('suno_st.wav')
bar_s = lambda n: (B0 + n * 4 * P) / k            # song bar n downbeat in stretched time
FEAT_BAR = 4                                      # song bar where groove A enters
off = bar_s(FEAT_BAR) - 7.0                       # stretched song time at motion 0
print('k', k, 'motion0 = song', off * k, 'raw')

DUR = 30.0; N = int(DUR * sr)
PRE = 0.012                                       # cut just before the transient
XF = 0.010                                        # crossfade length

# pieces: (song_start_stretched, motion_start, motion_end)
mb = lambda n: 0.25 + 2.25 * n                    # motion bar downbeat, n=3 -> 7.0
pieces = [
    (off, 0.0, mb(3)),                            # intro + build (song bars 1-3)
    (bar_s(12) - NUDGE_B, mb(3), mb(11)),         # second groove (song bars 12-19) under the 8 feature bars
    (bar_s(25) - 0.014, mb(11), mb(12)),
    (bar_s(27) - 0.018, mb(12), mb(13)),
    (bar_s(28) - 0.019, mb(13), DUR),
]
out = np.zeros((N, 2))
for i, (ss, m0, m1) in enumerate(pieces):
    a = m0 - (PRE if i else 0); b = min(DUR, m1 - PRE + XF) if m1 < DUR else DUR
    i0, i1 = int(a * sr), int(b * sr)
    src0 = int((ss - (m0 - a)) * sr)
    seg = x[src0: src0 + (i1 - i0)].copy()
    if len(seg) < i1 - i0:
        seg = np.vstack([seg, np.zeros((i1 - i0 - len(seg), 2))])
    n = int(XF * sr)
    w = np.linspace(0, np.pi / 2, n)
    if i:  seg[:n] *= np.sin(w)[:, None]
    if m1 < DUR: seg[-n:] *= np.cos(w)[:, None]
    out[i0:i1] += seg
# short fade at the very end
n = int(0.12 * sr); out[-n:] *= np.linspace(1, 0, n)[:, None] ** 2
sf.write(OUT, out, sr)
print('pieces (raw song sec):', [round(p[0] * k, 3) for p in pieces])
