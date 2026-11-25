#!/usr/bin/env node
/* QA 用の撮影スクリプト（Playwright。環境に入っているものを使い、追加のインストールはしない）
   使い方（リポジトリの一番上で）:
     node tools/shots.js --site warm-c --pages index,menu --widths 375,390 --langs ja,en --out /mnt/project-files/<作業>/shots/qa
   省略時: --site split  --pages index,menu,about,consulting,media  --widths 375,390,430,768,1440  --langs ja,en
   オプション: --query "fv=2&bg=b"（URL に付けて撮る） --top（ファーストビューだけ撮る。省略時はページ全体） --drawer（SP幅でメニューを開いた状態も撮る）
   出力: {out}/{page}-{lang}-{width}.png と {out}/report.json。
   各画面で、横スクロール（はみ出し）、コンソールのエラー、読み込めなかったローカルのファイルを記録し、最後に一覧を表示する。
   撮っただけで終わりにしない。QA は画像を必ず開いて、実際の表示を確認する。 */
const http = require('http'), fs = require('fs'), path = require('path');
let pw; try { pw = require('playwright'); } catch (e) { pw = require('/opt/node-tools/node_modules/playwright'); }

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const flag = k => process.argv.includes('--' + k);
const ROOT = path.resolve(__dirname, '..');
const site = arg('site', 'split');
const pages = arg('pages', 'index,menu,about,consulting,media').split(',');
const widths = arg('widths', '375,390,430,768,1440').split(',').map(Number);
const langs = arg('langs', 'ja,en').split(',');
const query = arg('query', '');  // 例: --query "fv=2&bg=b"（デモの切り替えを指定して撮る。名前の末尾に付く）
const out = path.resolve(arg('out', path.join(ROOT, '.shots', site)));
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.json': 'application/json' };

// リポジトリの一番上をそのまま配る小さなサーバー（ポートは空いているものを自動で使う）
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  let f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}/${site}/`;
  fs.mkdirSync(out, { recursive: true });
  const browser = await pw.chromium.launch();
  const report = [];
  for (const lang of langs) for (const page of pages) for (const w of widths) {
    const url = base + (lang === 'en' ? 'en/' : '') + (page === 'index' ? '' : page + '/') + (query ? '?' + query : '');
    const mobile = w < 768;
    const ctx = await browser.newContext({ viewport: { width: w, height: mobile ? 844 : (w < 1200 ? 1024 : 900) },
      deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile });
    const pg = await ctx.newPage();
    const errors = [], missing = [], external = [];
    // 読み込み失敗はリクエスト側で数えるので、コンソールの「Failed to load resource」は除く
    pg.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push(m.text().slice(0, 200)); });
    // 外部（glutenfree.co.jp や Google Fonts など）の読み込み失敗は環境のせいのことが多いので、別に数える
    pg.on('requestfailed', r => { if (!r.url().startsWith(base.split('/' + site)[0])) external.push(r.url().slice(0, 120)); else missing.push('failed ' + r.url().replace(/^https?:\/\/[^/]+/, '')); });
    pg.on('pageerror', e => errors.push(String(e).slice(0, 200)));
    pg.on('response', r => { if (r.status() >= 400 && r.url().startsWith(base.split('/' + site)[0])) missing.push(r.status() + ' ' + r.url().replace(/^https?:\/\/[^/]+/, '')); });
    const res = await pg.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(e => null);
    await pg.waitForTimeout(600);
    // 遅延読み込みの画像も写るように、loading=lazy を外す
    await pg.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'));
    // 遅延表示の要素を出すため、一度下まで流してから上に戻す
    await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
    await pg.waitForLoadState('networkidle').catch(() => {});
    await pg.waitForTimeout(400);
    const over = await pg.evaluate(() => {
      const W = document.documentElement.clientWidth, list = [];
      document.querySelectorAll('body *').forEach(el => { const r = el.getBoundingClientRect();
        if (r.width && (r.right > W + 1 || r.left < -1) && getComputedStyle(el).position !== 'fixed') list.push((el.className && typeof el.className === 'string' ? el.tagName.toLowerCase() + '.' + el.className.split(' ')[0] : el.tagName.toLowerCase()) + ' ' + Math.round(r.left) + '–' + Math.round(r.right)); });
      return { scrollWidth: document.documentElement.scrollWidth, clientWidth: W, height: document.documentElement.scrollHeight, overflowing: list.slice(0, 8) };
    });
    const name = `${page}-${lang}-${w}${query ? '-' + query.replace(/[^a-z0-9]+/gi, '') : ''}.png`;
    await pg.screenshot({ path: path.join(out, name), fullPage: !flag('top') });
    let drawer = null;
    if (flag('drawer') && mobile) {
      const btn = await pg.$('.hd .menu-btn, .hd [aria-controls], .burger, .nav-toggle');
      if (btn) { await btn.click(); await pg.waitForTimeout(500); drawer = name.replace('.png', '-drawer.png'); await pg.screenshot({ path: path.join(out, drawer) }); }
    }
    report.push({ page, lang, width: w, url, status: res ? res.status() : 'error', shot: name, drawer,
      hScroll: over.scrollWidth > over.clientWidth, scrollWidth: over.scrollWidth, height: over.height, overflowing: over.overflowing, errors, missing, external });
    await ctx.close();
  }
  await browser.close(); server.close();
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  for (const r of report) {
    const bad = [r.status !== 200 && 'HTTP ' + r.status, r.hScroll && `横スクロール（${r.scrollWidth}px）`, r.errors.length && `エラー ${r.errors.length}件`, r.missing.length && `読み込めないファイル ${r.missing.length}件`].filter(Boolean);
    const note = r.external.length ? `（外部の読み込み失敗 ${r.external.length}件は参考）` : '';
    console.log(`${bad.length ? '要確認' : 'OK    '} ${r.shot}  高さ${r.height}px  ${bad.join(' / ')} ${note}`);
  }
  console.log('画像と report.json: ' + out);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
