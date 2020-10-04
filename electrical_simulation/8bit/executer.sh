#! /bin/bash
PATH="$PATH":/home/user/bin

echo "Simulation executer for 8bit adders"
i="./8bit_"$1".cir"
echo "Simulating sum "$3" in "$1" with "$2
## roda simulação
hspice $i
mv "./8bit_"$1".mt0.csv" "result_"$1"_"$2"_sum_"$3".csv"
mv *.csv ./results
echo
echo "Done."
