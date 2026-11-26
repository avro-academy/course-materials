#!/bin/bash
# Usage: stage.sh file... — copies files into avrosphere tmp-course-upload, commits and pushes; prints sha256.
set -e
R=/home/claude/avrosphere
mkdir -p $R/tmp-course-upload
ABS=(); for f in "$@"; do ABS+=("$(readlink -f "$f")"); done; cp "$@" $R/tmp-course-upload/
cd $R && git add tmp-course-upload && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Temporary: course files for upload (to be removed)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Qd7TXnyw2q2QvM7bq4p9pi" && git push -q origin claude/project-thread-a422he 2>&1 | grep -v "^remote:" || true
for f in "${ABS[@]}"; do echo "$(basename "$f") $(sha256sum "$f" | cut -c1-64)"; done
