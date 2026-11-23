// Fotografa cada estado das telas com abas (modo pdf + __pdfEstado), para conferir.
//   node fonte/abas.mjs <url do index.html> <pasta>
import { chromium } from '/Volumes/hd caique becker/Mac Caique/Projetos/ariuno-videos/node_modules/playwright/index.mjs';
import { mkdirSync } from 'node:fs';
const BASE = process.argv[2]; const OUT = process.argv[3]; mkdirSync(OUT, { recursive: true });
const nav = await chromium.launch({ channel: 'chrome' });
const pg = await nav.newPage({ viewport: { width: 1600, height: 900 } });
pg.on('pageerror', e => console.log('ERRO', e.message));
await pg.goto(BASE + '?pdf=1#1', { waitUntil: 'networkidle' }); await pg.evaluate(() => document.fonts.ready);
const total = await pg.evaluate(() => document.querySelectorAll('.tela').length);
for (let n = 1; n <= total; n++) {
  await pg.evaluate(n => { location.hash = '#' + n; }, n); await pg.waitForTimeout(400);
  const k = await pg.evaluate(() => window.__pdfEstados());
  for (let e = 1; e < k; e++) {
    await pg.evaluate(e => window.__pdfEstado(e), e); await pg.waitForTimeout(900);
    await pg.screenshot({ path: `${OUT}/${String(n).padStart(2, '0')}-${e}.jpg`, type: 'jpeg', quality: 70 });
  }
}
await nav.close(); console.log('ok');
