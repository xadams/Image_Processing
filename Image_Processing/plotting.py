import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

results = []
with open("result_summary.csv", "rt") as csvfile:
    fin = csv.reader(csvfile)
    for row in fin:
        title = row[0]
        results.append([title[0:2],title[6],title[10],
                        row[1].split()[0].strip(",").strip("["),
                        row[1].split()[1].strip(",").strip("["),
                        row[1].split()[2].strip(",").strip("]")])
frame = pd.DataFrame(results,columns=['Time','Concentration','Treatment','Average Peak Ratio','Peak Ratio std','Area Ratio'])

Times = ["60","45","30"]
Concs = ["5,", "2", "1"]
Treatments = ["N", "T"]

fig = plt.figure()
for T in Times:
    plt.title("Average Peak Ratios")
    for Tr in Treatments:
        x = frame['Concentration'][(frame['Time']==T) & (frame['Treatment']==Tr)]
        y = frame['Average Peak Ratio'][(frame['Time']==T) & (frame['Treatment']==Tr)]
        plt.plot(np.asarray(x,dtype=float),np.asarray(y,dtype=float),label="Time = {}, Treatment = {}".format(T,Tr))
    plt.xlabel("Concentration ($\mu$L)")
    plt.ylabel("Average Peak Height")
    plt.legend(loc='best')

fig = plt.figure()
for T in Times:
    plt.title("Area Ratios")
    for Tr in Treatments:
        x = frame['Concentration'][(frame['Time']==T) & (frame['Treatment']==Tr)]
        y = frame['Area Ratio'][(frame['Time']==T) & (frame['Treatment']==Tr)]
        plt.plot(np.asarray(x,dtype=float),np.asarray(y,dtype=float),label="Time = {}, Treatment = {}".format(T,Tr))
    plt.xlabel("Concentration ($\mu$L)")
    plt.ylabel("Average Peak Height")
    plt.legend(loc='best')

plt.show()