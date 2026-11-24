// Rendert eine HTML-Datei als 1200x630-PNG (Vorschaubild). Aufruf: node og.cjs <html> <png>
let lib; try { lib = require('playwright'); } catch (e) { lib = null; }
(async () => {
  if (lib) {
    const b = await lib.chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
    await p.goto('file://' + process.argv[2]); await p.waitForTimeout(300); await p.screenshot({ path: process.argv[3] }); await b.close(); return;
  }
  const pup = require('puppeteer');
  const b = await pup.launch({ headless: true }); const p = await b.newPage(); await p.setViewport({ width: 1200, height: 630 });
  await p.goto('file://' + process.argv[2]); await new Promise(r => setTimeout(r, 300)); await p.screenshot({ path: process.argv[3] }); await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
