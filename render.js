// Node twin of render.py (for containers where only the Node Playwright is installed).
// usage: PAGE=x.html node render.js frames 0,30,60 outdir   |   PAGE=x.html node render.js video out.mp4 [start end]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs'), url = require('url');
(async () => {
  const page = path.resolve(__dirname, process.env.PAGE || 'motion.html');
  const b = await chromium.launch({ args: ['--disable-web-security', '--allow-file-access-from-files', '--force-color-profile=srgb'] });
  const pg = await b.newPage({ viewport: { width: +(process.env.VW || 1080), height: +(process.env.VH || 1920) }, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()) });
  await pg.goto(url.pathToFileURL(page).href); await pg.evaluate('window.READY'); await pg.waitForTimeout(300);
  const [mode, a1, a2, a3] = process.argv.slice(2);
  if (mode === 'frames') {
    fs.mkdirSync(a2, { recursive: true });
    for (const f of a1.split(',').map(Number)) { await pg.evaluate(`render(${f})`); await pg.screenshot({ path: path.join(a2, `f${String(f).padStart(4, '0')}.png`) }); }
  } else {
    const s = a2 ? +a2 : 0, e = a3 ? +a3 : 900;
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', '30', a1], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = s; f < e; f++) { await pg.evaluate(`render(${f})`); const buf = await pg.screenshot({ type: 'png' }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (f % 100 === 0) console.log('frame', f); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 10));
  await b.close();
})();
