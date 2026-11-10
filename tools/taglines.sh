#!/bin/sh
# tools/taglines.sh "Uncanny" "Wondrous" ... — preview the page with each first word of the tagline.
# Takes a screenshot of index.html at desktop size for each word (animations paused, so the text is
# steady) into tools/out/, then opens them all in Preview to flip through. Needs Google Chrome.
# For a whole new first line, pass the full phrase, e.g. "Golden-age machinery".
set -e
cd "$(dirname "$0")/.."
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=tools/out; rm -rf "$OUT"; mkdir -p "$OUT"
i=0
for t in "$@"; do
  i=$((i+1)); f="$OUT/$i.html"
  case "$t" in
    *" "*) sed "s|<span><span class=\"word\">Curious</span> inventions.</span>|<span>$t.</span>|" index.html ;;
    *)     sed "s|<span class=\"word\">Curious</span>|<span class=\"word\">$t</span>|" index.html ;;
  esac | sed -e 's|</style>|*{animation:none!important}</style>|' -e 's|<script>|<script>/*|' -e 's|</script>|*/</script>|' \
       -e 's|"assets/|"../../assets/|g' > "$f"
  "$CH" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,900 --virtual-time-budget=4000 \
        --screenshot="$PWD/$OUT/$i.png" "file://$PWD/$f" 2>/dev/null
  echo "$OUT/$i.png  $t"
done
open -a Preview "$OUT"/*.png
