"""5ページから、RENEW第12次のデモ（renew12/：公式YouTubeの紹介を追加、メニューの六本木店の画像パスを修正）を作る。?mode=before（改修前）／renew2（前回）／renew3（今回、既定）。
本文・リンク・フォームの送信先は元ページのまま。足すのは写真・見出し枠・案内（新規の文言は renew3/NOTES に列挙）。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
V = '20261113a'
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
CTA = {}
LOADER_CSS = ('<script>(function(){var q=new URLSearchParams(location.search),m=q.get("mode"),d=document,r=d.documentElement,a=q.get("accent");'
              'm=m==="before"?m:"renew12";r.setAttribute("data-mode",m);r.classList.add("js");r.setAttribute("data-accent",/^(gold|yellow)$/.test(a)?a:"orange");r.setAttribute("data-hero",q.get("hero")==="b"?"b":"a");'
              'var h=m==="before"?\'<link rel="stylesheet" href="../anim/site.css?v=20261020a">\':\'<link rel="stylesheet" href="../renew/renew.css?v=20261103a"><link rel="stylesheet" href="../renew2/renew2.css?v=20261103b"><link rel="stylesheet" href="../renew3/renew3.css?v=20261104a"><link rel="stylesheet" href="../renew4/renew4.css?v=20261105a"><link rel="stylesheet" href="../renew5/renew5.css?v=20261106a"><link rel="stylesheet" href="../renew6/renew6.css?v=20261107a"><link rel="stylesheet" href="../renew7/renew7.css?v=20261108a"><link rel="stylesheet" href="../renew8/renew8.css?v=20261109c"><link rel="stylesheet" href="../renew9/renew9.css?v=20261110a"><link rel="stylesheet" href="../renew10/renew10.css?v=20261111a"><link rel="stylesheet" href="../renew11/renew11.css?v=20261112a"><link rel="stylesheet" href="renew12.css?v=' + V + '">\';d.write(h)})()</script>')
LOADER_JS = ('<script>(function(){var m=document.documentElement.getAttribute("data-mode"),h=m==="before"?\'<script src="../anim/site.js?v=20261020a"><\\/script>\':\'<script src="../renew/renew.js?v=20261103a"><\\/script><script src="../renew2/renew2.js?v=20261103b"><\\/script><script src="../renew4/renew4.js?v=20261105a"><\\/script><script src="../renew5/renew5.js?v=20261106a"><\\/script><script src="../renew6/renew6.js?v=20261107a"><\\/script><script src="renew12.js?v=' + V + '"><\\/script>\';document.write(h)})()</script>')
BAR = ('<details class="rn-bar"><summary>デモ用（本番には出ません）</summary><div role="group" aria-label="デモの切り替え">'
       '<button type="button" data-mode="before">改修前</button><button type="button" data-mode="renew12">今回のRENEW12</button><a href="../renew11/index.html">RENEW11へ</a><a href="../renew10/index.html">RENEW10へ</a><a href="../renew9/index.html">RENEW9へ</a><a href="../renew8/index.html">RENEW8へ</a><a href="../renew7/index.html">RENEW7へ</a><a href="../renew6/index.html">RENEW6へ</a><a href="../renew5/index.html">RENEW5へ</a><a href="../renew4/index.html">RENEW4へ</a><a href="../renew3/index.html">RENEW3へ</a>'
       '<span>アクセント色</span><button type="button" data-accent="orange">オレンジ</button><button type="button" data-accent="gold">ゴールド</button><button type="button" data-accent="yellow">イエロー</button></div></details>')
BARCSS = ('<style>.rn-bar{position:fixed;left:12px;bottom:12px;z-index:300;background:#fffcf3;color:#1c2b45;border:2px solid #1c2b45;border-radius:10px;font:13px/1.5 system-ui,sans-serif;max-width:calc(100vw - 24px)}'
          '.rn-bar summary{cursor:pointer;padding:6px 12px;font-size:12px;font-weight:700}.rn-bar>div{display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:4px 10px 10px}'
          '.rn-bar button,.rn-bar a{font:inherit;font-weight:700;border:1.5px solid #c9bfa3;background:#fff;color:#1c2b45;border-radius:999px;padding:4px 11px;cursor:pointer;text-decoration:none}'
          '.rn-bar button[aria-pressed=true]{background:#1c2b45;border-color:#1c2b45;color:#fbf6e9}.rn-bar span{font-size:12px;opacity:.7;margin:0 2px 0 6px}'
          'html[data-mode=before] .r3{display:none}</style>')
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
    if name == 'consulting':
        # 6) ヘッダー・ドロワーのボタン：レストラン予約ではなく、ページ内のお問い合わせフォームへ（文言は yuga の指示どおり）
        h = sub1(r'<a class="btn sm rsv hd-rsv" href="[^"]*"><span lang="ja">予約する</span><span lang="en">Book</span></a>',
                 '<a class="btn sm hd-rsv hd-consult" href="#contact"><span lang="ja">無料相談</span><span lang="en">Free consultation</span></a>', h)
        h = sub1(r'<div class="drawer-foot"><a class="btn sm rsv" href="[^"]*"><span lang="ja">予約する</span><span lang="en">Book a table</span></a></div>',
                 '<div class="drawer-foot"><a class="btn sm hd-consult" href="#contact"><span lang="ja">無料相談</span><span lang="en">Free consultation</span></a></div>', h)
    if name == 'menu':
        # デモはフォルダが1段深いので、メニュー切り替えのスクリプト内の画像パス（六本木店のお料理・デザート）も ../images/ に合わせる
        # （以前のデモでは renewN/images/ を探して表示されなかった。本番用の build_wp.py は別の方法で置き換えているので影響なし）
        h = h.replace("'images/menu-roppongi", "'../images/menu-roppongi")
        h = sub1(r"/\^\(https\?:\|images\\/\)/", lambda m: r"/^(https?:|(\.\.\/)?images\/)/", h)
    if name == 'media':
        h = h.replace('<section class="blk contact">', '<section class="blk contact" id="contact">', 1)

    if name == 'index':
        # 1) レストラン紹介：料理・店内の写真を添える
        h = sub1(r'(<section class="blk"><div class="wrap about">)',
                 r'\1\n  <div class="about-ph r3"><img class="a1" src="../images/entrance.jpg" alt="" loading="lazy"></div>', h)
        # 3) ケータリング：お弁当の写真を主役に、チラシは添える
        h = sub1(r'(<a class="flyer")', r'<div class="cater-vis"><img class="cater-ph r3" src="../images/bento.jpg" alt="" loading="lazy">\n  \1', h)
        h = sub1(r'(<span><span lang="ja">タップで拡大</span><span lang="en">Tap to enlarge</span></span>\n  </a>)', r'\1\n  </div>', h)
        # 4) 公式SNS：Instagram の紹介（文言はそのまま）の横に、公式YouTubeチャンネルへの導線を並べる（文言は案・yuga確認待ち）
        IG_SVG = '<svg class="sns-ic" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>'
        YT_SVG = '<svg class="sns-ic" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="4.5"/><path d="M10 9.2v5.6l4.8-2.8z" fill="currentColor" stroke="none"/></svg>'
        EXT = '<svg class="sns-ext" viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 3H3v10h10v-3M9 3h4v4M13 3 7.5 8.5"/></svg>'
        h = sub1(r'(  <p class="lead">)(<a href="https://www\.instagram\.com/glutenfreetskitchen/">@glutenfreetskitchen</a> <span lang="ja">で最新情報を発信中</span><span lang="en">— follow us for the latest news</span></p>)',
                 lambda m: '  <div class="sns-accts">\n  <p class="lead sns-acct">' + IG_SVG + m.group(2) + '\n  <p class="lead sns-acct"><a class="sns-yt" href="https://www.youtube.com/@glutenfreetskitchen" target="_blank" rel="noopener">' + YT_SVG
                   + '<span class="sns-h">@glutenfreetskitchen</span><span class="sns-go"><span lang="ja">YouTubeチャンネルを見る</span><span lang="en">Visit our YouTube channel</span>' + EXT
                   + '</span><span class="vh"><span lang="ja">（新しいタブで開きます）</span><span lang="en">(opens in a new tab)</span></span></a></p>\n  </div>', h)
    # フッター：各ページへのリンク（ヘッダーと同じ既存の表記のみ）
    h = h.replace('<div class="copy">', NAV + '\n  <div class="copy">', 1)
    h = h.replace('</body>', BAR + '\n<script src="demo.js?v=' + V + '"></script></body>', 1)
    (root/'renew12'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
