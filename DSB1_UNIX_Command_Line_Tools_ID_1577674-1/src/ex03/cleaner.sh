#!/bin/sh
head -1 ../ex02/hh_sorted.csv > hh_positions.csv
tail -n +2 ../ex02/hh_sorted.csv | while IFS= read -r line; do
   id_and_date=$(echo "$line" | sed -E 's/^("[^"]*","[^"]*"),"(.*)",(true|false),(.*)$/\1/')
   name=$(echo "$line" | sed -E 's/^("[^"]*","[^"]*"),"(.*)",(true|false),(.*)$/\2/')
   rest=$(echo "$line" | sed -E 's/^("[^"]*","[^"]*"),"(.*)",(true|false),(.*)$/\3,\4/')
   position=$(echo "$name" | grep -oE "Junior|Middle|Senior" | paste -sd/ -)
   if [ -z "$position" ]; then
        position="-"
   fi
   echo "${id_and_date},\"${position}\",${rest}"
done >> hh_positions.csv

