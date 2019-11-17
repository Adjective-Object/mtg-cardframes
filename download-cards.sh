#!/usr/bin/env bash

if [[ "$#" != "1" ]]; then
    echo "usage: $0 <path/to/cards/json/list>"
    exit 1
fi

QUERY_NAME=${1%.json}
mkdir -p "$QUERY_NAME"

LINES=$(cat $1 | jq '.[]|select(.image_uris.png != null)|.image_uris.png + ";" +( .name | sub( "[, '"'"'/]+" ; "-"; "g") ) + ".png"')


echo "$LINES"

for IMAGE_LINE in $LINES; do
    # echo "line: " $IMAGE_LINE
    NOQUOTES=`echo "$IMAGE_LINE" | sed s/\"//g`
    URL=`echo $NOQUOTES | cut -d ';' -f 1`
    FNAME=`echo $NOQUOTES | cut -d ';' -f 2`


    echo "IMAGE_LINE: '$IMAGE_LINE'"
    echo "'$NOQUOTES'" "'$URL'" "'$FNAME'"


    set -ex
    curl "$URL" > "$QUERY_NAME/$FNAME"
    set +ex
    sleep 0.5
done