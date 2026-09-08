#!/bin/sh
# Optional system provisioning for Ubuntu 24.04, shared by CI and the build image.
# Run as root; configure itself never installs system packages.
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates git make cmake g++ python3 python3-venv \
    latexmk texlive-latex-extra texlive-fonts-extra texlive-science \
    texlive-bibtex-extra texlive-xetex texlive-luatex \
    texlive-lang-chinese texlive-lang-french biber poppler-utils
