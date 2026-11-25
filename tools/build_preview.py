"""src/ の5ページから、プレビュー split/（日本語 / 、英語 /en/）を作る。
読み込むCSS・JS（renew〜renew14 の改修分）はすべて assets/ の中にある。ほかのデモは 2026-11-22 yuga の指示で削除（git の履歴から戻せる）。
本文・リンク・フォームの送信先は元ページのまま。"""
import re, pathlib, os, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import langsplit as LS
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

WARM_V = '20261125g'
WARM_NAME = {'a': ('白い食卓', 'Light'), 'b': ('黒板と赤い扉', 'Chalkboard'), 'c': ('紺の誌面', 'Navy')}
def warm(x, look, name, lang, up, rel):
    """Warm Editorial のデモ用。文言は変えず、上乗せCSS・data属性・デモの切り替え（フッター最下部）だけを足す。
    並べ替えなどのHTML変換は warm_a_html / warm_b_html に書く。"""
    x = x.replace('<html ', f'<html data-warm="{look}" ', 1)
    x = x.replace('</head>', f'<link rel="stylesheet" href="{up}assets/warm-{look}.css?v={WARM_V}"></head>', 1)
    x = warm_common(x, name, lang, up, rel)
    x = (warm_b_html if look == 'b' else warm_a_html)(x, name, lang)  # C（紺）は A と同じ組み方
    if look == 'c':
        if name == 'index':
            x = warm_c_reserve(x, lang)
        x = warm_c_html(x, name, lang, up, rel)
    # 電話・地図の 📞 📍 は全案で消す（yuga 2026-11-24「地図とか電話はどれも絵文字なし」）。番号と「地図」/「Map」は残す
    x = re.sub(r'(?:📞|📍)[  ]?', '', x)
    # 元のフォントURLは Fraunces の指定（opsz,wght@9..144,500;600;700）が書式違いで 400 エラーになり、4書体とも読み込まれない。デモでは正しい書き方に直す（本番は要確認）
    x = x.replace('Fraunces:opsz,wght@9..144,500;600;700', 'Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700')
    x = x.replace('</body>', f'<script src="{up}assets/warm.js?v={WARM_V}"></script></body>', 1)
    if look == 'c':
        # 案C：差し色の切り替え（デモ用）など。html[data-acc] は先に決めておき、読み込み時のちらつきを防ぐ
        x = x.replace('<html ', '<html data-acc="3" ', 1)
        x = x.replace('</body>', f'<script src="{up}assets/warm-c.js?v={WARM_V}"></script></body>', 1)
    cur = rel(name, lang)
    sw = ('<p class="demo-switch">' + ('デザイン案：' if lang == 'ja' else 'Design: ')
          + ' / '.join(
              (f'<b aria-current="true">{lab}</b>' if k == look else f'<a href="{up}{d}/{cur_path(name, lang)}">{lab}</a>')
              for k, d, lab in (('split', 'split', '今のデザイン' if lang == 'ja' else 'Current'),
                                ('a', 'warm-a', 'A ' + WARM_NAME['a'][0 if lang == 'ja' else 1]),
                                ('b', 'warm-b', 'B ' + WARM_NAME['b'][0 if lang == 'ja' else 1]),
                                ('c', 'warm-c', 'C ' + WARM_NAME['c'][0 if lang == 'ja' else 1])))
          + '</p>')
    return x.replace('</footer>', sw + '\n</footer>', 1)

def cur_path(name, lang):
    return ('en/' if lang == 'en' else '') + LS.SLUG[name]

def warm_common(x, name, lang, up, rel):
    """両案共通のHTML変換（デザイン批評 H4：2案とも同じ情報設計にそろえ、違いは誌面で比べる）。文言は既存のものだけ。"""
    if name != 'index':
        return x
    # 1) 店舗を「レストランについて」の前へ（SPで店舗・電話・地図・予約に早く着く）
    m_about = re.search(r'<section class="blk"><div class="wrap about">.*?</div></section>\n', x, flags=re.S)
    m_st = re.search(r'<section class="blk stores" id="stores">.*?\n</div></section>\n', x, flags=re.S)
    assert m_about and m_st and m_about.start() < m_st.start()
    about, stores = m_about.group(0), m_st.group(0)
    x = x.replace(stores, '', 1).replace(about, stores + about, 1)
    # 2) 受賞の帯を main の中、ケータリングの前へ（受賞をSNSより前に）
    m_aw = re.search(r'\n<section class="awards-band".*?</section>\n', x, flags=re.S)
    assert m_aw
    aw = m_aw.group(0)
    x = x.replace(aw, '\n', 1).replace('<section class="blk" id="catering">', aw.strip('\n') + '\n<section class="blk" id="catering">', 1)
    # 3) コンサルティングへの入口（既存の文言だけ：コンサルページの見出しと、ナビの「コンサルティング」）
    h = ('貴社の売上と競争力を、<br>グルテンフリーで伸ばす。' if lang == 'ja' else 'Grow your sales and competitiveness with gluten-free.')
    # リンクの文言は、何が起きるか分かるよう、コンサルページの既存のボタンの文言をそのまま使い、お問い合わせ欄へ飛ばす（2回目の批評）
    nav = '初回30分 無料相談を予約' if lang == 'ja' else 'Book a free 30-minute consultation'
    band = (f'<section class="blk cons-band"><div class="wrap cons-band-in">'
            f'<img src="{up}src/images/owner.jpg" alt="" loading="lazy" width="538" height="807">'
            f'<div><h2>{h}</h2><a class="cons-link" href="{rel("consulting", lang)}#contact">{nav}</a></div></div></section>\n')
    x = x.replace('</main>', band + '</main>', 1)
    return x

def warm_c_reserve(x, lang):
    """案C：店舗ごとの「◯◯店を予約」（3つとも同じ TableCheck の店舗選択画面へのリンク）をやめ、
    キャンセルポリシーの後に、既存の「ご予約はこちらから」/「Make a reservation」の共通ボタンを1つ置く（yuga の問いを ux・批評で検討、2026-11-24）"""
    m = re.search(r'<section class="blk stores" id="stores">.*?\n</div></section>\n', x, flags=re.S)
    st = m.group(0)
    hrefs = set(re.findall(r'<a class="r rsv" href="([^"]+)"', st))
    assert len(hrefs) == 1, hrefs
    href = hrefs.pop()
    new, n = re.subn(r'<a class="r rsv" href="[^"]+">.*?</a>', '', st)
    assert n == 3
    label = 'ご予約はこちらから' if lang == 'ja' else 'Make a reservation'
    new = new[:-len('</div></section>\n')] + f'  <p class="stores-rsv"><a class="btn rsv" href="{href}"><span lang="{lang}">{label}</span></a></p>\n</div></section>\n'
    return x.replace(st, new, 1)

CONTACT_TYPES = (('media', '取材のお問い合わせ', 'Media inquiry'),
                 ('consulting', 'コンサルティングのご相談', 'Consulting'),
                 ('catering', 'ケータリング・お弁当', 'Catering & Bento'),
                 ('other', 'その他', 'Other'))
def contact_type_field(lang, sel=None):
    """お問い合わせの種類（yuga 2026-11-24 の提案。デモのみ。本番のCF7は変えない）"""
    lab = 'お問い合わせの種類' if lang == 'ja' else 'Type of inquiry'
    ph = '選択してください' if lang == 'ja' else 'Please choose'
    opts = ''.join(f'<option value="{k}"{" selected" if k == sel else ""}>{ja if lang == "ja" else en}</option>'
                   for k, ja, en in CONTACT_TYPES)
    first = '' if sel else f'<option value="" disabled selected>{ph}</option>'
    return (f'<p class="ctype"><label><span lang="{lang}">{lab}</span> <em>*</em>'
            f'<select name="type" required>{first}{opts}</select></label></p>\n    ')

def warm_c_html(x, name, lang, up, rel):
    """案C 3回目（yuga 2026-11-24）のHTML変換。文言は既存のもの＋yuga が指定した言葉だけ。"""
    ja = lang == 'ja'
    # 英字の小見出し（COMPANY / MENU など）は消す（「いらないかな」）。日付はそのまま残す
    x = re.sub(r'\s*<p class="eyebrow">[A-Z ]+</p>', '', x)
    x = x.replace('<p class="eyebrow">MEDIA ・ ', '<p class="eyebrow date">', 1)
    # コンサルの3領域に付いた英字のタグ（GFCO · Certification / R&D / Advisory）も同じ扱いで消す
    x = re.sub(r'<p class="svc-tag">[^<]*</p>', '', x)
    # 「取材のお問い合わせ」を「お問い合わせ」に（ナビ・ドロワー・フッター）
    x = x.replace('<span lang="ja">取材のお問い合わせ</span>', '<span lang="ja">お問い合わせ</span>')
    x = x.replace('<span lang="en">Media inquiries</span>', '<span lang="en">Contact</span>')
    # 4回目：SP のメニューボタンを3本線に（2本だと切れて見える）
    x = x.replace('<span></span><span></span></button>', '<span></span><span></span><span></span></button>')
    # 4回目：背景色（?bg=a|b|c|d、既定 b）と FV（?fv=1|2|3）のデモ。描画前に html の属性を決めて、ちらつきを防ぐ
    x = x.replace('</head>', '<script>(function(){var r=document.documentElement,q=new URLSearchParams(location.search),s=window.localStorage,g=function(k){try{return s.getItem(k)}catch(e){return null}},p=function(k,v){try{s.setItem(k,v)}catch(e){}};'
                  'r.setAttribute("data-bg","b");'  # 背景は B 玄米に決定（yuga 2026-11-25）。切り替えはやめた
                  
                  'var f=q.get("fv");if(/^[0-6]$/.test(f||""))p("wc-fv",f);else f=g("wc-fv");if(f&&f!=="0")r.setAttribute("data-fv",f)})()</script></head>', 1)
    if name == 'index':
        # TOPの2つ目のボタン：店舗を見る → メニューを見る（menu へ）
        x = sub1(r'<a class="btn line" href="#stores"><span lang="(ja|en)">(店舗を見る|See locations)</span></a>',
                 f'<a class="btn line" href="{rel("menu", lang)}"><span lang="{lang}">{"メニューを見る" if ja else "See the menu"}</span></a>', x)
        # 私たちのレストランについて：ドアの写真 → 店内の写真
        x = sub1(r'<img class="a1" src="([^"]*?)entrance\.jpg"', r'<img class="a1" src="\1interior.jpg" width="450" height="303"', x)
        # ケータリング：メールソフトを開くボタン → お問い合わせ（種類＝ケータリング）。メールアドレスの表記は残す
        # 4回目：ボタンの文言は「ご相談」/「Ask us」（yuga 2026-11-25「お問い合わせではなく、ご相談に」。英語は要確認）
        x = sub1(r'<a class="btn" href="mailto:glutenfree@glutenfree\.co\.jp\?subject=[^"]*"><span lang="(?:ja|en)">(?:メールで相談する|Email us)</span></a>',
                 f'<a class="btn" href="{rel("media", lang)}?type=catering#contact"><span lang="{lang}">{"ご相談" if ja else "Ask us"}</span></a>', x)
        # 4回目：チラシは「チラシを見る」とサムネイルを1つのリンクにまとめ、「ご相談」のすぐ下（メールアドレスの上）へ。
        # 「タップで拡大」の文言は残し、表示だけ CSS で消す
        m_fl = re.search(r'\n\s*<a class="flyer" href="([^"]+)"[^>]*>\n\s*(<img [^>]*>)\n\s*(<span><span lang="(?:ja|en)">[^<]*</span></span>)\n\s*</a>', x)
        assert m_fl
        m_bl = re.search(r'\n\s*<a class="btn line" href="' + re.escape(m_fl.group(1)) + r'"[^>]*><span lang="(?:ja|en)">([^<]*)</span></a>', x)
        assert m_bl
        x = x.replace(m_bl.group(0), '', 1).replace(m_fl.group(0), '', 1)
        flyer = (f'\n    <a class="flyer" href="{m_fl.group(1)}" target="_blank" rel="noopener">{m_fl.group(2)}'
                 f'<span class="flyer-go"><span lang="{lang}">{m_bl.group(1)}</span></span>'
                 + m_fl.group(3).replace('<span>', '<span class="flyer-tap">', 1) + '</a>')
        x = sub1(r'(<div class="row">\s*<a class="btn" href="[^"]*type=catering#contact">.*?</a>\s*</div>)', lambda m: m.group(1) + flyer, x, flags=re.S)
        # 4回目：FV の3案（?fv=1|2|3）用の写真。今の FV（fv なし）では表示しない（display:none と loading=lazy で読み込まない）
        pics = ''.join(f'<img class="fv-{k}" src="{up}src/images/{f}" alt="" width="{w}" height="{h}" loading="lazy" decoding="async">'
                       for k, f, w, h in (('food', 'food.jpg', 1464, 943), ('ent', 'entrance.jpg', 1200, 800),
                                          ('har', 'harajuku.jpg', 1448, 1086), ('bento', 'bento.jpg', 1200, 800)))
        x = sub1(r'<div class="hero"><div class="hero-in">', f'<div class="hero"><div class="fv-pics" aria-hidden="true">{pics}</div><div class="hero-in">', x)
        # 7回目：FV の新しい3案（?fv=4|5|6）。H1 の直後に、案ごとに使う写真・認証マーク・認証の文を置く（.fvx。fv=4〜6 以外は display:none）。
        # 帯は div（中の img を拡大して切り出す）。FV の画像なので eager。food.jpg・award-gig.png はページ内でも使うので、fv=0 でも余分な通信はほぼ増えない（harajuku.jpg だけ増える）
        # 認証の文は、すぐ下の about の lead（既存の文）と同じもの
        cert = ('アジアで初めて、グルテンフリーの認証を取得したレストランです。' if ja
                else 'We were the first restaurant in Asia to receive gluten-free certification.')
        fvx = (f'<div class="fvx fvx-band"><img src="{up}src/images/food.jpg" alt="" width="1464" height="943" loading="eager" decoding="async"></div>'
               f'<img class="fvx fvx-har" src="{up}src/images/harajuku.jpg" alt="" width="1448" height="1086" loading="eager" decoding="async">'
               f'<p class="fvx fvx-cert"><img class="fvx-mark" src="{up}src/images/award-gig.png" alt="Validated Gluten Free Safe Spot" width="320" height="320" loading="eager" decoding="async">'
               f'<span class="fvx-cert-t"><span lang="{lang}">{cert}</span></span></p>')
        # 日本語の H1 は案4〜6だけ3行（「可能性を味わう／レストランです。」の間の改行は .fvx-br。ほかの案では表示しない）
        x = sub1(r'(<h1 lang="(?:ja|en)">.*?</h1>)', lambda m: m.group(1).replace('可能性を味わうレストランです。', '可能性を味わう<br class="fvx-br">レストランです。') + fvx, x)
        # コンサルへの入口：誰が・何を・初回無料を、コンサルページの既存の文言で
        role = ('アジア初GFFS認証レストラン創業者 ／ グルテンフリー専門コンサルタント' if ja
                else "Founder of Asia's first GFFS-certified restaurant / Gluten-free consultant")
        areas = (('GFCO認証 取得支援', 'グルテンフリー 商品開発', '現状診断・売上改善アドバイザリー') if ja
                 else ('GFCO certification support', 'Gluten-free product development', 'Business review & sales advisory'))
        free = '初回30分は無料 ・ オンライン相談OK' if ja else 'First 30 minutes free · Online consultations available'
        x = sub1(r'(<section class="blk cons-band"><div class="wrap cons-band-in">.*?<div>)(<h2>.*?</h2>)(<a class="cons-link"[^>]*>.*?</a>)',
                 lambda m: (m.group(1) + f'<p class="cons-role"><span lang="{lang}">{role}</span></p>' + m.group(2)
                            + '<ul class="cons-areas">' + ''.join(f'<li><span lang="{lang}">{a.replace("&", "&amp;")}</span></li>' for a in areas) + '</ul>'
                            + f'<p class="cons-free"><span lang="{lang}">{free}</span></p>' + m.group(3).replace('cons-link', 'btn cons-link')),
                 x, flags=re.S)
    if name == 'media':
        x = x.replace('メディア・取材のお問い合わせ｜', 'お問い合わせ｜').replace('Media inquiries | ', 'Contact | ')
        x = x.replace('<h1><span lang="ja">メディア・取材のお問い合わせ</span></h1>', '<h1><span lang="ja">お問い合わせ</span></h1>')
        x = x.replace('<h1><span lang="en">Media and press inquiries</span></h1>', '<h1><span lang="en">Contact</span></h1>')
        x = x.replace('取材・掲載などのご相談は、下のフォームからお送りください。',
                      '取材・コンサルティング・ケータリングなどのご相談は、下のフォームからお送りください。')
        x = x.replace('For interview requests, coverage and other media inquiries, please use the form below.',
                      'For media, consulting, catering and other inquiries, please use the form below.')
        x = sub1(r'(<form class="cf7 demo"[^>]*>\n\s*)', lambda m: m.group(1) + contact_type_field(lang), x)
        # 企業名は任意に（個人の方・ケータリングのお客様も送れるように。要確認）
        x = sub1(r'(<span lang="(?:ja|en)">(?:企業名|Company name)</span>) <em>\*</em>', r'\1', x)
    if name == 'about':
        # 数字帯の長い語がSPで「認証レ／ストラン」と切れないよう、折り返してよい位置だけを示す（文字は変えない）
        x = x.replace('<span lang="ja">グルテンフリー認証レストラン</span></div>', '<span lang="ja">グルテンフリー<wbr>認証レストラン</span></div>', 1)
    if name == 'consulting':
        x = sub1(r'(<form class="cf7 demo"[^>]*>\n\s*)', lambda m: m.group(1) + contact_type_field(lang, 'consulting'), x)
    return x

def warm_a_html(x, name, lang):
    """デモA「白い食卓」だけのHTML変換。文言・リンクは変えない。"""
    if name == 'index':
        # ショップと SNS を1つの帯にまとめる（中身・id はそのまま、外側を div.shop-sns で包むだけ）
        m = re.search(r'<section class="blk shop" id="shop">.*?</section>\n+<section class="blk sns-sec">.*?\n</div></section>\n', x, flags=re.S)
        assert m, 'warm-a: #shop / .sns-sec が見つからない'
        x = x.replace(m.group(0), '<div class="shop-sns">\n' + m.group(0) + '</div>\n', 1)
    return x

def warm_b_html(x, name, lang):
    """デモB「黒板と赤い扉」。文言・並びは変えない。
    元の Google Fonts の URL（Fraunces:opsz,wght@9..144,500;600;700）は書式の誤りで 400 が返り、4書体とも読み込まれていない。
    このデモでは正しい書式の URL に差し替え、大きな数字用の Fraunces 斜体（300/400）を足す。"""
    fonts = ('https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700'
             '&amp;family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,300;1,9..144,400'
             '&amp;family=Zen+Old+Mincho:wght@500;700&amp;family=Zen+Kaku+Gothic+New:wght@400;500;700&amp;display=swap')
    x, n = re.subn(r'<link href="https://fonts\.googleapis\.com/css2\?family=Figtree[^"]*" rel="stylesheet">',
                   lambda m: f'<link href="{fonts}" rel="stylesheet">', x, count=1)
    assert n == 1, name
    return x


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
    # ── 日本語・英語を別URLに分けた版（split/）：/ と /en/ の2系統。公開サイトと同じ並びのフォルダで、リンクは相対パス ──
    #    Warm Editorial のデモ（warm-a/ 白い食卓、warm-b/ 黒板と赤い扉、warm-c/ 紺の誌面）も、同じページに上乗せCSSとHTML変換（warm()）を足して作る（2026-11-24。yuga が選ぶまで src/ には入れない）
    for out, look in (('split', None), ('warm-a', 'a'), ('warm-b', 'b'), ('warm-c', 'c')):
        for lang in ('ja', 'en'):
            d = root/out/(('en'/pathlib.Path(LS.SLUG[name])) if lang == 'en' else pathlib.Path(LS.SLUG[name]))
            def rel(page, l, _d=d, _o=out):
                t = root/_o/(('en'/pathlib.Path(LS.SLUG[page])) if l == 'en' else pathlib.Path(LS.SLUG[page]))
                r = os.path.relpath(t, _d).replace(os.sep, '/')
                return './' if r == '.' else r + '/'
            up = os.path.relpath(root, d).replace(os.sep, '/') + '/'
            x = LS.strip_other(h, lang)
            # 店舗は選択式（タブ）をやめ、3店舗を常に並べて表示する（yuga・お店のフィードバック 2026-11-22）
            x = re.sub(r'  <div class="store-tabs" role="tablist">.*?</div>\n', '', x, count=1, flags=re.S)
            x = x.replace('<article class="card">', '<article class="card on">')
            # タブをやめたので、店舗見出し下の「ご来店の店舗をお選びください。」「Choose your location.」は削除（yuga承認）。残りの文は元のまま
            for t in ('ご来店の店舗をお選びください。', 'Choose your location. '):
                x = x.replace(t, '', 1)
            x = LS.set_lang(x, lang)
            x = x.replace('<html lang=', '<html data-stores="3" lang=', 1)
            x = LS.switch_button(x, lang, rel(name, 'en' if lang == 'ja' else 'ja'))
            x = LS.fix_links(x, lang, rel)
            x = re.sub(r'(href|src)=(\\?["\'])(renew\d*\.(?:css|js)|form\.js)', lambda m: f'{m.group(1)}={m.group(2)}{up}assets/{m.group(3)}', x)
            x = x.replace('../src/', up + 'src/')
            x = x.replace('</head>', f'<link rel="stylesheet" href="{up}split/stores.css?v=20261122a"></head>', 1)
            x = x.replace(r"(\.\.\/src\/)?images\/", r"(\.\.\/)*(src\/)?images\/")
            title, desc = (None, None)
            if lang == 'en':
                title, desc = LS.EN_META[name]
                x = re.sub(r'<title>.*?</title>', lambda m: f'<title>{title}</title>', x, count=1)
                if desc: x = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{desc}">', x, count=1)
                else: x = re.sub(r'<meta name="description" content="[^"]*">\n?', '', x, count=1)
            alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{rel(name, l)}">' for l in ('ja', 'en')) + f'<link rel="alternate" hreflang="x-default" href="{rel(name, "ja")}">'
            x = x.replace('</head>', alt + '</head>', 1)
            if look:
                x = warm(x, look, name, lang, up, rel)
            d.mkdir(parents=True, exist_ok=True)
            (d/'index.html').write_text(x, encoding='utf-8')
    print(name)
