#!/bin/bash
# Harvest Google autocomplete suggestions for app-demand phrasings
out=demand_raw.txt; : > $out
prefixes=("is there an app that" "is there an app for" "app that lets me" "i wish there was an app" "app to help me" "best app for" "app that tracks" "app that reminds me" "why is there no app" "need an app that")
for p in "${prefixes[@]}"; do
  for l in "" a b c d e f g h i j k l m n o p q r s t u v w x y z; do
    q="$p $l"
    curl -s --max-time 8 "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")" \
      | python3 -c "import sys,json
try:
  d=json.load(sys.stdin)
  for s in d[1]: print(s)
except Exception: pass" >> $out
    sleep 0.15
  done
done
sort -u $out > demand.txt
wc -l demand.txt
