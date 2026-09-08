# Refactor validation

Verified locally on 2026-09-08, using macOS arm64, MiKTeX, and Python 3.14.2.

- All 34 existing metadata files migrated to v3 and validated against the checked-in
  schema. Tests reject v1/v2, unknown fields, invalid aliases, and reserved outputs.
- 19 build-tool tests pass on Python 3.12 and 3.14. All build modules also parse with
  Python 3.11 syntax rules; Python 3.11 runtime execution was not available locally.
- Real configure/Make builds produced all 29 catalogue PDFs. This includes minted,
  generated standalone figures, texcount, the renamed CV, and all three pinned
  external-source PDFs. The cheatsheet alias was also built from its own directory.
- `make site` completed for 32 catalogue entries: 29 PDF targets, two page entries,
  and the cheatsheet alias. Zensical 0.0.41 reported no issues.
- All 3,545 local href/src references across the 44 generated HTML files resolve.
- Repeating actual Zensical assembly produced identical generated document sources
  and left the tracked site sources unchanged. Artifact previews remain reusable.
- Tests cover real Make execution in paths containing spaces and dollar signs,
  dependency changes, failed/missing outputs, retrying a repaired TeX build, pinned
  Git source reuse with an unavailable origin, explicit artifact imports, cleanup,
  alias cycles, and failed site assembly preserving the previous site.
- The workflow YAML parses and its build → deploy → indexing dependency chain was
  checked. The Ubuntu provisioning script passes shell syntax checking.

## Environment-specific limits

The `COMP2113-Project` Ubuntu 24.04 x86_64 ZIP and its `ENGG1340-Project` alias were
excluded from native macOS compilation. Their environment rejection and ZIP packaging
are tested with fixtures. The pinned CMake source was inspected, including its resource
copy target and external FTXUI dependency. The Docker daemon was unavailable locally,
so the Ubuntu image, Ubuntu compilation, and hosted GitHub Actions run were not executed.

The local test setup used `.venv`, installed Poppler, and installed MiKTeX's `sourcesans`
package to provide the missing `sourcesanspro.sty`. No document content was changed to
work around the missing package. No deployment or indexing notifications were sent.

## Repeating the checks

```sh
python build/build.py validate
PYTHONPATH=build python -m unittest discover -s build/tests -v
```

For full catalogue verification, use the Ubuntu container instructions in the root
README, or a matching native Ubuntu environment, followed by `./configure && make -j2 site`.

## MiKTeX provisioning correction

CI and the optional Ubuntu image now install MiKTeX, initialize a writable per-user
package tree, and enable on-the-fly package installation. The workflow caches that
package tree and uses serial document builds during cold package installation.
The revised shell scripts pass syntax checking and the workflow YAML parses.
Ubuntu/Docker execution remains unverified locally.

## Source-aware artifact reuse

Added source fingerprints, protected metadata hashing, gitignore-style
`build.hash_ignore`, verified artifact restoration, and explicit force rebuilding.
All 30 tests pass, including fresh-checkout reuse, added/deleted inputs, ignored
files and negation, source PDF inputs, corrupt/missing artifacts, metadata changes,
source overrides, failed forced builds, and supplied-artifact provenance.

Real MiKTeX checks for `MATH1853-Assignment-II.1`, `CCCH9044-Individual-Essay`, and
`COMP2120-Notes` confirmed that generated files leave source fingerprints unchanged
and a second build executes no preparation/compiler/finishing commands. The workflow
YAML was checked for both package and artifact caches and the force-rebuild flag.
Hosted cache restoration remains untested locally.

## Missing xkeyval contingency fix

Inspected CI run 34226126677. The grouped legacy `mpm --install=...` invocation
reported “The requested package is unknown,” but setup continued; the CV later
failed loading `xkeyval.sty`. Restored individual `miktex packages install` calls
for the original contingency packages, package updates, and explicit file-resolution
checks after refreshing the filename database. Setup now fails immediately if any
of the four required style files remains unavailable.

All 34 tests pass, including installer failure, a zero-exit installer that creates
no package file, and empty/failed file lookups. Shell syntax checking passes; local
MiKTeX resolves all four styles. The Ubuntu CI setup itself has not been rerun with
this fix. Its changed setup-script hash invalidates the previous package cache key.
