import os
import pandas as pd
from pathlib import Path
from random import sample
from arc_gen import gen_files

################################# OBSERVACOES #########################################
# -> coloquei sim_time e voltage para facilitar na hora de realizar reducao de tensao #
# -> fazer analiticamente os caminhos criticos dos somadores                          #
# -> selecionar 500 somas aleatoriamente para realizar simulacoes, alem dos caminhos  #
#    criticos                                                                         #
# -> estou confiante agora que tudo aqui funciona, e posso executar todas as          #
#    simulacoes durante a noite e avaliar os resultados amanha                        #
#######################################################################################

# executa simulacoes
def run_hspice(cell, adder_type, sum):
    # decide soma a ser executada
    with open('./8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('sources_sumXX.cir', 'sources_sum' + str(sum) + '.cir')
    with open('./8bit_' + adder_type + '.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)

    # uhm, nesse ponto estou quaaaase me livrando do desse bash
    # executa simulacoes
    os.system('./executer.sh ' + adder_type + ' ' + cell + ' ' + str(sum))

    # retorna arquivo para formato original
    with open('./8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('sources_sum' + str(sum) + '.cir', 'sources_sumXX.cir')
    with open('./8bit_' + adder_type + '.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)


# organiza dados de um output .csv do HSPICE
def organize_results(sim_time, voltage, adder_type, cell):
    adder_results = []
    p = Path('.')
    for csv in list(p.glob('**/*_'+adder_type+'_'+cell+'_*.csv')):
        res_df = pd.read_csv(csv, skiprows=3, na_values="failed")
        print(res_df)
        # seleciona colunas relevantes
        delay_df = res_df.filter(regex='tp')
        power = (-1) * res_df['q_dut'].iloc[0] * voltage / sim_time
        # pior caso de atraso
        delay = delay_df.max(axis=1).iloc[0]
        adder_results.append({'delay' : delay, 'power' : power})
        # limpa diretorio para restarem somente os arquivos relevantes
        os.remove(csv)
    sums_res = pd.DataFrame(adder_results)
    avg_pow = sums_res['power'].mean()
    delay = sums_res['delay'].max(axis=0)
    return {'delay' : delay, 'power' : avg_pow}

def run():
    add_type = ['RCA', 'CSA']
    ls_adders = ['EMA', 'EXA', 'SMA', 'AMA1', 'AMA2', 'AXA2', 'AXA3']
    results = {}
    # seleciona as somas que serao simuladas no HSPICE
    sums = sample(range(gen_files(True, 2**8 + 1)), 500)
    for adder in add_type:
        for fa in ls_adders:

            # altera FA no arquivo de simulacao
            with open('./8bit_' + adder + '.cir', 'r') as f:
                filedata = f.read()
            newdata = filedata.replace('ema', fa)
            with open('./8bit_' + adder + '.cir', 'w') as f:
                f.seek(0)
                f.write(newdata)

            # executa simulacao nas somas da amostra    
            for sum in sums:    
                print(sum)
                run_hspice(fa, adder, sum)
            
            # retorna arquivo pro original
            with open('./8bit_' + adder + '.cir', 'r') as f:
                filedata = f.read()
            newdata = filedata.replace(fa, 'ema')
            with open('./8bit_' + adder + '.cir', 'w') as f:
                f.seek(0)
                f.write(newdata)
            
            results[fa] = organize_results(5e-9, 0.7, adder, fa)
        prime = pd.DataFrame(results)
        prime.to_csv('./results/8bit_'+adder+'_results.csv')
        results = {}

run()