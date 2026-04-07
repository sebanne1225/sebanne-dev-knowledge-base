# PUBLIC_RELEASE_GUIDELINES

## 目的
Unity / VRChat ツール公開時に、毎回ゼロから考えずに進めるための共通ルール。  
対象は主に次の公開導線です。

- GitHub Release
- VPM listing
- VCC 導入
- BOOTH 公開

---

## 基本の公開順
公開順は次を基本形にします。

1. GitHub Release
2. VPM listing 更新
3. VCC で導入確認
4. BOOTH 公開

### 考え方
- VPM / VCC で使われる最新版は、release と version と listing 反映を基準に見る
- BOOTH の導入案内や商品説明は、実際に使える release / listing / VCC 導線が先にある状態を前提にした方が事故が少ない
- BOOTH は最後に購入者向け導線をまとめる段として扱う

---

## version 表記
version 表記は `1.0.0` のような SemVer 形式を正とし、`v` は付けません。

### 運用ルール
- package.json.version は `1.0.0`
- Git tag も `1.0.0`
- GitHub Release の title も `1.0.0`
- CHANGELOG の見出しも `1.0.0`
- release asset 名も `...-1.0.0.zip`
- 公開文面も、特に理由がない限り `1.0.0` で揃える

### 補足
- workflow が `v1.0.0` を許容していても、運用上の基準は `1.0.0`
- すでに公開済み version に対して公開物の中身を変える場合は、基本的に patch version を上げる

---

## GitHub / owner / URL
GitHub の標準 owner / アカウント名は `sebanne1225` を前提にします。
branch は `main` 固定ではなく、対象 repo の default branch に合わせます。

### 基本形
- package repo: `https://github.com/sebanne1225/<repo-name>`
- changelogUrl: `https://github.com/sebanne1225/<repo-name>/blob/<default-branch>/CHANGELOG.md`
- licensesUrl: `https://github.com/sebanne1225/<repo-name>/blob/<default-branch>/LICENSE`

---

## VPM / VCC 導線
VCC に追加する URL と、listing 閲覧ページは役割を分けます。

### 正とする URL
- **VCC に追加する URL**  
  `https://sebanne1225.github.io/sebanne-listing/index.json`
- **listing page**  
  `https://sebanne1225.github.io/sebanne-listing/`

### 運用ルール
- `index.json` は VCC に追加するための URL
- listing page は閲覧用ページ
- README、BOOTH_PACKAGE、BOOTH 商品説明文ではこの役割を混ぜない
- listing page を参考ページとして併記する場合も、VCC に追加する URL ではないと分かる形で書く
- GitHub の listing repo URL は主導線にしない

### listing 更新の流れ
- package repo が `source.json` の `githubRepos` に登録済みなら、listing repo への commit・変更は不要
- 新 version は GitHub Release の asset zip から自動取得される
- ただし listing の再ビルドが必要。方法は次のいずれか：
  - listing repo に変更を push する（source.json 等の変更がある場合）
  - GitHub Actions の workflow_dispatch で手動実行する（変更がない場合）
- Release publish 後、listing の Pages を確認し、反映されていなければ手動 dispatch

---

## package 公開の基本

### package.json
最低限そろえる項目は次です。

- `name`
- `displayName`
- `version`
- `description`
- `documentationUrl`
- `changelogUrl`
- `licensesUrl`
- `url`

### release workflow
- GitHub Release に version 付き package zip を assets として添付できる workflow を基本構成にする
- release tag と package.json.version は一致させる
- release published 時に package zip を release assets に添付する
- 必要なら workflow_dispatch でも zip 作成確認ができるようにする
- listing に package が出ない時は、まず release asset zip の有無と version / tag の一致を確認する

### release asset
- repo 丸ごとの source zip は使わない
- package に必要な中身だけを zip にする
- zip 展開直下に `package.json` が見える形を基本にする
- asset 名は `package-id-<version>.zip`
  - 例: `com.sebanne.avatar-audio-safety-guard-1.0.1.zip`

### release zip に入れないもの
- `.github`
- `BOOTH_PACKAGE`
- repo 専用メモ
- handoff 文書
- 内部向け notes

---

## BOOTH_PACKAGE の基本形
BOOTH_PACKAGE は最小 4 点を基本形にします。

- `00_README_FIRST.txt`
- `01_VCC_INSTALL.txt`
- `02_QUICKSTART.txt`
- `LICENSE`

### 文面方針
- BOOTH 購入者向けに短く、安心感優先
- 技術説明より先に「何のツールか」「どう導入するか」「まず何をするか」を出す
- まず VCC / VPM
- まず Dry Run
- 非破壊ツールなら「元アバターには直接変更を加えません」を先に出す
- 「追加後の確認」「詰まりやすい点」などの補足は最小導線から外す
- VCC の導入案内は  
  `Settings -> Packages -> Add Repository から index.json を追加`  
  を基準にする

### 00_README_FIRST.txt
- ツールの一言説明
- 主な方針
  - まず Dry Run
  - 非破壊
  - 必要時のみ Build 補正
- 最初にやること
- 導入の基本
  - 主導線は VCC / VPM
- GitHub repo / `index.json` / listing page の導線

### 01_VCC_INSTALL.txt
- VCC / VPM 推奨導入
- `VCC` を開き、`Settings -> Packages -> Add Repository` から `index.json` を追加する
- `index.json` URL
- package 一覧から対象 package を追加する
- 必要最小限の導入手順だけを書く

### 02_QUICKSTART.txt
- 導入後に何を追加するか
- 最初の動作モード
- まず診断
- 一覧とレポート確認
- 必要な時だけ Build 補正
- 最後に短い補足
  - 非破壊
  - 未対応事項
  - `README` 誘導

### BOOTH 配布 zip ファイル名
BOOTH 配布 zip のファイル名は `{ToolName}_BOOTH_Package_v{version}.zip` を基本形にする。
- 例: `FlipbookMaterialGenerator_BOOTH_Package_v1.0.0.zip`
- 例: `SkinnedMeshMirror_BOOTH_Package_v0.1.2.zip`

### BOOTH zip の作成
BOOTH 配布 zip は Claude Code に依頼して作成する。
- 入力: repo 内の `BOOTH_PACKAGE/` フォルダ
- 出力: `Releases/booth/{ToolName}_BOOTH_Package_v{version}.zip`
- zip 展開直下にファイルが見える形にする（BOOTH_PACKAGE/ フォルダ自体は含めない）
- .meta ファイルは除外する

---

## BOOTH 商品説明文の基本形
BOOTH 商品ページ本文は、既存 shop の説明スタイルに合わせます。

### 基本の流れ
1. 何のツールか
2. できること
3. 現在の対応範囲
4. 想定用途
5. 使い方（最短）
6. VPM 導入リンク
7. 注意点
8. 動作確認
9. 配布内容
10. 更新履歴
11. ライセンス
12. 最後に短い問い合わせ案内

### 書き方の方針
- 最初の数行で「何を解決するツールか」が分かるようにする
- Dry Run や非破壊など、安心感につながる要素は前半に出す
- 技術的に正しいだけでなく、BOOTH 購入者が「怖くない」「使い道が分かる」と感じる説明を優先する
- VPM / VCC 導入を主導線にする
- 商品本文は README のコピペではなく、BOOTH 向けに読みやすく再構成する
- 詳しい仕様や細かい制限事項は README に逃がしてよい

---

## 公開準備の進め方
公開準備は次の順で進めます。

1. 棚卸し
2. README / TOOL_INFO / package.json / CHANGELOG 調整
3. release workflow 整備
4. BOOTH_PACKAGE 作成
5. 導線 URL の整合確認
6. version 固定
7. GitHub Release
8. VPM listing（source.json + README の package リスト更新、listing repo 側も走査）
9. VCC 確認
10. BOOTH 公開

---

## 公開前チェック

### repo 内
- README
- TOOL_INFO
- package.json
- CHANGELOG
- workflow
- BOOTH_PACKAGE

### 確認観点
- VCC 用 URL が `index.json` になっているか
- listing page と index.json の役割が混ざっていないか
- package.json の URL 系がそろっているか
- README の UI 名称が実装とズレていないか
- release zip に不要ファイルが混ざらないか
- BOOTH_PACKAGE と README の説明が矛盾していないか
- listing repo の走査（source.json の githubRepos + README の package リスト）
- default branch が main / master のどちらか確認し、URL に反映しているか

### repo 外
- BOOTH 商品本文
- 商品画像
- 告知文
- SNS 固定文
- 下書きメモ

---

## リリース後の振り返り観点
リリース完了後に短く振り返る時の観点です。

- コード面の確認タイミングは適切だったか
- 公開面の確認タイミングは適切だったか
- listing repo の走査は漏れなかったか（source.json + README）
- 文字化けやエンコーディング問題がなかったか
- 冗長だった手順はないか
- commit 分割の判断は適切だったか

---

## commit の考え方
実装変更がない公開準備では、基本は次の分類で考えます。

- `docs`: README / TOOL_INFO / CHANGELOG / BOOTH_PACKAGE / 公開導線
- `ci`: workflow
- `chore`: version 整理や公開準備の横断調整

README が複数目的にまたがる場合は、無理に細かく分けず、公開準備一式としてまとめてよいです。

---

## 切り分けルール
作業を始める時は、まずこれを分けます。

- **今回 repo 固有の話**
- **全 repo 共通の話**
- **repo 外で手修正する話**

この切り分けを先にやっておくと、Codex に渡す範囲と自分で最終確認する範囲が見やすくなります。

---

## ひとことで言うと
公開時は  
**Release -> listing -> VCC確認 -> BOOTH**  
を軸にして、  
**URL・version・導線・同梱物のズレを先に潰す**。

---

## 共通前提と今回だけの差分の分け方

### 共通前提
- 公開順
- version 表記
- owner / URL の基本形
- VPM / VCC 導線の役割分離
- BOOTH_PACKAGE の基本構成
- BOOTH 商品説明文の基本構成
- 公開前チェック観点

### 今回だけの差分
- ツール名
- repo 名
- package id
- version
- index.json / listing page / repo URL の具体 URL
- UI 名称
- 未対応事項
- 商品画像や本文の固有内容
