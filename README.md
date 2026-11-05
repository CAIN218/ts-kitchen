# Gluten Free T's Kitchen 新ホームページ（プレビュー版）

[glutenfree.co.jp](https://glutenfree.co.jp/) のリニューアル案です。お店に確認してもらうためのプレビューで、検索エンジンには載らない設定（noindex / robots.txt）にしています。

## 主な変更点
- 店舗情報を3店舗のカードに整理（営業時間の表、電話・地図・店舗別予約ボタン）
- 日本語 / English 切替（予約ページ・メニューのリンクも英語版に切替）
- キャンセルポリシーを店舗一覧の下で強調
- ケータリング・お弁当を独立したセクションに（画面右下に重なるチラシを廃止）
- スマホ用メニュー
- 原宿店の地図リンクを修正（現行サイトでは六本木店の地図になっている）
- 会社概要ページ（about.html）・メニューページ（menu.html）を新規作成

## 本番化の前にやること
- [ ] お店に内容（特にアレルギー表記・営業時間）を確認してもらう
- [ ] 写真をこのリポジトリの `src/images/` に移す（今は現行サイトから読み込み）
- [ ] TableCheck英語版の予約URLが正しく開くか確認
- [ ] メニュー・会社概要など他ページの扱いを決める
- [ ] 公開先（Cloudflare Pages / Netlify など）とドメイン切替の方法を決める（メールのMXレコードに注意）

## 写真の差し替え
- 原宿店の写真：`src/images/harajuku.jpg` という名前で置くと、トップページの原宿店カードに自動で表示されます（横長、1200×750px程度がおすすめ）。置くまではロゴが表示されます。

## フォルダの構成（2026-11-05 整理）
- `src/`：本番（WordPress）用の元データ。`index.html` / `menu.html` / `about.html` / `consulting.html` / `media.html`、`style.css`、`script.js`、`anim/site.*`、`images/`
- `tools/build_wp.py`：`src/` から WordPress に貼る断片（`wp/`）を作る
- `renew14/`：新デザインのプレビュー（`python3 tools/build_preview.py` で `src/` から作り直す）
- ルートの `index.html`：プレビュー（`renew14/`）へ転送するだけのページ
- 以前のデモ（concepts / refine / refresh / renew〜renew13 など）は削除済み。必要なら git の履歴から戻せます
