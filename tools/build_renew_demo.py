"""5ページから、サイト全体リニューアルのデモ（renew/）を作る。?mode=before で改修前、既定は今回の改修後。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
V = '20261103a'
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
CTA = {  # ページの目的に合わせた主要ボタン（ヘッダー・メニュー）。href は同ページ内のフォーム
    'consulting': ('#contact', '無料相談', 'Free consultation'),
    'media': ('#contact', '取材のご相談', 'Press inquiry'),
}
LOADER_CSS = ('<script>(function(){var q=new URLSearchParams(location.search),m=q.get("mode")==="before"?"before":"renew",d=document,r=d.documentElement,a=q.get("accent");'
              'r.setAttribute("data-mode",m);r.classList.add("js");r.setAttribute("data-accent",/^(gold|yellow)$/.test(a)?a:"orange");'
              'd.write(m==="before"?\'<link rel="stylesheet" href="../anim/site.css?v=20261020a">\':\'<link rel="stylesheet" href="renew.css?v=' + V + '">\')})()</script>')
LOADER_JS = ('<script>document.write(document.documentElement.getAttribute("data-mode")==="before"?\'<script src="../anim/site.js?v=20261020a"><\\/script>\':\'<script src="renew.js?v=' + V + '"><\\/script>\')</script>')
BAR = ('<details class="rn-bar"><summary>デモ用（本番には出ません）</summary><div role="group" aria-label="デモの切り替え">'
       '<button type="button" data-mode="before">改修前</button><button type="button" data-mode="renew">今回の改修後</button>'
       '<a href="../refine/@PAGE@.html">前回のデモ</a><span>アクセント色</span>'
       '<button type="button" data-accent="orange">オレンジ</button><button type="button" data-accent="gold">ゴールド</button><button type="button" data-accent="yellow">イエロー</button></div></details>')
BARCSS = ('<style>.rn-bar{position:fixed;left:12px;bottom:12px;z-index:300;background:#fffcf3;color:#1c2b45;border:2px solid #1c2b45;border-radius:10px;font:13px/1.5 system-ui,sans-serif;max-width:calc(100vw - 24px)}'
          '.rn-bar summary{cursor:pointer;padding:6px 12px;font-size:12px;font-weight:700}.rn-bar>div{display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:4px 10px 10px}'
          '.rn-bar button,.rn-bar a{font:inherit;font-weight:700;border:1.5px solid #c9bfa3;background:#fff;color:#1c2b45;border-radius:999px;padding:4px 11px;cursor:pointer;text-decoration:none}'
          '.rn-bar button[aria-pressed=true]{background:#1c2b45;border-color:#1c2b45;color:#fbf6e9}.rn-bar span{font-size:12px;opacity:.7;margin:0 2px 0 6px}'
          'html[data-mode=before] .lang .lg,html[data-mode=before] .hd-cta,html[data-mode=before] .ft-nav{display:none}'
          'html[data-mode=renew] .lang>span[lang]{display:none}</style>')
NAV = ('<nav class="ft-nav" aria-label="サイト内リンク / Site links">'
       '<a href="menu.html"><span lang="ja">メニュー</span><span lang="en">Menu</span></a>'
       '<a href="about.html"><span lang="ja">会社概要</span><span lang="en">About us</span></a>'
       '<a href="consulting.html"><span lang="ja">コンサルティング</span><span lang="en">Consulting</span></a>'
       '<a href="media.html"><span lang="ja">取材のお問い合わせ</span><span lang="en">Media inquiries</span></a></nav>')
for name in PAGES:
    h = (root/f'{name}.html').read_text(encoding='utf-8')
    h = re.sub(r'(href|src)="(style\.css|script\.js|anim/|images/)', r'\1="../\2', h)
    h = re.sub(r"url\('(images/)", r"url('../\1", h)
    h = re.sub(r'<link rel="stylesheet" href="\.\./anim/site\.css[^>]*>', LOADER_CSS + '\n' + BARCSS, h, count=1)
    h = re.sub(r'<script src="\.\./anim/site\.js[^>]*></script>', LOADER_JS, h, count=1)
    h = re.sub(r'<body( class="sub")?>', lambda m: f'<body{m.group(1) or ""} data-page="{name}">', h, count=1)
    # 言語切替：日本語 / EN を並べて、いまの言語が分かるように
    h = re.sub(r'(<button class="lang"[^>]*data-lang-toggle[^>]*>.*?)(</button>)',
               r'\1<span class="lg lg-ja">日本語</span><span class="lg lg-en">EN</span>\2', h, flags=re.S)
    # ページごとの主要ボタン（改修後のみ表示）
    if name in CTA:
        href, ja, en = CTA[name]
        cta = f'<a class="btn sm hd-cta" href="{href}"><span lang="ja">{ja}</span><span lang="en">{en}</span></a>'
        h = re.sub(r'(<a class="btn sm rsv hd-rsv"[^>]*>.*?</a>)', r'\1\n      ' + cta, h, count=1, flags=re.S)
        h = re.sub(r'(<div class="drawer-foot">)', r'\1' + cta, h, count=1)
    if name == 'media':
        h = h.replace('<section class="blk contact">', '<section class="blk contact" id="contact">', 1)
    # 絵文字は飾りなので、改修後は隠す（改修前は今のまま）
    h = h.replace('>📞 ', '><span class="emo">📞 </span>').replace('>📍 ', '><span class="emo">📍 </span>')
    # フッターに、各ページへのリンク
    h = h.replace('<div class="copy">', NAV + '\n  <div class="copy">', 1)
    h = h.replace('</body>', BAR.replace('@PAGE@', name) + '\n<script src="demo.js?v=' + V + '"></script></body>', 1)
    (root/'renew'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
