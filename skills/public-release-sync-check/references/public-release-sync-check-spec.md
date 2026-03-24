# public-release-sync-check Spec

## 目的

`public-release-sync-check` は、Unity / VRChat package repo の公開前に、
公開面のズレを検出して次アクションを案内する診断専用 Skill として設計する。

初版の役割は次に限定する。

- version / URL / metadata / BOOTH_PACKAGE / README / TOOL_INFO / workflow の整合確認
- 問題の `Blocking` / `Warning` 分類
- 次に使う prompt 番号と修正方向の案内

初版では、自動修正、自動 release、listing 更新、BOOTH 本文生成までは広げない。

## この文書の置き場所

この spec の正本は
`skills/public-release-sync-check/references/public-release-sync-check-spec.md`
に置く。

理由:

- Skill 本体と参照 spec を同じ knowledge repo 内で管理できる
- package repo 側に正本を残さず、共通ルールの参照先を 1 つにできる
- repo 固有差分は package repo の `CODEX_HANDOFF.md` に残し、共通 spec とは分離できる

## 対象範囲

初版で対象にするのは、単一 package repo に対する `pre-release` 診断のみ。

- repo root の公開面ファイルを読む
- 共通知識として knowledge repo の公開運用ルールを読む
- repo 固有差分は `CODEX_HANDOFF.md` で確認する
- 出力は診断結果と次アクション案内だけに留める

対象ファイル:

- `package.json`
- `README.md`
- `TOOL_INFO.md`
- `CHANGELOG.md`
- `.github/workflows/*`
- `BOOTH_PACKAGE/*`
- `CODEX_HANDOFF.md` があれば参照

## 非対象範囲

初版では次を対象外にする。

- Skill 実装本体
- 自動修正処理
- commit / push
- GitHub Release 作成
- listing repo 更新
- VCC 実機確認
- BOOTH 商品本文、画像、zip 作成
- workflow の細部実装レビュー
- release asset の中身確認
- repo 外の実公開状態確認
- AGENTS / config 追加

対象外にする理由は、最初の 1 個目として軽く安全に始めるためであり、
診断と修正実行を分けた方が再利用しやすいから。

## 最小 I/O

### 入力

| 項目 | 必須 | 初版の扱い |
| --- | --- | --- |
| `target_repo` | 必須 | local の repo root path |
| `expected_version` | 任意 | 指定があれば canonical version に使う |
| `check_scope` | 任意 | 省略時は `pre-release` |

初版の `check_scope` は `pre-release` だけを正式対応とする。
それ以外の値は将来拡張用の予約枠として残し、
初版では issue 化せず、入力未対応として即終了する。

このケースでは:

- `status` は `unsupported-input`
- `scope.supported` は `false`
- `issues` は空
- `suggested_next_action` は prompt 番号ではなく入力修正案内を返す

### 出力

人間向けレポートでは、次の区分で返せればよい。

- `Summary`
- `Canonical values`
- `Blocking issues`
- `Warnings`
- `Suggested next action`
- `Optional patch hints`

最小出力の想定:

- `Summary`
  - `status`
  - `check_scope`
  - `blocking_count`
  - `warning_count`
- `Canonical values`
  - `package_name`
  - `display_name`
  - `canonical_version`
  - `repo_url`
  - `vcc_index_url`
  - `listing_page_url`
- `Blocking issues`
  - `id`
  - `files`
  - `current`
  - `expected`
  - `why_blocking`
- `Warnings`
  - `id`
  - `files`
  - `current`
  - `expected`
  - `why_warning`
- `Suggested next action`
  - primary prompt 番号 1 つ
  - 必要なら secondary prompt 番号 1 つ
  - なぜその prompt を使うかの短い理由
- `Optional patch hints`
  - file path
  - 直す方向を 1 行

### 出力 schema 固定案

人間向けの見出しとは別に、内部の固定 schema は次で揃える。

```json
{
  "status": "ok | warning | blocking | unsupported-input",
  "scope": {
    "requested": "string",
    "effective": "pre-release | null",
    "supported": "boolean"
  },
  "canonical_values": "CanonicalValues | null",
  "issues": ["Issue"],
  "suggested_next_action": "SuggestedNextAction | null"
}
```

#### `status`

- `unsupported-input`
  - `check_scope` が初版未対応
- `ok`
  - `issues` が 0 件
- `warning`
  - `blocking` 0 件、`warning` 1 件以上
- `blocking`
  - `blocking` 1 件以上

`Summary` は別 field にせず、`status` と `issues` 件数から組み立てる。

#### `scope`

```json
{
  "requested": "pre-release",
  "effective": "pre-release",
  "supported": true
}
```

unsupported input の時だけ `effective` は `null` になる。

#### `canonical_values`

```json
{
  "canonical_version": {
    "value": "0.1.3",
    "source": "expected_version | package.json.version"
  },
  "package_name": {
    "value": "com.example.tool",
    "source": "package.json.name"
  },
  "display_name": {
    "value": "Example Tool",
    "source": "package.json.displayName"
  },
  "repo_url": {
    "value": "https://github.com/example/repo",
    "source": "git_remote | repo_name_rule"
  },
  "vcc_index_url": {
    "value": "https://.../index.json",
    "source": "knowledge.PUBLIC_RELEASE_GUIDELINES.vcc_index_url"
  },
  "listing_page_url": {
    "value": "https://.../",
    "source": "knowledge.PUBLIC_RELEASE_GUIDELINES.listing_page_url"
  }
}
```

#### `Issue`

```json
{
  "id": "version.package_json.mismatch",
  "severity": "blocking | warning",
  "category": "version | url | metadata | file-existence | docs-role-drift",
  "summary": "short sentence",
  "files": ["package.json", "CHANGELOG.md"],
  "current": "0.1.2",
  "expected": "0.1.3",
  "rule_source": "PUBLIC_RELEASE_GUIDELINES.md",
  "why": "why this matters",
  "patch_hint": {
    "file": "CHANGELOG.md",
    "direction": "Update latest heading to canonical_version"
  }
}
```

固定ルール:

- `unsupported-input` の時は `issues` を空にする
- `Blocking issues` / `Warnings` は `issues` を severity で分けて表示する
- `patch_hint` は任意で、実 patch や自動修正は含めない

#### `SuggestedNextAction`

```json
{
  "mode": "prompt-bank | fix-input | none",
  "primary_prompt_id": "2-8b | null",
  "secondary_prompt_id": "2-10 | null",
  "reason": "short sentence",
  "source": "CODEX_PROMPT_BANK.md | null"
}
```

固定ルール:

- 通常診断時は `mode: prompt-bank`
- unsupported input の時は `mode: fix-input`
- 問題なしで次アクション不要なら `mode: none`
- primary は最大 1 件、secondary も最大 1 件

### I/O 妥当性メモ

この 3 入力で初版は成立する。

- `target_repo` だけで対象ファイル位置を特定できる
- `expected_version` があれば公開予定 version に寄せて診断できる
- `check_scope` を 1 つだけ持たせれば、将来の scope 拡張余地を残せる

追加入力を増やさない理由:

- repo 固有例外は Skill 入力ではなく `CODEX_HANDOFF.md` に逃がしたい
- prompt bank 番号体系は knowledge repo 側に残したい
- owner や listing URL は共通知識から引けるため、毎回入力させる必要が薄い

## 参照する情報源

### Skill が参照する共通情報源

- `PUBLIC_RELEASE_GUIDELINES.md`
  - 公開順
  - version 表記ルール
  - URL 役割分離
  - package metadata 最低限
  - BOOTH_PACKAGE 最小構成
  - 公開前チェック観点
- `CODEX_PROMPT_BANK.md`
  - 次アクションで返す prompt 番号の参照元
- `PROJECT_SHARED_CONTEXT.md`
  - 共通前提と repo 固有差分の置き分け
- `REPO_INDEX.md`
  - package repo 群と運用コンテキストの確認

### Skill が参照する repo 内情報源

- `package.json`
- `README.md`
- `TOOL_INFO.md`
- `CHANGELOG.md`
- `.github/workflows/*`
- `BOOTH_PACKAGE/00_README_FIRST.txt`
- `BOOTH_PACKAGE/01_VCC_INSTALL.txt`
- `BOOTH_PACKAGE/02_QUICKSTART.txt`
- `BOOTH_PACKAGE/LICENSE`
- `CODEX_HANDOFF.md`

## Canonical values の決め方

初版では、公開面で揃うべき値を次の順で決める。

1. `canonical_version`
   - `expected_version` があればそれを採用
   - なければ `package.json.version`
2. `package_name`
   - `package.json.name`
3. `display_name`
   - `package.json.displayName`
4. `repo_url`
   - git remote origin から取得できるならそれを優先
   - 無ければ knowledge repo の owner 規則と repo 名から期待値を組み立てる
   - `package.json.url` は canonical 値の元ではなく、比較対象として扱う
5. `vcc_index_url`
   - `PUBLIC_RELEASE_GUIDELINES.md` の `VPM / VCC 導線` セクションから期待値を取る
6. `listing_page_url`
   - `PUBLIC_RELEASE_GUIDELINES.md` の `VPM / VCC 導線` セクションから期待値を取る

重要:

- 初版は missing 値を黙って補完しない
- 推定できても、repo 側に値が無い時は `expected` として示し、`current` は missing 扱いにする
- repo 固有例外は Skill の内部ルールに埋め込まず、`CODEX_HANDOFF.md` に逃がす

## 判定ルール

### 1. version 整合

初版で見るもの:

- `package.json.version`
- `CHANGELOG.md` の最新数値 version 見出し
- `BOOTH_PACKAGE` 内の明示 version
- `README.md` と `TOOL_INFO.md` の明示 version

補足:

- `CHANGELOG.md` の先頭が `[Unreleased]` の時は、それを比較対象にしない
- この場合は `[Unreleased]` をスキップして、最初の数値 version 見出しを使う

`Blocking` にするもの:

- `package.json.version` が missing
- `package.json.version` が SemVer でない
- `package.json.version` が `v1.2.3` のように `v` 付き
- `expected_version` 指定時に `package.json.version` と一致しない
- `CHANGELOG.md` の最初の数値 version 見出しが canonical version と一致しない
- `BOOTH_PACKAGE` 内の明示 version が canonical version と一致しない

理由:

- version の基準値が曖昧だと release / listing / BOOTH の全導線で事故になりやすい
- `CHANGELOG.md` と BOOTH_PACKAGE は公開面の version 表示として直接見られる

`Warning` にするもの:

- `README.md` に明示 version があり、canonical version とズレる
- `TOOL_INFO.md` に明示 version があり、canonical version とズレる

理由:

- `README.md` と `TOOL_INFO.md` は version を常時書く前提ではない
- ただし書いてあるなら stale な記載は検出したい

### 2. URL 役割整合

初版で見るもの:

- repo URL
- VCC / VPM 用 `index.json` URL
- listing page URL
- `README.md` と `BOOTH_PACKAGE` の案内文

`Blocking` にするもの:

- `README.md` または `BOOTH_PACKAGE` が、VCC に追加する URL として listing page を案内している
- `README.md` または `BOOTH_PACKAGE` が、repo URL を VCC 追加先として案内している
- `01_VCC_INSTALL.txt` に `index.json` が出てこない

理由:

- URL の役割混線は、そのまま導入失敗につながる

`Warning` にするもの:

- `README.md` に listing page が無い、または repo URL 導線が弱い
- `README.md` の VCC 導線があるが、listing page との役割説明が弱い
- `BOOTH_PACKAGE` の repo / listing page 導線が不足している

理由:

- 主導線が壊れていなければ即失敗ではない
- ただし公開面の迷いやすさは早めに拾いたい

### 3. package metadata 基本整合

初版で見るもの:

- `name`
- `displayName`
- `version`
- `url`
- `changelogUrl`
- `licensesUrl`

`Blocking` にするもの:

- 上記キーが missing または空
- `url` が別 repo を向いている
- `changelogUrl` が `CHANGELOG.md` 以外を向いている
- `licensesUrl` が `LICENSE` 以外を向いている
- `displayName` と `README.md` / `TOOL_INFO.md` の公開名が明確に食い違う

理由:

- package metadata は listing と package manager 上の公開面に直結する
- ここが壊れていると repo 文書を直しても公開面が揃わない

初版で `Warning` に留めるもの:

- URL の branch 名までの厳密一致

理由:

- default branch は repo ごとに揺れ得る
- 初版は branch 判定まで広げず、まず file 先と repo 先の整合だけを見る

初版で対象外にするもの:

- `documentationUrl`

理由:

- `PUBLIC_RELEASE_GUIDELINES.md` 上は重要だが、最初の 1 個目としては判定対象を増やしすぎる
- まずはユーザーが指定した 6 項目に絞る

### 4. 公開導線ファイルの存在確認

初版で見るもの:

- `.github/workflows/*`
- `BOOTH_PACKAGE` の基本 4 点

`Blocking` にするもの:

- `BOOTH_PACKAGE/00_README_FIRST.txt` が無い
- `BOOTH_PACKAGE/01_VCC_INSTALL.txt` が無い
- `BOOTH_PACKAGE/02_QUICKSTART.txt` が無い
- `BOOTH_PACKAGE/LICENSE` が無い

理由:

- BOOTH 向けの最小導線が欠けているため

`Warning` にするもの:

- `.github/workflows/` が空、または workflow file が無い
- workflow file はあるが、初版の簡易確認では release workflow か判定しづらい

理由:

- 初版では workflow の中身深掘りはやらない
- `.github/workflows/` が空でも、初版では「即 release 不可」ではなく「標準運用未達」として扱う
- ただし `2-10` を促すべきかの補助情報にはなる

### 5. README / TOOL_INFO の役割ズレ

初版で見るもの:

- ツール名
- 冒頭説明
- VCC 導線の有無
- 非破壊 / Dry Run の案内有無

`Blocking` にするもの:

- `README.md` のタイトル、`TOOL_INFO.md` のツール名、`package.json.displayName` が別物に見える

理由:

- ツールの同一性が崩れると公開面の信頼性が落ちる

`Warning` にするもの:

- `README.md` 冒頭説明と `TOOL_INFO.md` の想定用途が大きくズレる
- `README.md` に VCC / VPM 導線が無い
- repo 内の他文書では `Dry Run` や `非破壊` を重視しているのに、`README.md` と `BOOTH_PACKAGE` で触れていない

理由:

- 使い始めの理解コストは上がるが、即座に release 不可とまでは言い切れない
- `Dry Run` や `非破壊` は repo 固有差分を含みやすいため、初版では presence check を Warning に留める

## 初版であえて入れないもの

次は初版で対象外にする。

- GitHub Release の実在確認
- listing repo 側 `source.json` との突合
- VCC 実機確認
- release zip の中身確認
- workflow の trigger や upload step の詳細評価
- UI 文言や menu path をコードから検証すること
- BOOTH 商品本文、商品画像、SNS 告知文
- repo ごとの特殊な許容ルールの自動分岐

理由:

- 実装が重くなりやすい
- repo 固有差分を Skill に飲み込みやすい
- 「診断専用の 1 個目」という狙いから外れやすい

## 最小手順

1. `check_scope` が `pre-release` か確認し、未対応なら `unsupported-input` で即終了する
2. knowledge repo の共通ルールを読む
3. `target_repo` の公開面ファイルを読む
4. `expected_version` があればそれを優先して canonical values を組み立てる
5. version / URL / metadata / file existence / role drift の順に診断する
6. `Blocking` / `Warning` を分類する
7. issue のまとまりから次に使う prompt 番号を 1 つ決める
8. 必要なら secondary prompt 番号と patch hint を付ける

## Suggested next action の返し方

Skill は prompt 本文を持たず、番号と使い分けだけ返す。

初版の最小マッピング:

| 主な検出内容 | 返す prompt |
| --- | --- |
| 公開前の最終再確認を回したい | `2-8` |
| 公開面の違和感レビューを先にしたい | `2-8a` |
| `README.md` / `TOOL_INFO.md` / `package.json` の公開面を揃えたい | `2-8b` |
| 公開準備全体の不足整理が必要 | `2-9` |
| release workflow が無い、または怪しい | `2-10` |
| `BOOTH_PACKAGE` 基本 4 点が欠ける | `2-11` |

制約:

- 返すのは primary 1 件を基本にする
- secondary は本当に次に分けて頼む価値がある時だけ付ける
- prompt 番号体系と本文の正本は knowledge repo 側に残す

## 参照元の切り分け

### Skill に持たせるもの

- 再利用できる判定ルール
- 見るファイル一覧
- 出力フォーマット
- `Blocking` / `Warning` の判定基準

### knowledge repo に残すもの

- 公開順
- version 表記ルール
- VCC / listing の役割分離
- BOOTH_PACKAGE 最小構成
- prompt bank の番号体系

### AGENTS にまだ入れないもの

- 公開ルール全文
- repo ごとの差分
- 特殊ケース分岐

### `CODEX_HANDOFF.md` に残すもの

- 今回だけの target version
- 例外扱い
- repo 固有の公開導線
- 今回だけ未対応だが許容するもの

補足:

- 初版 Skill は `CODEX_HANDOFF.md` を「例外の置き場」として読む
- ただし handoff から自由に新ルールを注入しない
- handoff は issue の注記や許容理由の参照先に留める

## 将来拡張候補

初版の外に置く拡張候補:

- `documentationUrl` の厳格チェック
- workflow の trigger / zip 名 / 除外対象まで見る詳細診断
- release asset 名と `package.json.version` の一致確認
- listing repo `source.json` との突合
- GitHub Release / tag の実在確認
- UI 文言や menu path のコード照合
- patch 提案の半自動生成
- `pre-release` 以外の scope 追加

将来拡張候補は書いてよいが、初版本体に混ぜない。
