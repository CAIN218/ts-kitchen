"""GitHub版のページから、WordPress（WPCodeのHTMLスニペット）用の断片を作る。
画像は {{IMG:ファイル名}} の形で残し、WordPressにアップロードしたURLに置き換えて使う。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
css = (root/'style.css').read_text(encoding='utf-8')
js = (root/'script.js').read_text(encoding='utf-8')
ABOUT = '/%e4%bc%9a%e7%a4%be%e6%a6%82%e8%a6%81/'
def links(s):
    s = s.replace('href="./"', 'href="/"').replace('href="menu.html"', 'href="/menu/"').replace('href="about.html"', 'href="'+ABOUT+'"')
    return re.sub(r'images/([a-z0-9-]+\.(?:jpg|png))', r'{{IMG:\1}}', s)
head = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">\n'
        "<script>(function(){var l='ja';try{l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('tsk-lang')||((navigator.language||'ja').toLowerCase().indexOf('ja')===0?'ja':'en')}catch(e){}document.documentElement.setAttribute('data-lang',l)})();</script>\n"
        '<style>\n/* WordPressテーマの影響を打ち消す */\nbody{margin:0!important;padding:0!important;background:#fff}\n.tsk-root h1,.tsk-root h2,.tsk-root h3,.tsk-root h4{font-family:inherit;margin:0;letter-spacing:normal;text-transform:none}\n.tsk-root p{margin:0}\n.tsk-root a{text-decoration-thickness:auto}\n.tsk-root img{height:auto}\n.tsk-root button{text-transform:none;letter-spacing:normal;box-shadow:none;min-height:0}\n.tsk-root{background:#fff}\n/* 新デザインのページでは、サイト共通のチラシのポップアップとreCAPTCHAバッジを出さない（チラシはケータリング欄に掲載） */\n.pum,.pum-overlay{display:none!important}\n.grecaptcha-badge{visibility:hidden!important}\nhtml.pum-open,html.pum-open body{overflow:auto!important}\n'
        + '/* ▼原宿店の写真：メディアにアップロードした画像のURLを url("...") の形で入れる（例：url("https://glutenfree.co.jp/wp-content/uploads/2026/10/harajuku.jpg")） */\n:root{--harajuku-photo:url(\"{{IMG:harajuku.jpg}}\")}\n'
        + links(css).replace('url("{{IMG:harajuku.jpg}}")','var(--harajuku-photo)') + '\n</style>\n')
for name in ['index', 'about', 'menu']:
    html = (root/f'{name}.html').read_text(encoding='utf-8')
    body = re.search(r'<body[^>]*>(.*?)<script src="script\.js[^"]*"></script>', html, re.S).group(1)
    out = ('<!-- Gluten Free T\'s Kitchen 新デザイン（GitHub: CAIN218/ts-kitchen の tools/build_wp.py で生成） -->\n'
           + head + '<div class="tsk-root" style="font-family:\'Noto Sans JP\',system-ui,sans-serif;color:#1f2933;line-height:1.7">\n'
           + links(body).strip() + '\n</div>\n<script>\n' + js + '\n</script>\n')
    (root/'wp'/f'{name}.html').write_text(out, encoding='utf-8')
    print(name, len(out), sorted(set(re.findall(r'\{\{IMG:([^}]+)\}\}', out))))
