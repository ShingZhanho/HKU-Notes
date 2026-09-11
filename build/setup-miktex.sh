#!/bin/sh
# Initialize the compiling user's writable MiKTeX installation (no sudo).
# Package installation remains on-the-fly; install only the CLI tools checked by
# configure and the small compatibility set used by the previous pipeline.
set -eu
# Retry individual operations so a failed download preserves completed installs.
retry() {
    attempt=1
    while :; do
        if "$@"; then return 0; else status=$?; fi
        if [ "$attempt" -ge 3 ]; then return "$status"; fi
        echo "Retrying MiKTeX operation ($attempt/3): $*" >&2
        sleep "$((attempt * 5))"
        attempt=$((attempt + 1))
    done
}
export PATH="$HOME/bin:$PATH"
retry miktexsetup finish
initexmf --set-config-value '[MPM]AutoInstall=1'
retry miktex packages update-package-database
retry miktex packages update
# MiKTeX install is not idempotent: warm caches report "already installed" as
# an error. Recheck state on every attempt, including after a partial install.
ensure_package() {
    installed=$(miktex packages info --template='{isInstalled}' "$1") || return $?
    case "$installed" in
        true|1) echo "Already installed: $1" ;;
        false|0) miktex packages install "$1" ;;
        *) echo "Unexpected MiKTeX installation state for $1: $installed" >&2; return 1 ;;
    esac
}
# Restore the original contingency installs individually. The legacy mpm comma
# list reported "requested package is unknown" in CI without failing setup.
for package in latexmk texcount xkeyval kvsetkeys iftex kvoptions; do
    retry ensure_package "$package"
done
retry initexmf --enable-installer --update-fndb
retry initexmf --enable-installer --mkmaps

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
