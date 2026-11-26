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

WARM_V = '20261126f'
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
    if look == 'c':
        # 16回目（yuga 2026-11-25「開発者用のデザイン選択など消して」）：案Cでは切り替えの行を出さない
        return x
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
    # 背景は B 玄米、FV は 8回目の「写真1枚」（data-fv=7）に決定。切り替えはやめた（yuga 2026-11-25）。描画前に html の属性を決めて、ちらつきを防ぐ
    x = x.replace('</head>', '<script>(function(){var r=document.documentElement,q=new URLSearchParams(location.search),s=window.localStorage,g=function(k){try{return s.getItem(k)}catch(e){return null}},p=function(k,v){try{s.setItem(k,v)}catch(e){}};'
                  'r.setAttribute("data-bg","b");'  # 背景は B 玄米に決定（yuga 2026-11-25）。切り替えはやめた
                  
                  'r.setAttribute("data-fv","8")})()</script></head>', 1)  # 12回目：FV は「全画面の写真からふわっと」（fv=8）に決定（yuga 2026-11-25）。切り替えはやめた
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
        fvx = (f'<div class="fvx fvx-band"><picture><source media="(max-width:767px)" srcset="{up}assets/img/food-sp.jpg" width="943" height="1464"><img src="{up}src/images/food.jpg" alt="" width="1464" height="943" loading="eager" decoding="async"></picture></div>'
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
                if look == 'c' and name == 'consulting':
                    # 11回目（yuga 2026-11-25）：ページ下の相談フォームはやめ、お問い合わせページ（種類＝コンサルティング）へ送る。ボタンの文言は同じページの既存のもの
                    btn = '初回30分 無料相談を予約' if lang == 'ja' else 'Book a free 30-minute consultation'
                    x, n = re.subn(r'<form class="cf7 demo".*?</form>', f'<p class="cons-cta cons-go"><a class="btn" href="../media/?type=consulting#contact"><span lang="{lang}">{btn}</span></a></p>', x, count=1, flags=re.S)
                    assert n == 1, 'consulting: form not found'
                    # 12回目：無料相談のボタン（ヘッダー・ドロワー・浮きボタン・本文）はどれもお問い合わせページへ（種類＝コンサルティング）
                    x, n = re.subn(r'href="#contact"', 'href="../media/?type=consulting#contact"', x)
                    assert n >= 4, ('consulting: #contact links', n)
                # ── 15回目（yuga 2026-11-25「重複コンテンツ整理」）：同じ実績・強み・説明を繰り返さず、節ごとに役割を持たせる。文は変えず、移動・統合・削除だけ。
                #    一覧（どこに何が重複し、どこに集約したか）は /mnt/project-files/warm-editorial/c-r15/dup-map.md と r15-changes.md
                if look == 'c' and name in ('consulting', 'about'):
                    mm = re.search(r'(<main id="top">\n)(.*?)(</main>)', x, flags=re.S)
                    blocks = re.findall(r'<div class="page-hero.*?</div></div>|<section[^>]*>.*?</section>', mm.group(2), flags=re.S)
                    def pick(pat):
                        hit = [b for b in blocks if re.search(pat, b, flags=re.S)]
                        assert len(hit) == 1, (name, lang, pat, len(hit))
                        return hit[0]
                    if name == 'consulting':
                        hero = pick(r'cons-hero'); nums = pick(r'class="numbers"'); only = pick(r'class="only"')
                        why = pick(r'class="ticks".*?</ul>\s*</div>\s*</div></section>$') if False else [b for b in blocks if 'class="quote"' in b and 'ticks' in b][0]
                        svc = pick(r'id="services"'); reasons = pick(r'class="dl-grid".*class="more"'); cases = [b for b in blocks if 'class="sec tint"' in b and 'dl-grid' in b][0]
                        book = pick(r'book-card'); founder = pick(r'class="sec founder"'); flow = pick(r'class="steps"'); contact = pick(r'id="contact"')
                        # 取り組む理由（市場背景は1回だけ）：GFCO の項目はサービス（GFCO認証取得支援）へ移す。商品開発の項目の末尾「700以上…」は数字と重なるので外す
                        gfco = re.search(r'<div><h3><span lang="(?:ja|en)">[^<]*GFCO[^<]*</span></h3><p><span lang="(?:ja|en)">(.*?)</span></p></div>\s*', reasons, flags=re.S)
                        assert gfco, 'cons: gfco item'
                        reasons = reasons.replace(gfco.group(0), '')
                        reasons, n = re.subn(r'(<div><h3><span lang="(?:ja|en)">(?:商品開発で市場の先を行く|[^<]*product development[^<]*)</span></h3><p><span lang="(?:ja|en)">.*?)\s*(?:700以上のレシピ開発経験から、売れる商品づくりを直接支援します。|With[^<]*700[^<]*\.)(</span></p></div>)', r'\1\2', reasons, count=1, flags=re.S | re.I)
                        more = re.search(r'\s*<p class="more">.*?</p>', reasons, flags=re.S).group(0)
                        reasons = reasons.replace(more, '')
                        svc, n = re.subn(r'(<article class="svc-row"><div><h3><span lang="(?:ja|en)">[^<]*GFCO.*?<p><span lang="(?:ja|en)">.*?)(</span></p></article>)', lambda m: m.group(1) + ('' if lang == 'ja' else ' ') + gfco.group(1) + m.group(2), svc, count=1, flags=re.S)
                        assert n == 1, 'cons: svc gfco'
                        # 支援実績：数字帯を実績の節の頭に。「大使館・省庁…相談できます」＋ボタンは実績の後ろへ
                        cases = cases.replace('<div class="sec-head">', nums.replace('<section class="numbers"><div class="wrap nums nums3">', '<div class="nums nums3 cases-nums">').replace('</div></section>', '</div>') + '<div class="sec-head">', 1) if False else cases
                        cases = re.sub(r'(</div>\s*)(</div></section>)$', lambda m: m.group(1) + more.strip() + m.group(2), cases.rstrip(), count=1, flags=re.S)
                        # 選ばれる理由＝依頼するメリット：実績の項目（大使館…）は実績の節にあるので外す。現役オーナーの項目のうち、ここにない3つを合わせる
                        why, n = re.subn(r'\s*<li><span lang="(?:ja|en)">(?:大使館・省庁・大手企業・海外著名アーティストからの実績と信頼|[^<]*embass[^<]*)</span></li>', '', why, count=1, flags=re.I)
                        assert n == 1, 'cons: why embassy'
                        ow = re.findall(r'<li>.*?</li>', re.search(r'<ul class="ticks">(.*?)</ul>', book, flags=re.S).group(1), flags=re.S)
                        assert len(ow) == 5, 'cons: owner ticks'
                        why = why.replace('</ul>', ''.join('\n      ' + li for li in ow[2:]) + '\n    </ul>', 1)
                        # 代表者紹介：経歴の要約（only）と書籍を、写真と引用の節に集める
                        bk_h = re.search(r'<h2>(.*?)</h2>', book, flags=re.S).group(1)
                        bk_p = re.search(r'<p class="muted">(.*?)</p>', book, flags=re.S).group(1)
                        bk_card = re.search(r'<div class="book-card">.*?</div>', book, flags=re.S).group(0)
                        only_t = re.search(r'<p class="only-text">.*?</p>', only, flags=re.S).group(0)
                        founder, n = re.subn(r'(<p class="muted" style="margin-top:20px">)', lambda m: only_t.replace('class="only-text"', 'class="founder-bio"') + f'\n    <h3 class="book-h">{bk_h}</h3>\n    <p class="muted">{bk_p}</p>\n    ' + bk_card + '\n    ' + m.group(1), founder, count=1)
                        assert n == 1, 'cons: founder'
                        # 相談：同じ案内（初回30分無料・オンライン）は下の1行にまとめる
                        contact = re.sub(r'\s*<p class="free-badge">.*?</p>', '', contact, count=1, flags=re.S)
                        new = [hero, reasons, svc, cases.replace('<section class="sec tint">', '<section class="sec tint cases">', 1), why.replace('<section class="sec">', '<section class="sec why">', 1), founder, flow, contact]
                        x = x.replace(mm.group(2), '\n\n'.join(new) + '\n', 1)
                        # 数字帯は実績の節の頭へ
                        x, n = re.subn(r'(<section class="sec tint cases"><div class="wrap sec-in">\s*<div class="sec-head">.*?</div>\s*)(<div class="dl-grid">)', lambda m: m.group(1) + '<div class="cases-body">' + nums.replace('<section class="numbers"><div class="wrap nums nums3">', '<div class="nums nums3 cases-nums">').replace('</div></section>', '</div>') + m.group(2), x, count=1, flags=re.S)
                        assert n == 1, 'cons: nums'
                        x, n = re.subn(r'(<div class="cases-body">.*?</div>\s*</div>\s*)(<p class="more">.*?</p>)(</div></section>)', r'\1\2</div>\3', x, count=1, flags=re.S)
                        assert n == 1, 'cons: cases-body end'
                    if name == 'about':
                        hero = pick(r'class="page-hero"'); prof = pick(r'wrap profile'); phil = pick(r'philosophy'); nums = pick(r'class="numbers"')
                        cv = pick(r'wrap cv'); biz = pick(r'biz-sec'); hist = pick(r'class="timeline"'); jt = pick(r'media-sec'); pol = pick(r'class="policy"')
                        # 受賞歴は会社情報から外し、沿革の受賞・掲載の行（年つき）とまとめて「受賞歴」の節に
                        aw_h = re.search(r'<h3 class="sub-h">(.*?)</h3>', prof, flags=re.S).group(1)
                        prof = re.sub(r'\s*<h3 class="sub-h">.*?</ul>', '', prof, count=1, flags=re.S)
                        items = re.findall(r'<li><time>(\d{4})</time>(.*?)</li>', hist, flags=re.S)
                        biz_kw = ('オープン', 'Uber', '書籍', 'opened', 'open', 'moved', 'book', 'Opened', 'Moved')
                        keep, award = [], []
                        for yr, body in items:
                            ps = re.findall(r'<p[^>]*>.*?</p>', body, flags=re.S) or [body]
                            for ptxt in ps:
                                inner = re.sub(r'^<p[^>]*>|</p>$', '', ptxt) if ptxt.startswith('<p') else re.sub(r'^\s*<div[^>]*>|</div>\s*$', '', ptxt)
                                hl = ' class="hl"' if 'class="hl"' in ptxt else ''
                                (keep if any(k in inner for k in biz_kw) else award).append((yr, inner.strip(), hl))
                        assert len(award) >= 7, ('about: awards', len(award))
                        def tl(rows):
                            out = []
                            for yr in dict.fromkeys(r[0] for r in rows):
                                ps = [r for r in rows if r[0] == yr]
                                out.append(f'    <li><time>{yr}</time><div>' + ''.join(f'<p{h}>{t}</p>' for _, t, h in ps) + '</div></li>')
                            return '<ol class="timeline">\n' + '\n'.join(out) + '\n  </ol>'
                        hist = re.sub(r'<ol class="timeline">.*?</ol>', lambda m: tl(keep), hist, count=1, flags=re.S)
                        honors = f'<section class="blk honors"><div class="wrap">\n  <h2>{aw_h}</h2>\n  ' + tl(award) + '\n</div></section>'
                        # 理念：TOP の H1 と同じ見出しは外す。数字（700+）と重なる1行も外す
                        b1 = re.search(r'<div class="cv-box">\s*<h2>.*?</h2>\s*(.*?)\s*</div>\s*(?=<div class="cv-box">)', cv, flags=re.S)
                        assert b1, 'about: cv box1'
                        cv = cv.replace(b1.group(0), '', 1)
                        phil = phil.replace('</div></section>', '  <div class="phil-more">' + b1.group(1) + '</div>\n</div></section>', 1)
                        cv, n = re.subn(r'\s*<li><span lang="(?:ja|en)">(?:700を超えるオリジナルレシピ・商品を開発|[^<]*700[^<]*)</span></li>', '', cv, count=1)
                        assert n == 1, 'about: cv 700'
                        # 数字：トリップアドバイザー No.1 とアジア初は受賞歴の節にあるので外す
                        nums, n = re.subn(r'\s*<div><b>No\.1</b>.*?</div>|\s*<div><b><span lang="(?:ja|en)">(?:アジア初|1st)</span></b>.*?</div>', '', nums, flags=re.S)
                        assert n == 2, ('about: nums', n)
                        nums = nums.replace('class="wrap nums"', 'class="wrap nums nums2"')
                        # 事業内容：概要だけ。詳しいページへつなぐ（文言はそのまま、写真と名前をリンクに）
                        links = {0: rel('menu', lang), 1: rel('index', lang) + '#catering', 2: rel('menu', lang)[:-5] + 'products/'}
                        divs = re.findall(r'<div><div class="ph.*?</b></div>', biz, flags=re.S)
                        assert len(divs) == 4
                        for i, dv in enumerate(divs):
                            if i in links:
                                biz = biz.replace(dv, '<a class="biz-go" href="' + links[i] + '">' + dv[5:-6] + '</a>', 1)
                        # 16回目（yuga 2026-11-25「会社概要って会社情報が最初のイメージ」）：見出しの直後に会社情報
                        new = [hero, prof, phil, cv, nums, biz, hist, honors, jt, pol]
                        x = x.replace(mm.group(2), '\n\n'.join(new) + '\n', 1)
                if look == 'c' and name == 'index':
                    # TOP のコンサル入口：無料の1行はコンサルページと同じ文なので外す。見出しはコンサルページへ、ボタンはお問い合わせ（コンサル）へ
                    x, n = re.subn(r'<p class="cons-free">.*?</p>', '', x, count=1, flags=re.S)
                    assert n == 1, 'index: cons-free'
                    x, n = re.subn(r'(<section class="blk cons-band">.*?)<h2>(.*?)</h2>', lambda m: m.group(1) + f'<h2><a class="cons-h" href="{rel("consulting", lang)}">' + m.group(2) + '</a></h2>', x, count=1, flags=re.S)
                    assert n == 1, 'index: cons h2'
                    x, n = re.subn(r'(<a class="btn cons-link" href=")[^"]*(")', r'\1' + rel('media', lang) + r'?type=consulting#contact\2', x, count=1)
                    assert n == 1, 'index: cons-link'
                if look == 'c' and lang == 'en':
                    # 15回目（yuga 2026-11-25「違ってたら日本語が正しいので直して」）：英語を日本語の意味に合わせる。一覧は /mnt/project-files/warm-editorial/c-r15/ja-en-audit.md
                    EN_FIX = [
                        ('menu', '<p lang="en">We are a gluten-free restaurant. Our dishes and drinks are made without wheat, barley, rye or MSG. We try to accommodate all food allergies — including nuts, egg, dairy, soy and shellfish — as much as possible, but due to our limited kitchen space we cannot guarantee every meal. Please use your own judgment.</p>',
                         '<p lang="en">We serve dishes and drinks made without wheat, barley or rye. We select ingredients based on gluten-free and allergen labeling, but some ingredients are processed in facilities that also handle wheat. Thank you for your understanding.</p>\n    <p lang="en">We accommodate allergies other than gluten wherever possible, but because we cook in a limited space, we cannot guarantee every dish with respect to allergens. Please use your own judgment.</p>'),
                        ('index', '100% gluten-free', 'Gluten-free'),
                        ('about', 'Iino Corporation — Gluten Free T&#x27;s Kitchen', 'Iino Co., Ltd. — Gluten Free T&#x27;s Kitchen'),
                        ('about', "Iino Corporation — Gluten Free T's Kitchen", "Iino Co., Ltd. — Gluten Free T's Kitchen"),
                        ('about', "as someone bringing true gluten-free to Japan, our owner was featured on the front page of The Japan Times and recognized internationally.",
                         "as someone who brought a groundbreaking approach to gluten-free in Japan, we were featured on the front page of The Japan Times and recognized overseas."),
                        ('about', '<th><span lang="en">Restaurants</span></th>', '<th><span lang="en">Major locations</span></th>'),
                        ('about', 'Takako Iino, CEO', 'Takako Iino, Representative Director'),
                        ('*', 'Gluten-free restaurant in Tokyo, made without wheat, barley or rye', 'Gluten-free restaurant made without wheat, barley or rye'),
                        ('*', '<span lang="en">4-28-14 Jingumae, Shibuya</span>', '<span lang="en">B1F, 4-28-14 Jingumae, Shibuya-ku</span>'),
                        ('*', '<span lang="en">7-8-5 Roppongi, Minato</span>', '<span lang="en">2F, 7-8-5 Roppongi, Minato-ku</span>'),
                        ('*', '<span lang="en">5-3-3 Sotokanda, Chiyoda</span>', '<span lang="en">5-3-3 Sotokanda, Chiyoda-ku</span>'),
                        ('*', 'Business review &amp; sales advisory', 'Current-state assessment &amp; sales improvement advisory'),
                        ('*', 'Business review &amp;<br>sales advisory', 'Current-state assessment &amp;<br>sales improvement advisory'),
                        ('consulting', 'Embassies &amp; Ministry of Foreign Affairs', 'Embassies &amp; Ministry of Foreign Affairs-related'),
                        # 16回目（yuga 2026-11-25）：取引先の英語表記は任せる → 各社の英文社名に。著作権表記は英語でOK
                        ('about', 'Amazon Japan G.K. / 日本酒類販売株式会社 / 国分グループ本社株式会社 / 井辻食産 / 新潟製粉',
                         'Amazon Japan G.K. / Nippon Shurui Hanbai Co., Ltd. / Kokubu Group Corp. / Itsuji Shokusan / Niigata Seifun'),
                        ('about', '<td><span lang="en">株式会社たいのいかこ</span></td>', '<td><span lang="en">Tainoikako Co., Ltd.</span></td>'),
                        ('*', '<div class="copy">© 株式会社飯野 / 株式会社たいのいかこ</div>', '<div class="copy">© Iino Co., Ltd. / Tainoikako Co., Ltd.</div>'),
                    ]
                    for pg, a, b in EN_FIX:
                        if pg in ('*', name):
                            x = x.replace(a, b)
                if look == 'c':
                    # 17回目（yuga 2026-11-25「GIGでOK」「カナダのも更新してOK」）：認証名は GIG に、カナダの賞は受賞マークどおりの正式名にそろえる（日英）
                    NAME_FIX = [
                        ('GFFS認証（Gluten-Free Food Service・飲食店向け）', 'GIG認証（Gluten Free Safe Spot・飲食店向け）'),
                        ('GFFS認証', 'GIG認証'),
                        ('GFFS (Gluten-Free Food Service) certified', 'GIG (Gluten Free Safe Spot) certified'),
                        ('GFFS-certified', 'GIG-certified'),
                        ('プロダクト・オブ・ザ・イヤー<br>2020 グランプリ', 'グルテンフリーオブザイヤー<br>カナダ2020 グランプリ'),
                        ('Product of the Year<br>2020 Grand Prix', 'Gluten-Free Canada Product<br>of the Year 2020 Grand Prix'),
                        ('alt="Gluten-Free Product of the Year 2020"', 'alt="Gluten-Free Canada Product of the Year 2020"'),
                        ('カナダ グルテンフリーオブザイヤー2020 パントリー部門 グランプリ', 'グルテンフリーオブザイヤー カナダ2020 パントリー部門 グランプリ'),
                        ('Gluten-Free Product of the Year 2020 Canada, Pantry category Grand Prix', 'Gluten-Free Canada Product of the Year 2020, Pantry Items Grand Prix'),
                        ('Gluten-Free Product of the Year 2020, Canada — Pantry category Grand Prix', 'Gluten-Free Canada Product of the Year 2020, Pantry Items Grand Prix'),
                    ]
                    # 21回目（yuga 2026-11-26「グルテンフリーシェフが考えた 米粉レシピのヘルシープレート これ本の正式名」）：本の名前を正式名に。英題は正式なものが無いので、コンサルの書き方にそろえる（要確認）
                    NAME_FIX += [
                        ('グルテンフリーシェフが教える 米粉のヘルシープレート', 'グルテンフリーシェフが考えた 米粉レシピのヘルシープレート'),
                        ('グルテンフリーシェフが教える米粉のヘルシープレート', 'グルテンフリーシェフが考えた 米粉レシピのヘルシープレート'),
                        ('December: first book, a rice-flour healthy plate cookbook by a gluten-free chef, published by', 'December: first book, "Healthy Rice-Flour Plates from a Gluten-Free Chef" (in Japanese), published by'),
                    ]
                    for a_, b_ in NAME_FIX:
                        x = x.replace(a_, b_)
                    # 18回目（yuga 2026-11-25「全ての写真は元データを使って画質の良いものに」）：
                    # 店内・入口は、手元にある一番大きい元（Canva の書き出し）に。WP の縮小版（-1024x574・Instagram の low）は、原寸（full）が読めた時だけ差し替える（data-hq、warm-c.js）
                    x = x.replace('src/images/interior.jpg" width="450" height="303"', 'assets/img/stores/counter.jpg" width="648" height="420"')
                    x = x.replace('src/images/interior.jpg', 'assets/img/stores/counter.jpg')
                    x = x.replace('src/images/entrance.jpg" alt="" width="1200" height="800"', 'assets/img/stores/entrance.jpg" alt="" width="1600" height="1131"')
                    x = x.replace('src/images/entrance.jpg', 'assets/img/stores/entrance.jpg')
                    x = re.sub(r"""style="background-image:url\('(https://glutenfree\.co\.jp/wp-content/uploads/2025/10/S__104693771)-1024x574\.jpg'\)\"""",
                               lambda m: f"style=\"background-image:url('{m.group(1)}-1024x574.jpg')\" data-hq=\"{m.group(1)}.jpg\"", x)
                    x = re.sub(r"""style="background-image:url\('(https://glutenfree\.co\.jp/wp-content/uploads/sb-instagram-feed-images/[^']+)low\.jpg'\)\"""",
                               lambda m: f"style=\"background-image:url('{m.group(1)}low.jpg')\" data-hq=\"{m.group(1)}full.jpg\"", x)
                if look == 'c' and name == 'index':
                    # 18回目（yuga「私たちのレストランについての写真を、カルーセルのように店舗の写真を何枚も見られるように」）
                    T = (lambda j, e: j if lang == 'ja' else e)
                    WP = 'https://glutenfree.co.jp/wp-content/uploads/'
                    dk1 = re.search(r"url\('(" + re.escape(WP) + r"2021/08/DK1-[^']+)'\)", x).group(1)
                    slides = [
                        (f'{up}src/images/harajuku.jpg', 1448, 1086, T('原宿店', 'Harajuku'), ''),
                        (dk1, 0, 0, T('六本木店', 'Roppongi'), ''),
                        (WP + '2025/10/S__104693771-1024x574.jpg', 1024, 574, T('上野広小路店', 'Ueno-Hirokoji'), WP + '2025/10/S__104693771.jpg'),
                        (f'{up}assets/img/stores/entrance.jpg', 1600, 1131, '', ''),
                    ]
                    def slide(i, sl):
                        u, w, h, cap, hq = sl
                        wh = f' width="{w}" height="{h}"' if w else ''
                        hqa = f' data-hq="{hq}"' if hq else ''
                        alt = cap or T('店内の写真', 'Inside the restaurant')
                        c = f'<figcaption>{cap}</figcaption>' if cap else ''
                        return (f'<figure class="car-s" role="group" aria-roledescription="slide" aria-label="{i + 1} / {len(slides)}">'
                                f'<img src="{u}"{wh}{hqa} alt="{alt}" loading="{"eager" if i == 0 else "lazy"}" decoding="async" data-car-img>{c}</figure>')
                    car = (f'<div class="about-ph r3 wc-car" role="region" aria-roledescription="carousel" aria-label="{T("店舗の写真", "Restaurant photos")}">'
                           f'<div class="car-track" tabindex="0">' + ''.join(slide(i, sl) for i, sl in enumerate(slides)) + '</div>'
                           f'<div class="car-dots"></div></div>')
                    x, n = re.subn(r'<div class="about-ph r3"><img class="a1" [^>]*></div>', lambda m: car, x, count=1)
                    assert n == 1, 'index: about-ph carousel'
                if look == 'c' and name == 'menu':
                    # 15回目（yuga 2026-11-25「料理写真を主役に」）：見出しのすぐ下に料理写真の帯。メニュー表はその下にすぐ続く
                    x, n = re.subn(r'(<div class="page-hero"><div class="wrap">.*?</div></div>)', lambda m: m.group(1) + f'\n<figure class="menu-photo"><img src="{up}src/images/food.jpg" alt="" width="1464" height="943" loading="eager" decoding="async"></figure>', x, count=1, flags=re.S)
                    assert n == 1, 'menu: hero'
                    # 16回目（yuga 2026-11-25「新しいほうを採用」）：上野広小路店の料理メニューは英語ページも2026年8月版（日本語と同じ画像）
                    x, n = re.subn(r"ueno:\[\['dish',\{ja:'2026/08/1\.png',en:'2021/08/[^']*'\}\]", "ueno:[['dish','2026/08/1.png']", x)
                    assert n == 1, 'menu: ueno image'
                if look == 'c' and name == 'media':
                    # 12回目（yuga 2026-11-25）：フォームの上の案内文は外す（見出し「お問い合わせ」と種類の選択で足りる）。メッセージを必須に
                    x, n = re.subn(r'\n\s*<p class="lead"><span lang="(?:ja|en)">(?:取材・コンサルティング・ケータリングなどのご相談は、下のフォームからお送りください。|For media, consulting, catering and other inquiries, please use the form below\.)</span></p>', '', x, count=1)
                    assert n == 1, 'media: lead not found'
                    x, n = re.subn(r'(<span lang="(?:ja|en)">(?:メッセージ|Message)</span>)(<textarea)', r'\1 <em>*</em>\2', x, count=1)
                    assert n == 1, 'media: message label not found'
                    x = x.replace('<textarea rows="6">', '<textarea rows="6" required>', 1)
                    # 13回目（yuga 2026-11-25）：お問い合わせを3段階（入力→確認→完了）に。左（SP は上）に STEP 表示。動きは warm-c.js（.wc3）。form.js（1段階のデモ）は使わない
                    st = (('入力情報', '入力内容の確認', '送信・完了') if lang == 'ja' else ('Your details', 'Review', 'Sent'))
                    steps = ('<ol class="wc-steps" aria-label="' + ('お問い合わせの手順' if lang == 'ja' else 'Steps') + '">'
                             + ''.join(f'<li data-s="{i+1}"' + (' aria-current="step"' if i == 0 else '') + f'><b>STEP {i+1}</b><span lang="{lang}">{t}</span></li>' for i, t in enumerate(st)) + '</ol>')
                    x, n = re.subn(r'<form class="cf7 demo" onsubmit="return false">', steps + '<div class="wc3-body"><form class="cf7 wc3" onsubmit="return false" novalidate>', x, count=1)
                    assert n == 1, 'media: form tag'
                    x, n = re.subn(r'(</form>)(\s*<!--/CF7-->)', r'\1</div>\2', x, count=1)
                    assert n == 1, 'media: form end'
                    nxt = '確認画面へ進む' if lang == 'ja' else 'Review your message'
                    x, n = re.subn(r'<button type="button" class="btn"><span lang="(?:ja|en)">(?:送信する|Send)</span></button>', f'<button type="button" class="btn wc3-next"><span lang="{lang}">{nxt}</span></button>', x, count=1)
                    assert n == 1, 'media: send button'
                    # 15回目：スマホで入力しやすく（自動入力・キーボードの種類・改行キーの表示。見た目の文言は同じ）
                    for lab, attrs in ((('企業名', 'Company name'), 'autocomplete="organization" enterkeyhint="next"'),
                                       (('お名前', 'Name'), 'autocomplete="name" enterkeyhint="next" required'),
                                       (('メールアドレス', 'Email'), 'autocomplete="email" inputmode="email" autocapitalize="off" spellcheck="false" enterkeyhint="next" required'),
                                       (('題名', 'Subject'), 'enterkeyhint="next"')):
                        x, n = re.subn(r'(<span lang="(?:ja|en)">(?:' + '|'.join(lab) + r')</span>(?: <em>\*</em>)?<input type="(?:text|email)")', r'\1 ' + attrs, x, count=1)
                        assert n == 1, ('media: input', lab)
                    # GDPR：中身を開いて読めるように（本文は本番に無いので仮置き。要確認）
                    if lang == 'ja':
                        g_old, g_new = '<span lang="ja">GDPRに同意する</span>', '<span lang="ja"><button type="button" class="gdpr-open" aria-expanded="false" aria-controls="gdpr-txt">GDPR</button>に同意する</span>'
                        g_txt = '（仮）ここに個人情報の取り扱い（プライバシーポリシー・GDPR）の本文が入ります。本文はお店に確認してから載せます。'
                    else:
                        g_old, g_new = '<span lang="en">I agree to the GDPR terms</span>', '<span lang="en">I agree to the <button type="button" class="gdpr-open" aria-expanded="false" aria-controls="gdpr-txt">GDPR terms</button></span>'
                        g_txt = '(Placeholder) The privacy policy / GDPR text will go here once confirmed with the restaurant.'
                    assert g_old in x, 'media: gdpr'
                    x = x.replace(g_old, g_new, 1)
                    x, n = re.subn(r'(<p class="chk">.*?</p>)', lambda m: m.group(1) + f'\n    <div class="gdpr-txt" id="gdpr-txt" hidden><p><span lang="{lang}">{g_txt}</span></p></div>', x, count=1, flags=re.S)
                    assert n == 1
                if look == 'c' and name == 'index':
                    # 9回目：FV の文字（H1〜注記）を .fv8-panel で包む。試し案 ?fv=8 で「下からふわっと出る板」にするため。写真1枚の案（fv=7）では display:contents で今まで通り
                    x = re.sub(r'(<div class="hero-in">.*?</p>\n)(\s*<p lang="(?:ja|en)" class="hero-sub">.*?<div class="sub">.*?</div>)', lambda m: m.group(1) + '<div class="fv8-panel">' + m.group(2) + '</div>', x, count=1, flags=re.S)
                    x = re.sub(r'(<div class="hero-in">\n?\s*)(<h1 .*?</h1>)(.*?)(<div class="fv8-panel">)', lambda m: m.group(1) + m.group(3) + m.group(4) + m.group(2), x, count=1, flags=re.S)
            d.mkdir(parents=True, exist_ok=True)
            (d/'index.html').write_text(x, encoding='utf-8')
    print(name)
