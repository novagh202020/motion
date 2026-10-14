import numpy as np
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, bell, beep, thump, norm, softclip, write, lp_fast, rng
F=lambda f:f/30
B=lambda k:210+67.5*k
T_ECU,T_TRIP,T_TXT,T_ANA,T_RES,T_RECAP,T_END=B(0),B(2),B(4),B(5),B(6),B(8),817.5
def cough(dur=0.16,mag=1.0):
    n=int(dur*SR); t=np.arange(n)/SR; return lp_fast(rng.standard_normal(n),420)*np.exp(-t*22)*mag
def sputter():
    out=np.zeros(int(0.9*SR))
    for d,a in [(0,1),(0.09,.7),(0.2,.9),(0.33,.5),(0.5,.35)]:
        c=cough(0.16,a); j=int(d*SR); out[j:j+len(c)]+=c
    return out
def build(full):
    b=np.zeros((N,2))
    # intro
    for k in (7.5,24.4,41.25,75,91.9,108.75,125.6): add(b,cough(),F(k),0.55,0.3)
    add(b,sputter(),F(56),0.9,0.3); add(b,pop(1100,0.1),F(23),0.25)
    add(b,whoosh(0.5,300,4000),F(134),0.35); add(b,whoosh(0.5,250,3000,False),F(150),0.25)
    add(b,tick(1800,0.06),F(168),0.6); add(b,pop(300,0.12),F(168),0.5); add(b,chime(),F(176),0.38)
    add(b,whoosh(0.6,200,2500),F(196),0.25)
    # steps
    add(b,tick(),F(T_ECU+6),0.35)
    for i in range(6): add(b,tick(3600,0.03),F(T_ECU+10+i*2.6),0.08)
    add(b,pop(500,0.14),F(T_ECU+25),0.30); add(b,pop(640,0.13),F(T_ECU+28),0.30)
    add(b,whoosh(0.4,500,5000),F(T_TRIP-22),0.18); add(b,pop(800,0.1),F(T_TRIP-8),0.25)
    add(b,whoosh(0.35,500,5000),F(T_TRIP)-0.18,0.20); add(b,pop(640,0.13),F(T_TRIP+32),0.30); add(b,pop(420,0.12),F(T_TRIP+42),0.22)
    add(b,whoosh(0.4,500,5000),F(T_TXT-22),0.18); add(b,pop(800,0.1),F(T_TXT-8),0.25)
    add(b,whoosh(0.35,500,5000),F(T_TXT)-0.18,0.20)
    for i in range(18): add(b,tick(4200+300*(i%3),0.025),F(T_TXT+6+i*1.7),0.07)
    add(b,tick(),F(T_TXT+44),0.35)
    add(b,whoosh(0.4,500,5000),F(T_ANA-18),0.18); add(b,pop(800,0.1),F(T_ANA-4),0.25)
    add(b,whoosh(0.5,250,3000,False),F(T_ANA-6),0.25); add(b,shimmer(0.9),F(T_ANA+4),0.35)
    for i in range(3): add(b,zap(0.18,500,2200),F(T_ANA+18+i*5),0.18); add(b,pop(700+150*i,0.1),F(T_ANA+28+i*5),0.22)
    add(b,whoosh(0.6,200,2500),F(T_RES-14),0.25); add(b,chime((1318.5,1661.2,1975.5),0.06,0.8),F(T_RES+4),0.30)
    add(b,pop(640,0.13),F(T_RES+36),0.30)
    # recap
    add(b,whoosh(0.5,300,3500,False),F(T_RECAP-2),0.25)
    for i in range(3): add(b,pop(560+80*i,0.1),F(T_RECAP+8+i*3),0.22,0.4*(i-1))
    add(b,chime((1568,2093),0.06,0.6),F(T_RECAP+32),0.22)
    # end card
    add(b,shimmer(0.9),F(846),0.40); add(b,pop(900,0.12),F(848),0.25)
    if full:
        add(b,thump(0.5),F(T_END),0.7); add(b,beep(1046.5,0.2),F(T_END),0.18)
        add(b,beep(1046.5,0.18),F(868),0.22); add(b,thump(0.4),F(868),0.40)
        add(b,beep(1046.5,0.18),F(885),0.30); add(b,thump(0.4),F(885),0.60)
        for k in (7.5,24.4,41.25,75,91.9,108.75,125.6): add(b,thump(0.3),F(k),0.3)
    return b
write('sfx_ai_full.wav',norm(softclip(norm(build(True),-1)),-1)); write('sfx_ai_light.wav',norm(build(False),-1))
