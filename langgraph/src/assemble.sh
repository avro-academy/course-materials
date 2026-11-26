#!/bin/sh
# Build cafe-helper-2/step-* from the overlays: each step is the step before plus its own files.
set -e
cd "$(dirname "$0")"
out=../cafe-helper-2
rm -rf "$out"; mkdir -p "$out"
prev=""
for pair in s1:step-1-graphs s2:step-2-model s3:step-3-tools s4:step-4-memory s5:step-5-approval s6:step-6-web; do
  src=${pair%%:*}; dst=$out/${pair#*:}
  if [ -n "$prev" ]; then cp -r "$prev" "$dst"; else mkdir -p "$dst"; fi
  cp -r "$src"/. "$dst"/
  prev=$dst
done
find "$out" \( -name __pycache__ -o -name .pytest_cache -o -name '*.db' \) -prune -exec rm -rf {} +
cp README.txt "$out"/README.txt 2>/dev/null || true
