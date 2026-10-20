"""アニメーション案のデモページを作る。anim/ のCSS・JSを、各ページのHTMLに重ねるだけ（本番用のページ・WordPress用の断片は変えない）。
使い方: python3 tools/build_anim.py → anim-a.html（トップ）、anim-a-consulting.html などを作り直す"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index', 'about', 'menu', 'consulting', 'media']
NAMES = {'a': 'ふわっと', 'b': '小麦をぬく', 'c': 'スクロール'}
CSS = '<link rel="stylesheet" href="style.css?v=20261019a">'
JS = '<script src="script.js?v=20261019a"></script>'
for k, label in NAMES.items():
    def out(page): return f'anim-{k}.html' if page == 'index' else f'anim-{k}-{page}.html'
    for page in PAGES:
        h = (root/f'{page}.html').read_text(encoding='utf-8')
        assert CSS in h and JS in h, page
        h = re.sub(r'<html lang="ja" data-lang="ja"[^>]*>', f'<html lang="ja" data-lang="ja" data-anim="{k}" data-page="{page}" class="anim-{k}">', h, count=1)
        h = re.sub(r'<title>', f'<title>【アニメーション案{k.upper()} {label}】', h, count=1)
        h = h.replace(CSS, CSS + f'\n<link rel="stylesheet" href="anim/common.css">\n<link rel="stylesheet" href="anim/{k}.css">')
        h = h.replace(JS, JS + f'\n<script src="anim/common.js"></script>\n<script src="anim/{k}.js"></script>')
        # 上のメニューのリンクも、同じ案のデモページに向ける
        for p in PAGES:
            h = h.replace(f'href="{p}.html"', f'href="{out(p)}"')
        h = h.replace('href="./"', f'href="{out("index")}"')
        (root/out(page)).write_text(h, encoding='utf-8')
        print(out(page))
