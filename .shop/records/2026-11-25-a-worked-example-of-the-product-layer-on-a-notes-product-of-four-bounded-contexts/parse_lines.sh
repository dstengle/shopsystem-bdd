#!/bin/bash
# usage: parse_lines.sh <context dir> <file of lines> : each line parsed in the context, OK or FAIL with the refusal
cd "$1" || exit 1
while IFS= read -r l; do
  [ -z "$l" ] && continue
  out=$(python3 /home/vscode/shopsystem-bdd/scripts/spec parse "$l" 2>&1)
  if [ $? -eq 0 ]; then echo "OK   $l"; else echo "FAIL $l"; echo "$out" | sed 's/^/     | /' | head -8; fi
done < "$2"
