cat > .devcontainer/postCreate.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  build-essential cmake pkg-config \
  curl ca-certificates git \
  ncurses-bin libtinfo6 libncursesw6

# 備援：若 clear 不存在，提供最小替代
if ! command -v clear >/dev/null 2>&1; then
  echo 'alias clear='\''printf "\033c"'\''' | sudo tee -a /etc/bash.bashrc
fi

# 安裝 xlings（含 xim / d2x）
if ! command -v xlings >/dev/null 2>&1; then
  curl -fsSL https://d2learn.org/xlings-install.sh | bash
fi

echo "Post-create steps finished."
EOF
chmod +x .devcontainer/postCreate.sh
