#! /bin/bash
PATH="$PATH":/home/user/bin

echo "Simulation executer for 8bit adders"
i="./8bit/8bit_"$1".cir"
y=${i%.*}
y=${y##*/}
echo "Simulating "$y
for j in $(find . -name "sources_sum*.cir")
do
  ## guarda somente o número da soma simulada
  s=`echo $j | cut -c 27-28`
  echo "Starting simulation of sum "$s
  ## troca arquivo de sources e measures
  sed -i "s+.include sources.cir+.include "$j"+g" $i
  ## roda simulação
  hspice $i
  mv $y".mt0.csv" "result_"$y"_"$2"_sum_"$s".csv"
  mv *.csv ./8bit/results
  ## retorna arquivo de simulação pro estado original para próxima iteração
  sed -i "s+.include "$j"+.include sources.cir+g" $i
  ## sinaliza fim da simulação dessa soma
  echo "End of simulation for sum "$s
  #sleep 5
  echo
done
echo
echo "Simulations finished."
