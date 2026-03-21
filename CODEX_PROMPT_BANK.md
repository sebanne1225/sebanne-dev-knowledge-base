# CODEX_PROMPT_BANK

## このファイルの役割
このファイルは、Codex に何度も渡す定型依頼文をまとめたプロンプト集です。  
ChatGPT は状況を見て、使うべきプロンプト番号と、今回用の差分だけを案内します。  
ユーザーは、その差分を足して Codex に渡します。

### 基本ルール
- まず ChatGPT が「今回はどの番号が合うか」を判断する
- 必要なら `<...>` のプレースホルダだけ差し替える
- repo ごとの具体状況は `CODEX_HANDOFF.md` に書く
- まだ commit / push したくない時は、その文言も明示する

### 早見表
- 新規 repo の土台づくり → `2-1` / `2-1a`
- Assets 実装の受け皿づくり → `2-2`
- MVP 移植 → `2-3`
- 公開前レビューだけ → `2-8a`
- 公開面を実際にそろえる → `2-8b`
- 公開準備整理 → `2-9`
- release workflow 整備 → `2-10`
- BOOTH_PACKAGE 作成 → `2-11`
- Plan mode だけで整理 → `3-5`

knowledge base / 情報源 repo の docs 整理は、既存番号に無理に当てず、専用の個別依頼で行う。

---

## 0. 定型の使い方
ChatGPT 側の案内例:

- 今回は **2-1** ベース
- 差し替えるのはこの 4 点
  - `<実ツール名>` → `SkinnedMeshMirror`
  - `<package名>` → `com.sebanne.skinned-mesh-mirror`
  - `<表示名>` → `Skinned Mesh Mirror`
  - `<Editor asmdef名>` → `Sebanne.SkinnedMeshMirror.Editor`

ユーザーは、その差分を加えて Codex に渡す。

---

## 2-1. テンプレ repo を実ツール化する
```text
いま開いている repo を対象に、
テンプレ repo を実ツール repo に変換してください。

重要ルール:
- 既存ファイルは削除せず、必要最小限の安全な変更で進める
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧と tree を出す
- まだ package 本体の移植は最小限でよい
- 今回の目的は「テンプレ名の置換」と「実ツール用の土台づくり」

やってほしいこと:
1. テンプレ名を実ツール名へ置換
   - `ToolTemplate` → `<実ツール名>`
   - `com.sebanne.tool-template` → `<package名>`
   - `Sebanne Tool Template` → `<表示名>`

2. 次のファイルを調整
   - `package.json`
   - `README.md`
   - `TOOL_INFO.md`
   - `CHANGELOG.md`
   - `Editor/*.asmdef`
   - `Runtime/*.asmdef`
   - `Editor/*CheckWindow.cs`

3. asmdef 名を実ツール名に合わせて変更
   - Runtime: `<Runtime asmdef名>`
   - Editor: `<Editor asmdef名>`
   - Editor asmdef は Runtime を参照
   - includePlatforms は Editor のまま

4. `package.json` を実ツール向けに調整
   - name
   - displayName
   - version
   - unity
   - description
   - author.name

5. README.md は日本語で公開向けに調整
   見出しは最低限:
   - タイトル
   - 概要
   - 何ができるか
   - 現在対応していること
   - 使い方
   - Dry Run / 診断
   - 制限事項
   - ライセンス

6. Check Window は名前やメニューを実ツール用に調整
   - ファイル名も必要なら変更
   - メニュー名も実ツール向けに変更
   - ログ文言も実ツール名に変更

7. 最後に報告
   - 変更ファイル一覧
   - tree
   - 今後 package 本体を移植する時の次ステップ

commit はまだしないでください。

```

---

## 2-1a. 既存 package repo を標準骨組みに寄せる
```text
いま開いている repo を対象に、
Listing repo 以外の sebanne 系 package repo として、標準の骨組みに寄せてください。

## 目的
- 他の sebanne 系 package repo と、フォルダ構成・root 文書・asmdef・補助ファイルの型をそろえる
- 実装ロジックはできるだけ壊さず、まず repo の土台を揃える
- 見た目と役割分担をそろえて、今後の保守と公開準備をしやすくする

## 前提
- 対象は listing repo ではなく package repo
- 既存の動作は壊さない
- まずは骨組みをそろえることを優先する
- 大規模な実装改修や全面書き換えはまだしない

## 重要ルール
- まず短い plan を出す
- 既存機能は壊さない
- 既存ファイルは必要以上に削除しない
- 実装の全面書き換えはまだしない
- 作業後に変更ファイル一覧と tree を出す
- まだ commit / push はしない

## やってほしいこと

1. repo のフォルダ構成を確認し、必要なら標準形に寄せる
   - `Editor/`
   - `Runtime/`
   - `Documentation~/`
   - `Samples~/`

2. root の主要ファイルを確認し、必要なら不足を補うか整理する
   - `README.md`
   - `TOOL_INFO.md`
   - `CHANGELOG.md`
   - `LICENSE`
   - `CODEX_HANDOFF.md`
   - `AGENTS.md`
   - `.gitignore`
   - `package.json`

3. asmdef 名と参照関係を確認し、必要なら整理する
   - Runtime asmdef
   - Editor asmdef
   - Editor asmdef が Runtime を参照しているか
   - Editor asmdef の `includePlatforms` が適切か

4. release workflow や `BOOTH_PACKAGE/` の有無を、他の package repo と比較して整理対象として報告する
   - 今回すぐ追加しなくてもよい
   - 不足しているなら「不足」として分かる形で報告する

5. 実装ファイルの置き場が大きくズレている場合は、必要最小限で責務分けの受け皿へ寄せる案を出す
   - `Editor/UI/`
   - `Editor/Core/`
   - `Editor/Diagnostics/`
   - `Editor/Utility/`

6. 公開向け文書と開発用文書の役割が混ざっていないか確認する
   - `README.md` は公開向け
   - `TOOL_INFO.md` は repo 固有の補助情報
   - `CODEX_HANDOFF.md` は開発用
   のように、役割が見えやすい状態を目指す

## 最後に報告してほしいこと
- 他 repo に寄せられた点
- まだ揃っていない点
- 今回は触らなかったが、次に触るとよさそうな点
- 次にやるならどの定型が自然か
```

---

## 2-2. Assets 配下の既存実装を Package に引っ越せるよう、受け皿構成を作る
```text
いま開いている repo を対象に、
現在別 Unity プロジェクト内の `Assets/...` にある既存実装を、
この package repo に移植しやすい受け皿構成へ整えてください。

目的:
- Unity package として配置できる構成にする
- Editor コード中心で整理する
- 既存実装を壊さず、まずは受け皿を作る

重要ルール:
- 既存ファイルは必要以上に壊さない
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧と tree を出す
- まだ本体コードは大移動しなくてよい
- まずは受け皿と移植マップを作る

やってほしいこと:
1. `Editor/` 配下に、本体を入れやすい構成案を作る
2. 必要ならサブフォルダを追加
   - `Editor/Core`
   - `Editor/UI`
   - `Editor/Diagnostics`
   - `Editor/Utility`
3. どの既存ファイルをどこへ移す想定か、移植マップを `CODEX_HANDOFF.md` に追記
4. Runtime が不要ならその旨を README と TOOL_INFO に明記
5. package repo として不自然な点があれば最小限修正
6. 最後に
   - 推奨移植順
   - 移植時の注意点
   - 依存確認ポイント
   を短く報告

まだ commit はしないでください。
```

---

## 2-3. 既存実装の MVP 範囲だけを Package に移植する
```text
いま開いている repo を対象に、
既存の Unity 実装から、現在動いている MVP 範囲だけを package repo へ移植してください。

目的:
- まずは「今動いているもの」を package 化して Unity で開ける状態にする
- 未完成機能は無理に入れない
- 最小の安全移植を優先する

重要ルール:
- 非破壊
- 既存挙動をできるだけ変えない
- まず短い plan を出す
- 作業後に変更ファイル一覧と tree を出す
- commit はまだしない

やってほしいこと:
1. 既存実装のうち、MVP に必要なファイルだけを package 構成へ移植
2. namespace / asmdef / using を package 側に合わせて整理
3. EditorWindow から本体処理へ繋がる最小導線を維持
4. Dry Run と Build の基本動線を壊さない
5. README に「現在 package 化されている範囲」を追記
6. 最後に
   - 移植したファイル一覧
   - 未移植のもの
   - Unity で確認すべき手順
   - 次にやるべき整理
   を報告

まだ commit はしないでください。
```

---

## 2-4. GitHub 公開前に README / LICENSE / CHANGELOG / .gitignore を整える
```text
いま開いている repo を対象に、
GitHub 公開前の最終整理をしてください。

目的:
- 初回コミットして GitHub 公開できる状態に整える
- 実装追加は最小限
- 既存の構成は壊さない

重要ルール:
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧と tree を出す
- まだ commit や push はしない

やってほしいこと:
1. repo 内を確認して、初回コミットに不要なファイルがあれば報告
2. Unity package repo として必要なファイルが揃っているか確認
3. README.md を公開向けに軽く調整
4. LICENSE / package.json / asmdef / 確認用 Window への導線が README から分かるように整える
5. .gitignore が不足していれば最小限補う
6. 空ディレクトリ維持が必要なら `.gitkeep` を追加
7. 最後に以下を報告
   - 変更ファイル一覧
   - 初回コミットに含める想定ファイル
   - 含めない方がよいファイル
   - 推奨コミットメッセージ

まだ commit はしないでください。
```

---

## 2-5. listing repo をテンプレ状態から実運用向けに整える
```text
いま開いている repo を対象に、
VPM listing repo を「テンプレそのまま」状態から、「実運用 listing repo」へ整えてください。

重要ルール:
- 既存機能は壊さない
- 変更は最小限で、安全第一
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧と tree を出す
- まだ commit はしない
- 画像そのものの差し替えは今回はしなくてよい
- 既存の listing URL / GitHub Pages 前提は維持する

今回の目的:
- 実運用 listing repo として見た目と文言を整える
- 自動再ビルド対象を広げる
- 軽い JS バグを直す
- package が少ない段階でも違和感の少ない状態にする

やってほしいこと:
1. workflow を調整して、`source.json` 以外の Pages 用ファイル更新でも再ビルドされるようにする
2. `README.md` を listing repo 用の公開向け説明に書き換える
3. `source.json` の name / description / infoLink.text を実運用向けに調整
4. `index.html` の title や文言のテンプレ感を減らす
5. `app.js` の copy ボタンや menu の軽いバグを修正
6. 最後に報告
   - 変更ファイル一覧
   - tree
   - 今すぐ反映される改善点
   - 次に package 追加時にやること

まだ commit はしないでください。
```

---

## 2-6. listing repo の最終仕上げ
```text
いま開いている repo を対象に、
listing repo の最終仕上げをしてください。

重要ルール:
- 既存機能は壊さない
- 変更は最小限、安全第一
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧と tree を出す
- まだ commit はしない
- GitHub Pages / listing URL / 現在の package 掲載内容は壊さない

今回の目的:
- landing page の残りの不自然さを減らす
- app.js の残りバグを直す
- 実運用前の最終調整をする

やってほしいこと:
1. copy ボタンが押したボタン自身を一時的に accent にするように整理
2. `e.target.dataset` 依存を減らして、svg/path クリックでも安定するようにする
3. row menu のイベントを整理
4. index.html の文言を自然な日本語寄りに整える
5. 重複 id や重複リンクがあれば最小限整理
6. 最後に報告
   - 変更ファイル一覧
   - tree
   - 今回直した不具合の要点
   - commit 前に自分が確認すべき点
   - 次に package 追加時にやること

まだ commit はしないでください。
```

---

## 2-7. listing に新しい package repo を追加する
```text
いま開いている repo を対象に、
VPM listing に新しい package repo を 1 件追加してください。

重要ルール:
- 既存 package は消さない
- 変更は最小限
- まず短い plan を出してから作業
- 作業後に変更ファイル一覧を出す
- まだ commit はしない

追加したい repo:
- `<owner>/<repo名>`

やってほしいこと:
1. `source.json` の `githubRepos` に新しい repo を追加
2. README の掲載 package 一覧があれば更新
3. package が複数ある前提で、必要なら landing page の説明文を軽く調整
4. 最後に
   - どこを更新したか
   - listing 再ビルド後に確認すべきこと
   を短く報告

まだ commit はしないでください。
```

---

## 2-8. GitHub 公開直前の最終確認
```text
いま開いている repo を対象に、
GitHub 公開直前の最終確認をしてください。

目的:
- commit / push 前に危ない点がないか見る
- 余計な実装変更はしない
- 必要なら軽微な修正だけ行う

重要ルール:
- まず短い plan を出す
- 大きな改修はしない
- 作業後に変更ファイル一覧を出す
- まだ commit / push はしない

やってほしいこと:
1. package.json / README / LICENSE / asmdef / EditorWindow 導線を確認
2. 不要ファイルや抜けているファイルがないか確認
3. 公開向けに不自然な文言がないか確認
4. 問題が軽微ならその場で直す
5. 最後に
   - 直した点
   - 問題なしの点
   - 自分で確認すべき項目
   - 推奨コミットメッセージ
   を報告
   必要なら 2-8a / 2-8b を使う
```
## 2-8a. 公開前違和感レビュー
レビューだけしたい時に使う。

```text
この repo を「初見の外部ユーザーが見る公開物」としてレビューしてください。

## 目的
README だけでなく、package metadata、UI文言、メニュー名、TOOL_INFO、公開に見える補助文書まで含めて、
「身内には通じるが、初見の人には伝わりにくい・違和感がある」箇所を洗い出したいです。

実装変更はまだ行わず、まずは文言・見せ方・命名・文書配置の違和感を拾うレビューに集中してください。

## 前提
- 公開向けでは「読めば意味が分かる言葉」を優先してください
- 開発中の整理用ラベルや、会話の流れがあって初めて通じる表現は、そのまま公開面に出さない前提で見てください
- package id や author 名のような内部識別子と、ユーザーに見える公開表示は分けて考えてください
- 「会話では自然でも、repo 単体で見ると意味が飛ぶ表現」を優先して拾ってください
- 特に `package.json` の `displayName` / `description` と、README 冒頭の見え方が listing 上で不自然になっていないかを優先して確認してください

## レビュー対象
優先的に確認するもの:
- README.md
- package.json
- TOOL_INFO.md
- ユーザーに見える UI 文言
- エラーメッセージ / 成功メッセージ
- メニュー名
- 公開 repo に置かれている補助文書

必要に応じて見るもの:
- 開発用文書
- 内部仕様書
- 実装コード内のユーザー表示文字列

## レビュー観点

1. 公開表示名の一貫性
- ツール名や表示名がファイルごとにズレていないか
- 作者名・ブランド名を出す場所と、出さない場所の整理が自然か
- package id や author 名として残すべきものと、公開表示から外したほうがよいものが混ざっていないか

2. 初見ユーザーに意味が伝わらない用語
- A方式 / B方式 / C方式 のような内部整理用語が残っていないか
- MVP、Generated、Same As Source、Custom などが説明なしで放置されていないか
- 略語・社内語・会話由来の言い回しが、そのまま公開面に出ていないか

3. UI と説明文のズレ
- README や補助文書の使い方説明が、実際の UI と一致しているか
- UI に存在しない操作を案内していないか
- 実際には可能な操作が説明から漏れていないか
- 今の UI でユーザーが実際に取れる行動と、案内文が一致しているか

4. 項目名・説明文・レイアウトの分かりやすさ
- ラベルが長すぎたり、見切れたり、ごちゃついたりしていないか
- 常設説明が多すぎて、逆に読みづらくなっていないか
- カテゴリ分け、見出し、余白、セクション分けが自然か
- 初心者向けにした結果、情報密度が上がりすぎていないか

5. 文書の役割分担
- README と TOOL_INFO と開発用文書の役割が混ざっていないか
- 初見ユーザーが「どの文書を読めばよいか」迷わないか
- 開発用文書が公開 repo の root にあることで、公開向け文書に見えてしまっていないか

6. 用語の揺れ
- 同じ概念を別名で呼んでいないか
  例:
  - Output Location / Output Location Mode / 保存先
  - Clip / clip / クリップ
  - frameRate / フレームレート
- UI、README、エラーメッセージで呼び方が揃っているか

7. 説明の順番
- 公開向けとして、
  - 何のツールか
  - 何ができるか
  - どう使うか
  - 何が未対応か
  の順で自然に読めるか
- 情報の出し方が開発者目線になりすぎていないか

8. 初心者が詰まりそうな点
- 「これは何？」
- 「何を入力するの？」
- 「エラーのとき何を直せばいいの？」
- 「成功したあと何を見ればいいの？」
が生まれそうな箇所を拾うこと

## 特に区別してほしいこと

そのままでよいもの:
- package id
- author 名
- namespace
- asmdef 名
- internal class 名
- 開発用文書の中だけで使う内部整理用語

公開向けには見直したいもの:
- README のタイトル
- displayName
- TOOL_INFO の表示名
- UI ラベル
- HelpBox 文言
- エラーメッセージ
- 成功メッセージ
- 公開 repo root に置かれた文書タイトルや冒頭説明

## 出力形式

### Must Fix
- file:
- current:
- issue:
- why awkward for first-time users:
- suggested rewrite:

### Nice to Fix
- file:
- current:
- issue:
- why awkward for first-time users:
- suggested rewrite:

### Looks Good
- そのままで問題ない公開向け表現があれば数件挙げる

## 判定基準
- 細かい言いがかりではなく、実際に初見ユーザーが迷いそうかどうかを基準にしてください
- 「開発者には自然だが、公開向けには少し引っかかる」レベルも拾ってよいです
- ただし過剰に全部を日本語化したり、全部を説明過多にする方向は避けてください
- 優先度は、公開時の違和感や混乱の大きさで判断してください

## 制約
- まずはレビューだけ
- 実装変更はしない
- 必要なら「今すぐ直すべきもの」と「後でもよいもの」を分けてください

```

---

## 2-8b. package repo の公開面と listing 見え方をそろえる
実際にそろえる作業をしたい時に使う。

```text
いま開いている repo を対象に、
Listing repo 以外の sebanne 系 package repo として、公開面と listing 上の見え方を他 repo に寄せてください。

## 目的
- `README.md`、`TOOL_INFO.md`、`package.json`、UI文言の公開向け表現をそろえる
- listing で見える名前や説明の温度感を他 repo と揃える
- 初見ユーザーが repo ごとの差に引っかかりにくい状態にする

## 前提
- 対象は listing repo ではなく package repo
- package id や author 名のような内部識別子は無理に変えない
- 公開表示名、README、説明文、listing に出る情報を優先して揃える
- 実装機能は変えず、まずは公開向けの見え方を整える

## 重要ルール
- まず短い plan を出す
- 実装機能は変えない
- 文言と公開向け見え方の整理を優先する
- 作業後に変更ファイル一覧を出す
- まだ commit / push はしない

## やってほしいこと

1. 次の公開向けファイルを確認する
   - `README.md`
   - `TOOL_INFO.md`
   - `package.json`

2. 公開表示名、概要、できること、想定用途、導入方法、使い方、制限事項の書き方を他 repo に寄せる
   - 初見の人が読んで意味が入る言葉を優先する
   - 会話前提・身内前提の表現は避ける

3. `package.json` の公開面に関わる項目を確認し、必要なら揃える
   - `displayName`
   - `description`
   - `version`
   - `unity`
   - `author`
   - `documentationUrl`
   - `changelogUrl`

4. listing で見える情報として不自然な差がないか確認する
   - `displayName`
   - `description`
   - repo 名とのズレ
   - README 冒頭の見え方
   - 他 package と並んだ時の温度感

5. 公開向けに不要な内部用語や会話依存の表現があれば、読めば意味が分かる言葉へ置き換える
   - 例:
     - `A方式 / B方式 / C方式`
     - 開発中だけの整理ラベル
     - repo 単体では意味が飛ぶ表現

6. UI や成功 / エラー文言で、公開向けに見直したほうがよいものがあれば最小限で整える
   - 項目名
   - HelpBox 文言
   - 成功メッセージ
   - エラーメッセージ
   - 初心者が見て迷いやすい案内

7. 用語の揺れがあれば整理する
   - 例:
     - `Output Location` / `Output Location Mode` / `保存先`
     - `Clip` / `clip` / `クリップ`
     - `frameRate` / `フレームレート`

8. 最後に、listing 側で見える情報として自分が確認すべき点も整理する
   - displayName
   - description
   - version
   - package 表示の自然さ
   - README とのズレ

## 最後に報告してほしいこと
- 揃えた点
- まだ差が残っている点
- listing 側で確認すべき点
- 必要なら次に使うべき定型番号

```

---

## 2-9. VPM / BOOTH 公開準備を整理する
```text
いま開いている repo と現在の実装状況を前提に、
公開準備を整理してください。

目的:
- GitHub / VPM / BOOTH 公開へ向けた不足を洗い出す
- 実装だけでなく、文章や画像も含めて整理する

重要ルール:
- まず短い plan を出す
- 実装変更は必要最小限
- 作業後に、実装面と公開面を分けて報告
- まだ commit / release はしない

やってほしいこと:
1. GitHub 公開に必要なものを確認
2. VPM 配布に必要なものを確認
3. BOOTH 配布に必要なものを確認
4. 不足があれば、優先度順に整理
5. README / package.json / release note / サムネ / 説明文で不足があれば指摘
6. 最後に
   - 今すぐやるべきこと
   - 後でもよいこと
   - 公開直前チェックリスト
   を出す

まだ commit / release はしないでください。
```

---

## 2-10. package repo に release workflow を追加する
```text
いま開いている repo を対象に、
GitHub release workflow を追加または整備して、release 時に package zip が自動で assets に付くようにしてください。

目的:
- VPM listing に拾われる release asset を作る
- 手動で zip を作って添付しなくてよい状態にする
- 可能なら workflow_dispatch でも zip 作成確認できるようにする

重要ルール:
- まず短い plan を出す
- 既存の package 構成や挙動は壊さない
- package 名、version、repo 構成に合わせて最小限で実装
- 作業後に変更ファイル一覧と tree を出す
- まだ commit / push はしない

やってほしいこと:
1. release published 時に package zip を作成し、GitHub Release assets に添付する workflow を追加または整備
2. 可能なら workflow_dispatch も追加し、手動実行時は artifact として zip を確認できるようにする
3. zip 名は `com.example.tool-<version>.zip` のような自然な形にする
4. release tag と `package.json.version` の一致確認が必要なら入れる
5. README に必要なら release asset 生成について短く追記
6. 最後に
   - 変更ファイル一覧
   - workflow の概要
   - どの event で動くか
   - 生成される想定 zip 名
   - release 後に自分が確認すべき点
   を報告

まだ commit / push はしないでください。
```

---

## 2-11. BOOTH 配布用フォルダ構成を作る
```text
いま開いている repo を対象に、
BOOTH 配布用の同梱フォルダ構成を作ってください。

目的:
- BOOTH から zip を落とした人が迷わないようにする
- 初見ユーザーでも、まず何を読めばいいか分かる構成にする
- VPM / VCC 導入前提のツールとして、最低限の案内を揃える
- 実装ロジックには触らない
- まだ commit / push はしない

重要ルール:
- まず短い plan を出す
- 既存コードや package 構成は壊さない
- 今回は配布用のフォルダ構成とテキスト整備だけ
- 過剰にファイルを増やさない
- 日本語で、短く分かりやすく
- 内部向け説明より、初見ユーザーが迷わないことを優先
- repo 内では `BOOTH_PACKAGE/` を作業用の固定フォルダ名として使ってよい
- BOOTH に貼る時の最終フォルダ名 / zip 名は別で、`<ToolName>_Booth_Package_v<version>` を推奨する
- 作業後に変更ファイル一覧と tree を出す
- まだ commit / push はしない

作りたい配布構成:
<BOOTH_PACKAGE_ROOT>/
├─ 00_README_FIRST.txt
├─ 01_VCC_INSTALL.txt
├─ 02_QUICKSTART.txt
└─ LICENSE

各ファイルの役割:
- 00_README_FIRST.txt: 最初に読む案内
- 01_VCC_INSTALL.txt: VCC / VPM での導入手順
- 02_QUICKSTART.txt: 最短の使い方
- LICENSE: ライセンス表記

命名の考え方:
- `BOOTH_PACKAGE/` は repo 内の作業用フォルダ名として扱う
- BOOTH に貼る時の最終フォルダ名 / zip 名は別で、`<ToolName>_Booth_Package_v<version>` を推奨する
- repo 内の `BOOTH_PACKAGE/` 自体は version ごとに変えない
- 例: `AnimationClipStartDelay_Booth_Package_v0.1.0`

やってほしいこと:
1. BOOTH 配布用のフォルダを作成
2. 上記 4 ファイルを作成
3. 文面は今回のツール向けに自然に埋める
4. 次の情報を文面に反映
   - ツール名: <TOOL_NAME>
   - ツールの一言説明: <TOOL_SUMMARY>
   - VPM Repository URL: <VPM_REPOSITORY_URL>
   - Unity メニュー位置: <UNITY_MENU_PATH>
   - 主な注意点: <NOTES>
5. 使い方は「まず Dry Run で確認してから本生成」を基本にする
6. 内部フォルダ構成や開発向け説明は書きすぎない
7. 最後に
   - 作成ファイル一覧
   - tree
   - 各 txt の要点
   - 推奨される最終 BOOTH 配布名
   を短く報告

まだ commit / push はしないでください。
```

---

## 3-1. 差分だけ見たい時の短縮文
```text
差分だけ見せてください。
- 変更ファイル一覧
- 各ファイルで何を変えたか 1〜2 行
- tree
- 次に確認すべき点

コード全文は必要な箇所だけで OK です。
```

---

## 3-2. まだ commit / push させたくない時の短縮文
```text
まだ commit / push はしないでください。
変更だけ反映して、最後に報告してください。
```

---

## 3-3. 実装前に確認だけしたい時の短縮文
```text
まだ実装しないでください。
まずは plan、想定変更ファイル、懸念点、確認項目だけ出してください。
```

---

## 3-4. 最小修正で頼みたい時の短縮文
```text
最小修正でお願いします。
大きなリネームや大規模整理はせず、今回必要な範囲だけ直してください。
```

---

## 3-5. Plan mode で進めたい時の短縮文
```text
まだ実装を始めず、まず Plan mode 相当で整理してください。

出してほしいもの:
- 想定変更ファイル
- 実施手順
- 懸念点
- 自分に確認したいこと
- repo 内コードを見て分かった前提
- このまま実装してよいか判断するための不足点

制約:
- 推測で仕様を埋めない
- まず repo 内コードと既存文書を確認する
- まだ commit / push はしない
- 実装は次の指示があるまで始めない
```
