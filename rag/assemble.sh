#!/bin/bash
# Builds handbook-assistant/step-1-load … step-6-web from the step folders s1…s6.
# Each step has everything from the steps before it, plus its own files. Every step gets a real copy of docs/.
set -e
cd "$(dirname "$0")"
rm -rf handbook-assistant && mkdir handbook-assistant
names=(step-1-load step-2-chunk step-3-index step-4-hybrid step-5-answers step-6-web)
prev=""
for i in 1 2 3 4 5 6; do
  out=handbook-assistant/${names[$((i-1))]}
  mkdir -p "$out"
  [ -n "$prev" ] && cp -r "$prev"/. "$out"/
  (cd s$i && tar --exclude=docs --exclude=chroma_db --exclude=__pycache__ --exclude=.pytest_cache -cf - .) | tar -xf - -C "$out"
  rm -rf "$out/docs" && cp -r docs "$out/docs"
  prev=$out
done
mkdir -p handbook-assistant/make-docs
cp src/make_docs.py src/docs_content.py src/README.txt handbook-assistant/make-docs/
cp README.txt handbook-assistant/README.txt
find handbook-assistant -name README.txt -path '*/step-*' -newer /dev/null >/dev/null
echo "Built $(find handbook-assistant -type f | wc -l) files"
