
# %% 
scatter_with_xnor = sim_data.plot.scatter(x='ED', y='PDP (aJ)', s=40, c='purple')
# %%
fig, ax = plt.subplots()
cmap = cm.get_cmap('seismic')
graph = sim_data[['ED', 'PDP (aJ)']].iloc[0:11,].plot(x='ED', y='PDP (aJ)', 
                                        kind='scatter', s=60, ax=ax,
                                        linewidth=1, c=range(len(sim_data.iloc[0:11,])),
                                        colormap=cmap)
for k, v in sim_data[['ED', 'PDP (aJ)']].iloc[0:11,].iterrows():
    ax.annotate(k, v, xytext=(10,-8), textcoords='offset points',
    family='sans-serif', fontsize=12, color='darkslategrey')
fig.show()
# fig.savefig('pdp_ed_no_xnors.pdf')
#%%
sim_data_noEXA = sim_data.drop(labels=['EXA'], axis=0, inplace=False)
#%%
fig, ax = plt.subplots()
cmap = cm.get_cmap('seismic')
graph = sim_data_noEXA[['ED', 'PDP (aJ)']].plot(x='ED', y='PDP (aJ)', 
                                        kind='scatter', s=50, ax=ax,
                                        linewidth=1, c=range(len(sim_data_noEXA)),
                                        colormap=cmap)

for k, v in sim_data_noEXA[['ED', 'PDP (aJ)']].iloc[:,].iterrows():
    ax.annotate(k, v, xytext=(10,-8), textcoords='offset points',
    family='sans-serif', fontsize=10, )
fig.savefig('pdp_ed_xnors_included_noEXA_annotate.pdf')
# %%
fig, ax = plt.subplots()
cmap = cm.get_cmap('seismic')
graph = sim_data[['ED', 'PDP (aJ)']].plot(x='ED', y='PDP (aJ)', 
                                        kind='scatter', s=50, ax=ax,
                                        linewidth=1, c=range(len(sim_data)),
                                        colormap=cmap)
fig.savefig('pdp_ed_xnors_included.pdf')
# %%
sim_data.iloc[0:11,0:3].plot.bar(rot=0, subplots=True, figsize=(6,6), legend=False)
plt.savefig('electric_no_xnors.pdf')
# %%
sim_data.iloc[0:11]['PDP (aJ)'].plot.bar(rot=0, subplots=True, figsize=(6,4), legend=False)
plt.savefig('pdp_no_xnors.pdf')
# %%
sim_data.iloc[:,0:3].plot.bar(rot=0, subplots=True, figsize=(8,6), legend=False)
plt.savefig('electric_xnors_included.pdf')
#%%
sim_data['PDP (aJ)'].plot.bar(rot=0, legend=False, figsize=(8,5))
plt.savefig('pdp_xnors_included.pdf')
# %%
sim_data_noEXA.iloc[:,0:3].plot.bar(rot=0, subplots=True, legend=False, figsize=(7,6))
plt.savefig('electric_noEXA.pdf')
#%%
sim_data_noEXA['PDP (aJ)'].plot.bar(rot=0, legend=True, figsize=(8,6))
plt.savefig('pdp_xnors_included_noEXA.pdf')
# %%
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
#%%
sim_data['ED']
sim_data.index[0]
# %%
