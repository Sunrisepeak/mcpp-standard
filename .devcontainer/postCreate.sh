# postCreate.sh
#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y ncurses-bin libtinfo6 libncursesw6 curl ca-certificates git

if ! command -v xlings >/dev/null 2>&1; then
  curl -fsSL https://d2learn.org/xlings-install.sh | bash
fi

echo "Post-create steps finished."
