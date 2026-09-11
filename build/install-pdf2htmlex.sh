#!/bin/sh
# Optional native converter for Ubuntu x86_64, including the full build image.
# Extract the upstream AppImage so FUSE and a nested Docker daemon are unnecessary.
set -eu
[ "$(uname -m)" = x86_64 ] || { echo 'Native installer requires x86_64; use the Docker backend on other hosts.' >&2; exit 1; }
apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 update
DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 install -y --no-install-recommends \
    ca-certificates curl libfontconfig1 libfreetype6 libglib2.0-0t64 libx11-6 libxcb1
install_root=${1:-/opt/pdf2htmlex}
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT HUP INT TERM
curl --fail --location --retry 3 --connect-timeout 30 --max-time 300 \
  https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-focal-x86_64.AppImage \
  -o "$work_dir/converter.AppImage"
echo "11de2583a3abce5f141fd7fafb1fea2c67b15886e546d6b7675c600012e6ab8c  $work_dir/converter.AppImage" | sha256sum --check
chmod +x "$work_dir/converter.AppImage"
(cd "$work_dir" && ./converter.AppImage --appimage-extract >/dev/null)
mkdir -p "$install_root"
cp -a "$work_dir/squashfs-root/." "$install_root/"
printf '#!/bin/sh\nexec "%s/AppRun" --data-dir "%s/usr/local/share/pdf2htmlEX" "$@"\n' "$install_root" "$install_root" > /usr/local/bin/pdf2htmlEX
chmod +x /usr/local/bin/pdf2htmlEX
pdf2htmlEX --version
