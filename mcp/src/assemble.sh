#!/bin/bash
# Builds cafe-mcp/step-1-hello … step-6-final from src/s1…s6. Each step has everything from the steps before it.
# The handbook folder gets a real copy of the RAG course's documents (../rag/docs).
set -e
cd "$(dirname "$0")/.."
rm -rf cafe-mcp && mkdir cafe-mcp
names=(step-1-hello step-2-tools step-3-resources step-4-agents step-5-http step-6-final)
prev=""
for i in 1 2 3 4 5 6; do
  out=cafe-mcp/${names[$((i-1))]}
  mkdir -p "$out"
  [ -n "$prev" ] && cp -r "$prev"/. "$out"/
  (cd src/s$i && tar --exclude=chroma_db --exclude=docs --exclude=__pycache__ --exclude=.pytest_cache \
     --exclude=bookings.db -cf - .) | tar -xf - -C "$out"
  if [ -d "$out/handbook" ]; then rm -rf "$out/handbook/docs"; cp -r ../rag/docs "$out/handbook/docs"; fi
  prev=$out
done
cp src/README.txt cafe-mcp/README.txt
echo "Built $(find cafe-mcp -type f | wc -l) files"
