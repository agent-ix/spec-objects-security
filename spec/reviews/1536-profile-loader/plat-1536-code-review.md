---
id: SR-049
title: "Code review of PR #52 source profile format test"
type: SpecReview
analysis: code-review
review_set: subset
scope: "agent-ix/spec-objects-security; tests/test_profiles.py (PR #52, git diff origin/main...HEAD at 135be4a)"
---
# SR-049: Code review of PR #52 source profile format test

## Summary

Ticket: PLAT-1536. The PR adds one file, `tests/test_profiles.py`. It defines the
FR-020 profile rules as `validate_profile`, tests them against synthetic
fixtures, and runs FR-021 and NFR-002 checks over every shipped profile. No
profile ships yet.

The repository gate was run on a fresh clone at 135be4a, in a temporary
in-project venv built with `poetry install` and `npm ci` (npmjs registry
overrides). `poe lint` passes: ruff, black, and the 51-schema drift check.
`poe test` (pytest with the repository's real addopts: coverage, a 100% floor,
and warnings as errors) gives **1 failed, 253 passed, 2 skipped, 9 xfailed**.
Coverage reaches 100%, because the package contains only `__init__.py`. The
failure is FND-001.

FR-020 rules, checked one at a time against the validator:

- Required keys: AC-2 deletes each of `name`, `title`, `description` and
  `clauseSets` and checks the matching message.
- `name` equal to the file stem: tested.
- Empty `clauseSets`, an empty key field, and a repeated key: each tested with
  its own message.
- Unknown top-level key, and an empty or non-string `context` value: tested.
- `text` or `title` under a `clauseSets` entry: tested. Entries must have
  exactly `authority`, `id` and `version`.
- `schemaVersion`: enforced, but no AC covers it.

Each fixture is otherwise valid, so only the rule under test can raise.

The FR-021 and NFR-002 tests that loop over shipped profiles collect zero
cases (pytest reports 2 skipped), which is correct today. FR-021 allows
"up to three" profiles, and forbids any profile that lists a key no module
declares. No module declares a clause set yet: neither this repository's
manifest at `origin/main` nor the 10 manifests under `~/.ix/filament/modules`
has `clause_sets`. The NIST and ASVS sets are in open PRs #50 and #51.
These tests are not ceremony. They are "for every shipped profile" checks
that apply as soon as a profile file is added, and that profile is the broken
state they guard against. The subset test (FR-021-AC-5) runs today and would
fail on an extra file. The synthetic-module test is the real coverage of the
declaration and publishability lookups, and FND-001 and FND-002 are both in
that test.

Licensing and leaks: the file names only the three profile names from FR-021,
the reserved `example.invalid` authority, and synthetic modules. It holds no
standard text, no licensed pack name and no roadmap content. The diff adds no
build artifacts.

## Verdict

**FAIL**: one high, two medium and two low findings. All can be fixed in this PR.

## Findings

| ID | Severity | Summary | Refs |
| --- | --- | --- | --- |
| FND-001 | high | `test_the_declaration_and_publishability_lookups_tell_modules_apart` fails against the engine this repository pins. `engine_tool` uses `node_modules/.bin/quire` before PATH. `package.json` pins `@agent-ix/quire-cli` 0.43.0, and that version has no `publish-check` subcommand: it prints "unrecognized subcommand" and exits 3. So after `npm ci`, `assert publish_check(open_module) == 0` fails. The coder's run passed only because the worktree had no `node_modules`, so the global quire 0.44.0 was used. Fix: bump `@agent-ix/quire-cli` to 0.44.0 in `package.json` and `package-lock.json`, the same bump open PR #50 makes, or land this PR after #50 | tests/test_profiles.py:209-216, tests/test_profiles.py:256, package.json:35 |
| FND-002 | medium | `assert publish_check(licensed) != 0` accepts any non-zero exit, including exit 3 (usage or I/O error). Measured: with the pinned 0.43.0 engine the licensed assertion passes on "unrecognized subcommand", so this negative check passes even when the engine cannot run the check at all. quire 0.44.0 exits 2 for a restricted set ("restricted clause sets: example.invalid/rules@2") and 3 for errors. Fix: assert `== 2`, and assert that stdout names `example.invalid/rules@2` | tests/test_profiles.py:209-216, tests/test_profiles.py:257 |
| FND-003 | medium | `reference_modules()` uses this module plus whatever happens to be installed under `$IX_HOME/filament/modules`. FR-021 defines a different set: the modules `quoin module ensure-defaults` installs, this module, and the published pack modules for intended sources. The installed set depends on the machine. A locally installed, unpublished or stale module (including an old installed copy of this module) can satisfy a shipped key on a dev box. In a clean environment with no matching install, a correct profile fails. This does not show today because no profile ships, but it will show on the first one. Fix: build the reference set explicitly, for example run `quoin module ensure-defaults` into a temporary `IX_HOME` and add the declared pack modules, instead of reading the ambient home | tests/test_profiles.py:192-197 |
| FND-004 | low | `shipped_profiles()` globs only `*.yaml`. A `profiles/x.yml` or `profiles/x.json` is invisible to the FR-021-AC-5 subset check, the FR-020 validator and the NFR-002 checks. NFR-002 covers "every file under `profiles/`". Fix: list every file in `profiles/` and fail on any that is not `<name>.yaml` | tests/test_profiles.py:97-98 |
| FND-005 | low | An unquoted numeric version in a profile (`version: 5`) is a YAML int. The validator refuses it with "a clause-set key field is empty", which is the wrong reason. Meanwhile `declared_keys` stringifies set versions with `str(...)`. The refusal is right, but the message sends the author the wrong way. Fix: report "must be a string" separately from "empty" | tests/test_profiles.py:64-65, tests/test_profiles.py:188 |
