# HKU Notes

HKU Notes is my personal revision resources management project for the courses I took
at The University of Hong Kong in pursuit of my Bachelor of Engineering (Computer Science)
degree.

Documents, project artifacts, and the website can be built locally with Python and
GNU Make. GitHub Actions runs the same build pipeline to publish the website; local
builds do not require access to Actions or deployment credentials.

## History of the Project

Originally, this project started at [notes for COMP2120](https://github.com/ShingZhanho/COMP2120-Notes)
and as I planned to add more notes for other courses, I decided to create a new repository
to manage them at one place. The original notes are also ported to this repository.
The original COMP2120 notes repository is now archived and will not be updated.
## Local builds

Builds require Python 3.11+, GNU Make, and a TeX distribution (TeX Live or MiKTeX)
providing `latexmk` and the document's TeX packages. Linux, macOS, and Windows via
WSL are supported. Native Windows shells are not currently supported.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r build/python-requirement-lists/general-pkgs.txt
cd src/MATH1853-Assignment-I.1
../../configure
make
```

The PDF is written to the document directory. `configure` checks dependencies but
never installs them. Minted documents additionally require the packages in
`build/python-requirement-lists/python-minted-pkgs.txt`. Preview images require
Poppler (`pdftoppm`); ordinary PDF builds do not.

At the repository root, `./configure` selects `build/build-targets.txt`. Use
`./configure --targets CV COMP2120-Notes` to select a subset, then `make -j2` or
`make CV`. Alias targets automatically include their destination. Running configure
again replaces only a previously generated Makefile. Documents read their metadata
on every build; rerun configure after changing target selection or aliases.

`make clean` removes LaTeX intermediate files. `make distclean` also removes runner
outputs, source caches, and generated configuration. Handwritten Makefiles and source
files are retained. `make preview` builds PDFs and creates page images.

Advanced document options: `--profile=NAME`, `--source-dir=/path/to/source`.
Repository or document option: `--artifact-dir=/path/to/artifacts`, whose children
are `<target>/<output_file>`. Targets found there use explicitly supplied artifacts;
other targets compile normally. Additional named outputs must also be supplied.
`--no-check` defers dependency checking to build time; it does not bypass runtime
checks or environment requirements.

All documents use [metadata v3](site/docs/contribution/syntax-reference/metadata.json/v3.md).
v1/v2 inputs are rejected; their reference documentation is retained.

Validate metadata and run the build-tool tests without a TeX installation:

```sh
python build/build.py validate
PYTHONPATH=build python -m unittest discover -s build/tests -v
```

## Build the website

Install the site dependencies into the same environment used by configure, and install
Poppler using your OS package manager (`brew install poppler` on macOS,
`sudo apt install poppler-utils` on Ubuntu).

```sh
python -m pip install -r build/python-requirement-lists/site-pkgs.txt
./configure --targets MATH1853-Assignment-I.1 COMP1110-Project
make -j2 site
python -m http.server --directory dist/site 8000
```

Omit `--targets` to build the entire catalogue. `make site` compiles the selected
targets, generates previews, stages Markdown/navigation under `.build/site`, and
writes the website to `dist/site`. It does not edit `site/docs` or `site/mkdocs.yml`.
Use `--site-url=https://example.org/notes/` for a different canonical URL. Local
preview and download links resolve within the generated site.

The entire catalogue includes `COMP2113-Project`, an Ubuntu 24.04 x86_64 binary ZIP.
On other systems, use the build container described below or pass an existing ZIP
through `--artifact-dir`. The tool will not silently omit the target or mislabel a
native build. External Git sources require network access on their first build;
the revision-pinned source cache is reused afterward. No build reads artifacts from
the production website, uses GitHub Actions APIs, or needs deployment credentials.

## Optional Ubuntu build container

This provides the environment for the entire catalogue, including the Ubuntu x86_64
ZIP, on a machine with Docker and amd64 container support:

```sh
docker build --platform linux/amd64 --build-arg BUILD_UID="$(id -u)" \
  -f build/Dockerfile -t hku-notes-build .
docker run --rm --platform linux/amd64 \
  -v "$PWD:/workspace" hku-notes-build
```

The default command runs `./configure && make site`. It overwrites a previously
generated root configuration with container paths. Rerun configure when returning
to native builds. For one document:

```sh
docker run --rm --platform linux/amd64 \
  -v "$PWD:/workspace" -w /workspace/src/CV hku-notes-build \
  sh -c '../../configure && make'
```

CI and the container use MiKTeX with automatic installation of missing TeX packages.
`build/bootstrap-ubuntu.sh` installs MiKTeX and system tools; run
`build/setup-miktex.sh` as the compiling user to initialize its writable package tree.
Add `$HOME/bin` to PATH afterward. Only the build CLI tools and a small compatibility
set are installed ahead of time; document packages are downloaded as needed.
This follows [MiKTeX's installation instructions](https://miktex.org/download).

CI builds canonical targets in parallel with a GitHub Actions matrix. Each job has
its own writable MiKTeX tree and target-specific package/artifact caches; unchanged
sources restore verified outputs and previews. Aliases share their canonical build.
A separate job collects the artifacts and assembles the website without compiling
again. `targets/<name>/<description>` branches select just that target (and its
canonical target if it is an alias).

The container defaults to serial document builds so cold builds do not install
packages concurrently into the same tree. Local `make -j` is available when the
required packages are already installed. The shared build runner remains compatible
with either MiKTeX or TeX Live.

The container runs as `builder`; the build argument above matches its UID to the
host. Do not override it with an arbitrary `docker run --user`, because MiKTeX needs
access to that user's initialized package/configuration directories.

## CI and deployment

GitHub Actions calls the same configure, Make, and test commands, then uploads `dist/`.
PRs build a reviewable site without publishing it. Only pushes to `master` deploy.
`targets/<target>/<description>` branches build that target and its alias destination.
`@nobuild` remains available for push commits. CI caches compiled artifacts and
previews, then compares each target's source fingerprint before reusing them.
`@force-rebuild` in a push commit bypasses these caches. Locally, use `make FORCE=1`.
The pipeline never queries the deployed website for checksums.

Configure `build.hash_ignore` with gitignore-style patterns to exclude scratch files
or other non-build inputs. Metadata is always hashed, even if a pattern matches it;
editing ignore rules or build settings therefore invalidates the cache. Declared
outputs and build caches are excluded automatically. See the v3 reference for details.

Indexing runs as a separate post-deployment CI job; local builds never send
notifications. To invoke it explicitly elsewhere, install
`build/python-requirement-lists/indexing-pkgs.txt` and run `build/request_indexing.py`
with its documented arguments if needed.
