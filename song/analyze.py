import librosa, numpy as np
y, sr = librosa.load('suno.wav', sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time', tightness=200)
print('tempo', tempo)
bt = np.array(beats); ibi = np.diff(bt)
print('median IBI', np.median(ibi), '-> bpm', 60/np.median(ibi), 'nbeats', len(bt))
print('first beats', np.round(bt[:24],3))
# RMS per 0.5s
hop=512; rms=librosa.feature.rms(y=y,hop_length=hop)[0]; t=librosa.frames_to_time(np.arange(len(rms)),sr=sr,hop_length=hop)
for a in np.arange(0,65,1.0):
    m=(t>=a)&(t<a+1); print(f'{a:4.0f}s rms {rms[m].mean():.3f}', end=' | ' if int(a)%4!=3 else '\n')
# onset strength + low-band (kick) energy
S=np.abs(librosa.stft(y,hop_length=hop)); f=librosa.fft_frequencies(sr=sr)
low=S[f<150].sum(0); low/=low.max()
np.save('low.npy',low); np.save('t.npy',t); np.save('beats.npy',bt)
