#!/bin/bash
# Backs up ~/cafe into ~/backups as a dated .tar.gz file, keeping the newest 7 backups.
set -euo pipefail

SOURCE="$HOME/cafe"
DEST="$HOME/backups"
STAMP=$(date +%Y-%m-%d_%H%M%S)

mkdir -p "$DEST"
tar -czf "$DEST/cafe-$STAMP.tar.gz" -C "$HOME" cafe
echo "Backed up $SOURCE to $DEST/cafe-$STAMP.tar.gz"

# keep the newest 7 backups, delete older ones
ls -1t "$DEST"/cafe-*.tar.gz | tail -n +8 | xargs -r rm --
echo "Backups kept: $(ls -1 "$DEST"/cafe-*.tar.gz | wc -l)"
