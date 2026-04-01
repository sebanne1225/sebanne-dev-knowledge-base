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
- Claude が自分で判断できることをユーザーへの質問に変えない。
  コードや CLAUDE.md を読めば分かること、過去の会話で方針が出ていることは
  質問せず自分で判断して進める。判断に自信がない場合は
  「〇〇と判断しました。問題あれば指摘してください」の形で進める

### 定型プロンプト集について
以前の ChatGPT + Codex 構成では、Codex にリポの文脈を手渡しするために
定型プロンプト集（CODEX_PROMPT_BANK）を使っていた。
Claude Code はリポ内の `CLAUDE.md` やファイルを直接読むため、
この補完手段は不要になった。
依頼内容はここ（Claude）で整理して、そのまま Claude Code に渡せばよい。

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

Claude Code に最初に求めること:
- 推測で仕様を埋めず、まず repo 内コードと既存文書を確認する
- 今ある repo 内前提と、このまま実装してよいか判断するための不足点を整理する
- まだ commit / push はしない

Claude Code への指示テンプレート:
- 調査・分析のみの指示文末尾に必ず明示する：
  「この段階では修正・実装は不要です。レポートだけ出してください」
- 計画確認後に実装の指示文末尾に必ず明示する：
  「計画のみ出してください。『進めてください』と返答するまで実装しないでください」
- Claude が作った指示をそのまま渡さない。
  必ず「Claude の方針案 → Claude Code がリポを読んで補完・修正 → 確認後に実装」の
  2段階を踏む。
  指示文の冒頭テンプレ：
  「以下は Claude の方針案です。実装前にリポ全体（または対象ファイル）を読んで、
  抜け・修正・追加すべき観点があれば計画に反映してください。
  計画のみ出してください。『進めてください』と返答するまで実装しないでください。」

初見の外部要素や外部仕様が絡む時は、実装前に分析 / 仕様確認フェーズを先に提案します。  
未確定点、一次ソース、想定変更ファイル、検証手順、実装へ進んでよい条件を先に整理してから進めます。

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

---

## 6. 調査が多かった技術領域の残し方
外部 package、フレームワーク、build pipeline など、web 検索や source 読みが多かった領域は、作業完了時に調査メモとして残すことを推奨する。

残す時の基本:
- 単なる検索ログではなく、判断に使った要点を残す
- 可能なら一次ソースを優先し、外部 package / build pipeline / framework は web の断片情報より local package source を先に確認する
- `共通化向き / repo 固有 / まだ不確実` を分ける
- version 依存や未検証条件は明示する

置き場所:
- 共通化しやすい土台 → 情報源候補
- repo 固有の判断 → repo 内メモ
- 次回再開に必要な短い要点 → `CLAUDE.md` に 3〜5 行で逆流

考え方:
- 調査し直しのコストを減らす
- ただし情報源を検索ログ置き場にはしない
- 変わりにくい原則だけ共通前提へ昇格する

---

## 7. スレ分けと終了時の振り返り
スレッドの区切りタイミングは基本的にユーザーが決める。  
ただし Claude が、目的の切り替わり・フェーズの変化・文脈の肥大化などを見て「ここでスレッドを分けたほうが次が整理しやすい」と判断した場合は、切り替え候補として提案してよい。  
提案は強制ではなく、必要な時だけ短く行う。

スレッドを区切るかどうかは、「話題が変わったか」よりも、「次の目的を少ない前提で始められるか」を基準に考える。

提案しやすいタイミングの例:
- 今の目的がひとまず完了し、次の目的を 1 文で言える
- 切り分けフェーズから、修正・仕上げ・公開準備など別フェーズへ移る
- repo が変わる
- 直前の試行錯誤やログが増えて、次に必要な前提が埋もれ始めている
- Claude Code に渡す指示が固まり、次は戻り確認や公開準備が主目的になる

まだ提案しないほうがよいタイミングの例:
- 再現条件の切り分け中
- 失敗原因の仮説がまだ動いている
- 要求や完成イメージがまだ揺れている
- Claude Code に渡す条件や成功条件がまだ固まっていない

#### Claude Code への指示を再送する時のルール
「含めて再送して」「まとめて出して」など、保留中の指示を含めた
再送を求められた場合、まず保留中の指示を箇条書きで列挙して
確認を取ってから、まとめた指示文を出す。
指示文の冒頭に「前回保留分：〇〇」を明示する形式にする。
確認なしにいきなり指示文を出さない。

#### closeout の起点は Claude から
スレッド終了のタイミングが来たら、Claude から能動的に
「closeout に入りましょうか」を提案する。
ユーザーに思い出させない。
closeout 候補が溜まっている場合はその内容も合わせて提示する。
※ スレ分割の提案（既存）とは別。closeout は振り返り+記録の起点。

#### 設計変更時の記録
設計変更が起きた時点で「変更前・変更後・理由」を短くスレ内に記録する。
closeout 時に拾いやすくするため、その場で残す。

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

スレッド終了時のドキュメントフロー:
1. Claude に会話要約を出してもらう
2. 対象 repo の `Documentation~/notes/` に MD メモとして保存する
3. メモの中から `CLAUDE.md` に昇格できそうなものがあれば寄せる
4. 次フェーズ候補リストがある repo は、スレ開始時点の候補と今回の結果をビフォーアフターで比較し、完了・設計変更・新規追加を整理してから `CLAUDE.md` に反映する
5. 実装内容の確認表は Claude 側で作らず、Claude Code にコードを読ませて「実装済み/未実装/懸念あり」の一覧を出させる。closeout 前に必ず 1 回実施する
   - 確認項目を列挙せず、Claude Code に repo 全体を網羅的に見させる
   - 観点：壊れている箇所・設計と実装の乖離・未実装・デッドコード・
     他モードと処理が揃っていない箇所・CLAUDE.md との乖離
   - 出力形式：実装済み・問題なし / 懸念あり / 未実装 / 要確認
     ＋ ファイル名・行番号・深刻度（致命的/中/軽微）
6. closeout の質を上げるためのチェックリスト：
   1. 今日触った機能を全モードで横断確認したか（新機能・修正が全モードに入っているか）
   2. 「仕様のつもり」の動作を Unity 上で実際に確認したか
   3. 会話中に発生した設計の認識合わせをその場で記録したか
   4. 「後回し」にした判断を全部次フェーズ候補リストに追加したか
   5. Claude Code の網羅的実装確認を closeout 前に必ず1回実施したか
7. `THREAD_CLOSEOUT_TEMPLATE.md` の「次スレ開始テンプレ」を使って引き継ぎパッケージを作り、次スレの冒頭に貼れる状態にする。Claude Code に対象 repo の `CLAUDE.md` と knowledge base を読ませて整形・補完してもらうと確実

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

## 10. Unity AnimatorController / MA リフレクション 共通知見
- `AddState` / `AddTransition` はサブアセットを内部で自動登録する
  → `AddObjectToAsset` の二重登録は不要、エラーになる
- `rootStateMachine` は個別に `SetDirty` が必要（controller だけでは不足）
- `CreateAnimatorControllerAtPath` は既存ファイルがあると空のまま返す
  → 呼ぶ前に `DeleteAsset` で削除する
- `ImportAsset(ForceUpdate)` はメモリ上の変更を消す
  → `SetDirty` + `SaveAssets` が正しい
- `ModularAvatarMergeAnimator` のプロパティは public フィールド
  → `GetProperty` ではなく `GetField` を使う
- VRC プロジェクトでは streamingMipmaps を常時 ON にする
  → `TextureImporter.streamingMipmaps = true` → `SaveAndReimport`
  → UI トグル不要、例外なし
- `controller.layers` はコピーを返す
  → レイヤー名などを変更した後は `controller.layers = layers` で再代入が必要
- MA MenuItem の `Control` フィールドは `AddComponent` 直後は null
  → `Activator.CreateInstance` で初期化してからフィールドをセットする
- MA / VRC SDK の enum 値はリフレクションで `Enum.Parse(fieldType, "名前")` で取得する
  → 数値直書き（`Enum.ToObject(type, 102)` 等）は MA バージョンで値がズレると無警告で壊れる
  → `Enum.Parse` なら名前変更時に `ArgumentException` を投げるため検知できる
  → try-catch で囲み、分かりやすいエラーログを出して処理を中断する
  → 参考: ControlType = Toggle / Button / SubMenu、AnimLayerType = FX、MergeAnimatorPathMode = Relative
- MA ObjectToggle のターゲット制約: 自分自身の先祖オブジェクトはターゲットにできない
  → ObjectToggle の子孫から見て先祖にあたるオブジェクトを Objects リストに入れると動作しない
  → ターゲットは ObjectToggle より下の階層に置く
- AvatarObjectReference の設定: `Set(GameObject)` を Prefab 保存前の一時オブジェクトに呼ぶとパス解決が壊れる
  → `referencePath` フィールドに相対パス文字列を直接セットし、`targetObject`（NonPublic フィールド）にも GameObject を直接セットする
- MA MenuInstaller の配置: root に直付けせず、専用の子オブジェクト（例: MA Menu/）に置く
  → MenuInstaller + SubMenu 型 MenuItem を同じオブジェクトにアタッチし、子の MenuItem を束ねる
- MA MenuItem SubMenu の MenuSource: `subMenuSource` フィールドを Children に明示設定しないと子の MenuItem が拾われない
  → デフォルト値に依存せず、リフレクションで明示的に設定する
- FX レイヤーと ObjectToggle の関係: MergeAnimator で FX に統合された AnimatorController はアバタールートの Animator で常時動作する
  → MA ObjectToggle で子オブジェクトをオフにしても FX の再生は止まらない
  → 「オフ中に止めて途中から再開」は VRChat + MergeAnimator 環境では実現困難
- keepAnimatorStateOnDisable: MergeAnimator なし・Animator 単体運用時にオブジェクトをオフにして途中から再開する手段として使える可能性があるが、VRChat 環境での動作は未検証・不安定の可能性あり
- `AssetDatabase.CreateAsset` は既存パスにアセットがあると上書きしない
  → Material: `LoadAssetAtPath` で既存を取得し `CopyPropertiesFromMaterial` でインプレース更新して GUID を保持する。既存がなければ `CreateAsset` で新規作成
  → Texture2DArray / AnimationClip: インプレース更新 API がないため `DeleteAsset` → `AssetDatabase.Refresh()` → `CreateAsset`（GUID は変わる）
  → PNG テクスチャ: `File.WriteAllBytes` で自然に上書き（.meta 保持で GUID 不変、対応不要）
  → AnimatorController: `DeleteAsset` → `CreateAnimatorControllerAtPath`（既存があると空で返るため事前削除必須）
- writeDefaultValues 非依存 = ON/OFF どちらでも動くよう AnimationClip で全ページを明示制御する設計
  → 各 AnimationClip が「自分 ON・他全ページ OFF」を明示的にキーフレームで制御する
  → writeDefaultValues = true のままでも問題ない（暗黙のデフォルト復帰に頼っていないため）
