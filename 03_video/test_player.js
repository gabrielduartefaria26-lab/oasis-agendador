const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + process.argv[2]); await p.waitForTimeout(800);
  await p.click('#play-big'); await p.waitForTimeout(3000);
  console.log('tempo após 3s:', await p.textContent('#vtime'));
  await p.click('#mute'); console.log('mutado ok');
  await p.click('#pp'); const a = await p.textContent('#vtime'); await p.waitForTimeout(1000); console.log('pausado:', a, '->', await p.textContent('#vtime'));
  console.log('erros:', errs); await b.close();
})();
