---
name: initial-release-prep
description: 初回リリース向けの公開準備を一括で進めるオーケストレーション Skill。棚卸し → ドキュメント整備 → workflow → BOOTH_PACKAGE → sync-check → version 固定 → BOOTH zip 作成までを Claude Code が実行し、GitHub Release 以降は手作業チェックリストとして出力する。
---

# initial-release-prep

初回リリース向けの公開準備 Skill。
PUBLIC_RELEASE_GUIDELINES.md の「公開準備の進め方（初回リリース）」10 ステップを一括で回す。

## Quick Start

Claude（claude.ai）から Claude Code に以下の形式で指示する:

```
initial-release-prep の SKILL.md を読んで、対象リポに対して初回リリース準備を実行してください。

- target_repo: {対象リポのパス}
- version: {リリース version（SemVer、v 無し）}

計画のみ出してください。「進めてください」と返答するまで実装しないでください。
```

## Inputs

| パラメータ | 必須 | 説明 |
|---|---|---|
| `target_repo` | 必須 | 対象リポのローカルパス |
| `template_repo` | 任意 | 横並び参照用テンプレリポのパス。省略時は `sebanne-unity-vrchat-tool-template` の標準パス |
| `version` | 必須 | 初回リリースの version（SemVer、`v` 無し。例: `1.0.0`） |

displayName・package name 等は対象リポの package.json から読む。
不足があればステップ 1（棚卸し）で検出する。

---

## Workflow

ステップ 1〜6b を Claude Code が実行する。
各ステップは PUBLIC_RELEASE_GUIDELINES.md の該当セクションに従う。
手順の詳細はここに重複して書かず、参照先に委ねる。

### ステップ 1: 棚卸し

対象リポ全体をコード面で網羅確認する。

観点:
- 壊れている箇所・設計と実装の乖離
- 未実装・デッドコード
- モード間の不整合
- CLAUDE.md との乖離
- package.json の必須フィールド不足

出力: 実装済み / 懸念あり / 未実装 / 要確認 に分類し、ファイル名・行番号・深刻度を添える。

### ── ゲート A ──

棚卸しレポートを提示し、せばんぬの承認を得る。
承認前にステップ 2 以降に進まない。

### ステップ 2: ドキュメント調整

README / TOOL_INFO / package.json / CHANGELOG をテンプレリポと横並びで整備する。

- テンプレリポの同等ファイルを読み、構成・トーン・情報量を揃える
- package.json: 必須フィールド（name / displayName / version / url / changelogUrl / licensesUrl）を確認・補完
- README: タイトル / 概要 / 使い方 / 制限事項 / VCC 導線
- TOOL_INFO: テンプレの構成に合わせる
- CHANGELOG: 初回リリースの見出しを version に合わせる

参照: PUBLIC_RELEASE_GUIDELINES.md「package 公開の基本」、テンプレリポの各ファイル。

### ステップ 3: release workflow 整備

テンプレリポの `.github/workflows/release-package.yml` をコピーし、
`include_paths` 配列をツール固有の構成に合わせて調整する。

確認観点:
- `include_paths` にツール固有のフォルダ・ファイルが含まれているか
- 不要なテンプレデフォルト（`Editor` / `Runtime` 等）が残っていないか、または不足していないか

参照: テンプレリポ `.github/workflows/release-package.yml`。

### ステップ 4: BOOTH_PACKAGE 作成

テンプレリポの `BOOTH_PACKAGE/` 4 ファイルをコピーし、ツール固有の内容に書き換える。

- `00_README_FIRST.txt` — ツール名・概要・リンク
- `01_VCC_INSTALL.txt` — VCC 導入手順（index.json URL）
- `02_QUICKSTART.txt` — 最短の使い方
- `LICENSE`

タグ判断:
- 共通タグを確認（PUBLIC_RELEASE_GUIDELINES.md「BOOTH タグの基本形」）
- MA タグの有無を判断（MA コンポーネントを使っているか / MA 対応か / MA 不使用か）
- ツール固有タグ・商品名はここでは決めない（ステップ 10 で決定）

参照: PUBLIC_RELEASE_GUIDELINES.md「BOOTH_PACKAGE の基本形」「文面方針」、テンプレリポ `BOOTH_PACKAGE/`。

### ステップ 5: sync-check 実行

既存の public-release-sync-check Skill を呼び出す。

```bash
python skills/public-release-sync-check/scripts/public_release_sync_check.py <target_repo> --expected-version <version>
```

出力の Blocking / Warning を確認し、修正計画を立てる。

### ── ゲート B ──

sync-check レポートと修正計画を提示し、せばんぬの承認を得る。
承認前にステップ 5b 以降に進まない。

### ステップ 5b: sync-check 指摘解消

ゲート B で承認された修正計画に従い、Blocking / Warning を解消する。

commit: ドキュメント・workflow・BOOTH_PACKAGE の変更をまとめて commit する。
commit prefix は `docs` または `chore`（PUBLIC_RELEASE_GUIDELINES.md「commit の考え方」参照）。

### ステップ 6: version 固定

package.json / CHANGELOG / BOOTH_PACKAGE 内の version を確定値に揃える。

commit: version bump を単独で commit + push する。

### ステップ 6b: BOOTH zip 作成

`BOOTH_PACKAGE/` フォルダから BOOTH 配布 zip を作成する。

- 出力先: `Releases/booth/{ToolName}/{ToolName}_BOOTH_Package_v{version}.zip`
- zip 展開直下にファイルが見える形にする（BOOTH_PACKAGE/ フォルダ自体は含めない）
- .meta ファイルは除外する

参照: PUBLIC_RELEASE_GUIDELINES.md「BOOTH zip の作成」。

---

## Handoff Checklist

ステップ 7〜10 はせばんぬの手作業。Claude Code はこのチェックリストを出力して終了する。

```
## 手作業チェックリスト

### 7. GitHub Release
- [ ] `gh release create {version} --notes "..."` で release 作成
- [ ] release asset zip が正しく添付されているか確認
- [ ] asset zip 内に package.json が展開直下に見えるか確認

### 8. VPM listing 更新
- [ ] source.json の githubRepos に対象リポが登録済みか確認
- [ ] listing repo の GitHub Actions workflow dispatch で再ビルド
- [ ] Pages で新 version が反映されているか確認
- [ ] listing repo 側の走査: source.json の githubRepos + README の package リスト

### 9. VCC 確認
- [ ] VCC で新 package が表示されるか確認
- [ ] VCC からインストールできるか確認

### 10. BOOTH 公開
- [ ] 商品名の決定
- [ ] ツール固有タグの決定（共通タグ + MA タグは Skill 内で判断済み）
- [ ] BOOTH zip アップロード（Releases/booth/{ToolName}/ にある zip）
- [ ] 商品説明文の作成（PUBLIC_RELEASE_GUIDELINES.md「BOOTH 商品説明文の基本形」参照）
- [ ] 商品画像の準備
- [ ] 公開
- [ ] リリース管理 DB 更新
```

---

## Boundaries

### やること

- 初回リリースの公開準備（ステップ 1〜6b）
- 既存の public-release-sync-check Skill の呼び出し（ステップ 5）
- 各ステップの実行結果レポート
- 手作業チェックリストの出力（ステップ 7〜10）

### やらないこと

- patch リリース（別フロー。PUBLIC_RELEASE_GUIDELINES.md「patch リリースチェックリスト」参照）
- GitHub Release の作成・asset 確認（手作業）
- listing repo の更新・走査（手作業）
- VCC の実機確認（手作業）
- BOOTH 商品ページの作成・公開（手作業）
- BOOTH 商品名・ツール固有タグの決定（手作業）
- 対象リポの新規作成（テンプレからの fork は別作業）
- sync-check のルール変更や拡張
- repo 固有の例外ルールの Skill への取り込み（CLAUDE.md に逃がす）

---

## References

- `PUBLIC_RELEASE_GUIDELINES.md` — 公開準備の手順 / version 表記 / BOOTH_PACKAGE 構成 / commit の考え方 / BOOTH 商品説明文の基本形
- `skills/public-release-sync-check/SKILL.md` — ステップ 5 で呼び出す既存 Skill
- テンプレリポ（`sebanne-unity-vrchat-tool-template`）— ステップ 2〜4 の横並び参照元
- `CLAUDE.md` セクション 11 — リリース前走査の推奨フロー（棚卸しと sync-check の役割分担）
