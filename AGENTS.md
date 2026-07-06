# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

## Core Principles (CRITICAL)

**Delete > Replace > Add.** Before writing any change, answer in order: what can I delete? what can I replace? only then, what must I add?

The most common agent failure in this repo is reaching for the locally-safest edit — a new guard, flag, or helper — instead of fixing ownership. These tripwires override that instinct:

1. **Never guard a symptom — relocate the trigger.** A fix that adds a condition to suppress bad behavior (a staleness check, an is-initialized flag, a skip-first-call guard, a try/except around broken logic) is wrong by default. Find the code path that should own the behavior, move the logic there, and delete the code that got it wrong. Example: a warning fired from stale state; the right fix was not a recency guard — it deleted the stale detection and moved the trigger into the code path that observes the event live.
2. **Bugfixes are net-negative by default.** A bugfix that adds more lines than it removes needs a one-sentence justification in the PR body naming why deletion and relocation were impossible.
3. **Search the repo before creating anything.** Before building a helper, search the whole package — it likely exists (`hub_sdk/base/` holds the shared `APIClient`/`CRUDClient`/`PaginatedList`, `hub_sdk/helpers/` the shared utilities). New resource modules subclass these rather than re-implementing HTTP or CRUD logic. If two modules grow the same logic, consolidate into the shared base and delete the duplicates. Avoid premature abstraction — three similar lines beat a helper nobody else calls.
4. **Deletion beats caution.** Zero regression means understanding the code you remove, not leaving it in place as insurance. Keeping broken or duplicated code "to be safe" is itself the regression: it is how repos rot. All changes must still ship debugged, validated, and production ready.

**Output gate:** every PR body must contain a `Deleted:` line naming the code removed (functions, branches, files, config). Features must name what they reused or consolidated. `Deleted: nothing` demands the rule-2 justification.

**Review gate:** adversarial reviewers must answer two questions before LGTM: (a) what could have been deleted instead of added? (b) does any added condition suppress a symptom rather than relocate a trigger? A finding on either blocks LGTM.

**This file is code — additions require deletions.** To add a rule here, remove or merge one. When everything is emphasized, nothing is.

**NEVER push to `main`. NEVER force push.** Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Launch an independent adversarial review agent with cold context (just the PR diff and this file) to hunt for bugs, regressions, and Core Principles violations — use the Codex CLI, one fresh `codex exec` run per round. Fix, push, and repeat until a fresh run reports LGTM.
3. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never force-push, reset, or revert commits you did not author.
4. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
# Editable install with docs + build tooling
uv pip install -e ".[dev]"

# Test-only dependencies (CI installs these, not the [dev] extra, for the Tests job)
uv pip install -r tests/requirements.txt

# Download test fixtures from Firebase Storage (needs FIREBASE_CRED + BUCKET_NAME env)
cd tests && python utils/test_data.py download

# Run the smoke suite exactly as CI does (hits the live HUB API — needs credentials)
python -m pytest -v -m "smoke" tests

# Single file / single test
python -m pytest tests/functional/test_model.py
python -m pytest "tests/functional/test_model.py::TestModel" -v

# Build and strict-check the docs as CI does
mkdocs build --strict
```

- CI (`ci.yml`) runs `Docs` (`mkdocs build --strict`) and `Tests` (smoke marker only) on Python 3.13 / ubuntu-latest, plus a `Summary` job that Slack-alerts on `push`/`schedule` failures (not PRs). The package supports Python >= 3.8.
- The `Tests` job needs live secrets (`FIREBASE_CRED`, `ULTRALYTICS_HUB_API`, `ULTRALYTICS_HUB_WEB`, `BUCKET_NAME`): fixtures download from Firebase Storage and the `setup` fixture logs a real `HUBClient` into the HUB API. These cannot run without credentials — do not add offline stubs to force them green.
- Test markers (`smoke`, `regression`) and the active pytest config live in `tests/pytest.ini` — that is the `configfile` pytest resolves, not `pyproject.toml`. CI selects `-m "smoke"`.

## Architecture

`hub_sdk` is a thin, layered REST client for the Ultralytics HUB API. `HUBClient` (`hub_sdk/hub_client.py`) is the single entry point: it extends `Auth`, logs in via API key or email/password, and its `.model()`, `.dataset()`, `.project()`, `.user()`, and `*_list()` methods return per-resource objects. The `@require_authentication` decorator on `HUBClient` gates every method except `.model()` unless the client authenticated; the `*_list()` methods additionally accept `public=True` to fetch public listings without auth.

- `hub_sdk/base/` — shared plumbing: `api_client.py` (`APIClient` wraps `requests` + `APIClientError`), `crud_client.py` (`CRUDClient` adds create/read/update/delete/list on top), `paginated_list.py` (`PaginatedList`), `auth.py` (`Auth`), and `server_clients.py` (`ModelUpload`/`ProjectUpload`/`DatasetUpload` for uploads, exports, predictions, heartbeats).
- `hub_sdk/modules/` — one resource class per file (`models.py`, `datasets.py`, `projects.py`, `users.py`, `teams.py`), each subclassing `CRUDClient`; most (all but `users.py`) also ship a paginated `*List` companion subclassing `PaginatedList`. Adding a resource means a module here plus, if it uploads, a client in `server_clients.py`. `Teams`/`TeamList` exist, but the `HUBClient.team()`/`team_list()` entry points are stubbed (`raise Exception("Coming Soon")`).
- `hub_sdk/helpers/` — `error_handler.py` (maps HTTP status codes to messages), `logger.py`, `exceptions.py`, `utils.py`.
- `hub_sdk/config.py` — all runtime config from env vars: API/web roots, Firebase auth, and `HUB_EXCEPTIONS` (default `true`, set via `ULTRALYTICS_HUB_EXCEPTIONS`). The `CRUDClient` methods catch every exception and return `None` after logging, so a resource call returning `None` signals a logged failure, not empty data — check the logs.
- Docs reference pages under `docs/reference/` are committed by hand (there is no autogenerator) and wired into `mkdocs.yml`'s `nav`; keep both in sync when you add, rename, or remove a public module.

## Conventions

- Every Python file starts with `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` — Ultralytics Actions adds headers automatically; don't add or revert them manually.
- Google-style docstrings with types in parentheses (`arg1 (int): ...`). Formatting is applied in CI by Ultralytics Actions (`format.yml`: Ruff, docformatter, prettier for YAML/JSON/Markdown, codespell); its output can differ from local, so expect bot commits on PR branches. The repo also ships `.pre-commit-config.yaml` (yapf/isort/docformatter/mdformat) for local use.
- `tests/functional/` holds the pytest classes (`TestModel`, `TestDataset`, `TestProject`, `TestAuth`, all subclassing `tests/utils/base_class.py`); `tests/features/` holds the page-object helpers they drive; `tests/conftest.py` wires fixtures. Tests are integration tests against the live HUB — there are no offline unit tests.
- Releases: bump `__version__` in `hub_sdk/__init__.py`; on push to main, `publish.yml` detects the increment, then tags, creates the GitHub release, and publishes to PyPI (gated to the `ultralytics/hub-sdk` repo and `glenn-jocher`).
