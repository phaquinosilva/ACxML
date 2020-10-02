import os
import pandas as pd
from pathlib import Path

### OBSERVAcoES ###
# → coloquei sim_time e voltage para facilitar na hora de realizar reducao de tensao
#

# executa simulacoes
def run_hspice(cell, adder_type):
    # selecionamos a celula a ser usada
    # e altera o FA da simulacao
    with open('./8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('ema', cell)
    with open('./8bit_' + adder_type + '.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)

    # executa simulacoes
    os.system('./executer.sh ' + adder_type + ' ' + cell)

    # retorna arquivo para formato original
    with open('./8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace(cell, 'ema')
    with open('./8bit_' + adder_type + '.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)


# organiza dados de um output .csv do HSPICE
def organize_results(sim_time, voltage, adder_type, cell):
    adder_results = []
    p = Path('.')
    for csv in list(p.glob('**/result_8bit_'+adder_type+'_'+cell+'*.csv')):
        res_df = pd.read_csv(csv, skiprows=3, na_values='failed')
        # seleciona colunas relevantes
        # preciso lidar com os 'failed'
        delay_df = res_df.filter(regex='tp')
        power = res_df['q_dut'].iloc[0] * voltage / sim_time
        # pior caso de atraso
        delay = delay_df.max(axis=1).iloc[0]
        adder_results.append({'delay' : delay, 'power' : power})
        # os.remove(csv)
    sums_res = pd.DataFrame(adder_results)
    avg_pow = sums_res['power'].mean()
    delay = sums_res['delay'].max(axis=0)
    # limpa diretorio para proxima simulacao
    return {'delay' : delay, 'power' : avg_pow}

def run():
    ls_adders = ['EMA', 'EXA', 'SMA', 'AMA1', 'AMA2', 'AXA2', 'AXA3']
    add_type = ['RCA', 'CSA']
    results = {}
    for adder in add_type:
        for fa in ls_adders:
            run_hspice(fa, adder)
            results[fa] = organize_results(20e-9, 0.7, adder, fa)
        prime = pd.DataFrame(results)
        prime.to_csv('./results/8bit_'+adder+'_results.csv')
        # print(prime)
        results = {}

run()
