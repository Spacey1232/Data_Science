#!/bin/sh

input="../ex03/hh_positions.csv"
header=$(head -1 "$input")

tail -n +2 "$input" | while IFS= read -r line; do

    date=$(echo "$line" | cut -d',' -f2 | cut -d'T' -f1 | tr -d '"')
    filename="${date}.csv"

    if [ ! -f "$filename" ]; then
        echo "$header" > "$filename"
    fi

    echo "$line" >> "$filename"

done