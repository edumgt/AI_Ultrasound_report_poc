#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ ! -f ".venv-linux/bin/activate" ]; then
  echo "[ERROR] .venv-linux not found. Run: bash scripts/setup_wsl_venv.sh"
  exit 1
fi

source .venv-linux/bin/activate
python web_django/manage.py migrate
exec python web_django/manage.py runserver 0.0.0.0:8000
