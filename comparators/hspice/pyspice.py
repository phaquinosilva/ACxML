import os
import pandas as pd
from pathlib import Path
from random import sample


################################# HSPICE SCRIPT #######################################

# executa simulacoes
def run_hspice(comparator, comp_num, cell=None):
    # sets type of sources file and name of output file
    if cell == None:
        name = 'results/result_' + comparator + '_' + str(comp_num) +'.csv'
        source ='source_exact_' + str(comp_num) + '.cir'
    elif cell == 'exa' or cell == 'ema':
        name = 'results/result_' + comparator + '_' + cell + '_' + str(comp_num) +'.csv'
        source ='source_exact_' + str(comp_num) + '.cir'
    else:
        name = 'results/result_' + comparator + '_' + cell + '_' + str(comp_num) +'.csv'
        source = 'source_' + cell + str(comp_num) + '.cir'
    # decide soma a ser executada
    with open('./' + comparator + '.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('source_XX.cir', source)
    with open('./' + comparator + '.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)
    # chamadas de sistema pra executar o hspice
    os.system('hspice '+ comparator + '.cir')
    os.rename('./' + comparator + '.mt0.csv',  name)
    # retorna arquivo ao formato original
    with open('./' + comparator +'.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace(source, 'sources_XX.cir')
    with open('./comp_'+ comparator +'.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)

# organiza dados de um output .csv do HSPICE
def organize_results(sim_time, voltage, comparator, cell=None):
    if cell == None: 
        return organize_dedicated(sim_time, voltage, comparator)
    else:
        return organize_adders(sim_time, voltage, comparator, cell)

def organize_adders(sim_time, voltage, comparator, cell):
    adder_results = []
    p = Path('.')
    for csv in list(p.glob('**/result_' + comparator+'_' + cell+'_*.csv')):
        res_df = pd.read_csv(csv, skiprows=3, na_values="failed")
        print(res_df)
        # seleciona colunas relevantes
        delay_df = res_df.filter(regex='tp')
        if cell == "AXA2" or cell == "AXA3" or cell == "EXA":
            power = (-1) * (res_df['q_dut'].iloc[0] + res_df['q_in'].iloc[0]) * voltage / sim_time
        else:
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


def organize_adders(sim_time, voltage, comparator):
    results = []
    p = Path('.')
    for csv in list(p.glob('**/*' + comparator + '*.csv')):
        res_df = pd.read_csv(csv, skiprows=3, na_values="failed")
        print(res_df)
        # seleciona colunas relevantes
        delay_df = res_df.filter(regex='tp')
        power = (-1) * res_df['q_dut'].iloc[0] * voltage / sim_time
        # pior caso de atraso
        delay = delay_df.max(axis=1).iloc[0]
        results.append({'delay' : delay, 'power' : power})
        # limpa diretorio para restarem somente os arquivos relevantes
        os.remove(csv)
    sums_res = pd.DataFrame(results)
    avg_pow = sums_res['power'].mean()
    delay = sums_res['delay'].max(axis=0)
    return {'delay' : delay, 'power' : avg_pow}

# executa simulações
def adders_sim():
    fa = ['ema', 'exa', 'sma', 'ama1', 'ama2', 'axa2', 'axa3']
    n = 5
    sample_sizes = [960, 960, 512, 340, 320, 512, 512]
    comparator = 'comp_subtractor'
    results = {}
    # simulação para subtratores
    for i in range(7):
        # altera FA no arquivo de simulacao
        with open('./' + comparator + '.cir', 'r') as f:
            filedata = f.read()
        newdata = filedata.replace('ema', fa[i])
        with open('./' + comparator + '.cir', 'w') as f:
            f.seek(0)
            f.write(newdata)
        # executa simulacao nas somas da amostra    
        # for j in range(sample_sizes[i]):
        for j in range(n):
            run_hspice(comparator, i, fa[i])
        # retorna arquivo pro original
        with open('./' + comparator + '.cir', 'r') as f:
            filedata = f.read()
        newdata = filedata.replace(fa[i], 'ema')
        with open('./' + comparator + '.cir', 'w') as f:
            f.seek(0)
            f.write(newdata)            
        results[fa[i]] = organize_results(5e-9, 0.7, compa, fa[i])
    prime = pd.DataFrame(results)
    prime.to_csv('./results/' + comparator + '_results.csv')
    results = {}

def dedicated_sim():
    comparator = 'comp_dedicated'
    results = {}
    # simulação para subtratores
    for i in range(5):
#    for i in range(960):
        run_hspice(comparator, i)
    results = organize_results(5e-9, 0.7, comparator)
    prime = pd.DataFrame(results)
    prime.to_csv('./results/' + comparator + '_results.csv')

if __name__ == '__main__':
    adders_sim()
    dedicated_sim()
