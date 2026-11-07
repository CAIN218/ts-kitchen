"""5ページ（ルートの本番用HTML）から、プレビュー renew14/ を作る。
読み込むCSS・JS（renew〜renew14 の改修分）はすべて renew14/ の中にある。デモ用の切り替えパネルは無し（2026-11-05 yuga の指示で削除）。
本文・リンク・フォームの送信先は元ページのまま。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
V = '20261117a'
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
CTA = {}
LOADER_CSS = ('<script>(function(){var q=new URLSearchParams(location.search),m=q.get("mode"),d=document,r=d.documentElement,a=q.get("accent");'
              'm="renew14";r.setAttribute("data-mode",m);r.classList.add("js");r.setAttribute("data-accent","orange");r.setAttribute("data-hero","a");'
              'var h=\'<link rel="stylesheet" href="renew.css?v=20261103a"><link rel="stylesheet" href="renew2.css?v=20261103b"><link rel="stylesheet" href="renew3.css?v=20261104a"><link rel="stylesheet" href="renew4.css?v=20261105a"><link rel="stylesheet" href="renew5.css?v=20261106a"><link rel="stylesheet" href="renew6.css?v=20261107a"><link rel="stylesheet" href="renew7.css?v=20261108a"><link rel="stylesheet" href="renew8.css?v=20261109c"><link rel="stylesheet" href="renew9.css?v=20261110a"><link rel="stylesheet" href="renew10.css?v=20261111a"><link rel="stylesheet" href="renew11.css?v=20261112a"><link rel="stylesheet" href="renew13.css?v=20261114a"><link rel="stylesheet" href="renew14.css?v=' + V + '">\';d.write(h)})()</script>')
LOADER_JS = ('<script>(function(){var m=document.documentElement.getAttribute("data-mode"),h=\'<script src="renew.js?v=20261103a"><\\/script><script src="renew2.js?v=20261103b"><\\/script><script src="renew4.js?v=20261105a"><\\/script><script src="renew5.js?v=20261106a"><\\/script><script src="renew6.js?v=20261107a"><\\/script><script src="renew14.js?v=' + V + '"><\\/script>\';document.write(h)})()</script>')
NAV = ('<nav class="ft-nav" aria-label="サイト内リンク / Site links">'
       '<a href="menu.html"><span lang="ja">メニュー</span><span lang="en">Menu</span></a>'
       '<a href="about.html"><span lang="ja">会社概要</span><span lang="en">About us</span></a>'
       '<a href="consulting.html"><span lang="ja">コンサルティング</span><span lang="en">Consulting</span></a>'
       '<a href="media.html"><span lang="ja">取材のお問い合わせ</span><span lang="en">Media inquiries</span></a></nav>')
# フッターの会社情報・認証（文言は会社概要・トップの既存の文言のみ）
FT_EXTRA = ('<div class="ft-co r3"><div><b><span lang="ja">株式会社飯野</span><span lang="en">Iino Co., Ltd.</span></b>'
            '<span lang="ja">〒135-0034 東京都江東区永代2-35-8</span><span lang="en">2-35-8 Eitai, Koto-ku, Tokyo 135-0034</span></div>'
            '<ul class="ft-aw"><li><img src="../src/images/award-gig.png" alt="Validated Gluten Free Safe Spot"><span lang="ja">アジア初 GIG認証</span><span lang="en">First GIG-certified in Asia</span></li>'
            '<li><img src="../src/images/award-gf-product-of-the-year.png" alt="Gluten-Free Product of the Year 2020"><span lang="ja">プロダクト・オブ・ザ・イヤー2020</span><span lang="en">Product of the Year 2020</span></li>'
            '<li><img src="../src/images/award-food-action-nippon.png" alt="Food Action Nippon Award 2019"><span lang="ja">フードアクションニッポン2019</span><span lang="en">Food Action Nippon 2019</span></li>'
            '<li><img src="../src/images/award-tripadvisor.png" alt="Tripadvisor"><span lang="ja">トリップアドバイザー東京No.1（2019）</span><span lang="en">Tripadvisor No.1 Tokyo (2019)</span></li></ul></div>')
SEND_NOTE = '<p class="req-note r3"><span lang="ja"><em>*</em> は必須項目です</span><span lang="en"><em>*</em> Required</span></p>'

def sub1(pat, rep, s, **kw):
    n, c = re.subn(pat, rep, s, count=1, **kw)
    assert c == 1, pat
    return n

for name in PAGES:
    h = (root/'src'/f'{name}.html').read_text(encoding='utf-8')
    h = re.sub(r'(href|src)="(style\.css|script\.js|anim/|images/)', r'\1="../src/\2', h)
    h = re.sub(r"url\('(images/)", r"url('../src/\1", h)
    h = sub1(r'<link rel="stylesheet" href="\.\./src/anim/site\.css[^>]*>', LOADER_CSS, h)
    h = sub1(r'<script src="\.\./src/anim/site\.js[^>]*></script>', LOADER_JS, h)
    h = sub1(r'<body( class="sub")?>', lambda m: f'<body{m.group(1) or ""} data-page="{name}">', h)
    if name == 'consulting':
        # 6) ヘッダー・ドロワーのボタン：レストラン予約ではなく、ページ内のお問い合わせフォームへ（文言は yuga の指示どおり）
        h = sub1(r'<a class="btn sm rsv hd-rsv" href="[^"]*"><span lang="ja">予約する</span><span lang="en">Book</span></a>',
                 '<a class="btn sm hd-rsv hd-consult" href="#contact"><span lang="ja">無料相談</span><span lang="en">Free consultation</span></a>', h)
        h = sub1(r'<div class="drawer-foot"><a class="btn sm rsv" href="[^"]*"><span lang="ja">予約する</span><span lang="en">Book a table</span></a></div>',
                 '<div class="drawer-foot"><a class="btn sm hd-consult" href="#contact"><span lang="ja">無料相談</span><span lang="en">Free consultation</span></a></div>', h)
    if name == 'menu':
        # デモはフォルダが1段深いので、メニュー切り替えのスクリプト内の画像パス（六本木店のお料理・デザート）も ../src/images/ に合わせる
        # （以前のデモでは renewN/images/ を探して表示されなかった。本番用の build_wp.py は別の方法で置き換えているので影響なし）
        h = h.replace("'images/menu-roppongi", "'../src/images/menu-roppongi")
        h = sub1(r"/\^\(https\?:\|images\\/\)/", lambda m: r"/^(https?:|(\.\.\/src\/)?images\/)/", h)
    if name == 'media':
        h = h.replace('<section class="blk contact">', '<section class="blk contact" id="contact">', 1)

    if name == 'index':
        # 1) レストラン紹介：料理・店内の写真を添える
        h = sub1(r'(<section class="blk"><div class="wrap about">)',
                 r'\1\n  <div class="about-ph r3"><img class="a1" src="../src/images/entrance.jpg" alt="" loading="lazy"></div>', h)
        # 3) ケータリング：お弁当の写真を主役に、チラシは添える
        h = sub1(r'(<a class="flyer")', r'<div class="cater-vis"><img class="cater-ph r3" src="../src/images/bento.jpg" alt="" loading="lazy">\n  \1', h)
        h = sub1(r'(<span><span lang="ja">タップで拡大</span><span lang="en">Tap to enlarge</span></span>\n  </a>)', r'\1\n  </div>', h)
        # 4) 公式SNS（yuga 承認：見出し「公式SNS」/"Follow Us"）：Instagram と YouTube を同じ形で並べる。
        #    Instagram の既存の文（@glutenfreetskitchen で最新情報を発信中）とリンク先・写真はそのまま。リンクの文言は案（yuga 確認待ち）
        IG_ICON = ('<svg class="sns-logo" viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><defs><radialGradient id="igg" cx="30%" cy="107%" r="150%">'
                   '<stop offset="0" stop-color="#fdf497"/><stop offset=".05" stop-color="#fdf497"/><stop offset=".45" stop-color="#fd5949"/><stop offset=".6" stop-color="#d6249f"/><stop offset=".9" stop-color="#285AEB"/></radialGradient></defs>'
                   '<rect width="48" height="48" rx="12" fill="url(#igg)"/><rect x="11" y="11" width="26" height="26" rx="8" fill="none" stroke="#fff" stroke-width="3"/>'
                   '<circle cx="24" cy="24" r="6.3" fill="none" stroke="#fff" stroke-width="3"/><circle cx="31.6" cy="16.4" r="1.9" fill="#fff"/></svg>')
        YT_ICON = ('<svg class="sns-logo" viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><rect x="2" y="9" width="44" height="30" rx="9" fill="#FF0000"/>'
                   '<path d="M20 17.5v13l11.2-6.5z" fill="#fff"/></svg>')
        EXT = '<svg class="sns-ext" viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 3H3v10h10v-3M9 3h4v4M13 3 7.5 8.5"/></svg>'
        NEWTAB = '<span class="vh"><span lang="ja">（新しいタブで開きます）</span><span lang="en">(opens in a new tab)</span></span>'
        def item(cls, href, icon, name, handle_html, go_ja, go_en):
            return (f'    <li><a class="sns-item {cls}" href="{href}" target="_blank" rel="noopener">{icon}<span class="sns-tx">'
                    f'<span class="sns-name">{name}</span><span class="sns-handle">{handle_html}</span>'
                    f'<span class="sns-go"><span lang="ja">{go_ja}</span><span lang="en">{go_en}</span>{EXT}</span>{NEWTAB}</span></a></li>')
        def sns(m):
            return ('<section class="blk sns-sec"><div class="wrap">\n  <h2><span lang="ja">公式SNS</span><span lang="en">Follow Us</span></h2>\n  <ul class="sns-list">\n'
                    + item('is-ig', 'https://www.instagram.com/glutenfreetskitchen/', IG_ICON, 'Instagram',
                           '@glutenfreetskitchen <span lang="ja">で最新情報を発信中</span><span lang="en">— follow us for the latest news</span>', 'アカウントを見る', 'View account') + '\n'
                    + item('is-yt', 'https://www.youtube.com/@glutenfreetskitchen', YT_ICON, 'YouTube', '@glutenfreetskitchen', 'チャンネルを見る', 'View channel')
                    + '\n  </ul>\n')
        h = sub1(r'<section class="blk" style="padding-top:0"><div class="wrap">\n  <h2>Instagram</h2>\n  <p class="lead"><a href="https://www\.instagram\.com/glutenfreetskitchen/">@glutenfreetskitchen</a> <span lang="ja">で最新情報を発信中</span><span lang="en">— follow us for the latest news</span></p>\n', sns, h)
    # ヘッダー・フッター：Instagram アイコン（a.sns）の横に、同じ大きさ・同じ線の YouTube アイコンを並べる（表示・非表示の条件も Instagram と同じ）
    YT_A = ('<a class="sns sns-yt-ic" href="https://www.youtube.com/@glutenfreetskitchen" aria-label="YouTube" target="_blank" rel="noopener">'
            '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="4.5"/>'
            '<path d="M10 9.2v5.6l4.8-2.8z" fill="currentColor" stroke="none"/></svg></a>')
    h, n_yt = re.subn(r'(<a class="sns" href="https://www\.instagram\.com/glutenfreetskitchen/"[^>]*>.*?</svg></a>)', lambda m: m.group(1) + YT_A, h)
    assert n_yt == 2, (name, n_yt)
    # フッター：各ページへのリンク（ヘッダーと同じ既存の表記のみ）
    h = h.replace('<div class="copy">', NAV + '\n  <div class="copy">', 1)
    h = h.replace('</body>', '<script src="form.js?v=' + V + '"></script></body>', 1)
    (root/'renew14'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
