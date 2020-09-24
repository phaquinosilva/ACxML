import os
import pandas as pd
from pathlib import Path

### OBSERVAÇÕES ###
# → coloquei sim_time e voltage para facilitar na hora de realizar redução de tensão
#

# executa simulações
def run_hspice(cell, adder_type):
    # selecionamos a celula a ser usada
    # e altera o FA da simulação
    with open('./8bit/8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('ema', cell)
    with open('./8bit/8bit_' + adder_type + '.cir', 'w') as f:
        f.write(newdata)

    # executa simulações
    os.system('./executer.sh ' + cell)

    # retorna arquivo para formato original
    with open('./8bit/8bit_' + adder_type + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace(cell, 'ema')
    with open('./8bit/8bit_' + adder_type + '.cir', 'w') as f:
        f.write(newdata)


# organiza dados de um output .csv do HSPICE
def organize_results(sim_time, voltage):
    adder_results = []
    p = Path('.')
    for csv in list(p.glob('**/result_*.csv')):
        res_df = pd.read_csv(csv, skiprows=3)
        # seleciona colunas relevantes
        delay_df = res_df.filter(regex='tp')
        power = res_df.iloc[0]['q_dut'] * voltage / sim_time
        # pior caso de atraso
        delay = delay_df.max(axis=1).iloc[0]
        adder_results.append({'delay' : delay, 'power' : power})
        # limpa diretório para próxima simulação
        # os.remove(csv)
    sums_res = pd.DataFrame(adder_results)
    delay = sums_res['delay'].max()
    avg_pow = sums_res['power'].mean()
    return {'delay' : delay, 'power' : avg_pow}


def run():
    ls_adders = ['ema', 'exa', 'sma', 'ama1', 'ama2', 'axa2', 'axa3']
    add_type = ['RCA', 'CSA']
    results = {}
    for adder in add_type:
        for fa in ls_adders:
            run_hspice(fa, adder)
            results[fa] = organize_results(10e-9, 0.7)
        pd.DataFrame(results).to_csv('./8bit_'+adder+'_results.csv')
        results = {}
