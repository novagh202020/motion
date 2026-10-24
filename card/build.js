const {chromium}=require('playwright');const path=require('path');
(async()=>{const d=__dirname,b=await chromium.launch(),mm=96/25.4;
const open=async s=>{const pg=await b.newPage({viewport:{width:363,height:250},deviceScaleFactor:s});await pg.goto('file://'+d+'/card.html');await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(300);return pg};
const pg=await open(1);await pg.pdf({path:d+'/cardiag_card_print.pdf',width:'96mm',height:'66mm',printBackground:true});
const p2=await open(300/96);const pages=await p2.$$('.page');
for(const [i,n] of ['front','back'].entries()){const bb=await pages[i].boundingBox();
 await p2.screenshot({path:`${d}/card_${n}.png`,fullPage:true,clip:{x:bb.x+3*mm,y:bb.y+3*mm,width:90*mm,height:60*mm}})}
await b.close()})();
