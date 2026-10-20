"""GitHub版のページから、WordPress（WPCodeのHTMLスニペット）用の断片を作る。
画像は {{IMG:ファイル名}} の形で残し、WordPressにアップロードしたURLに置き換えて使う。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
css = (root/'style.css').read_text(encoding='utf-8')
js = (root/'script.js').read_text(encoding='utf-8')
ABOUT = '/%e4%bc%9a%e7%a4%be%e6%a6%82%e8%a6%81/'
CONSULTING = 'https://glutenfree.co.jp/%e3%82%b3%e3%83%b3%e3%82%b5%e3%83%ab%e3%83%86%e3%82%a3%e3%83%b3%e3%82%b0/'
MEDIA = 'https://glutenfree.co.jp/%e3%83%a1%e3%83%87%e3%82%a3%e3%82%a2%e3%83%bb%e5%8f%96%e6%9d%90%e3%81%ae%e3%81%8a%e5%95%8f%e3%81%84%e5%90%88%e3%82%8f%e3%81%9b/'
# お問い合わせフォーム：GitHubのプレビューでは見本の見た目だけ。WordPressではContact Form 7（問合せ）に置き換える
CF7 = '[contact-form-7 id="8a2859b" title="問合せ"]'
# テーマ（Bootstrap・Hestia・Font Awesome）と名前がぶつかるクラスは、WordPress用の出力だけ tk- を付けて別名にする
CLASH = ('btn', 'fab', 'lead')
def rename_css(s):
    return re.sub(r'\.(' + '|'.join(CLASH) + r')(?![\w-])', r'.tk-\1', s)
def rename_html(s):
    def fix(m):
        return 'class="' + ' '.join(('tk-' + t) if t in CLASH else t for t in m.group(1).split()) + '"'
    return re.sub(r'class="([^"]*)"', fix, s)
def links(s):
    s = s.replace('href="./"', 'href="/"').replace('href="menu.html"', 'href="/menu/"').replace('href="about.html"', 'href="'+ABOUT+'"').replace('href="consulting.html"', 'href="'+CONSULTING+'"').replace('href="media.html"', 'href="'+MEDIA+'"')
    s = re.sub(r'<!--CF7-->.*?<!--/CF7-->', CF7, s, flags=re.S)
    return re.sub(r'images/([a-z0-9-]+\.(?:jpg|png))', r'{{IMG:\1}}', s)
head = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">\n'
        "<script>(function(){var l='ja';try{l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('tsk-lang')||((navigator.language||'ja').toLowerCase().indexOf('ja')===0?'ja':'en')}catch(e){}document.documentElement.setAttribute('data-lang',l)})();</script>\n"
        '<style>\n/* WordPressテーマの影響を打ち消す（:where で詳細度を最小にし、各ページ用のクラス指定が打ち消されないようにする） */\nbody{margin:0!important;padding:0!important;background:#fff}\n.tsk-root{background:#fff;font-size:16px;font-weight:400}\n:where(.tsk-root) h1,:where(.tsk-root) h2,:where(.tsk-root) h3,:where(.tsk-root) h4{font-family:inherit;margin:0;letter-spacing:normal;text-transform:none;font-weight:700;line-height:inherit}\n:where(.tsk-root) p,:where(.tsk-root) ul,:where(.tsk-root) ol,:where(.tsk-root) label{margin:0}\n:where(.tsk-root) p,:where(.tsk-root) li,:where(.tsk-root) ul,:where(.tsk-root) ol,:where(.tsk-root) div,:where(.tsk-root) span,:where(.tsk-root) a,:where(.tsk-root) label,:where(.tsk-root) small,:where(.tsk-root) figcaption,:where(.tsk-root) dd,:where(.tsk-root) dt,:where(.tsk-root) address{font-family:inherit;font-weight:inherit;font-size:inherit;line-height:inherit}\n.tsk-root a{text-decoration-thickness:auto}\n.tsk-root img{height:auto}\n:where(.tsk-root) button{text-transform:none;letter-spacing:normal;box-shadow:none;min-height:0;margin:0}\n/* 新デザインのページでは、サイト共通のチラシのポップアップとreCAPTCHAバッジを出さない（チラシはケータリング欄に掲載） */\n.pum,.pum-overlay{display:none!important}\n.grecaptcha-badge{visibility:hidden!important}\nhtml.pum-open,html.pum-open body{overflow:auto!important}\n'
        + '/* ▼原宿店の写真：メディアにアップロードした画像のURLを url("...") の形で入れる（例：url("https://glutenfree.co.jp/wp-content/uploads/2026/10/harajuku.jpg")） */\n:root{--harajuku-photo:url(\"{{IMG:harajuku.jpg}}\")}\n'
        + rename_css(links(css)).replace('url("{{IMG:harajuku.jpg}}")','var(--harajuku-photo)') + '\n</style>\n')
for name in ['index', 'about', 'menu', 'consulting', 'media']:
    html = (root/f'{name}.html').read_text(encoding='utf-8')
    body = re.search(r'<body[^>]*>(.*?)<script src="script\.js[^"]*"></script>', html, re.S).group(1)
    out = ('<!-- Gluten Free T\'s Kitchen 新デザイン（GitHub: CAIN218/ts-kitchen の tools/build_wp.py で生成） -->\n'
           + head + '<div class="tsk-root" style="font-family:\'Noto Sans JP\',system-ui,sans-serif;color:#1f2933;line-height:1.7">\n'
           + rename_html(links(body)).strip() + '\n</div>\n<script>\n' + js + '\n</script>\n')
    (root/'wp'/f'{name}.html').write_text(out, encoding='utf-8')
    print(name, len(out), sorted(set(re.findall(r'\{\{IMG:([^}]+)\}\}', out))))
