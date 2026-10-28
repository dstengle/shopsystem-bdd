#!/bin/bash
for i in $(seq 1 100); do
  [ -f .shop/scratch/3-integrate/drafts/round-1/writer.reply.md ] && exit 0
  sleep 5
done
exit 1
