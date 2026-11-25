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
V = "20261125r1"

NAV = {"ja": ("商品", "会社概要", "卸売・お取り扱い"), "en": ("Products", "About us", "Wholesale")}

def stores_from_footer(html, lang):
    """フッターの3店舗（店名・住所・電話）をそのまま取り出す"""
    out = re.findall(r'<div><b><span lang="%s">([^<]+)</span></b><span lang="%s">([^<]+)</span><br><a href="(tel:\d+)">([^<]+)</a></div>' % (lang, lang), html)
    assert len(out) == 3, out
    return out

def pic(up, name, alt, w, h, cls="", eager=False, png=False):
    ext = "png" if png else "jpg"
    return (f'<picture{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><source srcset="{up}assets/img/products/{name}.webp" type="image/webp">'
            f'<img src="{up}assets/img/products/{name}.{ext}" alt="{alt}" width="{w}" height="{h}" '
            f'{"fetchpriority=" + chr(34) + "high" + chr(34) if eager else "loading=" + chr(34) + "lazy" + chr(34)} decoding="async"></picture>')

def main_html(lang, up, stores):
    ja = lang == "ja"
    t = lambda a, b: a if ja else b
    D = t('<span class="draft" data-draft>仮</span>', '<span class="draft" data-draft>Draft</span>')
    st = "".join(f'<li><b>{n}</b><span>{a}</span><a href="{tel}">{num}</a></li>' for n, a, tel, num in stores)
    ing = t(["米粉", "馬鈴薯", "ひよこ豆粉"], ["Rice flour", "Potato", "Chickpea flour"])
    ing_li = "".join(f"<li>{x}</li>" for x in ing)

    fv_a = f'''<section class="pd-fv" aria-labelledby="pd-h1">
<div class="pd-fv-in">
  <div class="pd-fv-pics">
    {pic(up, "tempura-vegetables", t("T'sてんぷら粉で揚げた野菜の天ぷら", "Vegetable tempura made with T's Tempura Batter Mix"), 624, 428, "pd-fv-photo", eager=True)}
    {pic(up, "tempura-bag", t("T'sてんぷら粉の袋（140g）", "T's Tempura Batter Mix pouch (140 g)"), 481, 810, "pd-fv-bag", eager=True, png=True)}
  </div>
  <div class="pd-fv-tx">
    <div class="pd-fv-head">
      <h1 class="pd-h1" id="pd-h1">{t("T'sの商品", "T's Products")}</h1>
      <p class="pd-name">{t("T'sてんぷら粉", "T's Tempura Batter Mix")}<span class="pd-name-sub">{t("Tempura Batter Mix", "T'sてんぷら粉")}</span></p>
    </div>
    <p class="pd-ing-label">{t("原材料", "Ingredients")} {D}</p>
    <ul class="pd-ing" data-draft>{ing_li}</ul>
    <p class="pd-fv-facts">{t("28品目アレルゲン不使用", "Free from 28 allergens")}<span>{t("内容量 140g", "140 g")}</span></p>
    <p class="pd-fv-buy"><span>{t("販売は店頭のみ", "In store only")}</span><a href="#buy">{t("買えるお店", "Where to buy")}</a><a href="#wholesale">{t("お取り扱いをご希望の事業者様へ", "For businesses")}</a></p>
    <nav class="pd-fv-more" aria-label="{t('ほかの商品', 'Other products')}"><span>{t("ほかの商品", "Also")}</span><a href="#hotsauce">{t("ホットソース", "Hot Sauce")}</a><a href="#takoyaki">{t("たこ焼き粉", "Takoyaki Mix")}</a><a href="#karaage">{t("唐揚げ粉", "Karaage Mix")}</a></nav>
  </div>
</div>
</section>'''

    fv_b = f'''<section class="pd-fvb" aria-labelledby="pd-h1b">
<h1 class="pd-h1 pd-fvb-h1" id="pd-h1b">{t("T'sの商品", "T's Products")}</h1>
<div class="pd-fvb-half is-navy">
  {pic(up, "tempura-bag", t("T'sてんぷら粉の袋（140g）", "T's Tempura Batter Mix pouch (140 g)"), 481, 810, "pd-fvb-pic", png=True)}
  <div><p class="pd-fvb-name">{t("T'sてんぷら粉", "T's Tempura Batter Mix")}</p>
  <p>{t("28品目アレルゲン不使用", "Free from 28 allergens")}<br>{t("内容量 140g", "140 g")}</p>
  <a href="#tempura-detail">{t("てんぷら粉について", "About the batter mix")}</a></div>
</div>
<div class="pd-fvb-half">
  {pic(up, "hotsauce-original", t("T'sホットソース（オリジナル）の瓶", "A jar of T's HOT SAUCE ORIGINAL"), 450, 590, "pd-fvb-pic")}
  <div><p class="pd-fvb-name">{t("T'sホットソース（オリジナル）", "T's HOT SAUCE ORIGINAL")}</p>
  <p>{t("無添加・グルテンフリー・ヴィーガン", "Additive-free, gluten-free, vegan")}<br>{t("内容量 160g", "160 g")}</p>
  <a href="#hotsauce">{t("ホットソースについて", "About the hot sauce")}</a></div>
</div>
<p class="pd-fvb-buy"><span>{t("販売は店頭のみ", "In store only")}</span><a href="#buy">{t("買えるお店", "Where to buy")}</a><a href="#wholesale">{t("お取り扱いをご希望の事業者様へ", "For businesses")}</a><a href="#takoyaki">{t("たこ焼き粉・唐揚げ粉", "Takoyaki and karaage mixes")}</a></p>
</section>'''

    s2 = f'''<section class="pd-s2" id="tempura-detail" aria-labelledby="pd-s2-h">
<div class="pd-wrap pd-s2-grid">
  <div class="pd-s2-main">
    <h2 class="pd-h2" id="pd-s2-h">{t("てんぷら粉について", "About the tempura batter mix")}</h2>
    <p class="pd-lead">{t("無添加、グルテンフリー、ヴィーガン、ハラールなど様々な食の多様化に対応しています。",
      "It suits a wide range of diets, such as additive-free, gluten-free, vegan and halal.")}</p>
    <p class="pd-tx" data-draft>{t("小麦由来の天ぷら粉に比べ、吸油量が約40%少なくなります。", "It absorbs about 40% less oil than wheat-based tempura flour.")} {D}</p>
    <h3 class="pd-h3">{t("作り方", "How to use")} {D}</h3>
    <ol class="pd-steps" data-draft>
      <li>{t("粉70gに、油15gと水または炭酸水60〜70mlを加えて混ぜます。", "Mix 70 g of the batter mix with 15 g of oil and 60–70 ml of water or sparkling water.")}</li>
      <li>{t("具材に衣をつけ、170℃以上の油で揚げます。", "Coat your ingredients and fry at 170°C or higher.")}</li>
      <li>{t("塩か醤油でどうぞ。", "Serve with salt or soy sauce.")}</li>
    </ol>
    <p class="pd-tx-plain">{t("衣に抹茶、カレー粉、ゴマ、チーズ、ゆかり、青のり、コーンフレーク等、味をつけたり、粉だけを直接、具材にまぶして、揚げることも出来ます。",
      "You can flavour the batter with matcha, curry powder, sesame, cheese, yukari, aonori, cornflakes and more, or dust the mix straight onto ingredients and fry.")}</p>
  </div>
  <figure class="pd-s2-ebi">
    {pic(up, "tempura-ebi", t("エビの天ぷら", "Shrimp tempura"), 482, 328)}
    <figcaption>{t("参考例　140gの天ぷら粉から、エビ(13cm)20尾揚げることが出来ます。", "Example: one 140 g bag makes about 20 shrimp (13 cm).")}
    <span class="pd-note" data-draft>{t("えびは特定原材料です。28品目不使用は粉としての表記です。", "Shrimp is a specified allergen in Japan. “Free from 28 allergens” refers to the batter mix only.")} {D}</span></figcaption>
  </figure>
  <dl class="pd-spec">
    <div><dt>{t("内容量", "Net weight")}</dt><dd>140g</dd></div>
    <div><dt>{t("原材料", "Ingredients")}</dt><dd data-draft>{t("米粉、馬鈴薯、ひよこ豆粉", "Rice flour, potato, chickpea flour")} {D}</dd></div>
    <div><dt>{t("アレルギー", "Allergens")}</dt><dd>{t("28品目アレルゲン不使用", "Free from 28 allergens")}</dd></div>
    <div><dt>{t("賞味期限", "Best before")}</dt><dd>{t("1年", "1 year")}</dd></div>
    <div><dt>{t("ほか", "Also")}</dt><dd>{t("ソイフリー。化学調味料・保存料・人工香料・人工甘味料・人工着色料不使用。遺伝子組み換えをしていません。",
      "Soy-free. No chemical seasonings, preservatives, artificial flavours, sweeteners or colours. Non-GMO.")}</dd></div>
    <div><dt>{t("PL保険", "Product liability")}</dt><dd>{t("加入済", "Insured")}</dd></div>
  </dl>
</div>
</section>'''

    s3 = f'''<section class="pd-s3" id="hotsauce" aria-labelledby="pd-s3-h">
<div class="pd-wrap pd-s3-grid">
  <figure class="pd-s3-pic">{pic(up, "hotsauce-original", t("T'sホットソース（オリジナル）の瓶", "A jar of T's HOT SAUCE ORIGINAL"), 450, 590)}</figure>
  <div class="pd-s3-tx">
    <h2 class="pd-h2" id="pd-s3-h">{t("T'sホットソース（オリジナル）", "T's HOT SAUCE ORIGINAL")}<span class="pd-name-sub">{t("T's HOT SAUCE ORIGINAL", "T'sホットソース（オリジナル）")}</span></h2>
    <p class="pd-lead">{t("野菜の旨みを最大限に活かした無添加万能調味料。", "An additive-free, all-purpose sauce that makes the most of the flavour of vegetables.")}</p>
    <p class="pd-tx-plain">{t("餃子・サラダ・ヴィーガン寿司・パスタなどに。", "Try it with gyoza, salads, vegan sushi, pasta and more.")}</p>
    <p class="pd-facts">{t("無添加・グルテンフリー・ヴィーガン", "Additive-free, gluten-free, vegan")}<span>{t("内容量 160g", "160 g / 5.6 oz")}</span></p>
    <p class="pd-tx" data-draft>{t("（仮）原材料・アレルギー表記は確認中です", "(Draft) Ingredients and allergen labelling are being confirmed.")} {D}</p>
  </div>
</div>
</section>'''

    s4 = f'''<section class="pd-s4" aria-labelledby="pd-s4-h">
<div class="pd-wrap">
  <h2 class="pd-h2 pd-h2-sm" id="pd-s4-h">{t("詳しい情報は確認中", "Details being confirmed")} {D}</h2>
  <div class="pd-s4-list">
    <div class="pd-s4-item" id="takoyaki">
      {pic(up, "takoyaki-pack", t("T'sたこ焼き粉のパッケージ（246g）", "Takoyaki mix package (246 g)"), 462, 572, "pd-s4-pic")}
      <div><h3 class="pd-h3">{t("たこ焼き粉", "Takoyaki Mix")}</h3>
      <p>{t("28品目アレルゲン不使用", "Free from 28 allergens")}<span class="pd-sep">{t("内容量 246g", "246 g")}</span></p>
      <p class="pd-tx" data-draft>{t("販売状況は確認中です。", "Availability is being confirmed.")} {D}</p></div>
    </div>
    <div class="pd-s4-item" id="karaage">
      <div><h3 class="pd-h3">{t("唐揚げ粉", "Karaage Mix")}</h3>
      <p>{t("28品目アレルゲンフリー からあげ粉", "A karaage mix free from 28 allergens")}</p>
      <p class="pd-tx" data-draft>{t("販売状況は確認中です。", "Availability is being confirmed.")} {D}</p></div>
    </div>
  </div>
</div>
</section>'''

    s5 = f'''<section class="pd-s5" id="buy" aria-labelledby="pd-s5-h">
<div class="pd-wrap pd-s5-grid">
  <div>
    <h2 class="pd-h2" id="pd-s5-h">{t("販売は店頭のみ", "In store only")}</h2>
    <p class="pd-tx" data-draft>{t("在庫は各店にお電話でお問い合わせください。", "Please call the restaurant to check stock.")} {D}</p>
  </div>
  <ul class="pd-stores">{st}</ul>
</div>
</section>'''

    s6 = f'''<section class="pd-ws" id="wholesale" aria-labelledby="pd-ws-h">
<div class="pd-wrap pd-ws-grid">
  <div>
    <h2 class="pd-h2" id="pd-ws-h">{t("お取り扱いをご希望の事業者様へ", "For businesses interested in stocking T's products")}</h2>
    <p>{t("T'sの商品を取り扱いたい事業者様を募集しています。", "We are looking for businesses who would like to carry T's products.")}</p>
  </div>
  <div>
    <dl class="pd-ws-dl">
      <div><dt>{t("てんぷら粉", "Tempura batter mix")}</dt><dd>{t("業務用サイズの販売が可能です。", "Available in a catering size.")}</dd></div>
      <div><dt>{t("ホットソース", "Hot sauce")}</dt><dd><span data-draft>{t("ミニマム発注数 36個", "Minimum order: 36 jars")} {D}</span><br><span data-draft>{t("賞味期限 14か月", "Best before: 14 months")} {D}</span></dd></div>
      <div><dt>{t("PL保険", "Product liability")}</dt><dd>{t("加入済", "Insured")}</dd></div>
      <div><dt>{t("ご相談の流れ", "How it works")}</dt><dd class="pd-tx" data-draft>{t("お問い合わせフォームで「卸売・お取り扱い」を選んでお送りください。担当者からご連絡します。", "Send the contact form with “Wholesale” selected, and we will get back to you.")} {D}</dd></div>
    </dl>
    <a class="btn pd-ws-btn" href="../media/?type=wholesale"><span lang="{lang}">{t("卸売のお問い合わせ", "Wholesale inquiries")}</span></a>
  </div>
</div>
</section>'''

    body = fv_a + fv_b + s2 + s3 + (s4 + s5 if ja else s5 + s4) + s6
    return f'<main id="top" class="pd">\n{body}\n</main>'

HEAD_JS = ('<script>(function(){var r=document.documentElement,q=new URLSearchParams(location.search),s=window.localStorage,'
           'g=function(k){try{return s.getItem(k)}catch(e){return null}},p=function(k,v){try{s.setItem(k,v)}catch(e){}};'
           'r.setAttribute("data-bg","b");var f=q.get("fv");if(/^[ab]$/.test(f||""))p("wc-pdfv",f);else f=g("wc-pdfv");'
           'if(f==="b")r.setAttribute("data-pdfv","b")})()</script>')

def make_page(lang):
    up = "../../" if lang == "ja" else "../../../"
    src = (C / ("media" if lang == "ja" else "en/media") / "index.html").read_text()
    stores = stores_from_footer(src, lang)
    html = re.sub(r'<main id="top">.*?</main>', lambda m: main_html(lang, up, stores), src, flags=re.S)
    t = (lambda a, b: a if lang == "ja" else b)
    html = re.sub(r"<title>.*?</title>", t("<title>商品｜Gluten Free T's Kitchen</title>", "<title>Products | Gluten Free T's Kitchen</title>"), html)
    html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % t(
        "Gluten Free T's Kitchen のオリジナル商品（てんぷら粉、ホットソースほか）のご紹介。販売は店頭のみ。卸売・お取り扱いのご相談も受け付けています。",
        "Original products from Gluten Free T's Kitchen: tempura batter mix, hot sauce and more. Sold in store only. Wholesale inquiries welcome."), html)
    html = html.replace('data-page="media"', 'data-page="products"')
    # 背景・FV の小さなスクリプト（トップの wc-fv は読まない）
    html = re.sub(r'<script>\(function\(\)\{var r=document\.documentElement,q=new URLSearchParams.*?</script>', lambda m: HEAD_JS, html, count=1, flags=re.S)
    html = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=%s">' % (up, V), html, count=1)
    html = html.replace("</body>", f'<script src="{up}assets/products.js?v={V}"></script></body>')
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
    if f'products/"><span lang="{lang}">{nav}</span></a>' in s or f'aria-current="page"><span lang="{lang}">{nav}</span>' in s: return
    pat = re.compile(r'(<a(?: class="[^"]*")? href="[^"]*"(?: aria-current="page")?><span lang="%s">%s</span></a>)' % (lang, about))
    s, n = pat.subn(lambda m: f'<a href="{prefix}products/"><span lang="{lang}">{nav}</span></a>' + m.group(1), s)
    path.write_text(s); print(path, "nav", n)

def entry(lang, up):
    t = (lambda a, b: a if lang == "ja" else b)
    return (f'<section class="blk pd-entry" id="shop" aria-labelledby="pd-entry-h"><div class="wrap pd-entry-in">'
            f'<a class="pd-entry-pics" href="products/" tabindex="-1" aria-hidden="true">'
            + pic(up, "tempura-bag", "", 481, 810, "pd-entry-bag", png=True)
            + pic(up, "hotsauce-original", "", 450, 590, "pd-entry-jar") +
            f'</a><div class="pd-entry-tx"><h2 id="pd-entry-h"><span lang="{lang}">{t("T&#39;sの商品", "T&#39;s Products")}</span></h2>'
            f'<p><span lang="{lang}">{t("てんぷら粉、ホットソースなど。お店で販売しています。", "Tempura batter mix, hot sauce and more, sold at our restaurants.")}</span></p>'
            f'<a class="btn line" href="products/"><span lang="{lang}">{t("商品を見る", "See the products")}</span></a></div></div></section>')

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
        s, n = re.subn(r'<section class="blk (?:shop|pd-entry)" id="shop".*?</section>', lambda m: entry(lang, up), s, count=1, flags=re.S)
        s = re.sub(r'<link rel="stylesheet" href="[./]*assets/products\.css[^"]*">', "", s)
        s = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=%s">' % (up, V), s, count=1)
        p.write_text(s); print(p, "entry", n)

if __name__ == "__main__": main()
