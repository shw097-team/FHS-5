# PUBLICATION STATUS

- repo: `https://github.com/shw097-team/FHS-5.git`
- branch: `codex/w1-nf-r3-20261125`
- base: `c2d8084ba24dd8df3fa62259bba496f4fb9caa85` (main untouched, no force, no merge)
- content commit: `bb87f441d0e16d7371e064b3ce614a0972709889`
- published commit: `a539b1c3dab89b4fd62d3cc537191cd6ce2ad74e`
- pull request entry: https://github.com/shw097-team/FHS-5/pull/new/codex/w1-nf-r3-20261125

## Push state: PUSHED_AND_VERIFIED

`git push` returned rc=0; the remote reports the branch at the same commit as
local HEAD. Credential was injected only as temporary environment configuration
(`http.extraheader` via GIT_CONFIG_* env vars); it was not written to argv, git
config, logs, evidence or the repository, and the temporary env was removed.

## Independent readback from the remote (fresh clone)

| 項目 | 遠端重算值 |
|---|---|
| `remote HEAD` | `a539b1c3dab89b4fd62d3cc537191cd6ce2ad74e` |
| `05_W1_SOURCE_MANIFEST.json` sha256 | `61f34a08fa63190b9213d2affab2df0688a2497ba0bf753edf60c82ce4bfa30a` |
| `EVIDENCE_MANIFEST.json` sha256 | `69e28274045975d82e2130a2ae20986ed61bd7d91cd224b363242fb7029205b8` |
| `W1/impl/*.py` | 10 files |
| `W1/check/*.py` | 12 files |
| `openspec/changes/w1-nf-r2-product` | present |

The pack digest equals the manifest pin, so the public tree is byte-faithful
for the frozen six-file pack.

## History preserved

- `main` remains `c2d8084ba24dd8df3fa62259bba496f4fb9caa85`
- `codex/w1-nf-r2-20261125` remains `ae05a74514d2c310f82bbf9bb1a2009078f11c87`
- new branch only; fast-forward push; no force, no rewrite

## Claim effect

Publishing does not equal `W1_NF_VALIDATED`, `RELEASED` or `M-DONE`.
`W1_PARTIAL_VALIDATED` and `W2_TECHNICALLY_READY = NOT_READY` stand unchanged.
