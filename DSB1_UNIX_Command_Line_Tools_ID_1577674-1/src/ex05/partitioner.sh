#!/bin/sh
set -eu
input="${1:-../ex03/hh_positions.csv}"
awk -F, '
NR == 1 { header = $0; next }
{
    date = $2
    gsub(/"/, "", date)
    sub(/T.*/, "", date)
    file = date ".csv"
    if (!(file in seen)) { print header > file; seen[file] = 1 }
    print $0 >> file
}
' "$input"
