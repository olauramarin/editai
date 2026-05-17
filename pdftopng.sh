#!/bin/bash

mkdir -p pages3

find "editoriale org2" -type f -iname "*.pdf" | while IFS= read -r pdf; do
  rel="${pdf#editoriale org2/}"
  name="${rel%.pdf}"

  safe_name=$(echo "$name" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's#[ /]#_#g' \
    | sed 's/[^a-z0-9_-]/_/g' \
    | sed 's/_\+/_/g' \
    | sed 's/^_//;s/_$//')

  mkdir -p "pages3/$safe_name"

  pdftoppm -png -r 200 "$pdf" "pages3/$safe_name/page"
done