# PUBLIC_RELEASE_GUIDELINES

## 目的
Unity / VRChat ツール公開時に、毎回ゼロから考えずに進めるための共通ルール。  
対象は主に次の公開導線です。

- GitHub Release
- VPM listing
- VCC 導入
- BOOTH 公開

---

## テンプレリポとの役割分担

- テンプレリポ (`sebanne-unity-vrchat-tool-template`) = 新ツールを作る時にコピーして使う実物（フォルダ構成、package.json、workflow、BOOTH_PACKAGE 等）
- このガイドライン = 公開時の手順・判断基準・チェック観点（テンプレには入らない、人が判断する部分）
- 新ツール作成時はテンプレリポをコピーし、公開時はこのガイドラインの手順に従う
- テンプレリポがカバーしている実物の詳細は、このガイドラインでは繰り返さない

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
- フォーマットの実物は `sebanne-unity-vrchat-tool-template` の package.json / CHANGELOG を参照
- version は `1.0.0` 形式。`v` は付けない
- Git tag・GitHub Release title・CHANGELOG 見出し・release asset 名・公開文面、全ての公開面で揃える
- すでに公開済み version に対して公開物の中身を変える場合は、基本的に patch version を上げる

### 補足
- release workflow は `v` 付き tag を reject する。`1.0.0` 形式のみ受け付ける

---

## GitHub / owner / URL
GitHub の標準 owner / アカウント名は `sebanne1225` を前提にします。
branch は `main` 固定ではなく、対象 repo の default branch に合わせます。

### 基本形
URL パターンの実物は `sebanne-unity-vrchat-tool-template` の package.json / README / TOOL_INFO を参照。
default branch は `main` 固定ではなく、対象 repo の default branch に合わせる（テンプレは `main` 前提だが、既存 repo に `master` のものがある）。

---

## VPM / VCC 導線
VCC に追加する URL と、listing 閲覧ページは役割を分けます。

### 正とする URL
URL の実物は `sebanne-unity-vrchat-tool-template` の README / TOOL_INFO / BOOTH_PACKAGE を参照。

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

### package.json / release workflow / release asset
実物は `sebanne-unity-vrchat-tool-template` を参照。

- package.json: 必須項目はテンプレに揃っている
- release workflow: tag 検証・zip 作成・asset 添付・workflow_dispatch 対応
- release asset: `package-id-<version>.zip` 命名。zip 展開直下に `package.json` が見える形
- release zip には package に必要な中身だけを含める（`.github`・`BOOTH_PACKAGE`・内部メモ等は除外）
- listing に package が出ない時は、まず release asset zip の有無と version / tag の一致を確認する

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

### ファイル構成
4 ファイル構成（`00_README_FIRST.txt` / `01_VCC_INSTALL.txt` / `02_QUICKSTART.txt` / `LICENSE`）。
各ファイルの骨組みと構成は `sebanne-unity-vrchat-tool-template` の `BOOTH_PACKAGE/` を参照。

### BOOTH 配布 zip ファイル名
BOOTH 配布 zip のファイル名は `{ToolName}_BOOTH_Package_v{version}.zip` を基本形にする。
- 例: `FlipbookMaterialGenerator_BOOTH_Package_v1.0.0.zip`
- 例: `SkinnedMeshMirror_BOOTH_Package_v0.1.2.zip`

### BOOTH zip の作成
BOOTH 配布 zip は Claude Code に依頼して作成する。
- 入力: repo 内の `BOOTH_PACKAGE/` フォルダ
- 出力: `Releases/booth/{ToolName}/{ToolName}_BOOTH_Package_v{version}.zip`
- ツールごとにサブフォルダで分離する（過去 version も積んで残すため、リポごとに隔離して誤操作を防ぐため）
- zip 展開直下にファイルが見える形にする（BOOTH_PACKAGE/ フォルダ自体は含めない）
- .meta ファイルは除外する

### BOOTH タグの基本形
BOOTH 商品ページのタグは、共通タグ＋ツール固有タグで構成する。

共通タグ:
ツール, 簡単, Unity, アバター, VRChat, VCC対応, Editor拡張, アバター改変, アバター改変ツール

MA タグ（MA 公式定義に準拠、該当する場合のみ追加）:
- 「ModularAvatar設定済み」: MA コンポーネントをあらかじめ組み込んで配布しているもの（ユーザーにとって MA 必須）。ロゴ使用可
- 「ModularAvatar対応」: MA を使って導入できることを確認したもの（ユーザーにとって MA 必須ではない）。ロゴ使用不可
- MA を使っていないツールには MA タグを付けない

ツール固有タグは各ツールに合わせて追加する。

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

## 公開準備の進め方（初回リリース）
初回リリース向け。patch は次セクション参照。

1. 棚卸し
2. README / TOOL_INFO / package.json / CHANGELOG 調整
3. release workflow 整備
4. BOOTH_PACKAGE 作成 + テンプレタグ確定（共通タグ + MA タグ有無判断）
5. sync-check 実行
6. version 固定
7. GitHub Release
8. VPM listing（source.json + README の package リスト更新、listing repo 側も走査）
9. VCC 確認
10. BOOTH 公開（商品名・ツール固有タグもこの段階で決定）

---

## patch リリースチェックリスト

初回リリース済みの repo に対する patch（バグ修正・軽微な改善）のフロー。
初回リリースとの主な違い: repo 構成・workflow・source.json 登録・BOOTH 商品ページ作成は済んでいる前提。

### フロー
1. □ 修正内容の実装・テスト完了
2. □ package.json の version bump（patch）
3. □ CHANGELOG 追記
4. □ BOOTH_PACKAGE 内の文面更新（version 記載があれば）
5. □ sync-check 実行
6. □ commit + push
7. □ GitHub Release（`gh release create {version} --notes "..."`）
8. □ release asset zip 確認
9. □ VPM listing 更新（GitHub Actions 手動 dispatch）
10. □ VCC で新 version が見えるか確認
11. □ BOOTH 更新（該当する場合のみ — 下記判断基準を参照）
12. □ リリース管理 DB 更新

### BOOTH 更新の判断基準
patch のたびに毎回 BOOTH を更新する必要はない。VPM が主導線なので、BOOTH は以下の基準で判断する。

更新する:
- ユーザーから見える機能追加・UI 変更がある
- BOOTH 商品説明文の「できること」「使い方」に影響する修正
- BOOTH_PACKAGE 内の導入手順やクイックスタートが変わる修正

更新しない:
- 内部バグ修正で使い方が変わらない
- エラーメッセージ改善やログ修正
- 依存 version の追従だけ

判断の境界線: 「BOOTH の商品説明文や同梱テキストを書き換える理由があるかどうか」。

BOOTH を更新する場合:
- BOOTH zip 再作成（`Releases/booth/{ToolName}/` に出力）
- 商品ページの更新履歴に追記
- 必要に応じて商品説明文を更新

---

## sync-check（公開面の整合確認）

リリース前に、公開面の整合を Claude Code に確認させる走査。
棚卸し（コード面の網羅確認）とは役割が異なる。

### 確認対象
- version: package.json / CHANGELOG / TOOL_INFO / BOOTH_PACKAGE 間で一致しているか
- URL: package.json / README / TOOL_INFO / BOOTH_PACKAGE 内の URL が正しいか
- metadata: package.json の displayName / description / author 等
- file existence: README / TOOL_INFO / CHANGELOG / LICENSE / workflow / BOOTH_PACKAGE が揃っているか
- docs role drift: README の機能説明や UI 名称が実装とズレていないか

### 実行方法
Claude Code に以下の定型指示で依頼する。

```
対象リポの public-release-sync-check を実行してください。
確認対象: version / URL / metadata / file existence / docs role drift
README / TOOL_INFO / package.json / CHANGELOG / BOOTH_PACKAGE / workflow を横断で突合し、
Blocking / Warning に分類してレポートしてください。
この段階では修正は不要です。レポートだけ出してください。
```

### タイミング
- commit 前に実行する
- 棚卸し → ドキュメント整備 → sync-check → commit の順が自然
- 軽微な変更のみの場合でも省略しない（version や URL のズレは目視で見落としやすい）

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

この切り分けを先にやっておくと、Claude Code に渡す範囲と自分で最終確認する範囲が見やすくなります。

---

## ひとことで言うと
公開時は  
**Release -> listing -> VCC確認 -> BOOTH**  
を軸にして、  
**URL・version・導線・同梱物のズレを先に潰す**。

