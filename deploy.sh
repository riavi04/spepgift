#!/bin/sh
# Rebuild and publish soundbird. Safe to run repeatedly.
set -e
cd "$(dirname "$0")"
python3 src/build.py dist/sound-bird.html >/dev/null
git add -A
if git diff --cached --quiet; then
  echo "nothing changed"
else
  git commit -q -m "${1:-Update soundbird}"
fi
git push -q origin main
echo "pushed. live shortly at https://riavi04.github.io/soundbird/"
