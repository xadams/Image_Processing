import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


def plot_FA(inputfiles, show=False):
    peak_per_exp = []
    area_per_exp = []
    for inp in inputfiles:
        results = []
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
                                      'Area Ratio', 'Replica']).sort_values(by=['Concentration','Treatment'])
        # TODO:Add check that flags if times,concs, or treatments are unexpected values
        times = frame.Time.unique()
        treatments = frame.Treatment.unique()

        n_colors = len(times)
        blues = plt.cm.Blues(np.linspace(0.25, 0.75, n_colors))
        reds = plt.cm.Reds(np.linspace(0.25, 0.75, n_colors))
        cmap = [blues, reds]

        plt.figure()
        for i, T in enumerate(times):
            plt.title("Average Ratio of Green to Red Intensity Peak Heights")
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
                    peak_per_exp.append([x, y_samples.mean(), T, Tr, inp[5:11]])
                plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float),
                             label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
            plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
        if not show:
            inputbase = input.split('_')[0]
            plt.savefig(inputbase + "_PeakHeightRatios.png")

        plt.figure()
        for i, T in enumerate(times):
            plt.title("Average Ratio of Green to Red Intensity Peak Areas")
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
                    area_per_exp.append([x, y_samples.mean(), T, Tr, inp[5:11]])
                plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float),
                             label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
            plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.ylabel("Ratio of Green to Red Intensity")
            # plt.legend(loc='lower right')
        if not show:
            plt.savefig(inputbase + "_AreaRatio.png")

    if len(inputfiles) > 1:
        peaks = pd.DataFrame(peak_per_exp,
                             columns=['Concentration', 'Ratio', 'Time', 'Treatment', 'Experiment']).sort_values(
            by=['Concentration'])
        areas = pd.DataFrame(area_per_exp,
                             columns=['Concentration', 'Ratio', 'Time', 'Treatment', 'Experiment']).sort_values(
            by=['Concentration'])
        plt.figure()
        for i, T in enumerate(times):
            plt.title("Average Ratio of Green to Red Intensity Peak Heights Across Experiments")
            for j, Tr in enumerate(treatments):
                xbar = []
                ybar = []
                yerr = []
                x_samples = peaks['Concentration'][(peaks['Time'] == T) & (peaks['Treatment'] == Tr)]
                for x in x_samples.unique():
                    y_samples = np.asarray(
                        peaks['Ratio'][(peaks['Time'] == T) & (peaks['Treatment'] == Tr) & (
                                peaks['Concentration'] == x)], dtype=float)
                    xbar.append(x)
                    ybar.append(y_samples.mean())
                    yerr.append(y_samples.std())
                plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float),
                             label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
            plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
    plt.figure()

    for i, T in enumerate(times):
        plt.title("Average Ratio of Green to Red Intensity Peak Heights Across Experiments")
        for j, Tr in enumerate(treatments):
            xbar = []
            ybar = []
            yerr = []
            x_samples = areas['Concentration'][(areas['Time'] == T) & (areas['Treatment'] == Tr)]
            for x in x_samples.unique():
                y_samples = np.asarray(
                    areas['Ratio'][(areas['Time'] == T) & (areas['Treatment'] == Tr) & (
                            areas['Concentration'] == x)], dtype=float)
                xbar.append(x)
                ybar.append(y_samples.mean())
                yerr.append(y_samples.std())
            plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                         yerr=np.asarray(yerr, dtype=float),
                         label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
        plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
        plt.ylabel("Ratio of Green to Red Intensity")
        plt.legend(loc='best')

    if show:
        plt.show()