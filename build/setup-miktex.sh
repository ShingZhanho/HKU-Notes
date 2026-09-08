#!/bin/sh
# Initialize the compiling user's writable MiKTeX installation (no sudo).
# Package installation remains on-the-fly; install only the CLI tools checked by
# configure and the small compatibility set used by the previous pipeline.
set -eu
export PATH="$HOME/bin:$PATH"
miktexsetup finish
initexmf --set-config-value '[MPM]AutoInstall=1'
mpm --update-db
mpm --install=latexmk,texcount,xkeyval,kvsetkeys,iftex,kvoptions
initexmf --update-fndb
initexmf --mkmaps
