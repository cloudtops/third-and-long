import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
TMP = HERE / ".cards"; TMP.mkdir(exist_ok=True)

CARD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Zilla+Slab:wght@400;600;700&display=swap">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1200px;height:630px;overflow:hidden;background:#101418;color:#EDEEE9;
  font-family:"Zilla Slab",Georgia,serif;display:flex;flex-direction:column;
  justify-content:space-between;padding:64px 72px 0}}
.top{{display:flex;align-items:baseline;justify-content:space-between}}
.mast{{font-family:"Archivo Narrow",sans-serif;font-weight:700;font-size:26px;
  text-transform:uppercase;letter-spacing:.28em}}
.edition{{font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:22px;
  text-transform:uppercase;letter-spacing:.2em;color:#F2C74A}}
h1{{font-weight:600;font-size:{size}px;line-height:1.0;letter-spacing:-.025em;
  max-width:16ch;margin-top:56px}}
.foot{{display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid #2C333A;margin-top:auto;padding:26px 0;
  font-family:"Archivo Narrow",sans-serif;font-weight:600;font-size:23px;
  text-transform:uppercase;letter-spacing:.16em}}
.foot .dim{{color:#8B9490;font-weight:500}}
.bars{{display:flex;height:10px;margin:0 -72px}}
.bars i{{flex:1}} .bars .a{{background:#A81B2C}} .bars .n{{background:#1B3E86}}
.bars .p{{background:#F2C74A;flex:0 0 90px}}
</style></head><body>
<div class="top"><span class="mast">3rd &amp; Long</span><span class="edition">{kicker}</span></div>
<div><h1>{title}</h1></div>
<div class="foot"><span>{left}</span><span class="dim">{right}</span></div>
<div class="bars"><i class="a"></i><i class="p"></i><i class="n"></i></div>
</body></html>"""

ICON = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>*{box-sizing:border-box;margin:0;padding:0}
html,body{width:512px;height:512px;overflow:hidden}
svg{display:block}</style></head><body>
<!-- Goalposts head-on. Pure geometry, no webfont: favicons never load one. -->
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <rect width="512" height="512" fill="#101418"/>
  <g fill="#F2C74A">
    <rect x="112" y="70" width="88" height="185"/>
    <rect x="312" y="70" width="88" height="185"/>
    <rect x="112" y="255" width="288" height="88"/>
    <rect x="212" y="343" width="88" height="99"/>
  </g>
</svg></body></html>"""

CARDS = [
 ("og.png", "3rd &amp; Long", "NFL Reports", "Adam Long", "Four editions", 104),
 ("og-2026-preseason.png", "2026&ndash;2027 NFL Preseason Report", "Preseason", "By Adam Long", "2026", 82),
 ("og-2025-midseason.png", "2025 NFL Midseason Report", "Midseason", "By Adam Long", "2025", 90),
 ("og-2025-preseason.png", "2025&ndash;2026 NFL Preseason Report", "Preseason", "By Adam Long", "2025", 82),
 ("og-2024-midseason.png", "2024 NFL Midseason Report", "Midseason", "By Adam Long", "2024", 90),
]

async def shot(page, path, w, h, dest):
    await page.set_viewport_size({"width": w, "height": h})
    await page.goto("file://" + str(path), wait_until="networkidle")
    await page.evaluate("document.fonts.ready")
    await page.wait_for_timeout(500)
    await page.screenshot(path=str(dest))
    print("rendered", dest.name)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(device_scale_factor=1)
        for name, title, kicker, left, right, size in CARDS:
            f = TMP / (name + ".html")
            f.write_text(CARD.format(title=title, kicker=kicker, left=left,
                                     right=right, size=size), encoding="utf-8")
            await shot(pg, f, 1200, 630, OUT / "assets/img" / name)
        f = TMP / "icon.html"; f.write_text(ICON, encoding="utf-8")
        await shot(pg, f, 512, 512, OUT / "icon-512.png")
        await b.close()

asyncio.run(main())
