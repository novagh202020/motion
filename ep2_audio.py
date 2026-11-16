"""Episode 2 (باتری سوم) sound: narration + real CC0 SFX (sfx_cc0/, Meta Open Sound) + music.
usage: python3 ep2_audio.py NARRATION.mp3 OUT.wav      (cue times = seconds on the narration clock)"""
import sys, os, subprocess, numpy as np, soundfile as sf

SR, DUR = 48000, 68.0
N = int(SR * DUR)
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    if path.endswith('.ogg'):
        d, sr = sf.read(path, always_2d=True)
    else:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
        d, sr = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64), SR
    if d.shape[1] == 1: d = np.repeat(d, 2, 1)
    if sr != SR:
        idx = np.arange(0, len(d), sr / SR); d = np.stack([np.interp(idx, np.arange(len(d)), d[:, c]) for c in range(2)], 1)
    return d


def place(buf, sig, t, gain_db=0.0, length=None, fade=0.03, pan=0.0, start=0.0):
    s = sig[int(start * SR):].copy() * 10 ** (gain_db / 20)
    if length: s = s[: int(length * SR)]
    nf = min(max(1, int(fade * SR)), len(s) // 2)
    if nf > 1: s[-nf:] *= np.linspace(1, 0, nf)[:, None]; s[:nf] *= np.linspace(0, 1, nf)[:, None]
    if pan: s[:, 0] *= min(1, 1 - pan); s[:, 1] *= min(1, 1 + pan)
    i = int(t * SR); j = min(N, i + len(s))
    if j > i: buf[i:j] += s[: j - i]


def loop(buf, sig, t0, t1, gain_db, fade=0.4):
    n = int((t1 - t0) * SR); place(buf, np.tile(sig, (int(np.ceil(n / len(sig))) + 1, 1))[:n], t0, gain_db, fade=fade)


S = {f[:-4]: load(os.path.join(HERE, 'sfx_cc0', f)) for f in os.listdir(os.path.join(HERE, 'sfx_cc0')) if f.endswith('.ogg')}
b = np.zeros((N, 2))
CAR = S['VEHCar_CarStartRunStop_OS_02']; PAGE = S['PAPRHndl_BookPageTurns_OS_01']

# A 0-7: freezing morning, weak crank, coughs
loop(b, S['WINDVege_LightWindTreesBirds_LOOP_01'], 0.0, 7.2, -20)
place(b, S['UIClick_KeyboardTyping_OS_01'], 1.5, -14, length=.8, fade=.1)        # chattering teeth
place(b, S['VEHDoor_CarDoorOpen_OS_01'], 2.7, -10); place(b, S['VEHDoor_CarDoorClose_OS_01'], 3.0, -10)
place(b, CAR, 3.15, -8, length=1.0, fade=.15)                                     # weak crank
for t, k in ((5.4, 1), (5.87, 2), (6.33, 3)): place(b, S[f'HMNBurp_Burp_OS_0{k}'], t, -10, pan=.2)
place(b, PAGE, 6.8, -6, length=.9, fade=.15)
# B 7-12.6: sick battery
place(b, S['VOXMale_Male02Hurt_OS_01'], 7.6, -16)
place(b, S['UIClick_CasualPopsConfirm_OS_01'], 10.33, -8)
place(b, S['SWSH_Swoosh_OS_01'], 12.4, -8)
# C 12.6-19.5: battery, battery, battery
loop(b, S['WINDVege_LightWindTreesBirds_LOOP_01'], 12.6, 19.5, -26)
for t in (14.39, 17.16, 18.04):
    place(b, S['FGHTImpt_PunchRegular_OS_01'], t + .3, -16); place(b, S['OBJCoin_CoinDrop_OS_01'], t + .15, -8)
for t in (16.0, 16.95, 17.85): place(b, PAGE, t, -10, length=.45, fade=.08)
place(b, S['PAPRHndl_PaperCrumple_OS_01'], 19.1, -6, length=1.0, fade=.1); place(b, S['SWSH_Swoosh_OS_02'], 19.85, -8)
# D 19.5-31.7: the secret
place(b, S['VOXWhsp_WhispersCreepy_OS_01'], 19.7, -18, length=1.6, fade=.3)
place(b, S['MAGSpel_MagicSpell_OS_01'], 21.25, -16)                               # halo
place(b, S['WHSH_WhooshMedium_OS_03'], 23.65, -12)                               # spotlight moves
place(b, S['DSGNImpt_ImpactCreepyReverb_OS_01'], 26.06, -8)                      # "دینام!"
for t in (28.5, 29.5, 30.5, 31.1): place(b, S['UIAlert_Notification_OS_03'], t, -10)
place(b, S['SWSH_Swoosh_OS_01'], 29.9, -12)                                      # heater slides in
place(b, S['MAGSpel_MagicSpell_OS_01'], 30.7, -20)                               # hearts
place(b, S['PAPRRip_PaperTear_OS_01'], 31.5, -4)
# F 31.7-40.2: suspects
for t, k in ((33.48, 2), (34.27, 3), (35.04, 4)): place(b, S[f'TOONBoing_BounceCartoony_OS_0{k}'], t, -10)
place(b, S['VOXLaff_EvilLaugh_OS_01'], 37.0, -16)
place(b, S['WHSH_WhooshMedium_OS_03'], 38.43, -12)
place(b, S['UIAlert_Notification_OS_03'], 39.31, -8)
place(b, S['SWSH_Swoosh_OS_01'], 40.0, -8)
# G 40.2-45.8: off to buy battery #4 - blocked
for i, t in enumerate(np.arange(40.45, 43.6, 0.55)): place(b, S[f'FEETHmn_ShoeSnowWalk_OS_0{1 + i % 2}'], t, -14, length=.5, fade=.05)
place(b, S['WHSH_WhooshMedium_OS_03'], 43.15, -8); place(b, S['FGHTImpt_PunchRegular_OS_01'], 43.65, -12)
place(b, S['TOONBoing_BounceCartoony_OS_02'], 44.84, -12)
place(b, S['PAPRHndl_PaperCrumple_OS_01'], 45.4, -6, length=.9, fade=.1)
# H 45.8-54.4: CarDiag test
place(b, S['MECHSwtch_SwitchSmallOn_OS_01'], 46.0, -4); place(b, S['SWSH_Swoosh_OS_02'], 46.3, -10)
loop(b, S['UIData_ScifiCountup_LOOP_01'], 46.6, 47.5, -20, fade=.12)
place(b, S['UIMisc_Powerup_OS_01'], 47.55, -12)                                   # 12.6 V
place(b, S['UIAlert_Notification_OS_01'], 49.45, -8)                              # "سالم"
place(b, S['UIAlert_ScifiHightechError_OS_01'], 51.1, -6); place(b, S['UIAlert_CasualPopsError_OS_01'], 52.6, -8)   # weak alternator
place(b, S['MECHLock_DoorLockKey_OS_03'], 53.5, -6, length=.9, fade=.1)          # handcuffs
place(b, S['PLASImpt_PlasticObjDrop_OS_01'], 53.95, -10)
place(b, PAGE, 54.2, -6, length=.9, fade=.15)
# I 54.4-56: fixed
for t in (54.6, 55.0, 55.35): place(b, S['METLImpt_MetalHitSurface_OS_01'], t, -12, length=.4, fade=.05)
place(b, S['SWSH_Swoosh_OS_01'], 55.8, -8)
# S 56-59.5: one turn, vroom
loop(b, S['WINDVege_LightWindTreesBirds_LOOP_01'], 56.0, 59.6, -26)
place(b, CAR, 57.3, -8, length=.9, fade=.12)                                       # crank...
place(b, CAR, 58.15, -6, start=7.5, length=1.9, fade=.3)                          # ...vroom
place(b, S['MUSCStngr_VictoryOrchestral_OS_01'], 58.4, -14)
place(b, PAGE, 59.3, -6, length=.9, fade=.15)
# J 59.5-62.6: retirement bench
place(b, S['AMBForst_ForestBirds_OS_01'], 59.5, -20, length=3.0, fade=.5)
place(b, S['MUSCStngr_BanjoHumorous_OS_01'], 59.9, -14)
place(b, PAGE, 62.4, -6, length=.9, fade=.15)
# end card
place(b, S['UIMisc_BelltreeUp_OS_01'], 63.0, -12)
place(b, S['MUSCStngr_AcousticGuitarPositive_OS_01'], 63.4, -16)

nar = np.zeros((N, 2)); place(nar, load(sys.argv[1]), 0.0, 0.0, fade=.01)
music = np.zeros((N, 2)); place(music, load(os.path.join(HERE, 'song', 'suno.mp3')), 0.0, -24, fade=2.5)
w = SR // 10; e = np.sqrt(np.convolve((nar ** 2).mean(1), np.ones(w) / w, 'same'))
duck = (1 - 0.5 * np.convolve((e > 10 ** (-42 / 20)).astype(float), np.ones(w) / w, 'same'))[:, None]
m = nar + b * 10 ** (-3 / 20) * duck + music * duck
sf.write(sys.argv[2], (m / max(1.0, np.abs(m).max() / 0.95)).astype(np.float32), SR)
print('ok')
