#!/usr/bin/env python3
"""商品ページのデモ（warm-c/products/・warm-c/en/products/）を作り、warm-c の各ページに入口を足す。
warm-c/media/ をひな形にし、何度実行しても同じ結果になる。"""
import re, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
C = R / "warm-c"

T = {
 "ja": dict(
  lang="ja", nav="商品", title="商品｜Gluten Free T's Kitchen",
  desc="Gluten Free T's Kitchen のオリジナル商品（ホットソース、てんぷら粉、たこ焼き粉、唐揚げ粉）のご紹介。",
  h1="T'sの商品", sub="お店で販売している、T'sオリジナルの商品です。", tag="販売は店頭のみ",
  items=[("ホットソース","hotsauce.png"),("てんぷら粉","tempura-mix.png"),("たこ焼き粉",None),("唐揚げ粉",None)],
  ph="写真準備中", ws_h="お取り扱いをご希望の事業者様へ",
  ws_p="T'sの商品を取り扱いたい事業者様を募集しています。",
  ws_btn="卸売のお問い合わせ", entry_p="ホットソース、てんぷら粉、たこ焼き粉、唐揚げ粉。お店で販売しています。",
  entry_btn="商品を見る", opt="卸売・お取り扱い", about="会社概要"),
 "en": dict(
  lang="en", nav="Products", title="Products | Gluten Free T's Kitchen",
  desc="Original products from Gluten Free T's Kitchen: hot sauce, tempura mix, takoyaki mix and karaage mix.",
  h1="T's Products", sub="Original T's products, sold at our restaurants.", tag="In store only",
  items=[("Hot Sauce","hotsauce.png"),("Tempura Mix","tempura-mix.png"),("Takoyaki Mix",None),("Karaage Mix",None)],
  ph="Photo coming soon", ws_h="For businesses interested in stocking T's products",
  ws_p="We are looking for businesses who would like to carry T's products.",
  ws_btn="Wholesale inquiries", entry_p="Hot sauce, tempura mix, takoyaki mix and karaage mix. Available at our restaurants.",
  entry_btn="See the products", opt="Wholesale", about="About us"),
}

def sp(l, s): return f'<span lang="{l}">{s}</span>'

def main_html(t, up):  # up: 画像・assets までの相対 (JA: ../../ / EN: ../../../)
    l = t["lang"]
    figs = []
    for name, img in t["items"]:
        pic = (f'<img src="{up}src/images/{img}" alt="" loading="lazy">' if img
               else f'<span class="pd-soon">{sp(l, t["ph"])}</span>')
        figs.append(f'<li class="pd-item"><div class="pd-pic{"" if img else " is-empty"}">{pic}</div>'
                    f'<h2 class="pd-name">{sp(l, name)}</h2></li>')
    mediaurl = "../media/?type=wholesale" if l == "ja" else "../media/?type=wholesale"
    return f'''<main id="top">
<div class="page-hero"><div class="wrap">
  <h1>{sp(l, t["h1"])}</h1>
  <p>{sp(l, t["sub"])}</p>
  <p class="pd-tag">{sp(l, t["tag"])}</p>
</div></div>

<section class="blk pd-list"><div class="wrap">
  <ul class="pd-grid">
    {"".join(figs)}
  </ul>
</div></section>

<section class="pd-ws"><div class="wrap">
  <h2>{sp(l, t["ws_h"])}</h2>
  <p>{sp(l, t["ws_p"])}</p>
  <a class="btn" href="{mediaurl}">{sp(l, t["ws_btn"])}</a>
</div></section>
</main>'''

def make_page(lang):
    t = T[lang]
    src = (C / ("media" if lang == "ja" else "en/media") / "index.html").read_text()
    html = re.sub(r"<main id=\"top\">.*?</main>", lambda m: main_html(t, "../../" if lang == "ja" else "../../../"), src, flags=re.S)
    html = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", html)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', html)
    html = html.replace('data-page="media"', 'data-page="products"')
    html = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=20261125a">' % ("../../" if lang == "ja" else "../../../"), html, count=1)
    # nav の現在地を商品に
    html = html.replace(' class="on" aria-current="page"', "")
    html = re.sub(r'hreflang" href', 'hreflang" href', html)
    # 言語切替・alternate
    if lang == "ja":
        html = html.replace('href="../en/media/"', 'href="../en/products/"')
    else:
        html = html.replace('href="../../media/"', 'href="../../products/"')
    html = html.replace('href="./" hreflang', 'href="./" hreflang')
    html = html.replace("../../split/media/", "../../split/").replace("../../../split/en/media/", "../../../split/en/")
    return html

def add_nav(path, lang, prefix):
    t = T[lang]; s = path.read_text()
    if "products/" in s and f">{t['nav']}</span>" in s: return
    pat = re.compile(r'(<a(?: class="[^"]*")? href="[^"]*"(?: aria-current="page")?><span lang="%s">%s</span></a>)' % (lang, t["about"]))
    s, n = pat.subn(lambda m: f'<a href="{prefix}products/"><span lang="{lang}">{t["nav"]}</span></a>' + m.group(1), s)
    path.write_text(s); print(path, "nav", n)

def main():
    for lang in ("ja", "en"):
        out = C / ("products" if lang == "ja" else "en/products"); out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(make_page(lang))
    for lang, base in (("ja", C), ("en", C / "en")):
        for p in [base / "index.html"] + sorted(base.glob("*/index.html")):
            if p.parent.name == "en": continue
            top = p.parent == base
            add_nav(p, lang, "" if top else "../")
    # お問い合わせの種類に「卸売」を足す
    for lang, p in (("ja", C / "media/index.html"), ("en", C / "en/media/index.html")):
        s = p.read_text()
        if 'value="wholesale"' not in s:
            s = re.sub(r'(<option value="catering">[^<]*</option>)', lambda m: m.group(1) + f'<option value="wholesale">{T[lang]["opt"]}</option>', s, count=1)
            p.write_text(s)
    # TOP の入口（オンラインショップ準備中の帯を置き換える）
    for lang, p, up in (("ja", C / "index.html", "../"), ("en", C / "en/index.html", "../../")):
        t = T[lang]; s = p.read_text()
        if "pd-entry" in s: continue
        new = (f'<section class="blk pd-entry" id="shop"><div class="wrap">'
               f'<div class="pd-entry-pics"><img src="{up}src/images/hotsauce.png" alt="" loading="lazy"><img src="{up}src/images/tempura-mix.png" alt="" loading="lazy"></div>'
               f'<div class="pd-entry-tx"><h2>{sp(lang, t["h1"])}</h2><p>{sp(lang, t["entry_p"])}</p>'
               f'<a class="btn line" href="products/">{sp(lang, t["entry_btn"])}</a></div></div></section>')
        s, n = re.subn(r'<section class="blk shop" id="shop">.*?</section>', lambda m: new, s, count=1, flags=re.S)
        print(p, "entry", n); p.write_text(s)
        # CSS
        s = p.read_text()
        s = re.sub(r'(<link rel="stylesheet" href="[./]*assets/warm-c\.css[^"]*">)', r'\1<link rel="stylesheet" href="%sassets/products.css?v=20261125a">' % up, s, count=1)
        p.write_text(s)

if __name__ == "__main__": main()
