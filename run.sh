#!/usr/bin/env bash
# Lance backend (Django, port 8000) + frontend (React/Vite, port 5173). Utilisable depuis Git Bash.
set -e
cd "$(dirname "$0")"
for c in python python3 py; do $c --version >/dev/null 2>&1 && PY=$c && break; done
[ -z "$PY" ] && { echo "Python introuvable. Installez Python 3.10+"; exit 1; }
command -v npm >/dev/null || { echo "Node.js/npm introuvable. Installez Node 18+"; exit 1; }
cd backend
[ -d .venv ] || $PY -m venv .venv
if [ -f .venv/Scripts/activate ]; then source .venv/Scripts/activate; else source .venv/bin/activate; fi
pip install -q -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed
python manage.py runserver 8000 &
BACK=$!
trap 'kill $BACK 2>/dev/null' EXIT
cd ../frontend
[ -d node_modules ] || npm install
echo ">>> Dashboard : http://localhost:5173  (Ctrl+C pour arrêter)"
npm run dev -- --open
