# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

HUB-SDK (`hub-sdk` on PyPI, AGPL-3.0) is the historical Python REST client for Ultralytics HUB, which was deprecated and shut down on July 31, 2026. The source is retained for reference only — HUB APIs and API keys no longer work, and current automation belongs in the [Platform REST API](https://docs.ultralytics.com/platform/api).

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
# Editable install with docs + build tooling
uv pip install -e ".[dev]"

# Build and strict-check the docs as CI does
mkdocs build --strict
```

- CI (`ci.yml`) builds documentation with `mkdocs build --strict` on Python 3.13 / ubuntu-latest for pushes, pull requests, and manual dispatches. It does not run on a schedule or call HUB services.
- Historical tests target the shut-down HUB API and are not runnable. Do not restore live HUB/Firebase CI or add offline stubs to simulate the retired service.

## Architecture

`hub_sdk` is the historical REST client for Ultralytics HUB, which was deprecated and shut down on July 31, 2026. The managed HUB-to-Platform migration was completed during Q2 2026 before shutdown; HUB APIs, services, and API keys no longer work, and this package is not compatible with the Platform API. The source remains for historical reference only; do not add HUB features, present these clients as usable integrations, or describe the completed migration as ongoing. Current automation belongs in the [Platform REST API](https://docs.ultralytics.com/platform/api).

Historically, `HUBClient` (`hub_sdk/hub_client.py`) was the single entry point: it extended `Auth`, logged in via API key or email/password, and its `.model()`, `.dataset()`, `.project()`, `.user()`, and `*_list()` methods returned per-resource objects. The `@require_authentication` decorator on `HUBClient` gated every method except `.model()` unless the client authenticated; the `*_list()` methods additionally accepted `public=True` to fetch public listings without auth.

- `hub_sdk/base/` — shared plumbing: `api_client.py` (`APIClient` wraps `requests` + `APIClientError`), `crud_client.py` (`CRUDClient` adds create/read/update/delete/list on top), `paginated_list.py` (`PaginatedList`), `auth.py` (`Auth`), and `server_clients.py` (`ModelUpload`/`ProjectUpload`/`DatasetUpload` for uploads, exports, predictions, heartbeats).
- `hub_sdk/modules/` — one resource class per file (`models.py`, `datasets.py`, `projects.py`, `users.py`, `teams.py`), each subclassing `CRUDClient`; most (all but `users.py`) also ship a paginated `*List` companion subclassing `PaginatedList`. Adding a resource means a module here plus, if it uploads, a client in `server_clients.py`. `Teams`/`TeamList` exist, but the `HUBClient.team()`/`team_list()` entry points are stubbed (`raise Exception("Coming Soon")`).
- `hub_sdk/helpers/` — `error_handler.py` (maps HTTP status codes to messages), `logger.py`, `exceptions.py`, `utils.py`.
- `hub_sdk/config.py` — all runtime config from env vars: API/web roots, Firebase auth, and `HUB_EXCEPTIONS` (default `true`, set via `ULTRALYTICS_HUB_EXCEPTIONS`). The `CRUDClient` methods catch every exception and return `None` after logging, so a resource call returning `None` signals a logged failure, not empty data — check the logs.
- The rendered documentation is a single shutdown/Platform redirect page. Historical API source remains in `hub_sdk/` but must not be exposed as an active-use guide.

## Conventions

- Every Python file starts with `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` — Ultralytics Actions adds headers automatically; don't add or revert them manually.
- Google-style docstrings with types in parentheses (`arg1 (int): ...`). Formatting is applied in CI by Ultralytics Actions (`format.yml`: Ruff, docformatter, prettier for YAML/JSON/Markdown, codespell); its output can differ from local, so expect bot commits on PR branches. The repo also ships `.pre-commit-config.yaml` (yapf/isort/docformatter/mdformat) for local use.
- `tests/functional/` contains retired HUB integration tests; there are no offline unit tests. Do not run or re-enable them against the shut-down service.
- HUB-SDK has no release workflow. Do not add publishing automation or bump the package for this historical source.
