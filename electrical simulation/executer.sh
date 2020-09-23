#! /bin/bash
PATH="$PATH":/home/user/bin

echo "Simulation executer for 8bit adders"
mkdir results
adder_type=$1
for i in $(find . -name "8bit_*.cir")
do
  y=${i%.*}
  y=${y##*/}
  echo "Simulating "$y
  for j in $(find . -name "sources_sum*.cir")
  do
    ## guarda somente o número da soma simulada
    s=`echo $j | cut -c 22-23`
    echo "Starting simulation of sum "$s
    ## troca arquivo de sources e measures
    sed -i "s+.include sources.cir+.include "$j"+g" $i
    ## roda simulação
    hspice $i
    mv $y".mt0.csv" "result_"$y"_"$adder_type"_sum_"$s".csv"
    mv *.csv results
    ## retorna arquivo de simulação pro estado original para próxima iteração
    sed -i "s+.include "$j"+.include sources.cir+g" $i
    ## sinaliza fim da simulação dessa soma
    echo "End of simulation for sum "$s
    #sleep 5
    echo
  done
  echo
done
echo "All simulations finished."
