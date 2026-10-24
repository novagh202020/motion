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
    python3 sfx_svc.py  (periodic service motion, 30 s -> sfx_svc_full.wav, mix_svc.wav)
    python3 sfx_buy.py  (pre-purchase motion, 36.75 s -> sfx_buy_full.wav, mix_buy.wav; needs song/song_buy.wav = extend.py 3)
    python3 sfx_trip.py (trip analysis motion, 41.25 s -> sfx_trip_full.wav, mix_trip.wav; needs song/song_trip.wav)
    cd song && python3 extend.py 5 song_trip.wav   # song_cut + 5 repeated groove bars (recap/end card move 11.25 s later)
    PAGE=trip_motion.html python3 render.py video silent.mp4 0 1238                # longer motions: pass the frame range
    (audio.py length: CARDIAG_DUR env, default 30; end card start: initEnd(null,{t0}))
    python3 sfx60.py    (1-minute app tour, 62.2 s -> sfx60_full.wav, mix60.wav; needs song/song_full.wav)
    cd song && python3 full.py      # -> song_full.wav: the whole track from motion 0 (no edits; breaks at bars 10 / 24, final hit 61.0 s)
    PAGE=motion60.html python3 render.py video silent.mp4 0 1866
    python3 sfx_tg.py   (Telegram channel promo, 30 s -> sfx_tg_full.wav, mix_tg.wav; song_cut.wav grid)
    python3 sfx_box.py  (what ships with CarDiag, 53.2 s -> sfx_box_full.wav, mix_box.wav; needs song/song_box.wav = song/box_cut.py)
    cd song && python3 box_cut.py   # the whole song without repeats: one groove-B phrase taken out at a phrase boundary
    python3 sfx_insp.py (technical-inspection motion, 41.25 s -> sfx_insp_full.wav, mix_insp.wav; needs song/song_trip.wav = extend.py 5)
    python3 sfx_mon.py  (live monitoring motion, 36.75 s -> sfx_mon_full.wav, mix_mon.wav; needs song/song_buy.wav = extend.py 3)
    python3 sfx_bat.py  (battery test motion -> sfx_bat_full.wav, mix_bat.wav; song ducked under the slow crank)
    ffmpeg -i silent.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-2 -c:a aac -b:a 192k out.mp4

## Files
- motion.html          Series C launch motion (8 features)
- motion60.html        1-minute app tour on the full song. Intro «عیب‌یابی هوش مصنوعی کاردیاگ / مکانیک تو جیبِت!» + fast connect, then
                       8 sections in order of importance (SEC table, on the bar grid; bar 2 of each = "what it does" card, 3 lines on the beats):
                       trip (bars 3-6: 20-min time-lapse, then the PDF report grows out of the phone, one section per beat), ECU, AI
                       troubleshooter (bars 9-11: type, analyse on the break, full answer on the drop), battery, health trend, mileage,
                       monitoring (13 sensors on eighth notes), periodic service -> recap: 8 tiles -> end card, last heartbeat on the final hit
- ai_motion.html       AI diagnosis motion (= ai_intro.html + ai_main_part.html)
- ecu_motion.html      ECU fault-finding motion: check-engine light -> plug diag -> splash, connect, Bluetooth scan,
                       connecting popup -> ECU scan finds P0420 -> clear all faults -> light off -> end card
- bat_motion.html      Battery & alternator test: "new battery, dead again?" -> slow dragging crank, battery light stays on ->
                       plug diag -> fast connect (~3 s) -> start test -> 4 steps with live voltage trace (12.6 / 10.4 / 13.1 / 12.7 V)
                       -> result: battery OK, alternator weak -> "test first, then buy" -> end card
- trip_motion.html     Trip analysis: car on the road streaming sensor data -> plug diag -> very fast connect -> trip page,
                       ECU scan finds 13 PIDs -> start trip -> 20-min time-lapse, O2/MAP/load/RPM cards pulled out of the phone with live
                       traces, long-term fuel trim climbs to +18% -> full report document grows out of the phone and scrolls through
                       every section of the app's PDF (health 78%, lean mixture, checklist, driving style, what to do) -> PDF fan -> end card (41 s)
- buy_motion.html      Pre-purchase check: seller says "it's perfect" -> plug diag -> fast connect -> ECU + trip montage (0 faults,
                       68%) -> AI troubleshooter, gold-subscription badge, "I want to buy this car" -> the AI answer grows out of
                       the phone: verdict, money issues, negotiation tip, mileage check, what the test can't see, questions for the
                       seller -> recap checklist + gold capsule -> end card (37 s)
- svc_motion.html      Periodic service: odometer climbs, forgotten oil-change note, oil lamp -> quick access -> periodic service,
                       add oil change every 5,000 km -> every 2 weeks a time-based reminder notification -> km entered with «اصلاح» (no GPS on a phone),
                       card goes green -> amber at 300 km left -> more services in the list -> end card (30 s)
- box_motion.html      What ships with CarDiag: the zip case opens -> 1. the Bluetooth diag (chips, plugs in) -> 2. the activation
                       card (foil scratched off) activates the gold plan, 72 credits, in the app -> free sections vs the two credit
                       sections -> what 72 credits mean (1 per AI use with 5 questions / per trip, 40 + 32 example) -> bronze 6 /
                       silver 24 plans (no prices) -> warranty, support, 5-day return -> compatibility -> end card (53 s)
- insp_motion.html     Technical-inspection check (redesigned look): 206 hatchback in the inspection queue, «مردود» stamp, rewind ->
                       line-art plug-in -> fast connect -> 1-2-3 step strip: ECU scan finds P0420, 20-min trip (the 206 smokes and bounces
                       down the street, O2 sensors swing together), AI troubleshooter «می‌خواهم بروم معاینه فنی» -> the inspection prediction
                       grows out of the phone (20% pass, what fails you, grey risks, to-do, what it can't see) -> after the repair the gauge
                       swings to 85% -> through the gate, «قبول» -> end card (41 s)
- mon_motion.html      Live monitoring: driver's questions -> plug diag -> fast connect -> ~1 s visible press on «مانیتورینگ خودرو» ->
                       «اسکن», 14 sensors found -> list: tick 13 on eighth notes, confirm -> «شروع خواندن»: 13 live cards refresh every
                       709 ms -> stop, «اسکن مجدد», tick 3 (battery/alternator, O2 1, O2 2) -> 3 live cards + big LIVE card -> end card (37 s)
- tg_motion.html       Telegram channel promo (@cardiagai): heartbeat line, a paper plane rides its tip and dives into the phone ->
                       channel page, one real post per bar (covers in assets/tg/) -> "what you get" card -> tap «عضو شو», bell, new-video
                       notification -> break: plane in a blue circle, «مکانیک تو جیبِت!» -> @cardiagai, CarDiag AI, cardiag.ir (30 s)
- endcard.js           shared end card: diag + phone with live link, "دیاگ رو بخر، / اشتراک طلایی هدیه بگیر" (initEnd(null,{health,t0,beats}): phone health %, start frame, heartbeat frames)
- cover*.html          Instagram / YouTube covers (cover_ecu.html = ECU post, cover_bat.html = battery post, render: python3 shot.py cover_ecu.html out.png); product_shot.html = white-background site image
- Brand rules: see project instructions (colors, Vazirmatn FD, RTL, max 5-word titles)
