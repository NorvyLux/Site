import asyncio,subprocess,os,sys
from playwright.async_api import async_playwright
page,prefix=sys.argv[1],sys.argv[2]
SEG=[(0,7),(7,13),(13,22.5),(22.5,30),(30,36.5),(36.5,45),(45,52),(52,59),(59,65),(65,69.5),(69.5,74),(74,80)]
async def main():
  async with async_playwright() as p:
    import os as _o
    b=await p.chromium.launch(**({'executable_path':'/usr/bin/google-chrome'} if _o.path.exists('/usr/bin/google-chrome') else {}))
    pg=await b.new_page(viewport={'width':1920,'height':1080})
    await pg.goto(f'http://localhost:8766/{page}');await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(300)
    for i,(a,z) in enumerate(SEG):
      if os.environ.get("ONLY") and str(i)!=os.environ["ONLY"]: continue
      tmp=f'{prefix}{i}.tmp.mp4'
      ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30','-f','mp4',tmp],stdin=subprocess.PIPE)
      for k in range(round((z-a)*30)):
        await pg.evaluate(f'render({a+k/30})');ff.stdin.write(await pg.screenshot(type='jpeg',quality=92))
      ff.stdin.close();ff.wait()
      if ff.returncode!=0: sys.exit('fail')
      os.replace(tmp,f'{prefix}{i}.mp4')
    await b.close()
  with open(f'{prefix}.txt','w') as f:
    for i in range(len(SEG)): f.write(f"file '{prefix}{i}.mp4'\n")
asyncio.run(main())
