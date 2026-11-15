/* Paper cut-out characters for the CarDiag story series.
   MOHANDES(id): the lazy one-goggle hero ("مهندس") - half-closed eye, moustache, limp arms.
   RAFIGH(id):   his friend who owns CarDiag ("رفیق مهندس") - two goggles, wide awake, phone in hand.
   Both: origin at the feet (centre), ~430 px tall at scale 1. Needs the #paper filter from the page.
   pose(id, o): o = {lid 0..1 (closed), look [dx,dy], mouth 'flat'|'yawn'|'smile'|'o', armL, armR (deg), bob (px), squash (0..1), tilt (deg)} */
(function(){
const SKIN='#F2C9A0', LID='#E2AE84', NAVY='#10203C', DEEP='#1565C0', BLUE='#2196F3', RIM='#E6EBF2';

function eye(id,cx,cy,r){return `
 <g transform="translate(${cx},${cy})">
  <circle r="${r+16}" fill="${RIM}" class="pp"/>
  <circle r="${r}" fill="#FFFFFF"/>
  <g id="${id}p"><circle r="${r*.34}" fill="${NAVY}"/><circle cx="${-r*.12}" cy="${-r*.14}" r="${r*.1}" fill="#FFFFFF"/></g>
  <clipPath id="${id}c"><circle r="${r}"/></clipPath>
  <g clip-path="url(#${id}c)"><rect id="${id}l" x="${-r-2}" y="${-r-2}" width="${2*r+4}" height="0" fill="${LID}"/>
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

const MOUTH={
 flat:(y)=>`<path d="M-30,${y} Q0,${y+8} 30,${y-2}" stroke="#10203C" stroke-width="7" fill="none" stroke-linecap="round"/>`,
 yawn:(y)=>`<g class="pp"><ellipse cx="0" cy="${y+18}" rx="30" ry="40" fill="#10203C"/><ellipse cx="0" cy="${y+38}" rx="18" ry="14" fill="#DC6E6E"/></g>`,
 smile:(y)=>`<g class="pp"><path d="M-42,${y-6} Q0,${y+46} 42,${y-6} Z" fill="#10203C"/><path d="M-30,${y} Q0,${y+12} 30,${y} Z" fill="#FFFFFF"/></g>`,
 o:(y)=>`<g class="pp"><ellipse cx="0" cy="${y+8}" rx="16" ry="20" fill="#10203C"/></g>`};

window.pose=function(id,o){o=o||{};const $=x=>document.getElementById(x);
 const isM=!!$(id+'El');
 const eyes=isM?[[id+'E',58]]:[[id+'E1',38],[id+'E2',38]];
 const lid=o.lid==null?(isM?.55:0):o.lid, lk=o.look||[0,0];
 eyes.forEach(([e,r])=>{const h=(2*r+4)*Math.min(1,lid);$(e+'l').setAttribute('height',h);$(e+'e').setAttribute('y',-r-2+h-2);$(e+'e').setAttribute('opacity',lid>.02?.55:0);
  $(e+'p').setAttribute('transform',`translate(${lk[0]*r*.45},${lk[1]*r*.45})`);});
 $(id+'m').innerHTML=MOUTH[o.mouth||(isM?'flat':'smile')](isM?-218:-226);
 const s=o.squash||0, bob=o.bob||0;
 $(id+'b').setAttribute('transform',`translate(0,${bob}) rotate(${o.tilt||0}) scale(${1+s*.08},${1-s*.08})`);
 if(o.armL!=null)$(id+'aL').setAttribute('transform',`translate(-96,-200) rotate(${o.armL})`);
 if(o.armR!=null)$(id+'aR').setAttribute('transform',`translate(96,-200) rotate(${o.armR})`);};
})();
