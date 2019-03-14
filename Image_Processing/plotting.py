import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


def plot_FA(inputfiles, show=False):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    results = []
    for inp in inputfiles:
        with open(inp, "rt") as csvfile:
            fin = csv.reader(csvfile)
            for row in fin:
                title = row[0].split()
                # results.append([title[0][0:2], title[1][0], title[2][0], # This slicing works for the sheet titles in 180808
                results.append([title[3], title[0], title[2][0],
                                row[1].split()[0].strip(",").strip("["),
                                row[1].split()[1].strip(",").strip("["),
                                row[1].split()[2].strip(",").strip("]"),  # ])
                                title[5]])
    frame = pd.DataFrame(results,
                         columns=['Time', 'Concentration', 'Treatment', 'Average Peak Ratio', 'Peak Ratio std',
                                  'Area Ratio', 'Replica']).sort_values(by=['Concentration'])
    # TODO:Add check that flags if times,concs, or treatments are unexpected values
    times = frame.Time.unique()
    treatments = frame.Treatment.unique()

    n_colors = len(times)
    blues = plt.cm.Blues(np.linspace(0.25, 0.75, n_colors))
    reds = plt.cm.Reds(np.linspace(0.25, 0.75, n_colors))
    cmap = [blues, reds]

    for i, T in enumerate(times):
        ax1.set_title("Average Ratio of Green to Red Intensity Peak Heights")
        for j, Tr in enumerate(treatments):
            xbar = []
            ybar = []
            yerr = []
            x_samples = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            for x in x_samples.unique():
                y_samples = np.asarray(
                    frame['Average Peak Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr) & (
                            frame['Concentration'] == x)], dtype=float)
                xbar.append(x)
                ybar.append(y_samples.mean())
                yerr.append(y_samples.std())
            ax1.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                         yerr=np.asarray(yerr, dtype=float),
                         label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
        ax1.set_xlabel("Concentration of C11BODIPY ($\mu$M)")
        ax1.set_ylabel("Ratio of Green to Red Intensity")
        ax1.legend(loc='best')
    if not show:
        inputbase = input.split('_')[0]
        plt.savefig(inputbase + "_PeakHeightRatios.png")

    for i, T in enumerate(times):
        ax2.set_title("Average Ratio of Green to Red Intensity Peak Areas")
        for j, Tr in enumerate(treatments):
            xbar = []
            ybar = []
            yerr = []
            x_samples = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
            for x in x_samples.unique():
                y_samples = np.asarray(frame['Area Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr) & (
                        frame['Concentration'] == x)], dtype=float)
                xbar.append(x)
                ybar.append(y_samples.mean())
                yerr.append(y_samples.std())
            ax2.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                         yerr=np.asarray(yerr, dtype=float),
                         label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
        ax2.set_xlabel("Concentration of C11BODIPY ($\mu$M)")
        ax2.set_ylabel("Ratio of Green to Red Intensity")
        # plt.legend(loc='lower right')
    if not show:
        plt.savefig(inputbase + "_AreaRatio.png")
    else:
        plt.show()
