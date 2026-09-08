#!/bin/sh
# System provisioning for Ubuntu 24.04, shared by CI and the build image.
# Run as root, then run setup-miktex.sh as the user who will compile documents.
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg git make cmake g++ python3 python3-venv \
    perl ghostscript poppler-utils

# Use MiKTeX's signed Noble repository, not Ubuntu's TeX Live packages.
key_file=$(mktemp)
trap 'rm -f "$key_file"' EXIT HUP INT TERM
curl -fsSL https://miktex.org/download/key -o "$key_file"
gpg --batch --yes --dearmor -o /usr/share/keyrings/miktex.gpg "$key_file"
cat > /etc/apt/sources.list.d/miktex.list <<'EOF'
deb [signed-by=/usr/share/keyrings/miktex.gpg] https://miktex.org/download/ubuntu noble universe
EOF
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends miktex
