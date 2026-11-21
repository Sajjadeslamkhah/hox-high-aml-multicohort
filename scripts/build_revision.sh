#!/usr/bin/env bash
# Rebuild the tracked-change revision from the submitted manuscript.
# Usage: bash scripts/build_revision.sh <submitted.docx> <out.docx>
set -euo pipefail
SRC=$(realpath "$1"); OUT=$(realpath -m "$2"); HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(dirname "$HERE")
SK=/root/.claude/skills/synced/b3f9ed0e-0069-4358-9404-5d0a37baea67_de29ebf9-2f95-4f87-a4f3-6da821d3b8a5/docx/scripts
W=$(mktemp -d); python3 -I -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$SRC" "$W"
python3 "$SK/merge_runs.py" "$W" >/dev/null
python3 -I "$HERE/track_edit.py" "$W/word/document.xml" "$HERE/depmap_edits.json" "Sajjad Eslamkhah" 2026-11-21T12:00:00Z >/dev/null
python3 -I "$HERE/revise_manuscript.py" "$W/word/document.xml"
[ -f "$HERE/revise_manuscript_B.py" ] && python3 -I "$HERE/revise_manuscript_B.py" "$W/word/document.xml"
python3 -I "$HERE/swap_image.py" "$W" rId9 "$REPO/figures/manuscript/Figure1.png"
python3 -I "$HERE/swap_image.py" "$W" rId14 "$REPO/figures/manuscript/Figure6.png"
[ -f "$REPO/figures/manuscript/Figure5.png" ] && python3 -I "$HERE/swap_image.py" "$W" rId13 "$REPO/figures/manuscript/Figure5.png"
rm -f "$OUT"; (cd "$W" && zip -XrDyq "$OUT" .)
python3 "$SK/office/validate.py" "$OUT" --original "$SRC" --author "Sajjad Eslamkhah" | tail -2
