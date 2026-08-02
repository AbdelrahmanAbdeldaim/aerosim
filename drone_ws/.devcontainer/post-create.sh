#!/usr/bin/env bash
# Runs once when the dev container is created.
set -euo pipefail

WS=/drone_ws

# Resolve declared package dependencies. `-r` keeps going when a package
# declares something unavailable rather than aborting the whole container setup.
sudo apt-get update
rosdep update
rosdep install --from-paths "${WS}/src" --ignore-src -y -r || true

cat <<'EOF'

Dev container ready. The workspace is /drone_ws.

EOF
