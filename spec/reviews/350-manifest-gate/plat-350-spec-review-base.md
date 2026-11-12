---
id: SR-020
title: "Spec review of PR #41 FR-003-AC-7 and the schema-ownership amendment"
type: SpecReview
analysis: base
review_set: subset
scope: "agent-ix/spec-objects-security; spec/functional/FR-003-semantic-manifest-contract.md, spec/functional/FR-001-module-manifest-activates.md, spec/stakeholder/StR-001-module-activation.md, spec/spec.md, spec/tests.md (PR #41 diff at 29c7445)"
---
# SR-020: Spec review of PR #41 FR-003-AC-7 and the schema-ownership amendment

## Summary

Ticket: PLAT-350. `quire validate --scope .` passes on all five changed spec
files. Removing the `ix://agent-ix/filament-core-service/FR-035` links leaves no
dangling reference: `git grep FR-035` finds no hit under `spec/`.

The ownership change is accurate. `filament-core-data` publishes
`schema/semantic/v1/module-manifest.schema.json` (its FR-149), and quire-rs
embeds that schema (`src/semantic/embedded.rs`). As a probe, the shipped
manifest was validated against that schema at filament-core-data main
`60d46cf2`. It has 0 errors. Nothing was copied into this repo.

The PR claims that `quire validate` and `quoin module install` gate different
things. Measured, the claim is accurate:

- `quire validate --module` refuses a top-level `bogus_key` (exit 3) but
  accepts `semantic.foo` (exit 0).
- `quoin module install` refuses `semantic.foo` (exit 1) but accepts
  `bogus_key` (exit 0).

FR-003-AC-7 states this split faithfully. The FR-003 Inputs and the `spec.md`
non-goal do not.

## Verdict

FAIL. AC-7 asserts an isolation that does not happen. The Inputs text
overstates what each engine checks. Three statements that predate AC-7 now
contradict it.

## Findings

| ID | Severity | Summary | Refs |
|----|----------|---------|------|
| FND-001 | high | FR-003-AC-7 says `quoin module install` runs "into an isolated config root". It does not. `IX_CONFIG_ROOT` leaves the install target at `~/.ix/filament/modules`, so the AC asserts an isolation the test does not deliver (see SR-019 FND-001). | spec/functional/FR-003-semantic-manifest-contract.md:68 |
| FND-002 | medium | The FR-003 Inputs say the schema is "embedded by the Quire engine, which applies it when it loads a module (`quoin module install` applies it too)" and that "the gate is the real engine applying it". The `spec.md` non-goal says the same: "engines that apply the authoritative schema". Measured, each engine enforces a different part. quire accepts `semantic.foo` and quoin accepts `bogus_key`, while the authoritative schema (root `additionalProperties: false`) refuses both. The PR deleted the accurate note that the carriers diverge. State the split as AC-7 does. | spec/functional/FR-003-semantic-manifest-contract.md:29-33, spec/spec.md:62-67 |
| FND-003 | low | "depends on no package that redistributes one" is now false as written. `pyproject.toml` depends on `quire`, whose engine embeds the schema, and the same paragraph says the engine embeds it. Say instead that no copy is held in this repository. | spec/functional/FR-003-semantic-manifest-contract.md:32, spec/spec.md:63-64 |
| FND-004 | medium | FR-003-CON-1 still says Quoin's refusal of an unknown `semantic` key "is assumed, evidenced only by the clean install of IT-002". FR-003-AC-7 and TC-115 now verify that refusal, naming `semantic.foo`. | spec/functional/FR-003-semantic-manifest-contract.md:58 |
| FND-005 | medium | The FR-003 Behavior says "`quoin module install` (FR-003-AC-5) is a Demonstration this repository cannot run", and the FR-003 note in `spec/tests.md` says "AC-5 is a Demonstration nothing here can discharge". AC-7 now runs `quoin module install path:<module dir>` and asserts exit 0. Once the install is truly isolated, AC-5's "listed by `quoin module`" can also be a Test, and its "restore the previous entry" clause becomes unnecessary. | spec/functional/FR-003-semantic-manifest-contract.md:47, spec/functional/FR-003-semantic-manifest-contract.md:66, spec/tests.md:93 |
