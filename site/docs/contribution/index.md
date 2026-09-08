# Contribution guide

Documents and the website can be built locally. GitHub Actions runs the same tools;
access to Actions or deployment credentials is not required to contribute.

## Build a document

Install Python 3.11+, GNU Make, and a TeX distribution providing latexmk and the
packages used by the document. From the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r build/python-requirement-lists/general-pkgs.txt
cd src/MATH1853-Assignment-I.1
../../configure
make
```

The PDF appears in the document directory. Missing dependencies are reported by
configure. For minted documents, additionally install
`build/python-requirement-lists/python-minted-pkgs.txt` into the same environment.
Run `make clean` for auxiliary files or `make distclean` for all runner outputs and
configuration. Source files and handwritten Makefiles are retained.

## Build the website

Install Poppler and `build/python-requirement-lists/site-pkgs.txt`, then run these
commands from the repository root:

```sh
./configure --targets MATH1853-Assignment-I.1 COMP1110-Project
make -j2 site
python -m http.server --directory dist/site 8000
```

Omit `--targets` to build the whole catalogue. The Ubuntu-specific project ZIP requires
Ubuntu 24.04 x86_64, the optional Docker build image, or an explicitly supplied
artifact directory. See the repository README for environment setup and Docker commands.
External sources are pinned to commits and cached locally after their first fetch.

Site sources are staged in `.build/site`; the final website is in `dist/site`.
Generating navigation and pages does not modify tracked site sources. Previews and
artifact manifests live in `dist/artifacts`. Deployment and indexing are separate
operations and never run as part of `make site`.

## Add material

1. Create `src/<target>/` with a [v3 metadata.json](syntax-reference/metadata.json/v3.md).
2. Add its source files. The default root is `<target>.tex`; override `build.root_file`
   when needed. Separating packages into `packages.tex` is optional.
3. Add the target to [build/build-targets.txt](syntax-reference/build-targets.txt.md)
   to include it in the catalogue. Individual document builds do not require this entry.
4. Run configure and make locally, then submit a pull request.

Only schema v3 is accepted. The v1/v2 references are retained for historical context.

## Change the build tools

The shared implementation is in `build/hkbuild`. Generated Makefiles call the runner;
GitHub Actions provisions tools and runs those Makefiles. Test changes locally:

```sh
python build/build.py validate
PYTHONPATH=build python -m unittest discover -s build/tests -v
```

The tests use temporary directories and fake compiler/site processes where appropriate;
no TeX installation or credentials are needed for the test suite. Also build a relevant
real document or website when changing compilation or rendering behavior.

## Attribution

Add yourself to [authors.json](syntax-reference/authors.json.md), then reference your
handle in the document's [authors field](syntax-reference/metadata.json/v3.md#authors).
