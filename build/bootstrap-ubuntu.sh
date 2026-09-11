#!/bin/sh
# System provisioning for Ubuntu 24.04, shared by CI and the build image.
# Run as root, then run setup-miktex.sh as the user who will compile documents.
set -eu
apt-get -o Acquire::Retries=3 -o Acquire::https::Timeout=30 -o APT::Update::Error-Mode=any update
DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::Retries=3 -o Acquire::https::Timeout=30 install -y --no-install-recommends \
    ca-certificates curl gnupg git make cmake g++ python3 python3-venv \
    perl ghostscript poppler-utils

# Use MiKTeX's signed Noble repository, not Ubuntu's TeX Live packages.
key_file=$(mktemp)
trap 'rm -f "$key_file"' EXIT HUP INT TERM
curl --retry 3 --retry-all-errors --retry-delay 5 --connect-timeout 30 --max-time 180 -fsSL https://miktex.org/download/key -o "$key_file"
gpg --batch --yes --dearmor -o /usr/share/keyrings/miktex.gpg "$key_file"
# Keep signature verification with the same MiKTeX key on either endpoint.
# APT retries can keep following the redirector to the same unreachable mirror.
miktex_sources=${MIKTEX_APT_SOURCES:-/etc/apt/sources.list.d/miktex.list}
for repository in https://miktex.org/download/ubuntu https://mirrors.mit.edu/CTAN/systems/win32/miktex/setup/deb; do
    echo "Trying MiKTeX APT repository: $repository"
    echo "deb [signed-by=/usr/share/keyrings/miktex.gpg] $repository noble universe" > "$miktex_sources"
    if apt-get -o Acquire::Retries=3 -o Acquire::https::Timeout=30 -o APT::Update::Error-Mode=any update &&
       DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::Retries=3 -o Acquire::https::Timeout=30 install -y --no-install-recommends miktex; then
        exit 0
    fi
    echo "MiKTeX repository failed: $repository" >&2
done
echo "Unable to install MiKTeX from either signed repository." >&2
exit 1
