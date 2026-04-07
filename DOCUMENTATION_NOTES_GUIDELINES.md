# Documentation~/notes/ 運用ガイド

## 目的

各 package repo の `Documentation~/notes/` は、開発中に生まれるメモ・知見・作業ログの置き場所です。
`CLAUDE.md` に昇格するほどではないが、後から参照する価値がある内容をここに残します。

---

## フォルダ構成

```
Documentation~/notes/
├── sessions/      ← セッション記録（作業ログ・closeout まとめ）
├── technical/     ← 技術メモ（設計判断・実装知見・デバッグ経緯）
├── guide-source/  ← PDF 素材（ユーザー向け使い方・操作手順・機能説明）
└── archive/       ← 整理候補（古い・重複・他に統合済み）
```

---

## 各フォルダの用途

### sessions/
- 作業セッションのログ、closeout まとめ、リリースノート
- 「いつ何をやったか」の記録。後から経緯を追う時に使う
- PDF にも技術メモにも直接は使わない

### technical/
- 設計判断の経緯、実装知見、デバッグで得た知見
- 開発者（自分）が後から「なぜこうしたか」を追う時に使う
- 一部は PDF 素材に転用できる場合もある

### guide-source/
- ユーザー向けの使い方・機能説明・操作手順
- BOOTH 同梱 PDF や README の素材として使う前提
- 技術的な実装経緯は含めず、ユーザーが読む内容に絞る

### archive/
- 内容が古くなったもの、他のファイルに統合済みのもの
- 削除ではなく archive に移動し、必要時に参照できる状態を保つ

---

## 命名規則

| フォルダ | 形式 | 例 |
|---|---|---|
| sessions/ | `YYYY-MM-DD_{トピック}.md` | `2026-04-07_v1.1.0-dev.md` |
| technical/ | `{トピック名}.md`（日付なし） | `playback-control-integration.md` |
| guide-source/ | `{トピック名}.md`（日付なし） | `ffmpeg-setup.md` |
| archive/ | 元のファイル名のまま | `preset-ui-implementation.md` |

- ケバブケース（小文字、ハイフン区切り）で統一
- sessions のみ日付プレフィックス付き（時系列で並ぶため）

---

## 判断基準

| 内容 | 置き場所 |
|---|---|
| ユーザー向けの使い方・操作手順 | guide-source/ |
| 設計判断・実装知見・デバッグ経緯 | technical/ |
| 作業ログ・closeout・リリースノート | sessions/ |
| CLAUDE.md に昇格済み・内容が古い | archive/ |
| 今後も何度も参照する変わりにくい前提 | notes ではなく CLAUDE.md に昇格 |

---

## 溜めすぎない原則

- notes は「一時的な中間置き場」であり、最終的な正本ではない
- CLAUDE.md に昇格済みの知見は archive/ に移動する
- 同じトピックのメモが複数ある場合は統合を検討する
- セッション記録は増えやすいが、古いものを積極的に削除する必要はない（archive で十分）
- 迷ったらまず notes に置き、次のセッションで昇格 or archive を判断する
