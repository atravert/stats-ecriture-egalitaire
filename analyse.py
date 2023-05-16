# %%
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

  
# %%

# Load data
df = pd.read_excel(Path("results_230515_raw_fr.xlsx"))

# plot 
from matplotlib.ticker import FuncFormatter
plt.style.use('ggplot')
colors = [c['color'] for c in list(plt.rcParams['axes.prop_cycle'])]

def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.fk' % (x * 1e-3)
formatter = FuncFormatter(thousands)

def plot_bar(loc, factor=1.):
    '''barplot
    
    loc: str or int
        column title or index'''
    
    if isinstance(loc, str):
        i = df.columns.get_loc(loc)
    else:
        i =loc
    df_ = df.iloc[:,i:i+3]
    df_.columns = ['Masculin', 'Féminin', 'Contracté']
    ax = (df_.sum(axis=0) * factor).plot.bar(color=colors, rot=0)
    ax.set_title(df.columns[i], y=0.87)
    ax.yaxis.set_major_formatter(formatter)
    ax.set_yticks([2e5, 4e5, 6e5, 8e5])
    ax.set_ylim([0, 0.8e6])

mm = 1/25.4 
fig, axes = plt.subplots(nrows=3, ncols=2, tight_layout=True, figsize=(183*mm, 220*mm), dpi=80)

plt.sca(axes[0,0])
plot_bar(0)
# plt.sca(axes[0,1])
# plot_bar(6)
# plt.sca(axes[1,0])
# plot_bar(9)
# plt.sca(axes[1,1])
# plot_bar(12)
# plt.sca(axes[2,0])
# plot_bar(15, factor=0.5)
# plt.sca(axes[2,1])
# plot_bar(18,)

for ax in axes.flat:
    ax.label_outer()
plt.show()

# Invisibilisation: (M - F)/M
# %%
def invisibilisation(i):
    return 100 - (df.iloc[:,i] - df.iloc[:,i+1]) / df.iloc[:,i] * 100

sum =  (df.sum(axis=1))
size = sum/max(sum) * 150

i_mcf = invisibilisation(3)
i_ch = invisibilisation(6)
i_ens = invisibilisation(9)
i_pr= invisibilisation(12)
i_etu= invisibilisation(15)
i_doc= invisibilisation(18)

fig, axes = plt.subplots(nrows=2, ncols=2, tight_layout=True, figsize=(183*mm, 183*mm), dpi=80)
plt.sca(axes[0,0])
plt.scatter(i_ens, i_doc, s=size, c=colors[1])
plt.xlim([0.0,100])
plt.xlabel("enseignante")
plt.ylim([0.0,100])
plt.ylabel("doctorante")

plt.sca(axes[0,1])
plt.scatter(i_ens, i_ch, s=size, c=colors[1])
plt.xlim([0.0,100])
plt.xlabel("enseignante")
plt.ylim([0.0,100])
plt.ylabel("chercheuses")

plt.sca(axes[1,0])
plt.scatter(i_ens, i_pr, s=size, c=colors[1])
plt.xlim([0.0,100])
plt.xlabel("enseignante")
plt.ylim([0.0,100])
plt.ylabel("professeure")

plt.sca(axes[1,1])
ax = plt.scatter(i_ens, i_mcf, s=size, c=colors[1])
plt.xlim([0.0,100])
plt.xlabel("enseignantes")
plt.ylim([0.0,100])
plt.ylabel("Maîtresse [de conférence]")

# %%
ii = pd.DataFrame([i_ch, i_ens, i_doc, i_pr, i_etu]).T
ii.boxplot() 
plt.ylim([0.0,100])
