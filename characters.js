/* Paper cut-out characters for the CarDiag story series.
   MOHANDES(id): the lazy one-goggle hero ("مهندس") - half-closed eye, moustache, limp arms.
   RAFIGH(id):   his friend who owns CarDiag ("رفیق مهندس") - two goggles, wide awake, phone in hand.
   Both: origin at the feet (centre), ~430 px tall at scale 1. Needs the #paper filter from the page.
   pose(id, o): o = {lid 0..1 (closed), look [dx,dy], mouth 'flat'|'yawn'|'smile'|'o', armL, armR (deg), bob (px), squash (0..1), tilt (deg)} */
(function(){
const SKIN='#F2C9A0', LID='#E2AE84', NAVY='#10203C', DEEP='#1565C0', BLUE='#2196F3', RIM='#E6EBF2';

function eye(id,cx,cy,r,lidc){return `
 <g transform="translate(${cx},${cy})">
  <circle r="${r+16}" fill="${RIM}" class="pp"/>
  <circle r="${r}" fill="#FFFFFF"/>
  <g id="${id}p"><circle r="${r*.34}" fill="${NAVY}"/><circle cx="${-r*.12}" cy="${-r*.14}" r="${r*.1}" fill="#FFFFFF"/></g>
  <clipPath id="${id}c"><circle r="${r}"/></clipPath>
  <g clip-path="url(#${id}c)"><rect id="${id}l" x="${-r-2}" y="${-r-2}" width="${2*r+4}" height="0" fill="${lidc||LID}"/>
   <rect id="${id}e" x="${-r-2}" y="${-r-2}" width="${2*r+4}" height="4" fill="${NAVY}" opacity=".55"/></g>
 </g>`}

const arm=(id,side,len)=>`<g id="${id}" transform="translate(${side*96},-200)">
  <path d="M0,0 Q${side*28},${len*.5} ${side*10},${len}" stroke="${SKIN}" stroke-width="22" fill="none" stroke-linecap="round" class="pp"/>
  <circle cx="${side*10}" cy="${len}" r="20" fill="${NAVY}" class="pp"/></g>`;

window.MOHANDES=function(id){return `<g id="${id}"><g id="${id}b">
 <ellipse cx="0" cy="6" rx="110" ry="16" fill="#142850" opacity=".25"/>
 <g class="pp"><rect x="-60" y="-60" width="38" height="60" fill="${NAVY}"/><rect x="22" y="-60" width="38" height="60" fill="${NAVY}"/>
  <rect x="-74" y="-14" width="58" height="22" rx="11" fill="#181C24"/><rect x="16" y="-14" width="58" height="22" rx="11" fill="#181C24"/></g>
 <g class="pp"><rect x="-100" y="-440" width="200" height="400" rx="100" fill="${SKIN}"/></g>
 ${arm(id+'aL',-1,150)}${arm(id+'aR',1,150)}
 <!-- slouchy overalls with a pen in the pocket: he IS the engineer -->
 <g class="pp"><path d="M-100,-190 H100 V-100 Q100,-40 40,-40 H-40 Q-100,-40 -100,-100 Z" fill="${DEEP}"/>
  <path d="M-70,-190 L-88,-262 L-66,-268 L-46,-190 Z M70,-190 L88,-262 L66,-268 L46,-190 Z" fill="${DEEP}"/>
  <rect x="-38" y="-176" width="76" height="56" rx="10" fill="${BLUE}"/><rect x="14" y="-200" width="8" height="40" rx="3" fill="${NAVY}"/></g>
 <g class="pp"><circle cx="-80" cy="-264" r="9" fill="${RIM}"/><circle cx="80" cy="-264" r="9" fill="${RIM}"/></g>
 <!-- three sad hairs -->
 <g class="pp" stroke="${NAVY}" stroke-width="7" fill="none" stroke-linecap="round"><path d="M-14,-438 q-10,-34 -32,-40"/><path d="M0,-440 q2,-38 -6,-52"/><path d="M14,-438 q14,-30 34,-30"/></g>
 <!-- strap + single goggle -->
 <g class="pp"><rect x="-102" y="-352" width="204" height="30" fill="${NAVY}"/></g>
 ${eye(id+'E',0,-338,58)}
 <!-- Iranian engineer moustache -->
 <g class="pp"><path d="M-46,-248 Q-24,-266 0,-252 Q24,-266 46,-248 Q30,-232 0,-240 Q-30,-232 -46,-248 Z" fill="${NAVY}"/></g>
 <g id="${id}m"></g>
 <g id="${id}win" opacity="0">
  <g class="pp"><path d="M-100,-210 Q0,-180 100,-210 L100,-176 Q0,-146 -100,-176 Z" fill="#FFFFFF"/><path d="M40,-186 L78,-186 L86,-96 L54,-96 Z" fill="#FFFFFF"/>
   <path d="M-70,-200 L-62,-170 M-30,-190 L-24,-160 M10,-188 L14,-158 M50,-196 L54,-166" stroke="#2196F3" stroke-width="10"/><path d="M58,-150 H82 M56,-126 H84" stroke="#2196F3" stroke-width="9"/></g>
  <g class="pp"><path d="M-98,-400 Q-100,-500 0,-500 Q100,-500 98,-400 Z" fill="#2196F3"/><rect x="-104" y="-414" width="208" height="30" rx="12" fill="#FFFFFF"/><circle cx="0" cy="-506" r="24" fill="#FFFFFF"/></g>
  <path d="M-40,-238 l6,18 l6,-18 M14,-238 l6,16 l6,-16" fill="#FFFFFF"/>
 </g>
</g></g>`};

window.RAFIGH=function(id){return `<g id="${id}"><g id="${id}b">
 <ellipse cx="0" cy="6" rx="104" ry="16" fill="#142850" opacity=".25"/>
 <g class="pp"><rect x="-56" y="-58" width="36" height="58" fill="${NAVY}"/><rect x="20" y="-58" width="36" height="58" fill="${NAVY}"/>
  <rect x="-70" y="-14" width="56" height="22" rx="11" fill="#FFFFFF"/><rect x="14" y="-14" width="56" height="22" rx="11" fill="#FFFFFF"/></g>
 <g id="${id}aR" transform="translate(92,-200)">
  <path d="M0,0 Q40,40 50,100" stroke="${SKIN}" stroke-width="22" fill="none" stroke-linecap="round" class="pp"/>
  <g transform="translate(50,100) rotate(-12)"><g class="pp"><rect x="-34" y="-62" width="68" height="120" rx="12" fill="#181C24"/></g>
   <rect x="-26" y="-52" width="52" height="98" rx="6" fill="${BLUE}"/>
   <path d="M-18,0 h10 l5,-12 l6,22 l5,-10 h10" stroke="#FFFFFF" stroke-width="4" fill="none" stroke-linejoin="round"/></g>
  <circle cx="50" cy="100" r="20" fill="${NAVY}" class="pp"/></g>
 <g class="pp"><rect x="-96" y="-400" width="192" height="360" rx="96" fill="${SKIN}"/></g>
 ${arm(id+'aL',-1,130)}
 <g class="pp"><path d="M-96,-180 H96 V-100 Q96,-40 40,-40 H-40 Q-96,-40 -96,-100 Z" fill="${BLUE}"/>
  <path d="M-66,-180 L-84,-250 L-62,-256 L-42,-180 Z M66,-180 L84,-250 L62,-256 L42,-180 Z" fill="${BLUE}"/>
  <rect x="-36" y="-168" width="72" height="52" rx="10" fill="#FFFFFF"/>
  <path d="M-24,-142 h12 l6,-12 l7,22 l6,-10 h17" stroke="${BLUE}" stroke-width="5" fill="none" stroke-linejoin="round"/></g>
 <!-- spiky hair -->
 <g class="pp"><path d="M-40,-392 L-30,-440 L-10,-400 L4,-452 L18,-400 L40,-436 L44,-388 Z" fill="${NAVY}"/></g>
 <g class="pp"><rect x="-98" y="-322" width="196" height="28" fill="${NAVY}"/></g>
 ${eye(id+'E1',-40,-308,38)}${eye(id+'E2',40,-308,38)}
 <g id="${id}m"></g>
</g></g>`};

// ---- episode 2 cast (all paper, minion goggles) ----
window.CHAR_META={};
function eyes2(id,y,dx,r,band,bandW,lidc){return `<g class="pp"><rect x="${-bandW/2}" y="${y-12}" width="${bandW}" height="24" fill="${band}"/></g>${eye(id+'E1',-dx,y,r,lidc)}${eye(id+'E2',dx,y,r,lidc)}`}
const limb=(id,x,y,side,len,col,hand)=>`<g id="${id}" transform="translate(${x},${y})"><path d="M0,0 Q${side*26},${len*.5} ${side*8},${len}" stroke="${col}" stroke-width="18" fill="none" stroke-linecap="round" class="pp"/><circle cx="${side*8}" cy="${len}" r="17" fill="${hand}" class="pp"/></g>`;

// car battery: navy body (brand rule), slate lid, two terminals. extras: cap, therm, halo, blanket, old (brows+cane)
window.BATTERY=function(id){CHAR_META[id]={eyes:[[id+'E1',34],[id+'E2',34]],my:-96,arm:[136,-130]};return `<g id="${id}"><g id="${id}b">
 <ellipse cx="0" cy="6" rx="150" ry="16" fill="#142850" opacity=".25"/>
 <g class="pp"><rect x="-70" y="-30" width="34" height="34" fill="#6E7D96"/><rect x="36" y="-30" width="34" height="34" fill="#6E7D96"/></g>
 ${limb(id+'aL',-136,-130,-1,100,'#6E7D96','#181C24')}${limb(id+'aR',136,-130,1,100,'#6E7D96','#181C24')}
 <g class="pp"><rect x="-110" y="-292" width="46" height="40" rx="8" fill="#E6EBF2"/><rect x="64" y="-292" width="46" height="40" rx="8" fill="#E6EBF2"/>
  <rect x="-140" y="-262" width="280" height="250" rx="24" fill="#10203C"/><rect x="-140" y="-262" width="280" height="46" rx="20" fill="#3A4252"/></g>
 <text x="-87" y="-226" text-anchor="middle" font-family="V" font-weight="900" font-size="34" fill="#FFFFFF">+</text><text x="87" y="-226" text-anchor="middle" font-family="V" font-weight="900" font-size="34" fill="#FFFFFF">−</text>
 ${eyes2(id,-160,54,34,'#6E7D96',284,'#3A4252')}
 <g id="${id}m"></g>
 <g id="${id}old" opacity="0"><path d="M-96,-210 q30,-22 62,-2 M34,-212 q32,-20 62,2" stroke="#FFFFFF" stroke-width="12" fill="none" stroke-linecap="round" class="pp"/></g>
 <g id="${id}cap" opacity="0"><g class="pp"><path d="M-130,-250 Q-40,-380 120,-250 Z" fill="#2196F3"/><rect x="-140" y="-262" width="270" height="26" rx="12" fill="#FFFFFF"/><circle cx="-110" cy="-330" r="24" fill="#FFFFFF"/></g></g>
 <g id="${id}therm" opacity="0"><g class="pp"><rect x="20" y="-96" width="120" height="14" rx="7" fill="#FFFFFF" transform="rotate(-18 20 -90)"/><circle cx="138" cy="-130" r="11" fill="#DC3232"/></g></g>
 <g id="${id}halo" opacity="0"><g class="pp"><ellipse cx="0" cy="-330" rx="110" ry="24" fill="none" stroke="#78CDFF" stroke-width="14"/></g></g>
 <g id="${id}blk" opacity="0"><g class="pp"><path d="M-200,-110 Q0,-150 200,-110 L210,10 H-210 Z" fill="#ADD6FA"/><path d="M-170,-90 L170,-90 M-180,-40 L180,-40" stroke="#FFFFFF" stroke-width="10" stroke-dasharray="26 18"/></g></g>
</g></g>`};

// alternator: round slotted body, pulley + belt at the bottom
window.ALTERNATOR=function(id){CHAR_META[id]={eyes:[[id+'E1',30],[id+'E2',30]],my:-140,arm:[118,-150]};
 let slots='';for(let k=0;k<16;k++){const a=k/16*Math.PI*2;slots+=`<line x1="${(Math.cos(a)*100).toFixed(1)}" y1="${(-180+Math.sin(a)*100).toFixed(1)}" x2="${(Math.cos(a)*122).toFixed(1)}" y2="${(-180+Math.sin(a)*122).toFixed(1)}" stroke="#6E7D96" stroke-width="9"/>`}
 return `<g id="${id}"><g id="${id}b">
 <ellipse cx="0" cy="6" rx="130" ry="16" fill="#142850" opacity=".25"/>
 <g class="pp"><rect x="-56" y="-60" width="32" height="64" fill="#6E7D96"/><rect x="24" y="-60" width="32" height="64" fill="#6E7D96"/>
  <rect x="-70" y="-14" width="54" height="20" rx="10" fill="#181C24"/><rect x="16" y="-14" width="54" height="20" rx="10" fill="#181C24"/></g>
 ${limb(id+'aL',-118,-150,-1,96,'#6E7D96','#181C24')}
 <g class="pp"><circle cx="0" cy="-180" r="128" fill="#ADB6C4"/></g><g class="pp">${slots}</g>
 <g class="pp"><circle cx="0" cy="-92" r="34" fill="#6E7D96"/><circle cx="0" cy="-92" r="12" fill="#10203C"/></g>
 ${eyes2(id,-208,42,30,'#10203C',256,'#8994A6')}
 <g id="${id}m"></g>
 <g id="${id}aR" transform="translate(118,-150)"><path d="M0,0 Q30,40 14,92" stroke="#6E7D96" stroke-width="18" fill="none" stroke-linecap="round" class="pp"/>
  <g id="${id}phone" transform="translate(14,92) rotate(-14)"><g class="pp"><rect x="-30" y="-56" width="60" height="104" rx="10" fill="#181C24"/></g><rect x="-23" y="-48" width="46" height="86" rx="5" fill="#F59628"/>
   <path d="M-12,-14 a8,8 0 0 1 12,-6 a8,8 0 0 1 12,6 q0,10 -12,20 q-12,-10 -12,-20z" fill="#FFFFFF"/></g>
  <circle cx="14" cy="92" r="17" fill="#181C24" class="pp"/></g>
 <g id="${id}cuffs" opacity="0" transform="translate(0,-64)"><g class="pp" fill="none" stroke="#E6EBF2" stroke-width="12"><circle cx="-34" r="24"/><circle cx="34" r="24"/></g><path d="M-10,0 H10" stroke="#E6EBF2" stroke-width="8"/></g>
</g></g>`};

// car heater vent: grille, long lashes, blush
window.HEATER=function(id){CHAR_META[id]={eyes:[[id+'E1',26],[id+'E2',26]],my:-12,arm:null};return `<g id="${id}"><g id="${id}b">
 <g class="pp"><rect x="-140" y="-110" width="280" height="200" rx="34" fill="#E6EBF2"/></g>
 <g class="pp" stroke="#10203C" stroke-width="10" stroke-linecap="round"><line x1="-100" y1="30" x2="100" y2="30"/><line x1="-100" y1="56" x2="100" y2="56"/></g>
 ${eye(id+'E1',-50,-50,26,'#C9D2DE')}${eye(id+'E2',50,-50,26,'#C9D2DE')}
 <g stroke="#10203C" stroke-width="6" stroke-linecap="round"><path d="M-74,-74 l-12,-14 M-56,-80 l-4,-18 M-36,-78 l4,-16 M26,-78 l-4,-16 M46,-80 l4,-18 M64,-74 l12,-14"/></g>
 <g id="${id}blush" opacity="0"><ellipse cx="-92" cy="-8" rx="24" ry="13" fill="#FFB0A8"/><ellipse cx="92" cy="-8" rx="24" ry="13" fill="#FFB0A8"/></g>
 <g id="${id}m"></g>
</g></g>`};

// the power thief: masked navy capsule carrying a sack of lightning
window.THIEF=function(id){CHAR_META[id]={eyes:[],my:-210,arm:[96,-200]};return `<g id="${id}"><g id="${id}b">
 <ellipse cx="0" cy="6" rx="110" ry="16" fill="#142850" opacity=".25"/>
 <g class="pp"><rect x="-58" y="-60" width="36" height="62" fill="#181C24"/><rect x="22" y="-60" width="36" height="62" fill="#181C24"/></g>
 <g class="pp"><path d="M60,-330 Q170,-300 160,-150 Q150,-90 70,-110 Q30,-200 60,-330 Z" fill="#FFFFFF"/></g>
 <g fill="#FFC446" stroke="#B86E0A" stroke-width="3"><path d="M110,-290 l-24,50 h22 l-12,44 l40,-60 h-22 l14,-34 z"/><path d="M134,-190 l-14,28 h12 l-6,24 l22,-34 h-12 l8,-18 z"/></g>
 <g class="pp"><rect x="-96" y="-420" width="192" height="380" rx="96" fill="#10203C"/></g>
 <g class="pp"><path d="M-92,-360 Q0,-470 92,-360 Z" fill="#181C24"/><rect x="-100" y="-372" width="200" height="22" rx="10" fill="#3A4252"/></g>
 <g class="pp"><rect x="-98" y="-330" width="196" height="60" rx="28" fill="#181C24"/></g>
 <ellipse cx="-38" cy="-300" rx="20" ry="14" fill="#FFFFFF"/><ellipse cx="38" cy="-300" rx="20" ry="14" fill="#FFFFFF"/>
 <circle id="${id}p1" cx="-34" cy="-300" r="7" fill="#10203C"/><circle id="${id}p2" cx="42" cy="-300" r="7" fill="#10203C"/>
 <g id="${id}m"></g>
</g></g>`};

const MOUTH={
 flat:(y)=>`<path d="M-30,${y} Q0,${y+8} 30,${y-2}" stroke="#10203C" stroke-width="7" fill="none" stroke-linecap="round"/>`,
 yawn:(y)=>`<g class="pp"><ellipse cx="0" cy="${y+18}" rx="30" ry="40" fill="#10203C"/><ellipse cx="0" cy="${y+38}" rx="18" ry="14" fill="#DC6E6E"/></g>`,
 smile:(y)=>`<g class="pp"><path d="M-42,${y-6} Q0,${y+46} 42,${y-6} Z" fill="#10203C"/><path d="M-30,${y} Q0,${y+12} 30,${y} Z" fill="#FFFFFF"/></g>`,
 o:(y)=>`<g class="pp"><ellipse cx="0" cy="${y+8}" rx="16" ry="20" fill="#10203C"/></g>`};

window.pose=function(id,o){o=o||{};const $=x=>document.getElementById(x);
 const isM=!!$(id+'El'), META=window.CHAR_META&&CHAR_META[id];
 const eyes=META?META.eyes:isM?[[id+'E',58]]:[[id+'E1',38],[id+'E2',38]];
 const lid=o.lid==null?(isM?.55:0):o.lid, lk=o.look||[0,0];
 eyes.forEach(([e,r])=>{const h=(2*r+4)*Math.min(1,lid);$(e+'l').setAttribute('height',h);$(e+'e').setAttribute('y',-r-2+h-2);$(e+'e').setAttribute('opacity',lid>.02?.55:0);
  $(e+'p').setAttribute('transform',`translate(${lk[0]*r*.45},${lk[1]*r*.45})`);});
 $(id+'m').innerHTML=MOUTH[o.mouth||(isM?'flat':'smile')](META?META.my:isM?-218:-226);
 if($(id+'win'))$(id+'win').setAttribute('opacity',o.winter?1:0);
 ['cap','therm','halo','blk','old','cuffs','blush'].forEach(k=>{if($(id+k))$(id+k).setAttribute('opacity',o[k]?1:0)});
 const s=o.squash||0, bob=o.bob||0;
 $(id+'b').setAttribute('transform',`translate(0,${bob}) rotate(${o.tilt||0}) scale(${1+s*.08},${1-s*.08})`);
 const ap=META&&META.arm?META.arm:[96,-200];
 if(o.armL!=null&&$(id+'aL'))$(id+'aL').setAttribute('transform',`translate(${-ap[0]},${ap[1]}) rotate(${o.armL})`);
 if(o.armR!=null&&$(id+'aR'))$(id+'aR').setAttribute('transform',`translate(${ap[0]},${ap[1]}) rotate(${o.armR})`);};
})();
