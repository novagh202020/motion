import sys,os,subprocess
from playwright.sync_api import sync_playwright
src,outdir,fps=sys.argv[1],sys.argv[2],int(sys.argv[3])
only=[float(x) for x in sys.argv[4:]]
os.makedirs(outdir,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=["--allow-file-access-from-files","--force-color-profile=srgb"])
    import re
    m=re.search(r'html,body\{\{?width:(\d+)px;height:(\d+)px',open(src).read());w,h=int(m[1]),int(m[2])
    pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
    pg.goto('file://'+src);pg.evaluate('document.fonts.ready');pg.wait_for_timeout(600)
    dur=pg.evaluate('DUR')
    ts=only or [i/fps for i in range(int(dur*fps))]
    for i,t in enumerate(ts):
        pg.evaluate(f'frame({t})')
        pg.screenshot(path=f'{outdir}/f{i:04d}.png')
    b.close()
