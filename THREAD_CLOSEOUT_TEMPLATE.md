# THREAD_CLOSEOUT_TEMPLATE

## 目的
スレ終了時に、そのスレで出た内容を
- knowledge repo に残す候補
- 各 repo の `CODEX_HANDOFF.md` に残す候補
- 整理 / 見送り候補
へ最小で切り分けるためのテンプレ。

## このテンプレでまだやらないこと
- AGENTS / config の自動更新
- `CODEX_HANDOFF.md` の自動更新
- Skill 実装や config 追加
- 単発ログの大量保存

## 抽出ルール
- 推測で埋めない
- 単発ログより、今後も再利用する内容を優先する
- `共通化向き / repo 固有 / 見送り` を分ける
- 迷うものはまず knowledge repo 候補として短く保持し、AGENTS 追加は保留する
- `CODEX_HANDOFF.md` 候補は 3〜5 行で短くする

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

### 2. `CODEX_HANDOFF.md` 候補
- repo:
- 入れる場所:
- 追記案（3〜5行）:
- knowledge repo ではなく handoff に寄せる理由:

### 3. 整理 / 統合 / 削除候補
- 対象:
- 理由:
- どう整理するか:

### 4. 今回は見送るもの
- 内容:
- 見送る理由:
- 次に拾う条件:

### 5. 次アクション
- ChatGPT 側:
- Codex 側:
- 次スレに持ち越すこと:
