# PROJECT_SHARED_CONTEXT

## このファイルの役割
このファイルは、このプロジェクトで繰り返し使う「変わりにくい前提」をまとめた共通文脈です。  
Claude はこの前提をもとに、状況整理、設計、切り分け、Claude Code に渡すタスク指示の整理を行います。

主要な情報源の役割は次のとおりです。

- `CLAUDE.md`（このファイル）: 変わりにくい共通前提
- `UNITY_VRCHAT_TOOL_UI_GUIDELINES.md`: Unity / VRChat ツール UI 方針
- `PUBLIC_RELEASE_GUIDELINES.md`: GitHub Release / VPM / VCC / BOOTH の公開運用
- `REPO_INDEX.md`: よく使う repo の入口一覧
- 各 repo の `CLAUDE.md`: repo 固有の前提、次回再開用の要点、今回だけの差分

情報源は増やしすぎず、「共通前提」と「再利用する定型」に寄せることを標準運用とします。

---

## 1. 開発の標準進行
Unity / VRChat 向けツール開発では、曖昧な点を推測で埋めず、先に確認してから進めます。  
最初に設計・切り分け・確認項目整理を行い、その後に実装へ進みます。

標準フローは次のとおりです。

1. 目的と対象を整理する  
2. 曖昧な点を確認する  
3. Claude で仕様・設計・切り分けを行う  
4. 実装や repo 整備は Claude Code に依頼する  
5. 戻ってきた内容を Claude で確認・整理する  
6. Unity で動作確認する  
7. UI や説明文を整える  
8. GitHub 公開準備をする  
9. VPM / BOOTH 配布準備まで整える

次の曖昧さがある時は、仮案で置き場所や対象を埋めて進めず、その場で止めて確認します。
- 置き場所が曖昧
- 対象 repo が曖昧
- 変更範囲が曖昧
- 現状のファイル構成、既存コード、既存文書の内容を見ないと判断できない
- 正本 / 入口 / 今回だけのメモ の役割が曖昧
- blocker 修正と改善が混ざっている
- 今回だけか共通化かが曖昧

確認質問の例:
- これはどの repo のどのファイルに置く想定か
- 今回触る範囲はどこまでか
- 今回判断に必要な既存ファイルはどれか
- 現在の配置や既存文書を見たいので、対象ファイルを確認したい
- 正本に寄せるのか、入口メモにするのか、今回だけのメモにするのか
- 今回は blocker 修正だけか、改善まで含めるのか
- 今回だけの差分か、共通前提へ上げる候補か

基本は、いきなり全部を作らず、まず MVP で成立させます。  
問題が出たらログを増やして切り分け、必要なら Dry Run や診断を先に固めます。

不具合を直す作業と、使いやすくする作業は分けて扱います。  
まずは成立を妨げる blocker を直し、UI 改善、ログ改善、説明追加、履歴保持、補助表示、拡張は改善作業として別で扱います。  
修正中に改善案が出ても、その場で混ぜてスコープを広げず、次フェーズ候補として保持します。  
判断に迷う時は、「今やらないと成立しないか」と「成立後に別作業として安全に進められるか」で分けます。

Play 入口 / Serialize / Inspector repaint のような頻発イベントに、重い再計算や ID 更新を直接ぶら下げません。  
頻発イベントでは軽量・冪等な処理だけにし、重いものは Dry Run / 明示 refresh / 明示操作へ寄せます。
重い検出 / 収集と、軽い分類更新 / 表示更新は分けて扱います。  
自動更新は軽い再評価までに留め、フル再走査は明示操作に寄せます。

---

## 2. Claude と Claude Code の役割分担
このプロジェクトでは Claude（claude.ai）と Claude Code を行き来しながら進めます。

### Claude の役割
Claude は次の内容を主に担当します。

- 要件確認
- 仕様整理
- 問題の言語化
- 安全設計の整理
- 手順のチェックリスト化
- 期待ログ / 期待結果の定義
- README や公開文面の整備
- Claude Code に渡すタスク指示の作成
- 今回用の差分だけを案内すること

### Claude Code の役割
Claude Code は次の内容を主に担当します。

- コード実装
- 複数ファイルの差分反映
- repo 整備
- フォルダ移設
- package 化
- VPM 化
- README / LICENSE / CHANGELOG / .gitignore の実ファイル編集
- 一括置換や機械的な整形作業

### 判断ルール
- 仕様が曖昧、問題が整理できていない、方針が未確定 → まず Claude
- 方針は決まっていて、あとはファイルを触るだけ → Claude Code
- 迷ったら、先に Claude で整理してから Claude Code に渡す
- 「何がおかしいか分からない」状況では、Claude で状況整理するより
  Claude Code にコードを読ませて分析・修正案を出させる方が精度が高い
- 推測ベースの修正指示を Claude 側で重ねるより、
  Claude Code に「現象・状況・確認してほしい箇所」を渡して
  分析→修正案→承認→実装 の流れにする
---

## 3. Claude Code の標準運用
Claude Code にそのまま実装させる前に、複数ファイル変更・外部依存確認・仕様の揺れがある作業では、まず repo 内を整理してから実装へ進む。

使いどころ:
- 変更対象ファイルが複数ありそう
- repo 内の現状確認が必要
- 外部 package / 依存仕様 / build 順序の確認が必要
- 仕様不足のまま実装に入ると事故りやすい
- まだ commit 単位を切るには早い

基本の流れ:
1. Claude で目的・制約・未確定点を整理する
2. Claude Code にはまず現状確認と計画を出させる
3. 想定変更ファイル、実施手順、懸念点、確認したいことを出させる
4. 方向がよければ実装へ進める
5. 実装後は Claude で差分・文言・公開面を確認する

#### ツールインストールの許可
Claude Code への指示で、効率・効果のためにツールのインストール（pip install、winget 等）が
必要な場合は遠慮なく実行してよい。
インストールを避けて劣った方式を選ぶ必要はない。

初見の外部要素や外部仕様が絡む時は、実装前に分析 / 仕様確認フェーズを先に提案します。  
未確定点、一次ソース、想定変更ファイル、検証手順、実装へ進んでよい条件を先に整理してから進めます。

#### コンパクト前チェック
コンテキストが長くなりコンパクト（圧縮）が近づいたら、圧縮前に以下を確認する。
- `git status` で未コミット・未ステージの変更がないか
- `git log --oneline -3` で直近の commit が意図通りか
- push し忘れがないか
- 作業中の変更がある場合は commit または stash してからコンパクトに入る
- 確認結果をユーザーに報告し、コンパクト後の再開時に拾えるようにする

---

## 4. 標準フォルダ構成
今後の Unity / VRChat ツール開発では、共通の開発用 Unity プロジェクトを 1 つ使い、ワークスペース直下に `UnityDev`、`PackagesSrc`、`Repos` を置く標準構成で進めます。

### 標準構成
```text
ToolDevWorkspace/
├─ UnityDev/
│  └─ SebanneToolDev/
│     ├─ Assets/
│     │  ├─ _Scenes/
│     │  ├─ _Sandbox/
│     │  ├─ _TestAvatars/
│     │  ├─ _SharedDebug/
│     │  └─ _Temp/
│     ├─ Packages/
│     └─ ProjectSettings/
│
├─ PackagesSrc/
│  ├─ com.sebanne.some-tool/
│  ├─ com.sebanne.another-tool/
│  └─ ...
│
├─ Repos/
│  ├─ some-tool/
│  ├─ another-tool/
│  ├─ sebanne-unity-vrchat-tool-template/
│  └─ ...
│
├─ Releases/
│  ├─ vpm/
│  ├─ unitypackage/
│  └─ booth/
│
└─ Docs/
   ├─ workflow-notes/
   ├─ screenshots/
   └─ prompts/
```

---

## 5. 情報源の運用ルール
- Claude は、会話の中で情報源に追加したほうがいい内容や、重複・統合済みで削除したほうがいい内容があれば、候補として保持したり提案したりしてよい
- 追加対象は、今後も何度も使う、変わりにくい、毎回説明するのがだるい、前提として話が進む内容
- 削除対象は、重複している内容、別の情報源へ統合済みの内容、単発の不具合ログ、一時メモ、今後ほぼ参照しない内容
- 情報源は増やしすぎず、「共通前提」と「再利用する定型」に絞る
- UI 方針は `UNITY_VRCHAT_TOOL_UI_GUIDELINES.md`、公開運用は `PUBLIC_RELEASE_GUIDELINES.md` に寄せ、このファイルへ重複して持ち込まない
- repo の入口整理は `REPO_INDEX.md`、repo ごとの今回だけの条件は各 repo の `CLAUDE.md` に寄せる
- `REPO_INDEX.md` には、今後も繰り返し参照する repo の入口だけを載せる
- AGENTS / config は最初から増やしすぎず、同じ詰まり・同じ修正指示・同じ前提不足が 2 回以上起きた時だけ更新候補にする
- repo 固有なら AGENTS / config ではなく `CLAUDE.md` に寄せ、候補判定はスレッド終了時に行う。迷ったらまず knowledge repo に残し、AGENTS 追加は保留する
- 各 repo の `CLAUDE.md` は、毎回なんでも自動更新するメモではなく、節目で Claude Code が更新する repo 固有の現場メモとして扱う
- Claude Code に渡すタスク指示では、毎回 `CLAUDE.md` の扱いを明示し、`before / after / none` を基本指定にし、必要なら `full / minimal` も添える
- handoff が長く更新されていない repo や、現況とズレている repo では、実装前に `before` で現況ベースへ更新してから進める
- 更新は計画が固まったあと、実装が一段落したあと、作業中断時、スレッド終了前などの節目だけでよく、`Current State` `Current Blocker` `Tasks` と次回再開用の短い要点 3〜5 行を中心に整理する
- 軽微な単発修正では `none` でもよいが、毎回明示は省略しない
- 未確認の推測、単発の試行錯誤ログ、まだ確定していない改善案の羅列は `CLAUDE.md` に溜めすぎない
- 共通 Skill は repo 内 notes で叩き台を作ってよいが、複数 repo で再利用する前提が固まり、schema と境界が定まり、forward test が通ったら knowledge repo を正本にする
- 最初の Skill は診断専用で始め、repo 固有例外は Skill に飲み込まず、まず `CLAUDE.md` に逃がす
- `PROJECT_INSTRUCTIONS.md` はリポ内ファイルとして Claude Code が更新する。せばんぬがプロジェクト手順欄に丸ごとコピペする運用。Claude 側で個別の行編集指示を出す必要はない

---

## 6. 調査が多かった技術領域の残し方
外部 package、フレームワーク、build pipeline など、web 検索や source 読みが多かった領域は、作業完了時に調査メモとして残すことを推奨する。

残す時の基本:
- 単なる検索ログではなく、判断に使った要点を残す
- 可能なら一次ソースを優先し、外部 package / build pipeline / framework は web の断片情報より local package source を先に確認する
- `共通化向き / repo 固有 / まだ不確実` を分ける
- version 依存や未検証条件は明示する

置き場所:
- 共通化しやすい土台 → Notion 技術リファレンスに昇格
- repo 固有の判断 → repo 内メモ
- 次回再開に必要な短い要点 → `CLAUDE.md` に 3〜5 行で逆流

考え方:
- 調査し直しのコストを減らす
- ただし情報源を検索ログ置き場にはしない
- 変わりにくい原則は共通前提（CLAUDE.md）へ、技術知見は Notion 技術リファレンスへ昇格する

---

## 7. 振り返りと昇格の判断基準
区切りのタイミングが来たら、そのスレッドで得られた内容のうち、今後も再利用しそうな前提・運用ルール・定型・注意点があるかを短く振り返る。

考え方:
- 会話中に、Claude が「これは情報源に追加したほうがよさそう」と感じたものは、振り返り候補として一時的に保持してよい
- ただし、その場ですぐ情報源へ入れる前提ではなく、まずはスレッド終了時にまとめて確認する
- 追加候補だけでなく、重複・古くなった内容・今後ほぼ参照しなさそうな内容があれば、整理や削除候補として挙げてよい
- 毎回長く振り返るのではなく、必要な時だけ短く整理する
- 単発の作業ログではなく、今後も再利用する内容を優先する

振り返りで見る観点:
- 共通前提として残す価値があるか
- 既存の情報源と重複していないか
- repo 固有に閉じるべきか、共通化するべきか
- 今後の会話で何度も参照しそうか

昇格の判断基準:
- 今後も何度も参照しそうか
- repo 固有に閉じるか、共通前提として使えるか
- 単発の作業ログではなく、判断の根拠や設計方針か

---

## 8. package repo を横並びで揃える時の前提
listing repo 以外の package repo は、機能差があっても、まず repo の外側をできるだけ共通の型に寄せる。

優先して揃えるもの:
- フォルダ構成
  - `Editor/`
  - `Runtime/`
  - `Documentation~/`
  - `Samples~/`
- root 文書
  - `README.md`
  - `TOOL_INFO.md`
  - `CHANGELOG.md`
  - `LICENSE`
  - `CLAUDE.md`
  - `AGENTS.md`
  - `.gitignore`
  - `package.json`
- 公開面
  - `README.md` のタイトル / 概要 / 使い方 / 制限事項
  - `TOOL_INFO.md`
  - `package.json` の `displayName` / `description`
  - listing に見える名前や説明

考え方:
- まず repo の骨組みと公開面を揃える
- 実装ロジックの大改修はその後でよい
- package id / author 名 / namespace などの内部識別子は、無理に公開表示へ合わせなくてよい
- listing repo は package repo と役割が違うため、同じ基準で揃えない

---

## 9. Unity ツールの OutputFolder 設計パターン
Unity / VRChat ツールで生成物の出力先を扱う場合、
以下の三択UIを標準パターンとして使う。

- **元ソース直下**（SourceRelative）: InputFolder直下に `Generated/` を作成
- **ツール共通フォルダ**（ToolDefault）: `Assets/Sebanne/{ToolName}/Generated/` に生成
- **フォルダを指定**（Custom）: ユーザー指定

デフォルトは **ToolDefault**。
理由: 素材と生成物を分けたい派のユーザーに配慮するため。

ToolDefault のパスは `Assets/Sebanne/{ToolName}/Generated_{ToolShortName}/` を基本形にする。
出力先フォルダが存在しない場合は `AssetDatabase.CreateFolder` で自動作成する。

Generated フォルダ名には `Generated_{ToolShortName}/` の形式でツール識別を含める。
理由：SourceRelative モードで他ツールの出力先フォルダと衝突するのを防ぐ。
例：`Generated_Flipbook/`

---

## 10. Unity 技術知見の参照先
AnimatorController / MA リフレクション / VRC SDK / NDMF / アセット操作パターンなどの共通技術知見は
Notion 技術リファレンスページに集約している。
https://www.notion.so/33f61f93d20181869f3edb7b3739db9b

Claude Code への指示文には、技術リファレンスの URL を常に添える（必要な時だけではなく全指示文に含める）。
各 repo 固有の技術知見は、その repo の CLAUDE.md 内「技術知見」セクションを参照する。

新しい技術知見が出た場合：
1. まず repo 固有の CLAUDE.md に書く
2. 複数リポで同じ罠を踏んだら Notion 技術リファレンスに昇格する
3. 汎用性があると判断したら、複数リポで踏む前でも先行昇格してよい（NDMF / MA の汎用パターン等）
4. 共通 CLAUDE.md にはもう技術知見を直接書かない
5. closeout 時に技術知見の昇格候補チェックを行う（反映リストの「技術知見」セクションで明示）

## 11. リリース前走査の推奨フロー
- 機能が固まったら棚卸し（コード面の網羅確認。観点はセクション 7 の closeout 補足（網羅的実装確認の観点）に準ずる）
- ドキュメント・公開基盤を整備したら public-release-sync-check（公開面: version / URL / metadata / file existence / docs role drift）
- commit → push 後、listing repo を更新する時は listing repo 側も走査する（source.json の githubRepos + README の package リスト）
- 2 つの走査は役割が異なる: 棚卸し = コードの正しさ、sync-check = 公開面の整合
- 棚卸しで見つけた乖離をドキュメントに反映してから公開面を確認する
- 棚卸し → ドキュメント整備 → sync-check → commit の順が自然
- 軽微な変更のみの場合でも sync-check は省略しない（version や URL のズレは目視で見落としやすい）
