import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


def plot_FA(input="result_summary.csv", show=False):
    results = []
    with open(input, "rt") as csvfile:
        fin = csv.reader(csvfile)
        for row in fin:
            title = row[0].split()
            results.append([title[0][0:2], title[1][0], title[2][0],
                            row[1].split()[0].strip(",").strip("["),
                            row[1].split()[1].strip(",").strip("["),
                            row[1].split()[2].strip(",").strip("]")])
    frame = pd.DataFrame(results, columns=['Time', 'Concentration', 'Treatment', 'Average Peak Ratio', 'Peak Ratio std',
                                           'Area Ratio'])

    times = ["60", "45", "30"]
    concs = ["5,", "2", "1"]
    treatments = ["N", "T"]

    n_colors = len(times)
    blues = plt.cm.Blues(np.linspace(0.25, 0.75, n_colors))
    reds = plt.cm.Reds(np.linspace(0.25, 0.75, n_colors))
    cmap = [blues, reds]

    plt.figure()
    for i, T in enumerate(times):
        plt.title("Average Peak Ratios")
        for j, Tr in enumerate(treatments):
            x = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            y = frame['Average Peak Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            plt.plot(np.asarray(x, dtype=float), np.asarray(y, dtype=float),
                     label="Time = {}, Treatment = {}".format(T, Tr), color=cmap[j][i])
        plt.xlabel("Concentration ($\mu$L)")
        plt.ylabel("Average Peak Height")
        plt.legend(loc='best')
    if not show:
        plt.savefig("AveragePeakRatios.png")

    plt.figure()
    for i, T in enumerate(times):
        plt.title("Area Ratios")
        for j, Tr in enumerate(treatments):
            x = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            y = frame['Area Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            plt.plot(np.asarray(x, dtype=float), np.asarray(y, dtype=float),
                     label="Time = {}, Treatment = {}".format(T, Tr), color=cmap[j][i])
        plt.xlabel("Concentration ($\mu$L)")
        plt.ylabel("Area Ratio")
        plt.legend(loc='best')
    if not show:
        plt.savefig("AreaRatio.png")
    else:
        plt.show()
