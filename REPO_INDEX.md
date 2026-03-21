# よく使う repo 一覧

この一覧は、今後も繰り返し参照する repo の入口だけをまとめたものです。  
単なるリンク集ではなく、「何の repo か」「どの場面で見るか」がすぐ分かる最小メモとして使います。

原則:
- 共通前提や再利用する定型は情報源に置く
- repo 固有の今回だけの状況や残件は、その repo の `CODEX_HANDOFF.md` に置く
- 単発の作業ログや一時メモは情報源に増やしすぎない
- 今後も繰り返し参照する repo だけを載せる
- 単発の作業用 repo は基本ここに増やしすぎない

---

## 1. 情報源 repo
- `sebanne1225/sebanne-dev-knowledge-base`
- 用途:
  - 共通前提
  - 定型プロンプト
  - 公開方針
  - UI 方針
  - 運用ルール
- 見る場面:
  - 新しい作業を始める前
  - 共通ルールを確認したい時
  - 情報源に追加 / 整理する内容を考える時

## 2. VPM listing repo
- `sebanne1225/sebanne-listing`
- 用途:
  - VPM / VCC 向け listing 管理
  - `source.json`
  - Pages / `index.json`
- 見る場面:
  - 新しい package repo を listing に追加する時
  - package 公開後に listing 反映を確認する時
  - VCC 導入導線を確認する時

## 3. package repo 一覧

### `sebanne1225/avatar-audio-safety-guard`
- 用途:
  - Avatar Audio Safety Guard 本体 repo
- 見る場面:
  - package.json / README / CHANGELOG / Release 確認
  - 公開準備、release、listing 反映確認
  - BOOTH 公開前の最終確認

### `sebanne1225/animation-clip-start-delay`
- 用途:
  - AnimationClip Start Delay 本体 repo
- 見る場面:
  - 公開文面、package metadata、BOOTH_PACKAGE の整合確認
  - release / listing / VCC 導線確認

### `sebanne1225/blendshape-clip-fixer`
- 用途:
  - Blendshape Clip Fixer 本体 repo
- 見る場面:
  - package 構成や公開面の横並び確認
  - 他 package と説明の温度感をそろえる時

### `sebanne1225/sebanne-skinned-mesh-mirror`
- 用途:
  - Skinned Mesh Mirror 本体 repo
- 見る場面:
  - 非破壊 / 冪等 / Dry Run / ログ設計の参照
  - UI や README の整え方を他 repo と比較する時

---

## repo ごとの運用メモ

各 repo では、共通前提だけでは足りない「今回の作業条件」を `CODEX_HANDOFF.md` に置く。  
そこには最低限、次を入れる。

- Goal
- Current State
- Current Blocker
- Rules
- Tasks
- Definition of Done

使い分け:
- 情報源 = 変わりにくい土台
- `CODEX_HANDOFF.md` = 今回だけの具体指示
- スレッド = 単発ログ、途中経過、試行錯誤
