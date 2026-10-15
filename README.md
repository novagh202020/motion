# CarDiag motion toolkit

Brand motion series for CarDiag (1080x1920, 30fps, 30 s). Every motion is an HTML page rendered frame-by-frame.

## Render
    pip install --break-system-packages playwright librosa soundfile
    PAGE=ai_motion.html python3 render.py frames 0,210,900 kf      # keyframes
    PAGE=ai_motion.html python3 render.py video silent.mp4         # 900 frames, H.264 CRF16

## Music (Suno track "CarDiag Pulse", song/suno.mp3, ~106 BPM)
    cd song && ffmpeg -i suno.mp3 -ac 2 -ar 48000 suno.wav
    python3 edit.py                 # -> song_cut.wav (Series C cut: groove A)
    python3 edit_ai.py 0.005        # -> song_ai.wav (AI cut: groove B)
Song is time-stretched 0.66% so 1 bar = 2.25 s = 67.5 frames. Groove downbeat at frame 210 (7.0 s);
feature k starts at frame 210 + 67.5*k; recap at 750; end card at 817.5; last heartbeat at 885.

## SFX / mux
    python3 sfx2.py   (Series C)  |  python3 sfx_ai.py  (AI motion)  |  python3 sfx_ecu.py  (ECU motion; needs song/song_cut.wav for mix_ecu.wav)
    python3 sfx_bat.py  (battery test motion -> sfx_bat_full.wav, mix_bat.wav; song ducked under the slow crank)
    ffmpeg -i silent.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-2 -c:a aac -b:a 192k out.mp4

## Files
- motion.html          Series C launch motion (8 features)
- ai_motion.html       AI diagnosis motion (= ai_intro.html + ai_main_part.html)
- ecu_motion.html      ECU fault-finding motion: check-engine light -> plug diag -> splash, connect, Bluetooth scan,
                       connecting popup -> ECU scan finds P0420 -> clear all faults -> light off -> end card
- bat_motion.html      Battery & alternator test: "new battery, dead again?" -> slow dragging crank, battery light stays on ->
                       plug diag -> fast connect (~3 s) -> start test -> 4 steps with live voltage trace (12.6 / 10.4 / 13.1 / 12.7 V)
                       -> result: battery OK, alternator weak -> "test first, then buy" -> end card
- endcard.js           shared end card: diag + phone with live link, "دیاگ رو بخر، / اشتراک طلایی هدیه بگیر" (initEnd(null,{health}) sets the phone's health %)
- cover*.html          Instagram / YouTube covers (cover_ecu.html = ECU post, render: python3 shot.py cover_ecu.html out.png); product_shot.html = white-background site image
- Brand rules: see project instructions (colors, Vazirmatn FD, RTL, max 5-word titles)
