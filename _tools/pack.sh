#!/bin/bash
# Usage: pack.sh <out.zip> <top-folder-name> <item>...  — zips items inside a top folder, using a fresh temp dir.
set -e
OUT=$(readlink -f "$1"); NAME=$2; shift 2
T=$(mktemp -d /tmp/claude-0/-home-claude/e5ba8f83-0f94-590d-b463-a91e18d3fbed/scratchpad/pack.XXXXXX)
mkdir "$T/$NAME"; cp -r "$@" "$T/$NAME/"
find "$T" -name node_modules -prune -o -name '.DS_Store' -print | xargs -r rm -f
cd "$T" && rm -f "$OUT" && zip -rqX "$OUT" "$NAME"
echo "$(basename "$OUT") $(du -k "$OUT" | cut -f1)K"
