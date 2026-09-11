#!/bin/sh
# Initialize the compiling user's writable MiKTeX installation (no sudo).
# Package installation remains on-the-fly; install only the CLI tools checked by
# configure and the small compatibility set used by the previous pipeline.
set -eu
export PATH="$HOME/bin:$PATH"
miktexsetup finish
initexmf --set-config-value '[MPM]AutoInstall=1'
miktex packages update-package-database
miktex packages update
# Restore the original contingency installs individually. The legacy mpm comma
# list reported "requested package is unknown" in CI without failing setup.
for package in latexmk texcount xkeyval kvsetkeys iftex kvoptions simpleicons; do
    miktex packages install "$package"
done
# Install SimpleIcons before generating maps: installing it on demand during
# pdfLaTeX can leave the new Type 1 font absent from the active pdftex.map.
initexmf --update-fndb
initexmf --mkmaps

# Do not trust the installer exit status alone: MiKTeX has reported success even
# when a requested package was not installed. Check actual TeX file resolution.
for package in xkeyval kvsetkeys iftex kvoptions; do
    sty_path=$(kpsewhich "$package.sty") || sty_path=
    if [ -z "$sty_path" ] || [ ! -f "$sty_path" ]; then
        echo "MiKTeX setup failed: $package.sty is still missing after explicit installation and filename database refresh." >&2
        exit 1
    fi
    echo "Verified $package.sty: $sty_path"
done

for font_file in simpleicons.map SimpleIcons.pfb; do
    font_path=$(kpsewhich "$font_file") || font_path=
    if [ -z "$font_path" ] || [ ! -f "$font_path" ]; then
        echo "MiKTeX setup failed: $font_file is missing after installing simpleicons." >&2
        exit 1
    fi
done
pdftex_map=$(kpsewhich pdftex.map) || pdftex_map=
if [ -z "$pdftex_map" ] || [ ! -f "$pdftex_map" ] || ! grep -q '^SimpleIcons--simpleiconstwo ' "$pdftex_map"; then
    echo "MiKTeX setup failed: SimpleIcons is missing from the active pdftex.map after refreshing font maps." >&2
    exit 1
fi
echo "Verified SimpleIcons Type 1 font and active pdfTeX mapping."
