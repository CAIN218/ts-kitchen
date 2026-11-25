#!/usr/bin/env python3
"""商品ページのデモ（warm-c/products/・warm-c/en/products/）を作り、warm-c の各ページに入口とナビを足す（2回目：2026-11-25 作り直し）。
- warm-c/media/ をひな形にし、<main> だけを差し替える。何度実行しても同じ結果になる
- 画像は tools/build_products_images.py が assets/img/products/ に書き出したもの
- 仮の文・数字には <span class="draft" data-draft>仮</span>（英語は Draft）。公開前に data-draft で一括検索して消す
- FV は2案：?fv=a（既定・紺の舞台）／?fv=b（2商品分割）。選んだものは localStorage（wc-pdfv）に残し、html[data-pdfv] で切り替える
- 店舗の住所・電話はフッター（既存）から読み取って使う（書き写さない）"""
import re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
C = R / "warm-c"
V = "20261125v3"

NAV = {"ja": ("商品", "会社概要", "卸売・お取り扱い"), "en": ("Products", "About us", "Wholesale")}

def main_html(lang, up):
    t = (lambda a, b: a if lang == "ja" else b)
    items = [
        ("tempura", t("てんぷら粉", "Tempura batter mix"), t("28品目アレルゲン不使用", "Free from the 28 Japanese-listed allergens")),
        ("hotsauce", t("ホットソース", "Hot sauce"), t("無添加・グルテンフリー・ヴィーガン", "Additive-free, gluten-free, vegan")),
        ("takoyaki", t("たこ焼き粉", "Takoyaki mix"), t("28品目アレルゲン不使用", "Free from the 28 Japanese-listed allergens")),
        ("karaage", t("唐揚げ粉", "Karaage mix"), t("28品目アレルゲンフリー", "Free from the 28 Japanese-listed allergens")),
    ]
    lis = "".join(
        f'<li class="pd-item"><div class="pd-slot" data-slot="{k}" role="img" aria-label="{n}"></div>'
        f'<h2 class="pd-name">{n}</h2><p class="pd-note">{d}</p></li>' for k, n, d in items)
    return f'''<main id="top" class="pd">
<section class="pd-fv" aria-labelledby="pd-h1">
  <picture class="pd-fv-pic"><source srcset="{up}assets/img/products/hero-food.webp" type="image/webp"><img src="{up}assets/img/products/hero-food.jpg" alt="{t("お店の料理", "Dishes from our restaurants")}" width="1600" height="996" fetchpriority="high"></picture>
  <div class="pd-wrap pd-fv-tx">
    <h1 id="pd-h1" class="pd-h1">{t("T&#39;sの商品", "T&#39;s Products")}</h1>
    <p class="pd-lead">{t("お店で販売している、T&#39;sオリジナルの商品です。販売は店頭のみです。", "Original T&#39;s products, sold at our restaurants only.")}</p>
  </div>
</section>
<section class="pd-list" aria-label="{t("商品", "Products")}"><div class="pd-wrap"><ul class="pd-grid">{lis}</ul></div></section>
<section class="pd-ws" id="wholesale" aria-labelledby="pd-ws-h"><div class="pd-wrap">
  <h2 class="pd-ws-h" id="pd-ws-h">{t("お取り扱いをご希望の事業者様へ", "For businesses interested in stocking T&#39;s products")}</h2>
  <p class="pd-ws-p">{t("T&#39;sの商品を取り扱いたい事業者様を募集しています。", "We are looking for businesses who would like to carry T&#39;s products.")}</p>
  <a class="pd-go" href="../media/?type=wholesale">{t("卸売のお問い合わせ", "Wholesale inquiries")}</a>
</div></section>
</main>'''

HEAD_JS = ('<script>document.documentElement.setAttribute("data-bg","b")</script>')

def make_page(lang):
    up = "../../" if lang == "ja" else "../../../"
    src = (C / ("media" if lang == "ja" else "en/media") / "index.html").read_text()
    html = re.sub(r'<main id="top">.*?</main>', lambda m: main_html(lang, up), src, flags=re.S)
    t = (lambda a, b: a if lang == "ja" else b)
    html = re.sub(r"<title>.*?</title>", t("<title>商品｜Gluten Free T's Kitchen</title>", "<title>Products | Gluten Free T's Kitchen</title>"), html)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % t(
        "Gluten Free T's Kitchen のオリジナル商品（てんぷら粉、ホットソースほか）のご紹介。販売は店頭のみ。卸売・お取り扱いのご相談も受け付けています。",
        "Original products from Gluten Free T's Kitchen: tempura batter mix, hot sauce and more. Sold in store only. Wholesale inquiries welcome."), html)
    html = html.replace('data-page="media"', 'data-page="products"')
    # 背景・FV の小さなスクリプト（トップの wc-fv は読まない）
    html = re.sub(r'<script>\(function\(\)\{var r=document\.documentElement,q=new URLSearchParams.*?</script>', lambda m: HEAD_JS, html, count=1, flags=re.S)
    html = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=%s">' % (up, V), html, count=1)
    # ナビの現在地（お問い合わせ → 商品）
    html = html.replace(' class="on" aria-current="page"', "").replace(' aria-current="page"', "")
    html = html.replace(f'<a href="../products/"><span lang="{lang}">{NAV[lang][0]}</span></a>',
                        f'<a href="./" aria-current="page"><span lang="{lang}">{NAV[lang][0]}</span></a>')
    # お問い合わせのリンク（ひな形では ./ になっている）を media へ
    html = re.sub(r'<a href="\./"><span lang="%s">(%s)</span></a>' % (lang, t("お問い合わせ", "Contact")), r'<a href="../media/"><span lang="%s">\1</span></a>' % lang, html)
    if lang == "ja":
        html = html.replace('href="../en/media/"', 'href="../en/products/"')
    else:
        html = html.replace('href="../../media/"', 'href="../../products/"')
    return html

def add_nav(path, lang, prefix):
    s = path.read_text(); nav, about, _ = NAV[lang]
    if f'aria-current="page"><span lang="{lang}">{nav}</span>' in s: return
    # 会社概要のリンクの直前に「商品」を足す。会社概要のページでは class="on" が href の後ろに付くので、その形も拾う。
    # すでに「商品」が直前にあるリンクには足さない（ヘッダー・ドロワー・フッターのどれか1つだけ足りない場合もあるため、1か所ずつ見る）
    link = f'<a href="{prefix}products/"><span lang="{lang}">{nav}</span></a>'
    pat = re.compile(r'(?<!%s)(<a(?: class="[^"]*")? href="[^"]*"(?: class="[^"]*")?(?: aria-current="page")?><span lang="%s">%s</span></a>)' % (re.escape(link), lang, about))
    s, n = pat.subn(lambda m: link + m.group(1), s)
    path.write_text(s); print(path, "nav", n)

def entry(lang, up):
    """TOP の入口：オンラインショップとは別の、静かな1項目（写真なし・帯なし）"""
    t = (lambda a, b: a if lang == "ja" else b)
    return (f'<section class="pd-entry" id="shop" aria-labelledby="pd-entry-h"><div class="pd-entry-in">'
            f'<h2 id="pd-entry-h"><span lang="{lang}">{t("T&#39;sの商品", "T&#39;s Products")}</span></h2>'
            f'<p><span lang="{lang}">{t("お店で販売している、T&#39;sオリジナルの商品です。", "Original T&#39;s products, sold at our restaurants.")}</span></p>'
            f'<a class="pd-go" href="products/"><span lang="{lang}">{t("商品を見る", "See the products")}</span></a></div></section>\n')

def main():
    for lang in ("ja", "en"):
        out = C / ("products" if lang == "ja" else "en/products"); out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(make_page(lang))
    for lang, base in (("ja", C), ("en", C / "en")):
        for p in [base / "index.html"] + sorted(base.glob("*/index.html")):
            if lang == "ja" and p.parent.name == "en": continue
            if p.parent.name == "products": continue
            add_nav(p, lang, "" if p.parent == base else "../")
    # お問い合わせの種類に「卸売・お取り扱い」を足す
    for lang, p in (("ja", C / "media/index.html"), ("en", C / "en/media/index.html")):
        s = p.read_text()
        if 'value="wholesale"' not in s:
            s = re.sub(r'(<option value="catering">[^<]*</option>)', lambda m: m.group(1) + f'<option value="wholesale">{NAV[lang][2]}</option>', s, count=1)
            p.write_text(s)
    # TOP の入口（前の版の入口、またはオンラインショップ準備中の帯を置き換える）
    for lang, p, up in (("ja", C / "index.html", "../"), ("en", C / "en/index.html", "../../")):
        s = p.read_text()
        # 前の版の入口（SNS の帯の中）を消し、SNS の帯（div.shop-sns）の直前に独立の帯として置く
        s, n = re.subn(r'<section class="(?:blk )?(?:shop|pd-entry)" id="shop".*?</section>\n?', "", s, count=1, flags=re.S)
        # 9回目（HP全体 作る係）：SNS の帯（div.shop-sns）の中の先頭に置き、「商品｜公式SNS」の2列にする（帯の外だと SNS が左の細い列に寄って小さくなっていた）
        s = s.replace('<div class="shop-sns">', '<div class="shop-sns">\n' + entry(lang, up), 1)
        s = re.sub(r'<link rel="stylesheet" href="[./]*assets/products\.css[^"]*">', "", s)
        s = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=%s">' % (up, V), s, count=1)
        p.write_text(s); print(p, "entry", n)

if __name__ == "__main__": main()
