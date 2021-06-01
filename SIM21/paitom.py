#%% 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np

sim_data = pd.read_csv('/home/pedro/Documentos/ECLab/ACxML/SIM21/approximate 4bit comparators_decision trees - comparator characterization.csv', index_col=0)
sim_data = sim_data.rename(columns={'delay (ps)' : 'Delay (ps)'})
sim_data = sim_data.rename(columns={'power (nW)':'Power (nW)'})
sim_data_noEXA = sim_data.drop(labels=['EXA'], axis=0, inplace=False)

fig, ax = plt.subplots()
df = sim_data_noEXA
colormap = cm.seismic
colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, len(df.iloc[:,0:0]))]
for i, c in enumerate(colorlist):
    x = df['ED'][i]
    y = df['PDP (aJ)'][i]
    l = df.index[i]
    ax.scatter(x,y,label=l,s=50,c=c)
ax.legend(ncol=3, fontsize=11)
ax.set_xlabel('ED', fontsize=13)
ax.set_ylabel('PDP (aJ)', fontsize=13)
plt.show()
# plt.savefig('pdpxed_noEXA.png')