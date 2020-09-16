import os, glob
import pandas as pd

# encontra e chama HSPICE para cada arquivo .cir do diretorio
def run_hspice():
    for sfile in glob.glob('*meas*.cir'):
        print('Starting simulation on ' + sfile)
        os.system('hspice ' + sfile)
        print('End of simulation')

# organiza dados de um output .csv do HSPICE
def organize_results(hspice_csv):
    res_df = pd.read_csv(hspice_csv, skiprows=3)
    # remove useless tail columns
    delay_df = df.filter(regex='tp')
    energy_df = df.filter(regex='e_')
    # pior caso de atraso
    delay = delay_df.max(axis=1)
    return pd.concat([delay_df, energy_df])


######## REVER ESTA FUNÇÃO ##########
# eu tinha começado, mas me parece cada vez mais desnecessariamente complicado
def near_threshold(filename):
    # sim_times = 0;
    sfile = open(filename, 'r+')
    voltage = 0.7
    interval_multiplier = 1
    while interval_multiplier <= 10:
        sfile.seek(0)
        sfile.write(sfile.replace(str(voltage), str(voltage-0.1)))
        os.system('hspice ' + filename)
        # the output is set to be a csv file
        output = filename.replace('.cir', '.mt0.csv')
        with
