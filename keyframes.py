import asyncio,sys
from playwright.async_api import async_playwright
TS=[float(x) for x in sys.argv[1:]]
async def main():
  async with async_playwright() as p:
    import os as _o
    b=await p.chromium.launch(**({'executable_path':'/usr/bin/google-chrome'} if _o.path.exists('/usr/bin/google-chrome') else {}))
    pg=await b.new_page(viewport={'width':1920,'height':1080})
    await pg.goto('http://localhost:8766/'+(sys.argv[0] and __import__('os').environ.get('FILM','film.html')));await pg.evaluate('document.fonts.ready');await pg.wait_for_timeout(300)
    for t in TS:
      await pg.evaluate(f'render({t})');await pg.screenshot(path=f'k{t}.jpg',type='jpeg',quality=85)
    await b.close()
asyncio.run(main())
