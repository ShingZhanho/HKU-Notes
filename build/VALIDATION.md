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

## SimpleIcons failure and parallel CI restoration

Inspected failed run 34227028174: the xkeyval contingency succeeded, but pdfLaTeX
failed on `SimpleIcons--simpleiconstwo`, attempting bitmap generation and reporting
`SimpleIcons.afm` missing. Setup now explicitly installs `simpleicons` before
refreshing font maps and checks both its Type 1 font files and the active
`pdftex.map` entry. Other document packages retain on-the-fly installation.

CI now validates and selects targets once, builds canonical targets in a matrix
with `fail-fast: false`, and assembles the site from downloaded document artifacts.
Each runner has its own writable MiKTeX installation and per-target caches;
source-fingerprint verification still skips unchanged compilation. The site job
uses the shared assembly command directly, without invoking document compilation.
Target branches preserve aliases in site selection while compiling only their
canonical target. Deployment waits for assembly.

All 40 unit/integration tests pass, including font setup failure checks, matrix
selection and alias deduplication, existing cache invalidation/restore tests, and
website assembly tests. Metadata validation passes for all 34 files. The full-site
matrix has 32 canonical targets. Actionlint reports no workflow errors, shell syntax
and git diff whitespace checks pass. The hosted Ubuntu build and artifact transfer
have not yet been executed with these commits; local checks do not reproduce a
fresh Ubuntu MiKTeX installation.


## General MiKTeX recovery and theorem compatibility

Compared the last successful legacy pipeline at 4874955 with the refactor. Legacy
commands used `latexmk -f -interaction=nonstopmode`, without `-halt-on-error`.
They also enabled MiKTeX installation explicitly. Restored explicit installer use
for filename/font-map maintenance, removed the SimpleIcons-specific installation
and map checks, and added generic bounded recovery in the shared LaTeX runner.
Compiler output remains live and is retained for diagnosis. Recognized font and
MiKTeX runtime/network failures refresh maps and force a fresh pass, up to three
compiler attempts total. Undefined commands and unrecognized source errors are
not retried. A final compiler/maintenance error still prevents publication.

APT downloads now retry with timeouts, and repository update errors are fatal
instead of falling through to “Unable to locate package miktex.” Signing-key curl
requests and individual MiKTeX setup operations have bounded retries. No mirrors
are hardcoded, and prolonged mirror outages can still exhaust the retry budget.

The COMP2120-Notes failure is reproducible with the current upstream
[alias-counter implementation](https://github.com/latex3/latex2e/blob/develop/base/ltcounts.dtx)
and [amsthm adaptation](https://github.com/latex3/latex2e/blob/develop/required/firstaid/latex2e-first-aid-for-external-files.dtx):
`newcounteralias` defines reference macros locally. The document grouped its
`newtheorem` declarations, so the new reference macros vanished at group end.
A temporary minimal fixture using those upstream definitions reproduced undefined
`p@theorem`; the same fixture with ungrouped declarations compiled successfully.
Declarations now remain at preamble scope, preserving the shared numbering.
This does not require ignoring compiler errors or downgrading packages.

All 48 tests pass, including arbitrary font recovery, network recovery, exhausted
retries, source-error rejection, TeX Live isolation, maintenance failure handling,
and live stdout/stderr preservation. Metadata validation, shell syntax, and
Actionlint pass. Real local MiKTeX forced builds of CV and COMP2120-Notes succeed
(the latter produces 38 pages). These use an existing macOS package tree; the
cold-install recovery path is covered by simulated failures, not a fresh Ubuntu
installation. Docker is installed but its daemon is unavailable. Hosted CI must
still verify cold Ubuntu installation and recovery after these commits are pushed.

## Mixed-encoding compiler diagnostics

Run 34588097607 passed 31 matrix targets but failed FREN2001-Grammaire in Python's
new live-output reader: a raw 0xe9 byte raised UnicodeDecodeError before the runner
could report the compiler result. The tee reader now explicitly decodes UTF-8 with
replacement for invalid bytes. This affects diagnostic display only, not document
files or the compiler's exit status. Raw TeX log files remain available in failure
artifacts.

All 49 tests pass, including a subprocess emitting mixed UTF-8/legacy bytes on
stdout plus stderr, checked with both zero and nonzero exits. A forced local
MiKTeX build of FREN2001-Grammaire succeeds. Hosted Ubuntu validation of this fix
is pending the next pushed run.

## Warm-cache setup and APT mirror fallback

Run 34589951391 exposed an idempotency bug: MiKTeX returns a failure for
`packages install latexmk` when the restored cache already contains latexmk.
Setup now queries `packages info --template={isInstalled}` before each install,
including on retries after partial success. Missing packages are still installed,
unknown/query failures remain errors, and style-file verification still runs.

Two inspected jobs instead failed fetching MiKTeX's signed APT index from the
redirector's selected mirror. Ubuntu provisioning now tries the MIT CTAN endpoint
after the primary repository exhausts retries, for either index or archive errors.
Both endpoints use the same signed-by MiKTeX key; verification is not disabled.
The MIT Noble InRelease endpoint was fetched successfully during investigation.
This is an APT fallback; it does not change MiKTeX's on-demand package mirror.

All 56 tests pass, including cold, warm, partial and repeated setup; partial
installer success followed by an error; primary APT success; index/archive fallback;
and both mirrors failing. Metadata validation, shell syntax, Actionlint and diff
checks pass. Hosted CI verification after pushing these fixes is still pending.

## HTML preview refactor — 2026-09-11

Branch: `codex/html-preview-refactor`.

- Converted all 29 existing compiled PDFs locally with pdf2htmlEX 0.18.8.rc2,
  using the pinned Docker image and SVG backgrounds. The PNG background backend
  crashed on the project report; the SVG backend converted all 303 pages.
- Assembled the complete 34-entry catalogue: 32 canonical details pages, including
  three non-PDF project pages, plus two aliases. The Ubuntu ZIP was imported from
  the currently published artifact; existing PDFs were reused without running TeX.
- The generated site is in `dist/site`. All 29 preview details pages contain
  declarative shadow roots in the initial HTML. Every converter text node and page
  count survived embedding. Standalone converter HTML is removed from public output.
- 61 build-tool tests pass. Coverage includes preview cache reuse, damaged-asset
  regeneration, converter changes, preservation of previous previews after failure,
  font isolation, and separation of preview tooling from PDF source fingerprints.
- A repeated preview pass reused all 29 cached conversions. Zensical 0.0.41 built
  the full website without reporting issues.
- Chrome browser checks visited all 29 PDF detail pages: no JavaScript exceptions,
  missing local HTTP resources, broken background images or failed preview fonts.
  Desktop and 390px mobile screenshots were reviewed for the report and cheatsheet.
  Zoom supports horizontal panning within the reader without widening the webpage.
  Page jumps clear the sticky toolbar; the desktop reader uses the former TOC space.
- The report renders all 16 pages with JavaScript disabled. A simulated theme
  navigation via `innerHTML` also initializes its shadow root. The in-app WebKit
  accessibility tree exposes all report pages and their text.
- Local OrbStack Rosetta execution hung; its alternate emulation mode worked.
  The setting was changed temporarily for validation. No hosted CI, deployment,
  Google URL inspection or indexing notifications were performed.

The converter preserves fixed PDF layout, including its fragmented text and weak
semantic structure. These checks establish rendering and text delivery, not WCAG
conformance or a guarantee of Google indexing.

Follow-up checks: the reader now establishes its own stacking context, so the
Zensical navigation drawer/backdrop covers its sticky toolbar. The page indicator
uses viewport-height pixel margins and stays on page 10 after a jump (and page 4
at mobile width). The upstream AppImage's runtime libraries were checked on Ubuntu
24.04; all report pages rendered, exposing a missing default manifest path. The
installer now supplies the extracted data directory explicitly, and a complete
AppImage report conversion with that path succeeded. The full MiKTeX build image
and hosted CI were not rerun.

## Remaining SEO fixes

The sitemap now derives URLs from self-canonical rendered HTML pages, excluding
404, verification, noindex, duplicate, and raw converter pages. It promotes HTML
details pages while preserving PDF download links. Generated robots.txt advertises
the sitemap and permits access to preview assets. Existing canonical paths remain
unchanged. Details have readable titles; static references have descriptions;
MATH1853 Part I/II and COMP2121 assignments now have distinct descriptions.

Removed Google Indexing API submissions, which are unsupported for these document
pages. IndexNow remains an explicit post-deployment operation; errors return a
nonzero status, URL/key scope is validated, and batches respect the 10,000 URL
limit. CI installs notification dependencies for the test job. No Cloudflare
configuration was changed and no live indexing requests were sent during testing.

Validation: all 65 unit/integration tests pass; all 34 metadata files validate;
Actionlint and git diff whitespace checks pass. Complete local website assembly
succeeds. The output audit finds 43 canonical HTML sitemap entries, including all
32 details pages, no missing or duplicate descriptions, no duplicate titles, and
no broken internal file links. All 29 embedded PDF previews remain present. This
checks the generated site, not Google's eventual indexing decision or hosted CI.
No MiKTeX/latexmk/TeX compilation processes remain running.
