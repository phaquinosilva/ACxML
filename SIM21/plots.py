#%% 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

sim_data = pd.read_csv('/home/pedro/Documentos/ECLab/ACxML/SIM21/approximate 4bit comparators_decision trees - comparator characterization.csv', index_col=0)
sim_data = sim_data.rename(columns={'delay (ps)' : 'Delay (ps)'})
sim_data = sim_data.rename(columns={'power (nW)':'Power (nW)'})
sim_data
# %% 
scatter_with_xnor = sim_data.plot.scatter(x='ED', y='PDP (aJ)', s=40, c='purple')
# %%
fig, ax = plt.subplots()
cmap = cm.get_cmap('Dark2')
graph = sim_data[['ED', 'PDP (aJ)']].iloc[0:11,].plot(x='ED', y='PDP (aJ)', 
                                        kind='scatter', s=60, ax=ax,
                                        linewidth=1, c=range(len(sim_data.iloc[0:11,])),
                                        colormap=cmap)
# for k, v in sim_data[['ED', 'PDP (aJ)']].iloc[0:11,].iterrows():
    # ax.annotate(k, v, xytext=(10,-8), textcoords='offset points',
    # family='sans-serif', fontsize=12, color='darkslategrey')

fig.savefig('pdp_ed_no_annotations.pdf')
_data['PDP (aJ)'].iloc[lambda s: s != 'EXA', :].# %%
fig, ax = plt.subplots()
cmap = cm.get_cmap('Dark2')
graph = sim_data[['ED', 'PDP (aJ)']].plot(x='ED', y='PDP (aJ)', 
                                        kind='scatter', s=50, ax=ax,
                                        linewidth=1, c=range(len(sim_data)),
                                        colormap=cmap)
fig.savefig('pdp_ed_xnors_included.pdf')
# %%
cmap = cm.get_cmap('Dark2')
sim_data.iloc[0:11,0:3].plot.bar(rot=2, subplots=True, figsize=(6,6), legend=False)
plt.savefig('bar_electric.pdf')
# %%
# cmap = cm.get_cmap('Dark2')
sim_data.iloc[lambda s: s == 'EXA', :]#.plot.bar(rot=2, legend=False, figsize=(8,5))
# plt.savefig('bar_pdp.pdf')
# %%
