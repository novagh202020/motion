/* Shared end card: diag + phone (home screen) joined by a live link, brand, offer, url.
   Usage: initEnd(); then call renderEnd(f) every frame (T0 = 817.5). */
(function(){
const T0=817.5;
const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), seg=(f,a,b)=>cl((f-a)/(b-a)), lerp=(a,b,t)=>a+(b-a)*t;
const E={oc:t=>1-Math.pow(1-t,3),io:t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,ic:t=>t*t*t,back:t=>{const c1=1.55,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)}};
const FA='۰۱۲۳۴۵۶۷۸۹', fa=s=>String(s).replace(/[0-9]/g,d=>FA[d]);
const P={home:'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z',add:'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z',
 more:'M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z',
 down:'M7 10l5 5 5-5z',plug:'M16 7V3h-2v4h-4V3H8v4h-.01C6.9 6.99 6 7.89 6 8.98v5.52L9.5 18v3h5v-3l3.5-3.51v-5.5c0-1.1-.9-2-2-2z',
 car:'M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z',
 warn:'M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z',
 wrench:'M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z',
 eye:'M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z',
 gift:'M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z'};
const sv=(p,c,s)=>`<svg width="${s}" height="${s}" viewBox="0 0 24 24"><path fill="${c}" d="${P[p]}"/></svg>`;
const tile=(ic,l)=>`<div style="background:#fff;border:2px solid #DEE6F2;border-radius:24px;height:170px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-weight:700;font-size:22px">
 <div style="width:76px;height:76px;border-radius:20px;background:#E3EFFC;display:flex;align-items:center;justify-content:center">${sv(ic,'#2196F3',40)}</div>${l}</div>`;
const HOME=`<div style="height:48px;display:flex;justify-content:space-between;align-items:center;padding:6px 40px 0;font-weight:700;font-size:19px;direction:ltr;color:#10203C"><span>۱۲:۳۴</span><span>●●● ▮ ۱۰۰٪</span></div>
 <div style="background:#fff;border:2px solid #DEE6F2;border-radius:24px;margin:8px 18px;padding:22px">
  <div style="height:72px;border:3px solid #2196F3;border-radius:16px;display:flex;align-items:center;justify-content:space-between;padding:0 20px"><span style="font-weight:800;font-size:30px">۲۰۶</span>${sv('down','#2196F3',40)}</div>
  <div style="margin-top:16px;font-weight:500;font-size:22px;color:#6E7D96">وضعیت اتصال: <b id="ecStat" style="font-weight:800;color:#22A050">متصل</b></div>
  <div style="text-align:center;margin-top:14px"><span id="ecNum" style="font-weight:900;font-size:96px;color:#22A050;line-height:1">۹۲٪</span>
   <div style="font-weight:700;font-size:23px;color:#6E7D96;margin-top:2px">سلامت خودرو</div></div>
  <div style="position:relative;margin:16px 6px 4px;height:28px;border-radius:14px;background:#E6EBF2;overflow:hidden;direction:ltr">
   <div id="ecFill" style="position:absolute;left:0;top:0;height:28px;width:92%;border-radius:14px;background:linear-gradient(90deg,#E63C3C 0%,#F59628 35%,#D7C832 65%,#32B455 100%);background-size:452px 28px"></div></div>
  <div style="display:flex;gap:14px;margin-top:20px">
   <div style="flex:1;height:62px;border-radius:31px;background:#2196F3;color:#fff;font-weight:700;font-size:23px;display:flex;align-items:center;justify-content:center;gap:8px">${sv('plug','#fff',28)}اتصال</div>
   <div style="flex:1;height:62px;border-radius:31px;border:2px solid #DEE6F2;color:#6E7D96;font-weight:700;font-size:23px;display:flex;align-items:center;justify-content:center">قطع اتصال</div></div>
 </div>
 <div style="padding:8px 26px 6px;font-weight:700;font-size:22px;color:#98A3B8">دسترسی سریع</div>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:0 18px">${tile('car','سفر')}${tile('warn','خطایابی <span style="direction:ltr;unicode-bidi:isolate">ECU</span>')}${tile('wrench','عیب‌یاب هوش مصنوعی')}${tile('eye','مانیتورینگ خودرو')}</div>
 <div style="position:absolute;left:0;bottom:0;width:572px;height:96px;background:#2196F3;display:flex;padding-bottom:6px">
  ${[['home','خانه',28],['add','افزودن خودرو',36],['more','بیشتر',34]].map(n=>`<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:500;font-size:17px;gap:4px">${sv(n[0],'#fff',n[2])}<span>${n[1]}</span></div>`).join('')}</div>`;

// geometry
const DX=325, DY=780, DW=470;                     // diag centre / width
const PX=728, PY=500, PS=0.43;                    // phone top-left / scale (600x1290 -> 258x555)
const L0=[DX+DW/2-22, DY-10], L1=[PX-6, PY+270];  // link endpoints
const LINK=`M${L0[0]} ${L0[1]} L${L0[0]+34} ${L0[1]} L${L0[0]+48} ${L0[1]-26} L${L0[0]+64} ${L0[1]+30} L${L0[0]+80} ${L0[1]-34} L${L0[0]+94} ${L0[1]+8} L${L0[0]+104} ${L0[1]} Q${(L0[0]+L1[0])/2+40} ${L0[1]} ${L1[0]} ${L1[1]}`;

window.initEnd=function(parent){
 const d=document.createElement('div'); d.id='ec'; d.style.cssText='position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:46;pointer-events:none;display:none';
 d.innerHTML=`
 <div id="ecBloom" style="position:absolute;left:-35px;top:380px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(40,160,255,.28) 0%,rgba(40,160,255,.10) 40%,rgba(40,160,255,0) 70%)"></div>
 <svg id="ecLinkSvg" style="position:absolute;left:0;top:0" width="1080" height="1920">
  <defs><filter id="ecGl" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="8"/></filter></defs>
  <path id="ecLinkG" d="${LINK}" fill="none" stroke="#78CDFF" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" filter="url(#ecGl)"/>
  <path id="ecLink" d="${LINK}" fill="none" stroke="#2196F3" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <g id="ecDots"></g>
 </svg>
 <div id="ecProd" style="position:absolute;left:${DX-DW/2}px;top:${DY-DW*0.3613}px;width:${DW}px;height:${DW*0.7225}px;transform-origin:50% 60%">
  <div style="position:absolute;left:12%;top:86%;width:76%;height:16%;border-radius:50%;background:radial-gradient(ellipse,rgba(20,40,80,.30),rgba(20,40,80,0) 70%)"></div>
  <img src="assets/diag_front.png" style="position:absolute;left:0;top:0;width:100%;height:100%">
 </div>
 <div id="ecPhone" style="position:absolute;left:${PX}px;top:${PY}px;width:600px;height:1290px;border-radius:78px;background:#181C24;border:3px solid #5F6878;transform-origin:0 0;
   box-shadow:0 50px 90px rgba(20,40,80,.28),0 12px 26px rgba(20,40,80,.18)">
  <div style="position:absolute;left:50%;top:14px;width:22px;height:22px;margin-left:-11px;border-radius:50%;background:#0b0e13;z-index:3"></div>
  <div style="position:absolute;left:11px;top:11px;width:572px;height:1262px;border-radius:66px;overflow:hidden;background:#EEF2F8;direction:rtl;font-family:V">${HOME}</div>
 </div>
 <div id="ecBrand" style="position:absolute;left:0;top:1080px;width:1080px;text-align:center;font-weight:900;font-size:120px;color:#1565C0;direction:ltr">CarDiag AI</div>
 <div id="ecBuy" style="position:absolute;left:0;top:1245px;width:1080px;text-align:center;font-weight:800;font-size:58px;color:#10203C;direction:rtl">دیاگ رو بخر،</div>
 <div id="ecGold" style="position:absolute;left:50%;top:1340px;height:108px;padding:0 54px;border-radius:54px;transform:translateX(-50%);
   background:linear-gradient(90deg,#F6CD5C 0%,#FFEA9C 50%,#E0A82C 100%);color:#4B3005;font-weight:800;font-size:54px;display:flex;align-items:center;gap:18px;white-space:nowrap;direction:rtl;box-shadow:0 18px 40px rgba(20,40,80,.18)">${sv('gift','#4B3005',56)}اشتراک طلایی هدیه بگیر</div>
 <div id="ecUrl" style="position:absolute;left:0;top:1484px;width:1080px;text-align:center;font-weight:700;font-size:56px;color:#506482;direction:ltr">cardiag.ir</div>`;
 (parent||document.getElementById('stage')||document.body).appendChild(d);
};

window.renderEnd=function(f){
 const ec=document.getElementById('ec'); if(f<T0){ec.style.display='none';return} ec.style.display='block';
 const t=f-T0;
 const beat=Math.exp(-Math.pow((f-868)/5,2))*0.6+Math.exp(-Math.pow((f-885)/4,2));
 // diag
 const pop=seg(t,0,20); const pd=document.getElementById('ecProd');
 pd.style.opacity=E.oc(seg(t,0,7));
 pd.style.transform=`translateY(${Math.sin((f-840)/14)*5*seg(t,22,34)}px) scale(${(pop<=0?0.001:lerp(0.5,1,E.back(pop)))*(1+0.04*beat)}) rotate(${lerp(6,0,E.oc(pop))}deg)`;
 document.getElementById('ecBloom').style.opacity=(0.6*seg(t,0,16))*(1+0.6*beat);
 // phone slides in from right
 const pp=E.oc(seg(t,6,24)); const ph=document.getElementById('ecPhone');
 ph.style.opacity=E.oc(seg(t,6,12)); ph.style.transform=`translateX(${(1-pp)*420}px) scale(${PS}) rotate(${lerp(10,4,pp)}deg)`;
 const h=E.oc(seg(t,22,40)); document.getElementById('ecFill').style.width=(h*92)+'%'; document.getElementById('ecNum').textContent=fa(Math.round(h*92))+'٪';
 // link: draws, then live dots + breathing glow
 const lk=document.getElementById('ecLink'), lg=document.getElementById('ecLinkG'); const L=lk.getTotalLength();
 const dr=E.io(seg(t,16,28)); [lk,lg].forEach(p=>{p.style.strokeDasharray=L;p.style.strokeDashoffset=L*(1-dr)});
 lg.style.opacity=dr*(0.35+0.25*(0.5+0.5*Math.sin(t/4))+0.4*beat);
 let dots=''; if(t>=26){for(let i=0;i<4;i++){const ph2=((t-26)/18+i/4)%1; const pt=lk.getPointAtLength(ph2*L);
   dots+=`<circle cx="${pt.x}" cy="${pt.y}" r="${8+4*beat}" fill="#78CDFF" opacity="${Math.sin(ph2*Math.PI)*seg(t,26,32)}"/><circle cx="${pt.x}" cy="${pt.y}" r="4" fill="#fff" opacity="${Math.sin(ph2*Math.PI)*seg(t,26,32)}"/>`;}}
 document.getElementById('ecDots').innerHTML=dots;
 // text
 const bi=E.oc(seg(t,14,26)); const br=document.getElementById('ecBrand'); br.style.opacity=bi; br.style.transform=`translateY(${(1-bi)*30}px)`;
 const by=E.oc(seg(t,24,34)); const b2=document.getElementById('ecBuy'); b2.style.opacity=by; b2.style.transform=`translateY(${(1-by)*24}px)`;
 const gp=seg(t,30,44); const g=document.getElementById('ecGold'); g.style.opacity=E.oc(seg(t,30,36)); g.style.transform=`translateX(-50%) scale(${gp<=0?0.6:lerp(0.6,1,E.back(gp))})`;
 const ui=E.oc(seg(t,40,52)); const u=document.getElementById('ecUrl'); u.style.opacity=ui; u.style.transform=`translateY(${(1-ui)*24}px)`;
};
})();
