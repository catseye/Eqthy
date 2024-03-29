#!/bin/sh

falderal doc/*.md || exit 1
for F in eg/*.eqthy.md; do
  echo "./bin/eqthy $F"
  ./bin/eqthy $F || exit 1
done
for F in eg/incorrect/*.eqthy.md; do
  echo $F
  ./bin/eqthy $F 2>&1 >/dev/null
  R=$?
  [ $R -eq 0 ] && echo "fail" && exit 1
done
exit 0
