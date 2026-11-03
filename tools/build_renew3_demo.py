"""5ページから、RENEW第3次のデモ（renew3/）を作る。?mode=before（改修前）／renew2（前回）／renew3（今回、既定）。
本文・リンク・フォームの送信先は元ページのまま。足すのは写真・見出し枠・案内（新規の文言は renew3/NOTES に列挙）。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
V = '20261104a'
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
CTA = {
    'consulting': ('#contact', '無料相談', 'Free consultation'),
    'media': ('#contact', '取材のご相談', 'Press inquiry'),
}
LOADER_CSS = ('<script>(function(){var q=new URLSearchParams(location.search),m=q.get("mode"),d=document,r=d.documentElement,a=q.get("accent");'
              'm=m==="before"||m==="renew2"?m:"renew3";r.setAttribute("data-mode",m);r.classList.add("js");r.setAttribute("data-accent",/^(gold|yellow)$/.test(a)?a:"orange");r.setAttribute("data-hero",q.get("hero")==="b"?"b":"a");'
              'var h=m==="before"?\'<link rel="stylesheet" href="../anim/site.css?v=20261020a">\':\'<link rel="stylesheet" href="../renew/renew.css?v=20261103a"><link rel="stylesheet" href="../renew2/renew2.css?v=20261103b">\'+(m==="renew3"?\'<link rel="stylesheet" href="renew3.css?v=' + V + '">\':"");d.write(h)})()</script>')
LOADER_JS = ('<script>(function(){var m=document.documentElement.getAttribute("data-mode"),h=m==="before"?\'<script src="../anim/site.js?v=20261020a"><\\/script>\':\'<script src="../renew/renew.js?v=20261103a"><\\/script><script src="../renew2/renew2.js?v=20261103b"><\\/script>\'+(m==="renew3"?\'<script src="renew3.js?v=' + V + '"><\\/script>\':"");document.write(h)})()</script>')
BAR = ('<details class="rn-bar"><summary>デモ用（本番には出ません）</summary><div role="group" aria-label="デモの切り替え">'
       '<button type="button" data-mode="before">改修前</button><button type="button" data-mode="renew2">前回のRENEW2</button><button type="button" data-mode="renew3">今回のRENEW3</button>'
       '<span>ファーストビュー</span><button type="button" data-hero="a">C案（既定）</button><button type="button" data-hero="b">B案（全面写真）</button>'
       '<span>アクセント色</span><button type="button" data-accent="orange">オレンジ</button><button type="button" data-accent="gold">ゴールド</button><button type="button" data-accent="yellow">イエロー</button></div></details>')
BARCSS = ('<style>.rn-bar{position:fixed;left:12px;bottom:12px;z-index:300;background:#fffcf3;color:#1c2b45;border:2px solid #1c2b45;border-radius:10px;font:13px/1.5 system-ui,sans-serif;max-width:calc(100vw - 24px)}'
          '.rn-bar summary{cursor:pointer;padding:6px 12px;font-size:12px;font-weight:700}.rn-bar>div{display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:4px 10px 10px}'
          '.rn-bar button,.rn-bar a{font:inherit;font-weight:700;border:1.5px solid #c9bfa3;background:#fff;color:#1c2b45;border-radius:999px;padding:4px 11px;cursor:pointer;text-decoration:none}'
          '.rn-bar button[aria-pressed=true]{background:#1c2b45;border-color:#1c2b45;color:#fbf6e9}.rn-bar span{font-size:12px;opacity:.7;margin:0 2px 0 6px}'
          'html[data-mode=before] .lang .lg,html[data-mode=before] .hd-cta,html[data-mode=before] .ft-nav,html[data-mode=before] .r3{display:none}'
          'html:not([data-mode=before]) .lang>span[lang]{display:none}</style>')
NAV = ('<nav class="ft-nav" aria-label="サイト内リンク / Site links">'
       '<a href="menu.html"><span lang="ja">メニュー</span><span lang="en">Menu</span></a>'
       '<a href="about.html"><span lang="ja">会社概要</span><span lang="en">About us</span></a>'
       '<a href="consulting.html"><span lang="ja">コンサルティング</span><span lang="en">Consulting</span></a>'
       '<a href="media.html"><span lang="ja">取材のお問い合わせ</span><span lang="en">Media inquiries</span></a></nav>')
# フッターの会社情報・認証（文言は会社概要・トップの既存の文言のみ）
FT_EXTRA = ('<div class="ft-co r3"><div><b><span lang="ja">株式会社飯野</span><span lang="en">Iino Co., Ltd.</span></b>'
            '<span lang="ja">〒135-0034 東京都江東区永代2-35-8</span><span lang="en">2-35-8 Eitai, Koto-ku, Tokyo 135-0034</span></div>'
            '<ul class="ft-aw"><li><img src="../images/award-gig.png" alt="Validated Gluten Free Safe Spot"><span lang="ja">アジア初 GIG認証</span><span lang="en">First GIG-certified in Asia</span></li>'
            '<li><img src="../images/award-gf-product-of-the-year.png" alt="Gluten-Free Product of the Year 2020"><span lang="ja">プロダクト・オブ・ザ・イヤー2020</span><span lang="en">Product of the Year 2020</span></li>'
            '<li><img src="../images/award-food-action-nippon.png" alt="Food Action Nippon Award 2019"><span lang="ja">フードアクションニッポン2019</span><span lang="en">Food Action Nippon 2019</span></li>'
            '<li><img src="../images/award-tripadvisor.png" alt="Tripadvisor"><span lang="ja">トリップアドバイザー東京No.1（2019）</span><span lang="en">Tripadvisor No.1 Tokyo (2019)</span></li></ul></div>')
SEND_NOTE = '<p class="req-note r3"><span lang="ja"><em>*</em> は必須項目です</span><span lang="en"><em>*</em> Required</span></p>'

def sub1(pat, rep, s, **kw):
    n, c = re.subn(pat, rep, s, count=1, **kw)
    assert c == 1, pat
    return n

for name in PAGES:
    h = (root/f'{name}.html').read_text(encoding='utf-8')
    h = re.sub(r'(href|src)="(style\.css|script\.js|anim/|images/)', r'\1="../\2', h)
    h = re.sub(r"url\('(images/)", r"url('../\1", h)
    h = sub1(r'<link rel="stylesheet" href="\.\./anim/site\.css[^>]*>', LOADER_CSS + '\n' + BARCSS, h)
    h = sub1(r'<script src="\.\./anim/site\.js[^>]*></script>', LOADER_JS, h)
    h = sub1(r'<body( class="sub")?>', lambda m: f'<body{m.group(1) or ""} data-page="{name}">', h)
    h = sub1(r'(<button class="lang"[^>]*data-lang-toggle[^>]*>.*?)(</button>)',
             r'\1<span class="lg lg-ja">日本語</span><span class="lg lg-en">EN</span>\2', h, flags=re.S)
    if name in CTA:
        href, ja, en = CTA[name]
        cta = f'<a class="btn sm hd-cta" href="{href}"><span lang="ja">{ja}</span><span lang="en">{en}</span></a>'
        h = sub1(r'(<a class="btn sm rsv hd-rsv"[^>]*>.*?</a>)', r'\1\n      ' + cta, h, flags=re.S)
        h = sub1(r'(<div class="drawer-foot">)', r'\1' + cta, h)
    if name == 'media':
        h = h.replace('<section class="blk contact">', '<section class="blk contact" id="contact">', 1)
    h = h.replace('>📞 ', '><span class="emo">📞 </span>').replace('>📍 ', '><span class="emo">📍 </span>')

    if name == 'index':
        # 1) レストラン紹介：料理・店内の写真を添える
        h = sub1(r'(<section class="blk"><div class="wrap about">)',
                 r'\1\n  <div class="about-ph r3"><img class="a1" src="../images/entrance.jpg" alt="" loading="lazy"><img class="a2" src="../images/interior.jpg" alt="" loading="lazy"></div>', h)
        # 2) 「100%」を数字として目立たせる（本文は変えない。英語本文の「100% gluten-free」に合わせた表示）
        h = sub1(r'(<div class="points">)',
                 '<div class="gf100 r3" aria-hidden="true"><b>100<small>%</small></b><span lang="ja">グルテンフリー</span><span lang="en">gluten-free</span></div>\n    \\1', h)
        # 3) ケータリング：お弁当の写真を主役に、チラシは添える
        h = sub1(r'(<a class="flyer")', r'<div class="cater-vis"><img class="cater-ph r3" src="../images/bento.jpg" alt="" loading="lazy">\n  \1', h)
        h = sub1(r'(<span><span lang="ja">タップで拡大</span><span lang="en">Tap to enlarge</span></span>\n  </a>)', r'\1\n  </div>', h)
    if name == 'menu':
        h = sub1(r'(<div class="menu-actions">)', r'\1\n    <p class="ma-lead r3"><span lang="ja">お選びいただいたメニューは、そのままご予約へ。</span><span lang="en">Found something you like? Reserve your table.</span></p>', h)
    if name == 'consulting':
        note = ('<p class="cert-note r3"><span lang="ja"><b>GFCO</b>はお菓子・食品などの「商品」向け、<b>GFFS</b>は「レストラン」向けの認証です。</span>'
                '<span lang="en"><b>GFCO</b> certifies products such as packaged foods; <b>GFFS</b> certifies restaurants.</span></p>')
        h = sub1(r'(<div class="svc-list">)', note + r'\n  \1', h)
        mid = ('<div class="cta-band r3"><p><b><span lang="ja">まずは30分、無料でご相談ください。</span><span lang="en">Start with a free 30-minute consultation.</span></b>'
               '<span lang="ja">オンライン相談もOKです。</span><span lang="en">Online consultations are available.</span></p>'
               '<a class="btn" href="#contact"><span lang="ja">初回30分 無料相談を予約</span><span lang="en">Book a free 30-minute consultation</span></a></div>')
        # サービス一覧の直後（#services の閉じ）に差し込む
        h = sub1(r'(</article>\s*</div>\s*)(</div></section>\s*<section class="sec">\s*<div class="wrap sec-in">\s*<div class="sec-head"><h2><span lang="ja">今、)',
                 lambda m: m.group(1) + mid + '\n' + m.group(2), h)
    if name in ('media', 'consulting'):
        h = re.sub(r'(<form class="cf7 demo"[^>]*>)', r'\1\n    ' + SEND_NOTE, h, count=1)
    # フッター：全ページ共通（店舗・会社・認証・リンク）
    h = h.replace('<div class="copy">', NAV + '\n  ' + FT_EXTRA + '\n  <div class="copy">', 1)
    h = h.replace('</body>', BAR + '\n<script src="demo.js?v=' + V + '"></script></body>', 1)
    (root/'renew3'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
