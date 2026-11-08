#!/bin/sh
set -eu
if [ "$#" -eq 0 ]; then
    printf 'Usage: %s date.csv [date.csv ...]\n' "$0" >&2
    exit 1
fi
# Input partitions are retained for reproducibility.
printf '%s\n' "$@" | sort | while IFS= read -r file; do
    if [ "$file" = "final.csv" ]; then
        printf 'final.csv cannot be an input\n' >&2
        exit 1
    fi
    if [ "${first:-yes}" = yes ]; then
        head -n 1 "$file"
        first=no
    fi
    tail -n +2 "$file"
done > final.csv
