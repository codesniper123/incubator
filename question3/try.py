import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

states = [ 1, 2, 3]
states_str = ['CA', 'NV', 'AZ']

amt1   = [ 1000, 2000,  4000]
amt2   = [ 500,  1200,  2300]

#sns.set(style="whitegrid")
#sns.set_color_codes("pastel")
plt.plot(states, amt1, label='State Department')
plt.plot(states, amt2, label='NASA')
#plt.xlim(1,3)
#plt.xlabel('State')
#plt.ylabel('Amount in $')
#plt.title( 'Federal Allocation by Department to States')
#plt.xticks(states, states_str)
#legend = plt.legend(loc='upper left', bbox_to_anchor=(0, 1),
#                        frameon=True)



plt.show()