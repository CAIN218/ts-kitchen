"""日英が1つのHTMLに同居しているページ（<span lang="ja">…</span><span lang="en">…</span>）から、
日本語だけ／英語だけのページを作る共通の部品。文言は一切変えず、反対の言語の要素を取り除くだけ。
build_preview.py（GitHub Pagesのプレビュー）と build_wp.py（WordPress用の断片）の両方が使う。"""
import re
from html.parser import HTMLParser

PAGES = ['index', 'menu', 'about', 'consulting', 'media']
# 公開URL（日本語は /、英語は /en/ の下）
SLUG = {'index': '', 'menu': 'menu/', 'about': 'about/', 'consulting': 'consulting/', 'media': 'media/'}

def site_path(page, lang):
    return ('/en/' if lang == 'en' else '/') + SLUG[page]

# 英語ページの <title> と description（元のページには英語版が無いため、ページ内の既存の英語の文だけで作った案。要確認）
EN_META = {
    'index': ("Gluten Free T's Kitchen | Gluten-Free Restaurant (Harajuku, Roppongi, Ueno-Hirokoji)",
              "We were the first restaurant in Asia to receive gluten-free certification."),
    'menu': ("Menu | Gluten Free T's Kitchen", None),
    'about': ("About us | Gluten Free T's Kitchen (Iino Co., Ltd.)", None),
    'consulting': ("Consulting | Gluten Free T's Kitchen (Iino Co., Ltd.)", None),
    'media': ("Media inquiries | Gluten Free T's Kitchen", None),
}

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

class _Strip(HTMLParser):
    def __init__(self, drop):
        super().__init__(convert_charrefs=False)
        self.drop, self.out, self.skip, self.depth = drop, [], None, 0
    def _lang(self, attrs):
        return dict(attrs).get('lang')
    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag == self.skip: self.depth += 1
            return
        if tag != 'html' and self._lang(attrs) == self.drop:
            if tag not in VOID: self.skip, self.depth = tag, 1
            return
        self.out.append(self.get_starttag_text())
    def handle_startendtag(self, tag, attrs):
        if self.skip: return
        if tag != 'html' and self._lang(attrs) == self.drop: return
        self.out.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip:
                self.depth -= 1
                if not self.depth: self.skip = None
            return
        self.out.append(f'</{tag}>')
    def _raw(self, s):
        if not self.skip: self.out.append(s)
    def handle_data(self, d): self._raw(d)
    def handle_entityref(self, n): self._raw(f'&{n};')
    def handle_charref(self, n): self._raw(f'&#{n};')
    def handle_comment(self, d): self._raw(f'<!--{d}-->')
    def handle_decl(self, d): self._raw(f'<!{d}>')

def strip_other(html, lang):
    """lang 以外の言語（lang属性つき）の要素を取り除く。"""
    p = _Strip('en' if lang == 'ja' else 'ja')
    p.feed(html); p.close()
    return ''.join(p.out)

def switch_button(html, lang, other_url):
    """言語ボタン（<button data-lang-toggle>）を、もう一方の言語のページへのリンクに替える。"""
    label, ol, aria = ('English', 'en', 'Switch to English') if lang == 'ja' else ('日本語', 'ja', '日本語のページへ')
    new = f'<a class="lang" href="{other_url}" lang="{ol}" hreflang="{ol}" aria-label="{aria}"><span>{label}</span></a>'
    html, n = re.subn(r'<button class="lang"[^>]*data-lang-toggle[^>]*>.*?</button>', lambda m: new, html, flags=re.S)
    assert n == 1, n
    return html

def fix_links(html, lang, url_of):
    """ページ間のリンク（menu.html など）を、その言語のページのURLにする。url_of(page, lang) はURLを返す。"""
    pat = {'./': 'index', 'index.html': 'index', 'menu.html': 'menu', 'about.html': 'about', 'consulting.html': 'consulting', 'media.html': 'media'}
    def rep(m):
        return 'href="' + url_of(pat[m.group(1)], lang) + '"'
    return re.sub(r'href="(\./|index\.html|menu\.html|about\.html|consulting\.html|media\.html)"', rep, html)

def set_lang(html, lang):
    html, n = re.subn(r'<html lang="ja" data-lang="ja">', f'<html lang="{lang}" data-lang="{lang}" data-lang-fixed="{lang}">', html)
    assert n == 1
    if lang == 'en':  # 予約ページも英語版へ（script.js の RSV と同じ対応。JSなしでも英語の予約ページが開く）
        html = html.replace('tablecheck.com/ja/glutenfree', 'tablecheck.com/en/glutenfree')
    return html
