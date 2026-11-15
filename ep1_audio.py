"""Episode 1 (مهندس / misfire) sound: narration + real CC0 SFX (sfx_cc0/, Meta Open Sound) [+ music].
usage: python3 ep1_audio.py NARRATION.mp3 OUTDIR
writes OUTDIR/mix_music.wav (narration + sfx + song) and OUTDIR/mix_nomusic.wav (narration + sfx).
All cue times are seconds on the narration clock (video frame = t*30)."""
import sys, os, subprocess, numpy as np, soundfile as sf

SR = 48000
DUR = 66.0
N = int(SR * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path, gain_db=0.0):
    if path.endswith('.ogg'):
        d, sr = sf.read(path, always_2d=True)
    else:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                             capture_output=True, check=True).stdout
        d, sr = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64), SR
    if d.shape[1] == 1: d = np.repeat(d, 2, 1)
    if sr != SR:
        idx = np.arange(0, len(d), sr / SR); d = np.stack([np.interp(idx, np.arange(len(d)), d[:, c]) for c in range(2)], 1)
    return d * 10 ** (gain_db / 20)


def fx(name): return os.path.join(HERE, 'sfx_cc0', name + '.ogg')


def place(buf, sig, t, gain_db=0.0, length=None, fade=0.03, pan=0.0):
    s = sig.copy() * 10 ** (gain_db / 20)
    if length: s = s[: int(length * SR)]
    nf = max(1, int(fade * SR)); nf = min(nf, len(s) // 2)
    if nf > 1: s[-nf:] *= np.linspace(1, 0, nf)[:, None]; s[:nf] *= np.linspace(0, 1, nf)[:, None]
    if pan: s[:, 0] *= min(1, 1 - pan); s[:, 1] *= min(1, 1 + pan)
    i = int(t * SR); j = min(N, i + len(s))
    if j > i: buf[i:j] += s[: j - i]


def loop(buf, sig, t0, t1, gain_db, fade=0.4):
    n = int((t1 - t0) * SR); reps = int(np.ceil(n / len(sig))) + 1
    place(buf, np.tile(sig, (reps, 1))[:n], t0, gain_db, fade=fade)


S = {k: load(fx(k)) for k in [f[:-4] for f in os.listdir(os.path.join(HERE, 'sfx_cc0')) if f.endswith('.ogg')]}
b = np.zeros((N, 2))

# --- 0-6.2 hook: city, the car burps (misfires), "seen", typing... ghosted
loop(b, S['VEHCar_CarEngineSlow_LOOP_01'], 0.0, 3.3, -20)
place(b, S['UIClick_CasualPopsConfirm_OS_01'], 0.28, -8)                     # lamp pops up
for t, k in ((1.0, 1), (1.67, 2), (2.33, 3)): place(b, S[f'HMNBurp_Burp_OS_0{k}'], t, -9, pan=.3)
place(b, S['UIAlert_Notification_OS_03'], 1.87, -8)                          # "seen" ticks
place(b, S['WHSH_WhooshMedium_OS_03'], 3.0, -6)                              # zoom in
place(b, S['UIAlert_Notification_OS_01'], 3.53, -8)
place(b, S['UIClick_KeyboardTyping_OS_01'], 4.53, -10, length=1.0, fade=.1)  # typing...
place(b, S['UIAlert_CasualPopsError_OS_01'], 5.62, -8)                       # ...nothing
place(b, S['PAPRHndl_BookPageTurns_OS_01'], 5.8, -6, length=0.9, fade=.15)   # page peel
# --- 6.2-14.7 Mohandes: seen, shrug, months fly, the car takes revenge
loop(b, S['VEHCar_CarEngineSlow_LOOP_01'], 6.2, 13.0, -26)
place(b, S['UIAlert_Notification_OS_03'], 7.0, -9)
place(b, S['CLOTHMvmt_ClothingMovement_OS_01'], 8.0, -6)                     # shrug
for t in (9.3, 10.2, 11.15): place(b, S['PAPRHndl_BookPageTurns_OS_01'], t, -9, length=.45, fade=.08)
place(b, S['FGHTImpt_Kick_OS_02'], 13.0, -6)                                 # backfire
place(b, S['HMNBurp_Burp_OS_03'], 13.02, -4)
place(b, S['TOONBoing_BounceCartoony_OS_02'], 13.3, -8)                      # he jumps
place(b, S['PAPRHndl_PaperCrumple_OS_01'], 14.2, -6, length=1.0, fade=.1)
place(b, S['SWSH_Swoosh_OS_01'], 14.95, -8)
place(b, S['PAPRImpt_PaperBallDrop_OS_01'], 15.4, -12)
# --- 14.7-26 inside the engine: three sweat, one goes to lunch
loop(b, S['VEHCar_CarEngineHigh_LOOP_01'], 15.0, 26.0, -24)
place(b, S['SWSH_Swoosh_OS_02'], 14.95, -10)
place(b, S['VOXEfrt_Male01Effort_OS_01'], 18.2, -12); place(b, S['VOXEfrt_Male02Effort_OS_01'], 19.6, -12)
place(b, S['MECHSwtch_SwitchSmallOff_OS_01'], 21.1, -6)                      # cylinder 1 clocks out
place(b, S['UIClick_WoodConfirm_OS_01'], 23.9, -6)                           # "lunch" sign
place(b, S['MUSCStngr_BanjoHumorous_OS_01'], 24.1, -12)
place(b, S['PAPRRip_PaperTear_OS_01'], 25.8, -4)
# --- 26-35.3 suspects
for t, k in ((27.8, 2), (28.6, 3), (29.3, 4)): place(b, S[f'TOONBoing_BounceCartoony_OS_0{k}'], t, -10)
place(b, S['VOXLaff_EvilLaugh_OS_01'], 30.4, -16)                            # masks on
place(b, S['WHSH_WhooshMedium_OS_03'], 32.6, -12)
place(b, S['UIAlert_Notification_OS_03'], 33.75, -8)                         # comment!
place(b, S['SWSH_Swoosh_OS_01'], 35.1, -8)
# --- 35.3-42 catalyst kebab
place(b, S['WEAPKnif_KnifeScrape_OS_01'], 39.9, -10)                         # skewer
place(b, S['MUSCStngr_LossOrchestral_OS_01'], 41.0, -12)                     # "و تمام!"
place(b, S['TOONBoing_BounceCartoony_OS_03'], 41.2, -10)
place(b, S['PAPRHndl_PaperCrumple_OS_01'], 41.6, -8, length=.9, fade=.1)
# --- 42-45.4 Rafigh to the rescue
place(b, S['WHSH_WhooshMedium_OS_03'], 42.1, -6)
place(b, S['MUSCStngr_VictoryOrchestral_OS_01'], 42.35, -13)
place(b, S['PAPRHndl_BookPageTurns_OS_01'], 45.0, -6, length=.9, fade=.15)
# --- 45.4-54.1 CarDiag spills it
place(b, S['MECHSwtch_SwitchSmallOn_OS_01'], 45.8, -4)                       # plug in
place(b, S['SWSH_Swoosh_OS_02'], 46.0, -10)
loop(b, S['UIData_ScifiCountup_LOOP_01'], 47.0, 49.3, -20, fade=.15)         # scanning
place(b, S['VOXWhsp_WhispersCreepy_OS_01'], 47.6, -16, length=1.8, fade=.3)  # gossip
place(b, S['UIAlert_ScifiHightechError_OS_01'], 49.9, -6)                    # P0301
place(b, S['UIClick_ScifiHightechConfirm_OS_01'], 52.1, -8)
place(b, S['PLASImpt_PlasticObjDrop_OS_01'], 52.6, -10, pan=-.3); place(b, S['PLASImpt_PlasticObjDrop_OS_01'], 52.85, -12, pan=-.4)
place(b, S['SWSH_Swoosh_OS_01'], 53.9, -8)
# --- 54.1-59.6 "good boy" car
loop(b, S['VEHCar_CarEngineSlow_LOOP_01'], 54.1, 59.6, -24)
place(b, S['MAGSpel_MagicSpell_OS_01'], 55.8, -16)                          # halo
place(b, S['UIMisc_Powerup_OS_01'], 57.4, -10)
place(b, S['MUSCStngr_LevelUpMallet_OS_01'], 58.6, -14)
place(b, S['SWSH_Swoosh_OS_02'], 59.4, -8)
# --- 59.6-62 gym
place(b, S['VOXEfrt_Male02Effort_OS_01'], 60.0, -10)
place(b, S['METLImpt_MetalObjDrop_OS_02'], 61.45, -6)
place(b, S['PAPRHndl_BookPageTurns_OS_01'], 61.8, -6, length=.9, fade=.15)
# --- 62-66 end card
place(b, S['UIMisc_BelltreeUp_OS_01'], 62.5, -12)
place(b, S['MUSCStngr_AcousticGuitarPositive_OS_01'], 63.0, -16)

nar = np.zeros((N, 2)); place(nar, load(sys.argv[1]), 0.0, 0.0, fade=.01)
music = np.zeros((N, 2)); place(music, load(os.path.join(HERE, 'song', 'suno.mp3')), 0.0, -24, fade=2.0)
# duck sfx and music under the voice: 100 ms RMS envelope of the narration, 6 dB dip while it speaks
w = SR // 10; e = np.sqrt(np.convolve((nar ** 2).mean(1), np.ones(w) / w, 'same'))
act = np.convolve((e > 10 ** (-42 / 20)).astype(float), np.ones(w) / w, 'same')
duck = (1 - 0.5 * act)[:, None]
b *= 10 ** (-3 / 20) * duck; music *= duck
out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for name, m in (('mix_music', nar + b + music), ('mix_nomusic', nar + b)):
    m = m / max(1.0, np.abs(m).max() / 0.95)
    sf.write(os.path.join(out, name + '.wav'), m.astype(np.float32), SR)
print('ok')
