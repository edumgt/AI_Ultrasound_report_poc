#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 not found. Install python3 first."
  exit 1
fi

if [ ! -d ".venv-linux" ]; then
  echo "[INFO] Creating virtual environment: .venv-linux"
  python3 -m venv .venv-linux
else
  echo "[INFO] Virtual environment already exists: .venv-linux"
fi

source .venv-linux/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "[DONE] WSL Ubuntu venv setup complete."
echo "[NEXT] source .venv-linux/bin/activate"
echo "[NEXT] python web_django/manage.py migrate"
echo "[NEXT] python web_django/manage.py runserver 0.0.0.0:8000"
