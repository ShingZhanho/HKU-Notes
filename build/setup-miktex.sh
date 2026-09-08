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
for package in latexmk texcount xkeyval kvsetkeys iftex kvoptions; do
    miktex packages install "$package"
done
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
