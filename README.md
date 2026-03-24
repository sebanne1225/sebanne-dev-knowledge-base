# sebanne-dev-knowledge-base

Unity / VRChat ツール開発で使う共通情報源をまとめる専用 repo。

## 置くもの
- `PROJECT_SHARED_CONTEXT.md`
  - 変わりにくい共通前提
- `CODEX_PROMPT_BANK.md`
  - 再利用する定型プロンプト
- `UNITY_VRCHAT_TOOL_UI_GUIDELINES.md`
  - Unity / VRChat ツール UI 方針
- `PUBLIC_RELEASE_GUIDELINES.md`
  - GitHub Release / VPM / VCC / BOOTH の公開運用
- `REPO_INDEX.md`
  - よく使う repo の入口一覧
- `THREAD_CLOSEOUT_TEMPLATE.md`
  - スレ終了時の抽出テンプレ
- `NDMF_BUILD_PASS_SHARED.md`
  - NDMF Build Pass の薄い shared note
- `skills/`
  - 複数 repo で再利用する共通 Skill 実装

## 置かないもの
- 各 repo 固有の前提
- 単発の作業ログ
- 一時メモ
- repo 固有の実装コード

repo 固有の内容は、各 repo 内の `CODEX_HANDOFF.md` や `Documentation~/notes/` に残す。  
ただし、`public-release-sync-check` のような診断専用で複数 repo に再利用する共通 Skill は knowledge repo に置いてよい。
