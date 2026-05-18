#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: bash pdftopng.sh <folder-with-pdfs>"
  exit 1
fi

pagesDir=$(mktemp -d '/tmp/temp.XXXXX')

find "$1" -type f -iname "*.pdf" | while IFS= read -r pdf; do
  rel="${pdf#$1/}"
  name="${rel%.pdf}"

  safe_name=$(echo "$name" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's#[ /]#_#g' \
    | sed 's/[^a-z0-9_-]/_/g' \
    | sed 's/_\+/_/g' \
    | sed 's/^_//;s/_$//')

  mkdir -p "$pagesDir/$safe_name"

  pdftoppm -png -r 200 "$pdf" "$pagesDir/$safe_name/page"
done

idx=2

while [ -d pages"$idx" ]; do
  idx=$((idx+1))
done

mv "$pagesDir" "pages$idx"

echo "Created pages$idx"
