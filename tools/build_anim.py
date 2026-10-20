"""アニメーション案のデモページを作る。anim/ のCSS・JSを、各ページのHTMLに重ねるだけ（本番用のページ・WordPress用の断片は変えない）。
使い方: python3 tools/build_anim.py → anim-a.html（トップ）、anim-a-consulting.html などを作り直す"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
NAMES = {'a': 'ふわっと', 'a2': 'ふわっと＋', 'b': '小麦をぬく', 'c': 'スクロール'}
# 案A+ は 案A に anim/plus.* を重ねる（a.css / a.js を先に読み込む）
EXTRA = {'a2': ['a', 'plus']}
CSS = '<link rel="stylesheet" href="style.css?v=20261019a">'
JS = '<script src="script.js?v=20261019a"></script>'
for k, label in NAMES.items():
    def out(page): return f'anim-{k}.html' if page == 'index' else f'anim-{k}-{page}.html'
    for page in PAGES:
        h = (root/f'{page}.html').read_text(encoding='utf-8')
        assert CSS in h and JS in h, page
        h = re.sub(r'<html lang="ja" data-lang="ja"[^>]*>', f'<html lang="ja" data-lang="ja" data-anim="{k}" data-page="{page}" class="anim-{k[0]}{" anim-"+k if k != k[0] else ""}">', h, count=1)
        h = re.sub(r'<title>', f'<title>【アニメーション案{k.upper().replace("2", "+")} {label}】', h, count=1)
        h = h.replace(CSS, CSS + '\n<link rel="stylesheet" href="anim/common.css">' + ''.join(f'\n<link rel="stylesheet" href="anim/{f}.css">' for f in EXTRA.get(k, [k])))
        h = h.replace(JS, JS + '\n<script src="anim/common.js"></script>' + ''.join(f'\n<script src="anim/{f}.js"></script>' for f in EXTRA.get(k, [k])))
        # 上のメニューのリンクも、同じ案のデモページに向ける
        for p in PAGES:
            h = h.replace(f'href="{p}.html"', f'href="{out(p)}"')
        h = h.replace('href="./"', f'href="{out("index")}"')
        (root/out(page)).write_text(h, encoding='utf-8')
        print(out(page))
