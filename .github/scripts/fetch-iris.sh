#!/usr/bin/env bash
# Download the latest signed iris release for linux/amd64 and verify it the
# way https://irisbooks.jp/install.sh does — except that the minisign check is
# mandatory here. Puts `iris` on the job's PATH.
set -euo pipefail

# IrisBooks release public key (minisign), key id 11D9CC26444B9F65.
PUBKEY="RWRln0tEJszZEcTL7VcSL5XR+zcAA2FyqnfOAeLDnwaE7LAa7E3tJCCJ"
BASE="https://github.com/irisbooks/iris/releases/latest/download"
ASSET="iris_linux_amd64"

dir="${RUNNER_TEMP:?}/iris"
mkdir -p "$dir"
cd "$dir"
for f in "$ASSET" checksums.txt checksums.txt.minisig version.txt; do
  curl -fsSL --retry 3 -o "$f" "$BASE/$f"
done
minisign -Vm checksums.txt -P "$PUBKEY"
grep " $ASSET\$" checksums.txt | sha256sum -c -
chmod +x "$ASSET"
mv "$ASSET" iris
echo "$dir" >>"$GITHUB_PATH"
echo "iris $(cat version.txt) verified"
