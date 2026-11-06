#!/bin/bash

sorted_files=$(printf '%s\n' "$@" | sort)

first_file=$(echo "$sorted_files" | head -1)
head -1 "$first_file" > final.csv

echo "$sorted_files" | while IFS= read -r f; do
    tail -n +2 "$f" >> final.csv
done
rm "$@"