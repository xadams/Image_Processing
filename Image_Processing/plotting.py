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
    # TODO:Add check that flags if times,concs, or treatments are unexpected values
    times = frame.Time.unique()
    concs = frame.Concentration.unique()
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
                     label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
        plt.xlabel("Concentration ($\mu$M)")
        plt.ylabel("Average Peak Height Ratio")
        plt.legend(loc='best')
    if not show:
        plt.savefig("PeakHeightRatios.png")

    plt.figure()
    for i, T in enumerate(times):
        plt.title("Area Ratios")
        for j, Tr in enumerate(treatments):
            x = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            y = frame['Area Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            plt.plot(np.asarray(x, dtype=float), np.asarray(y, dtype=float),
                     label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
        plt.xlabel("Concentration ($\mu$M)")
        plt.ylabel("Average Peak Area Ratio")
        plt.legend(loc='lower right')
    if not show:
        plt.savefig("AreaRatio.png")
    else:
        plt.show()
