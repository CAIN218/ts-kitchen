# Gluten Free T's Kitchen サイト（CAIN218/ts-kitchen）

## リポジトリ
- `src/`：本番（WordPress）用の元データ。`tools/build_wp.py` で `wp/` を作る。
- `split/`：新デザインのプレビュー（日本語 `split/`、英語 `split/en/`）。`python3 tools/build_preview.py` で `src/` から作り直す。共通のCSS・JSは `assets/`。
- 生成されたHTML（`split/`、`wp/`）は手で直さず、元を直して作り直す。

## 守ること
- 公開中サイトの文章・数字・名前・アレルギー表記・画像は変えない。食い違いは「要確認事項」として報告する。
- ブランドの紺 #1c2b45 は変えない。
- 公開中のWordPressを変える前は、必ず yuga さんの承認を取る（係の流れ：作る係 → yugaさんがデモを確認 → 公開する係 → HPを直す係）。

## 専門家チーム（`.claude/agents/`）
係のスレッドの中で、必要な専門家だけをサブエージェントとして呼ぶ。小さな修正では1〜2人に絞る。

| 名前 | 役割 |
|---|---|
| researcher | 既存サイト・競合・情報の正確さの調査（最初に呼ぶ） |
| brand-strategist | ブランドの方向・ターゲット・差別化 |
| art-director | ビジュアルの方向・配色・写真・文字組み・一貫性 |
| ux-designer | 情報設計・導線・ナビゲーション・スマホの使いやすさ |
| ui-designer | 画面構成・余白・文字組み・部品・レスポンシブ |
| content | 日英の対応・情報の優先順位（文章は書き換えず要確認事項を出す） |
| frontend-engineer | 実装・実装上の問題・速度・アクセシビリティ |
| design-critic | 実装前と実装後の批評（Critical / High / Medium / Low） |
| qa | 表示崩れ・リンク・スマホ・操作の検証（Critical / High / Medium / Low） |

### 進め方
1. 調査（researcher）→ 2. ブランド・ターゲット（brand-strategist）→ 3. 構成・UX（ux-designer）→ 4. コンセプト（art-director）→ 5. UI（ui-designer）→ 6. 実装前の批評（design-critic）→ 7. 実装（frontend-engineer）→ 8. 実装後の批評（design-critic）→ 9. QA（qa）→ 10. 修正・再評価 → 11. 総括経由で yuga さんにデモ
- 専門家同士は直接話せない。スレッドのClaudeが受け渡し役になる：前の専門家の出力を、次の専門家への依頼文にそのまま貼る。指摘は担当の専門家に戻し、直した結果を批評家に再評価させる。
- 受け渡しは1つの論点につき最大2往復。それでも決まらない時は、スレッドのClaudeが判断し、理由を報告に書く。
- Critical と High が残っている間は、デモとして出さない。
- 総括への報告には、調べたこと、呼んだ専門家、主な意見、採用したものと理由、残った指摘、要確認事項、次の作業を書く。
