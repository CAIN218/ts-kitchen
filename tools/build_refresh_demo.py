"""5ページから、配色・動きの改修デモ（refresh/）を作る。リンクで「改修前／改修後」とアクセント色を切り替えて比べられる。"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
BAR = ('<div class="rf-bar" role="group" aria-label="デモの切り替え"><b>デモ用（本番には出ません）</b>'
       '<button type="button" data-mode="before">改修前</button><button type="button" data-mode="after">改修後</button>'
       '<span>アクセント色</span><button type="button" data-accent="orange">オレンジ</button><button type="button" data-accent="gold">ゴールド</button><button type="button" data-accent="yellow">イエロー</button></div>')
BARCSS = ('<style>.rf-bar{position:fixed;left:12px;right:12px;margin:0 auto;width:max-content;max-width:calc(100vw - 24px);bottom:12px;z-index:200;background:#fffcf3;color:#1c2b45;border:2px solid #1c2b45;border-radius:14px;'
          'box-shadow:0 8px 28px rgba(17,28,48,.3);padding:8px 10px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;justify-content:center;font:13px/1.4 system-ui,sans-serif}'
          '.rf-bar b{flex-basis:100%;text-align:center;font-size:11px;opacity:.7}.rf-bar span{font-size:12px;opacity:.7;margin:0 2px 0 8px}'
          '.rf-bar button{font:inherit;font-weight:700;border:1.5px solid #c9bfa3;background:#fff;color:#1c2b45;border-radius:999px;padding:5px 12px;cursor:pointer}'
          '.rf-bar button[aria-pressed=true]{background:#1c2b45;border-color:#1c2b45;color:#fbf6e9}.fab{bottom:calc(112px + env(safe-area-inset-bottom))!important}</style>')
for name in ['index', 'about', 'menu', 'consulting', 'media']:
    h = (root/f'{name}.html').read_text(encoding='utf-8')
    h = re.sub(r'(href|src)="(style\.css|script\.js|anim/|images/)', r'\1="../\2', h)
    h = re.sub(r"url\('(images/)", r"url('../\1", h)
    h = h.replace('<link rel="stylesheet" href="../anim/site.css', '<link rel="stylesheet" id="refreshCssBase" href="../anim/site.css', 1)
    h = re.sub(r'(<link[^>]*href="\.\./anim/site\.css[^>]*>)', r'\1\n<link rel="stylesheet" id="refreshCss" href="refresh.css">\n' + BARCSS, h, count=1)
    h = h.replace('</body>', BAR + '\n<script src="demo.js"></script></body>', 1)
    (root/'refresh'/f'{name}.html').write_text(h, encoding='utf-8')
    print(name, len(h))
