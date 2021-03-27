import os
import pandas as pd
from pathlib import Path
from random import sample

################################# HSPICE SCRIPT #######################################

## SUBTRACTOR CIRCUITS ##

# executa hspice
def run_adders(comparator, comp_num, cell):
    # sets type of sources file and name of output file
    source = '.include sources/'
    if cell == 'exa' or cell == 'ema':
        name = 'results/result_' + comparator + '_' + cell + '_' + str(comp_num) +'.csv'
        source +='source_exact_' + str(comp_num) + '.cir'
        adder = '.include fas/' + cell + '.cir\n'
    else:
        name = 'results/result_' + comparator + '_' + cell + '_' + str(comp_num) +'.csv'
        source += 'source_' + cell + '_' + str(comp_num) + '.cir'
        adder = '.include fas/' + cell + '.cir\n'
    source += '\n'
    # decide soma a ser executada
    
    with open('./nondef_params.txt', 'w') as f:
        f.seek(0)
        f.write(source)
        f.write(adder)
    # chamadas de sistema pra executar o hspice
    os.system('hspice '+ comparator + '.cir')
    os.rename('./' + comparator + '.mt0.csv',  name)
# processa resultados
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

# executa simulações
def adders_sim():
    fa = ['ema', 'exa', 'sma', 'ama1', 'ama2', 'axa2', 'axa3']
    sample_sizes = [960, 960, 512, 340, 320, 512, 512]
    results = {}
    for i in range(len(fa)):
        # altera FA no arquivo de simulacao
        pre(fa[i])
        # executa simulacao nas somas da amostra    
        for j in range(sample_sizes[i]):
            run_hspice('comp_subtractor', j, fa[i])
        # retorna arquivo pro original
        post(fa[i])
        results[fa[i]] = organize_adders(5e-9, 0.7, 'comp_subtractor', fa[i])
    prime = pd.DataFrame(results)
    prime.to_csv('./results/comp_subtractor_results.csv')

def pre(adder):
    with open('./array_adders/4bRCA.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace('ema', adder)
    with open('./array_adders/4bRCA.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)
            
def post(adder):  
    with open('./array_adders/4bRCA.cir', 'r') as f:
        filedata = f.read()
    newdata = filedata.replace(adder, 'ema')
    with open('./array_adders/4bRCA.cir', 'w') as f:
        f.seek(0)
        f.write(newdata)


## DEDICATED CIRCUITS ##
# executa simulações
def dedicated_sim():
    comparators = ['comp_exact', 'comp_approx1', 'comp_approx2', 'comp_approx3', 'comp_approx4', 'comp_approx5', 'comp_approx6']
    sample_sizes = [480, 448, 448, 368, 368, 256, 352]
    results = {}
    for i in range(len(sample_sizes)) :
        # simulação para subtratores
        for j in range(sample_sizes[i]):
            run_dedicated(comparator=comparators[i], comp_num=j)
        results[comparators[i]] = organize_dedicated(5e-9, 0.7, comparators[i])
    prime = pd.DataFrame(results)
    prime.to_csv('./results/comp_dedicated_results.csv')
# executa hspice
def run_dedicated(comparator, comp_num):
    name = 'results/result_' + comparator + '_' + str(comp_num) +'.csv'
    source = '.include sources/source_'+comparator+'_'+str(comp_num)+'.cir\n'
    if comparator == 'comp_exact':
        with open('nondef_params.txt', 'w') as f:
            f.seek(0)
            f.write(source)
        os.system('hspice comp_dedicated.cir')
        os.rename('./comp_dedicated.mt0.csv',  name)
    else: 
        with open('nondef_params.txt', 'w') as f:
            f.seek(0)
            f.write('.include comparators/4bit_'+comparator+'.cir\n')
            f.write(source)
        os.system('hspice comp_dedicated_approx.cir')
        os.rename('./comp_dedicated_approx.mt0.csv',  name)
# processa resultados
def organize_dedicated(sim_time, voltage, comparator):
    comp_results = []
    p = Path('.')
    for csv in list(p.glob('**/result_'+comparator+'_*.csv')):
        res_df = pd.read_csv(csv, skiprows=3, na_values="failed")
        print(res_df)
        # seleciona colunas relevantes
        delay_df = res_df.filter(regex='tp')
        power = (-1) * res_df['q_dut'].iloc[0] * voltage / sim_time
        # pior caso de atraso
        delay = delay_df.max(axis=1).iloc[0]
        comp_results.append({'delay' : delay, 'power' : power})
        # limpa diretorio para restarem somente os arquivos relevantes
        os.remove(csv)
    sums_res = pd.DataFrame(comp_results)
    avg_pow = sums_res['power'].mean()
    delay = sums_res['delay'].max(axis=0)
    return {'delay' : delay, 'power' : avg_pow}

if __name__ == '__main__':
    adders_sim()
    dedicated_sim()
