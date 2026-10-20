# HKU Notes

Personal notes, cheatsheets, and project resources for courses at The University
of Hong Kong.

**[Browse and download materials](https://hku.jacobshing.com/)**

## Build a document

Requires Python 3.11+, GNU Make, and MiKTeX or TeX Live with `latexmk`.
Use Linux, macOS, or Windows through WSL. Run from the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r build/python-requirement-lists/general-pkgs.txt
cd src/MATH1853-Assignment-I.1
../../configure
make
```

The PDF appears in the document directory. `configure` checks dependencies but
never installs them. For minted documents, also install
`build/python-requirement-lists/python-minted-pkgs.txt` from the repository root.

To build several documents, run `./configure --targets CV COMP2120-Notes` at the
repository root, then `make`. Omit `--targets` to select the full catalogue.

## Build the website

Install Poppler and either native `pdf2htmlEX` or a running Docker-compatible
engine for HTML previews. From the repository root, with the virtual environment active:

```sh
python -m pip install -r build/python-requirement-lists/site-pkgs.txt
./configure --targets CV COMP2120-Notes
make site
python -m http.server --directory dist/site 8000
```

Open [localhost:8000](http://localhost:8000). The generated site is in `dist/site`.
Local builds need no GitHub Actions access or deployment credentials.

The full catalogue includes an Ubuntu 24.04 x86_64 project artifact. To build
it and the entire website, use Docker with amd64 support:

```sh
docker build --platform linux/amd64 --build-arg BUILD_UID="$(id -u)" \
  -f build/Dockerfile -t hku-notes-build .
docker run --rm --platform linux/amd64 -v "$PWD:/workspace" hku-notes-build
```

The container uses MiKTeX with on-demand package installation. Rerun `configure`
after switching between container and native builds.

## Everyday commands

- `make`: build selected documents; verified unchanged outputs are reused.
- `make preview`: build documents and generate cached HTML previews.
- `make site`: build documents, previews, and the website.
- `make FORCE=1`: force document rebuilding.
- `make clean`: remove intermediate files.
- `make distclean`: also remove generated outputs, caches, and configuration.
- `python build/build.py validate`: validate document metadata.

## Contribute

See the [contribution guide](site/docs/contribution/index.md) and
[metadata v3 reference](site/docs/contribution/syntax-reference/metadata.json/v3.md).
Only v3 is supported. `build.hash_ignore` accepts gitignore-style patterns;
`metadata.json` is always hashed.

CI builds documents in parallel and deploys pushes to `master`. Unchanged
artifacts skip compiler setup. Use `@force-rebuild` in a commit message to force
rebuilding, or `@nobuild` to skip a push build.
