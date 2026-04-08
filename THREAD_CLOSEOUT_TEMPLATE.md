# THREAD_CLOSEOUT_TEMPLATE

## 目的
スレ終了時に、そのスレで出た内容を
- knowledge repo に残す候補
- 各 repo の `CLAUDE.md` に残す候補
- 整理 / 見送り候補
へ最小で切り分けるためのテンプレ。

## このテンプレでまだやらないこと
- AGENTS / config の自動更新
- `CLAUDE.md` の自動更新
- Skill 実装や config 追加
- 単発ログの大量保存

## 抽出ルール
- 推測で埋めない
- 単発ログより、今後も再利用する内容を優先する
- `共通化向き / repo 固有 / 見送り` を分ける
- 迷うものはまず knowledge repo 候補として短く保持し、AGENTS 追加は保留する
- `CLAUDE.md` 候補は 3〜5 行で短くする

## closeout 出力チェックリスト

closeout に入ったら、以下を順番に出し切る。

1. □ 網羅的実装確認（Claude Code に依頼）
2. □ 修正が出たら修正依頼
3. □ closeout まとめ（やったこと・設計変更・後回し候補）
4. □ CLAUDE.md 更新指示（Claude Code 用）+ Notion セッション記録 DB 投入（Claude が直接）
5. □ knowledge base 追記案（具体文面まで出し切る）
6. □ 引き継ぎパッケージ（次スレ冒頭に貼れる状態）

全項目を1ターンで出し切る。「あとは〜」「残りは次回」にしない。
配置待ちファイル（technical/ や guide-source/ 向け）があれば CLAUDE.md 更新指示に含める。

## 出力テンプレ

### 0. closeout 要否
- 要否:
- 理由:

### 1. knowledge repo 追加候補
- 追加先候補:
- タイトル案:
- 残す内容:
- 再利用理由:
- 今回は草案だけでよいか:

### 2. `CLAUDE.md` 候補
- repo:
- 入れる場所:
- 追記案（3〜5行）:
- knowledge repo ではなく CLAUDE.md に寄せる理由:

### 3. 整理 / 統合 / 削除候補
- 対象:
- 理由:
- どう整理するか:

### 4. 今回は見送るもの
- 内容:
- 見送る理由:
- 次に拾う条件:

### 5. 次アクション
- Claude（claude.ai）側:
- Claude Code 側:
- 次スレに持ち越すこと:

---

## 次スレ開始テンプレ

closeout 後、次スレを始める時はこのテンプレをそのまま冒頭に貼る。

※ 冒頭に引き継ぎパッケージがないと、状況確認のやり取りが発生して
スレの立ち上がりが遅くなります。

```
## 前スレでやったこと
（箇条書き3〜5行）

## 現在の状態
（CLAUDE.md の Current State 要約）

## 今日やりたいこと
（1〜3行）

## 引き継ぎ
- repo: （対象 repo のパス）
- CLAUDE.md（repo 固有 / knowledge base）を読んでから始めてください
- 前回の closeout 候補の反映: 済み
```

### 引き継ぎパッケージの作り方

closeout 後、Claude（claude.ai）が草案を出したら
以下の指示を Claude Code に渡して整形・補完してもらう。

```
次スレの引き継ぎパッケージを作ってください。

## 読んでほしいファイル
- sebanne-dev-knowledge-base の CLAUDE.md 全体
- 対象 repo の CLAUDE.md

## 出力してほしいもの
THREAD_CLOSEOUT_TEMPLATE.md の「次スレ開始テンプレ」形式で
次スレ冒頭に貼れる状態にしてください。
```
