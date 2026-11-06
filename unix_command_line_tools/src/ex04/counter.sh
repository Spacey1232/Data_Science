echo '"name","count"' > hh_uniq_positions.csv
cut -d',' -f3 ../ex03/hh_position.csv | sort | uniq -c | sort -rn | awk '{print $2","$1}'>> hh_uniq_positions.csv