# HKU Notes

HKU Notes is my personal revision resources management project for the courses I took
at The University of Hong Kong in pursuit of my Bachelor of Engineering (Computer Science)
degree.

All resources are written in LaTeX. The purpose of this repository is to store the notes
remotely and use GitHub Actions to automatically compile and distribute the notes online.

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
