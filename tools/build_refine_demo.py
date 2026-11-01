"""5ページから、洗練デモ（refine/）を作る。改修前／前回のデモ／今回の改修後を切り替えて比べられる。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
BAR = ('<div class="rf-bar" role="group" aria-label="デモの切り替え"><b>デモ用（本番には出ません）</b>'
       '<button type="button" data-mode="before">改修前</button><button type="button" data-mode="v1">前回のデモ</button><button type="button" data-mode="v2">今回の改修後</button>'
       '<span>アクセント色</span><button type="button" data-accent="orange">オレンジ</button><button type="button" data-accent="gold">ゴールド</button><button type="button" data-accent="yellow">イエロー</button></div>')
BARCSS = ('<style>.rf-bar{position:fixed;left:12px;right:12px;margin:0 auto;width:max-content;max-width:calc(100vw - 24px);bottom:12px;z-index:200;background:#fffcf3;color:#1c2b45;border:2px solid #1c2b45;border-radius:14px;'
          'box-shadow:0 8px 28px rgba(17,28,48,.3);padding:8px 10px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;justify-content:center;font:13px/1.4 system-ui,sans-serif}'
          '.rf-bar b{flex-basis:100%;text-align:center;font-size:11px;opacity:.7}.rf-bar span{font-size:12px;opacity:.7;margin:0 2px 0 8px}'
          '.rf-bar button{font:inherit;font-weight:700;border:1.5px solid #c9bfa3;background:#fff;color:#1c2b45;border-radius:999px;padding:5px 12px;cursor:pointer}'
          '.rf-bar button[aria-pressed=true]{background:#1c2b45;border-color:#1c2b45;color:#fbf6e9}.fab{bottom:calc(112px + env(safe-area-inset-bottom))!important}'
          'html:not([data-mode=v2]) .lang .lg,html:not([data-mode=v2]) .pt .ic{display:none}html[data-mode=v2] .lang>span[lang]{display:none}</style>')
ICONS = ['<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 3 3 5-6"/></svg>',
         '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.600-7 10-7 10z"/></svg>',
         '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/></svg>']
for name in ['index', 'about', 'menu', 'consulting', 'media']:
    h = (root/f'{name}.html').read_text(encoding='utf-8')
    h = re.sub(r'(href|src)="(style\.css|script\.js|anim/|images/)', r'\1="../\2', h)
    h = re.sub(r"url\('(images/)", r"url('../\1", h)
    h = h.replace('<link rel="stylesheet" href="../anim/site.css', '<link rel="stylesheet" id="rfBase" href="../anim/site.css', 1)
    h = re.sub(r'(<link[^>]*href="\.\./anim/site\.css[^>]*>)',
               r'\1\n<script>document.documentElement.classList.add("js")</script>\n<link rel="stylesheet" id="v1Css" href="../refresh/refresh.css" disabled>\n<link rel="stylesheet" id="v2Css" href="v2.css?v=20261101b">\n' + BARCSS, h, count=1)
    h = h.replace('</button>', '<span class="lg lg-ja">日本語</span><span class="lg lg-en">EN</span></button>', 0)
    h = re.sub(r'(<button class="lang"[^>]*data-lang-toggle[^>]*>.*?)(</button>)', r'\1<span class="lg lg-ja">日本語</span><span class="lg lg-en">EN</span>\2', h, flags=re.S)
    it = iter(ICONS)
    h = re.sub(r'<div class="pt"><b>', lambda m: '<div class="pt"><span class="ic">' + next(it, '') + '</span><b>', h)
    h = re.sub(r'(<script src="\.\./anim/site\.js[^>]*></script>)', r'\1\n<script src="v2.js?v=20261101b"></script>', h, count=1)
    h = h.replace('</body>', BAR + '\n<script src="demo.js?v=20261101b"></script></body>', 1)
    (root/'refine'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
