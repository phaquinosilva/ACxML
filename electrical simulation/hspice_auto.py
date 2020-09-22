import os
import pandas as pd

# encontra e chama HSPICE para cada arquivo .cir do diretorio com a regex decidida por filetype
def run_hspice(voltage, sim_time): #adder_type):
    ## change adder in file
    os.system('executer.sh')
    adder_results = []
    # iterar usando pathlib
    for csv in os.listdir('results/'):
        adder_results.append(organize_results(csv, sim_time, voltage))
    return pd.DataFrame(adder_results)

# organiza dados de um output .csv do HSPICE
def organize_results(hspice_csv, sim_time, voltage):
    res_df = pd.read_csv(hspice_csv, skiprows=3)
    # remove useless tail columns
    delay_df = res_df.filter(regex='tp')
    power = res_df.iloc[0]['e_fa']
    # pior caso de atraso
    delay = delay_df.max(axis=1).iloc[0]
    return {'delay' : delay,
            'power' : power
    }


######## REVER ESTA FUNÇÃO ##########
# eu tinha começado, mas me parece cada vez mais desnecessariamente complicado
# def near_threshold(filename):
    # sim_times = 0
    # sfile = open(filename, 'r+')
    # voltage = 0.7
    # interval_multiplier = 1
    # while interval_multiplier <= 10:
        # sfile.seek(0)
        # sfile.write(sfile.replace(str(voltage), str(voltage-0.1)))
        # os.system('hspice ' + filename)
        # the output is set to be a csv file
        # output = filename.replace('.cir', '.mt0.csv')
        # with
