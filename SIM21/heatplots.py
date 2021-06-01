#%%
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import skimage.measure

def annotate_heatmap(ax, heatmap_data):
	for i in range(heatmap_data.shape[0]):
	    for j in range(heatmap_data.shape[1]):
	        text = ax.text(j, i, heatmap_data[i, j],ha="center", va="center", color="w")

# infile_path = "ded_error_table.csv"
# infile_path = "adder_error_table.csv"
infile_path = "erros.csv"
if "ded" in infile_path:
	approx_comparators = "ADC1,ADC2,ADC3,ADC4,ADC5,ADC6".split(",")
	circuit_type = "ded"
elif "adder" in infile_path:
	approx_comparators = "sma,ama1,ama2,axa2,axa3".split(",")
	circuit_type = "adder"
elif "erros" in infile_path:
	approx_comparators = "adc1,adc2,adc3,adc4,adc5,adc6".split(",")
	circuit_type = "ded"
#%%
df = pd.read_csv(infile_path, sep = ",")
df.rename(columns={'Unnamed: 0':'A_B'}, inplace = True)
df["A"] = df["A_B"].apply(lambda x: x >> 4)
df["B"] = df["A_B"].apply(lambda x: x % (2**4))

df["A+B"] = df["A"] + df["B"]
df = df.sort_values(["A+B", "A", "B"])
df = df.reset_index(drop=True)
#%%
step_reduce = 2
for approx in approx_comparators:
	heatmap_data = df[["A","B", approx]]
	heatmap_data = heatmap_data.pivot(index='A', columns='B', values=approx)
	heatmap_data = skimage.measure.block_reduce(heatmap_data, (step_reduce,step_reduce), np.sum)
	if heatmap_data.max() == 0:
		print('skipping heatmap for adder %s with no error' % (approx))
		continue

	im = plt.imshow(heatmap_data, cmap = 'Purples', vmin=0)
	ax = plt.gca()
	
	ax.set_xticks(np.arange(-.5, df["B"].max()/2+1, 1), minor = True)
	ax.set_yticks(np.arange(-.5, df["A"].max()/2+1, 1), minor = True)
	ax.set_xticklabels(np.arange(0, df["B"].max()+2,2))
	ax.set_yticklabels(np.arange(0, df["A"].max()+2,2))
	annotate_heatmap(ax,heatmap_data)

	ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

	plt.title(approx)
	plt.xlabel("B value")
	plt.ylabel("A value")
	

	# cb = plt.colorbar(boundaries=range(0, heatmap_data.max()+1))
	# plt.show()
	plt.savefig('heatmap_%s.png' % approx, dpi=600)
	plt.close()
	plt.clf()

#%%
mark_step = 16
markers = ['x','o','v','^','s','x','o','v','^','s']
colors = ['#6930c3', '#3b5360', '#00bcd4', '#00bd42', '#e600bf', '#6930c3', '#3b5360', '#00bcd4', '#00bd42', '#e600bf']
for i,approx in enumerate(approx_comparators):
	if i % 2:
		df[approx].cumsum().plot(marker = markers[i], markevery=(mark_step//2, mark_step), color = colors[i])
	else:
		df[approx].cumsum().plot(marker = markers[i], markevery=mark_step, color = colors[i])

plt.ylabel("Accumulated Error")
plt.xlabel("(A,B) values")
xticks = ['(%s,%s)' % (a,b) for a,b in zip(df["A"], df["B"])]
step = 30
plt.xticks(range(0,len(xticks)+1, step), xticks[::step] + [xticks[-1]])
plt.legend()
plt.show()
# plt.savefig("erro_acumulado_%s.pdf" % (circuit_type), bbox = 'tight')
#print(df1)

# %%
