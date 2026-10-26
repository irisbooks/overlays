#!/usr/bin/env bash
# Download the signed iris release pinned in .github/engine.txt for
# linux/amd64 and verify it the way https://irisbooks.io/install.sh does —
# except that the minisign check is mandatory here. Puts `iris` on the job's
# PATH. A pin, not releases/latest: a new engine release must not change the
# result of an unchanged package commit.
set -euo pipefail

# IrisBooks release public key (minisign), key id 11D9CC26444B9F65.
PUBKEY="RWRln0tEJszZEcTL7VcSL5XR+zcAA2FyqnfOAeLDnwaE7LAa7E3tJCCJ"
ASSET="iris_linux_amd64"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="$(python3 "$SCRIPT_DIR/check-engine.py" --version)"
BASE="https://github.com/irisbooks/iris/releases/download/$VERSION"

dir="${RUNNER_TEMP:?}/iris"
mkdir -p "$dir"
cd "$dir"
# A source tag or a draft is not a released engine, even if its name is stable.
curl -fsSL --retry 3 -H 'Accept: application/vnd.github+json' \
  -o release-state.json "https://api.github.com/repos/irisbooks/iris/releases/tags/$VERSION" \
  || { echo "::error::publish stable engine $VERSION before depending on it in an Overlay"; exit 1; }
python3 "$SCRIPT_DIR/check-engine.py" --release release-state.json
for f in "$ASSET" checksums.txt checksums.txt.minisig version.txt; do
  curl -fsSL --retry 3 -o "$f" "$BASE/$f"
done
minisign -Vm checksums.txt -P "$PUBKEY"
grep " $ASSET\$" checksums.txt | sha256sum -c -
grep " version.txt\$" checksums.txt | sha256sum -c -
[ "$(cat version.txt)" = "$VERSION" ] || { echo "::error::downloaded engine is $(cat version.txt), pinned $VERSION"; exit 1; }
chmod +x "$ASSET"
mv "$ASSET" iris
[ "$(./iris version)" = "iris $VERSION" ] || { echo "::error::engine binary does not report $VERSION"; exit 1; }
echo "$dir" >>"$GITHUB_PATH"
echo "iris $VERSION verified"
