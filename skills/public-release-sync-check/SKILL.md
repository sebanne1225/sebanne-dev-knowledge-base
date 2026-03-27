---
name: public-release-sync-check
description: 公開前の package repo に対して version / URL / metadata / BOOTH_PACKAGE / README / TOOL_INFO の整合を診断する。Blocking / Warning に分類して次アクションを案内する。自動修正・リリース実行はしない。
---

# public-release-sync-check

Run the bundled checker script against the target package repo.

## Quick Start

Use:

```bash
python scripts/public_release_sync_check.py <target_repo> [--expected-version X.Y.Z] [--check-scope pre-release]
```

The script prints JSON in the fixed schema from `references/public-release-sync-check-spec.md`.

Example:

```bash
python scripts/public_release_sync_check.py c:/vrc-pro/ToolDevWorkspace/Repos/blendshape-clip-fixer --check-scope pre-release
```

## Workflow

1. Run the script with the target repo path.
2. If `status` is `unsupported-input`, stop there and surface the input correction guidance.
3. Otherwise, read `issues` and group them into Blocking and Warning by `severity`.
4. Use `suggested_next_action` to recommend the next action.
5. Use `patch_hint` only as direction. Do not auto-fix, create releases, update listing repos, or perform VCC checks.

## Boundaries

- Keep this Skill diagnostic-only.
- Do not implement release execution, listing repo reconciliation, VCC verification, or automatic patching inside this Skill.
- Keep repo-specific exceptions in the target repo `CODEX_HANDOFF.md`. Do not turn them into shared rules.

## References

- Read `references/public-release-sync-check-spec.md` when adjusting rules or reviewing a suspected false positive.
- The script derives shared expectations from the knowledge repo root:
  - `PUBLIC_RELEASE_GUIDELINES.md`
  - `PROJECT_SHARED_CONTEXT.md`
  - `REPO_INDEX.md`
