#!/bin/bash
f=/home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-1/writer.reply.md
for i in $(seq 1 100); do
  if [ -f "$f" ]; then echo found; exit 0; fi
  sleep 5
done
echo timeout
