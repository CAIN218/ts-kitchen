#!/usr/bin/env python3
"""商品ページの画像を Canva 書き出し（/mnt/project-files/canva-photos/）から切り出し、assets/img/products/ に書く。
実行: python3 -I tools/build_products_images.py  （Pillow と numpy を使う。色の加工はしない。元より大きくしない）"""
import pathlib
from collections import deque
import numpy as np
from PIL import Image, ImageFilter
CP = pathlib.Path("/mnt/project-files/canva-photos")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/img/products"

def save(im, name, q=82):
    im.convert("RGB").save(OUT / f"{name}.jpg", quality=q, optimize=True, progressive=True)
    im.convert("RGB").save(OUT / f"{name}.webp", quality=q, method=6)
    print(name, im.size)

def bag_cutout(src):
    """袋（白い地とピンクの図形の上）を切り抜く。地の色を外側から塗りつぶしで探し、縁を内側に2px削って0.8pxだけぼかす"""
    im = src.convert("RGB"); a = np.asarray(im).astype(int); H, W, _ = a.shape
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = ((r >= 246) & (g >= 246) & (b >= 246)) | ((r >= 246) & (abs(g - 225) <= 14) & (abs(b - 229) <= 14)) \
         | ((r >= 246) & (g >= 220) & (b >= 224) & (b >= g - 4))
    seen = np.zeros((H, W), bool); q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if bg[y, x]: seen[y, x] = 1; q.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if bg[y, x] and not seen[y, x]: seen[y, x] = 1; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < W and not seen[yy, xx] and bg[yy, xx]: seen[yy, xx] = 1; q.append((yy, xx))
    m = Image.fromarray(((~seen) * 255).astype("uint8")).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert("RGBA"); out.putalpha(m)
    return out.crop(m.point(lambda v: 255 if v > 8 else 0).getbbox())

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = Image.open(CP / "raw/tempura_intro_jp_p1.png")      # 2400x1800
    h = Image.open(CP / "raw/hotsauce_vegan_p2.png")        # 1600x2844（ORIGINAL の瓶）
    bag = bag_cutout(t.crop((140, 260, 670, 1120)))
    bag.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(OUT / "tempura-bag.png", optimize=True); bag.save(OUT / "tempura-bag.webp", quality=86, method=6); print("tempura-bag", bag.size)
    save(t.crop((104, 1250, 728, 1678)), "tempura-vegetables")  # 野菜天
    save(t.crop((1036, 1356, 1518, 1684)), "tempura-ebi")       # エビ天
    save(h.crop((975, 1955, 1425, 2545)), "hotsauce-original")  # ORIGINAL 瓶1本（白い地）
    tk = Image.open(CP / "crops/takoyaki-mix-pack-front_flyer-p5.png")  # 490x620。左上の NEW! の赤を外す
    save(tk.crop((14, 40, 476, 612)), "takoyaki-pack")

if __name__ == "__main__": main()
