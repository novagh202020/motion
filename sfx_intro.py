import numpy as np
from audio import N, SR, add, whoosh, tick, pop, chime, zap, shimmer, norm, write, lp_fast, hp_fast, rng, env
F=lambda f:f/30
def cough(dur=0.18, mag=1.0):
    n=int(dur*SR); t=np.arange(n)/SR
    x=lp_fast(rng.standard_normal(n),420)*np.exp(-t*22)
    return x*mag
def sputter():
    out=np.zeros(int(0.9*SR))
    for i,(d,a) in enumerate([(0,1),(0.09,.7),(0.2,.9),(0.33,.5),(0.5,.35)]):
        c=cough(0.16,a); j=int(d*SR); out[j:j+len(c)]+=c
    return out
b=np.zeros((N,2))
for k in (7.5,24.4,41.25,75,91.9,108.75,125.6): add(b,cough(0.16),F(k),0.55,0.3)
add(b,sputter(),F(56),0.9,0.3)                       # stall on the missing beat
add(b,pop(1100,0.1),F(23),0.25)                     # check-engine badge
add(b,whoosh(0.5,300,4000),F(134),0.35)             # push-in
add(b,whoosh(0.5,250,3000,False),F(150),0.25)
add(b,tick(1800,0.06),F(168),0.6); add(b,pop(300,0.12),F(168),0.5)   # plug click
add(b,chime(),F(176),0.38)
add(b,whoosh(0.4,500,6000),F(203),0.3)
b=b[:int(7.5*SR)]
write('sfx_intro.wav', norm(b,-3))
