#!/bin/sh

falderal doc/*.md || exit 1
for F in eg/*.eqthy; do
  echo $F
  ./bin/eqthy $F || exit 1
done
