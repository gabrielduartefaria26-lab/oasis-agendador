const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + __dirname + '/video.html'); await p.evaluate(() => document.fonts.ready);
  const dur = await p.evaluate(() => window.DURATION); console.log('duração', dur, errs);
  const ts = process.argv.slice(2).map(Number);
  for (const t of ts) { await p.evaluate(t => renderAt(t), t); await p.screenshot({ path: `${__dirname}/shot_${t}.png` }); }
  await b.close();
})();
