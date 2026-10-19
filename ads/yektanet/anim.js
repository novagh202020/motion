// Shared 6s seamless loop for every Yektanet banner size. Each element is optional.
// #bt takes data-ox / data-oy (arc origin), data-r0 / data-r1 (radius range), data-w (stroke).
const DUR=6;
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const io=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
const back=x=>{const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const seg=(t,a,b)=>cl((t-a)/(b-a));
const u=document.querySelector('#title u');
const ulW=u?u.offsetWidth:0;
const chipW=$('chip')?$('chip').offsetWidth:0;
const bt=$('bt'),B=bt?bt.dataset:{};
function frame(t){
  const f=Math.sin(t/DUR*2*Math.PI);
  if($('diag'))$('diag').style.transform=`translateY(${Math.round(f*(+($('diag').dataset.amp||2)))}px)`;
  // check-engine halo: pulse every 1.5s
  const p=(t%1.5)/1.5;
  if($('halo')){$('halo').style.transform=`scale(${1+p*0.9})`;$('halo').style.opacity=(1-p)*.9;}
  // generic shines: .shine sweeps its parent once per loop, starting at data-t0
  document.querySelectorAll('.shine').forEach(el=>{const w=el.parentElement.offsetWidth,t0=+(el.dataset.t0||.2);
    const s=seg(t,t0,t0+.8);el.style.right=(-50+s*(w+100))+'px';el.style.opacity=s>0&&s<1?1:0;});
  // discount badge: soft pulse every 1.5s
  if($('badge')){const b=Math.max(0,Math.sin(((t+.4)%1.5)/1.5*Math.PI*2));$('badge').style.transform=`scale(${1+.08*b})`;}
  // shine across the check-engine pill 0.2–0.9s
  if($('shine')){const s=seg(t,.2,.9);$('shine').style.right=(-60+s*(chipW+120))+'px';$('shine').style.opacity=s>0&&s<1?1:0;}
  // underline under «خودت ببین»
  if($('ul')){const k=io(seg(t,.3,1.1))*(1-io(seg(t,5.5,5.9)));$('ul').style.width=(k*ulW)+'px';}
  // bluetooth arcs from the diag 0.8–2.6
  if(bt){const ox=+B.ox,oy=+B.oy,r0=+B.r0,r1=+B.r1,w=+B.w;let svg='';
    for(let k=0;k<3;k++){const q=seg(t,.8+k*.35,1.9+k*.35);if(q<=0||q>=1)continue;
      const r=r0+q*(r1-r0),o=Math.sin(q*Math.PI);
      const d=`M${ox-r*Math.cos(.25)} ${oy-r*Math.sin(.25)} A${r} ${r} 0 0 1 ${ox-r*Math.sin(.35)} ${oy-r*Math.cos(.35)}`;
      svg+=`<path d="${d}" stroke="#fff" stroke-opacity="${o}" stroke-width="${w*1.9}" fill="none" stroke-linecap="round"/><path d="${d}" stroke="#2196F3" stroke-opacity="${o}" stroke-width="${w}" fill="none" stroke-linecap="round"/>`;}
    bt.innerHTML=svg;}
  // app status «قطع شده» → «متصل»
  if($('st'))$('st').style.opacity=t>=2.1&&t<5.8?1:0;
  // error card pops 2.3, OK chip 3.3, leaves 5.3–5.7
  if($('card')){const ci=back(seg(t,2.3,2.75)),co=io(seg(t,5.3,5.7)),dy=+($('card').dataset.dy||12);
    $('card').style.opacity=cl(seg(t,2.3,2.5)-co);
    $('card').style.transform=`translateY(${(1-ci)*dy+co*dy*.6}px) scale(${.85+.15*ci-co*.06})`;}
  if($('ok')){const k=back(seg(t,3.3,3.65));$('ok').style.opacity=seg(t,3.3,3.45);$('ok').style.transform=`scale(${.7+.3*k})`;}
}
window.DUR=DUR;window.frame=frame;frame(0);
