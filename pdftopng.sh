mkdir -p pages2

find "editoriale org" -type f -iname "*.pdf" | while IFS= read -r pdf; do
  rel="${pdf#editoriale org/}"
  name="${rel%.pdf}"

  safe_name=$(echo "$name" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's#[ /]#_#g' \
    | sed 's/[^a-z0-9_-]/_/g' \
    | sed 's/_\+/_/g' \
    | sed 's/^_//;s/_$//')

  mkdir -p "pages2/$safe_name"

  pdftoppm -png -r 200 "$pdf" "pages2/$safe_name/page"
done