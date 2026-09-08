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
