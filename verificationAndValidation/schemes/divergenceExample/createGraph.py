import pandas as pd
import re
import matplotlib.pyplot as plt

def read_Txy(name):
    return pd.read_csv(name, sep='\t', header=None, names = ["distance","T"])

fig, ax = plt.subplots()

filepath = '.'
schemesFileName = 'system/schemesToTest'

counter = 0
with open(schemesFileName, 'r', encoding='utf-8') as file:
    for line in file:
        # sanitise: remove 'special' characters
        saniLine = re.sub(r' ', '_', line.strip())
        saniLine = re.sub(r'[^a-zA-Z0-9_]', '', saniLine)
        print(f"Scheme name from {schemesFileName} is {line.strip()} .")
        print(f"        tag is {saniLine}")
        # python 2
        #print("Scheme name from {0} is {1} .".format(schemesFileName, line.strip()))
        #print("        tag is {0}".format(saniLine))
        filename = filepath + '/line1_T_' + saniLine +'.xy'
        data01 = read_Txy(filename)
        #print(data01)
        
        if counter < 10:  # 10 colors
            ls = '-'  # solid
        else:
            ls = '--' # dashed
        ax.plot(data01["distance"], data01["T"], label=saniLine, linestyle=ls)
        counter += 1

ax.legend() #(fontsize=18)
ax.set_xlabel("distance [m]")
ax.set_ylabel("T [K]")
plt.show()
fig.savefig('divergenceExampleGraph.png')
