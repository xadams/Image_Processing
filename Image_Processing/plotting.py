import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


def plot_FA(inputfiles, show=False):
    var1, var2, var3 = 'Time', 'Environment', 'Treatment'  # x, color, shade
    filtervar, filterterm = 'Cell Line', 'HT1080'
    peak_per_exp = []
    area_per_exp = []
    for inp in inputfiles:
        data = pd.read_csv(inp)
        frame = pd.DataFrame(data).sort_values(by=[var1, var2])
        frame = frame[frame[filtervar] == filterterm]
        # TODO:Add check that flags if times,concs, or treatments are unexpected values
        times = frame[var3].unique()
        treatments = frame[var2].unique()

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
                x_samples = frame[var1][(frame[var3] == T) & (frame[var2] == Tr)]
                for x in x_samples.unique():
                    y_samples = np.asarray(
                        frame['Average Peak Ratio'][(frame[var3] == T) & (frame[var2] == Tr) & (
                                frame[var1] == x)], dtype=float)
                    xbar.append(x)
                    ybar.append(y_samples.mean())
                    yerr.append(y_samples.std())
                    peak_per_exp.append([x, y_samples.mean(), T, Tr, inp[5:11]])
                plt.errorbar(np.asarray(xbar), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float), capsize=8,
                             label="{} = {}, {} = {}".format(var3, T, var2, Tr), color=cmap[j][i])
            # plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.xlabel("Incubation Time (min)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
        if not show:
            inputbase = inp.split('_')[0]
            plt.savefig(inputbase + "_PeakHeightRatios.png")

        plt.figure()
        for i, T in enumerate(times):
            plt.title("Average Ratio of Green to Red Intensity Peak Areas")
            for j, Tr in enumerate(treatments):
                xbar = []
                ybar = []
                yerr = []
                x_samples = frame[var1][(frame[var3] == T) & (frame[var2] == Tr)]
                for x in x_samples.unique():
                    y_samples = np.asarray(frame['Area Ratio'][(frame[var3] == T) & (frame[var2] == Tr) & (
                            frame[var1] == x)], dtype=float)
                    xbar.append(x)
                    ybar.append(y_samples.mean())
                    yerr.append(y_samples.std())
                    area_per_exp.append([x, y_samples.mean(), T, Tr, inp[5:11]])
                plt.errorbar(np.asarray(xbar), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float), capsize=8,
                             label="{} = {}, {} = {}".format(var3, T, var2, Tr), color=cmap[j][i])
            # plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.xlabel("Incubation Time (min)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
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
                             yerr=np.asarray(yerr, dtype=float), capsize=8,
                             label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
            plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
        if not show:
            plt.savefig("data/AllExperiments_PeakRatio.png")

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
                             yerr=np.asarray(yerr, dtype=float), capsize=8,
                             label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
            plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
            plt.ylabel("Ratio of Green to Red Intensity")
            plt.legend(loc='best')
        if not show:
            plt.savefig("data/AllExperiments_AreaRatio.png")

    if show:
        plt.show()


def PlotComparison(inputfiles, show=False):
    for i, (inp, exp_name) in enumerate(
            zip(inputfiles, [['Erastin', 'Well Plate'], ['Radiation', 'Well Plate'], ['Radiation', 'Cytospin']])):
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
                                title[-1], inp[5:12]])
        frame = pd.DataFrame(results,
                             columns=['Time', 'Concentration', 'Treatment', 'Average Peak Ratio', 'Peak Ratio std',
                                      'Area Ratio', 'Replica', 'Experiment']).sort_values(
            by=['Concentration', 'Treatment'])
        # TODO:Add check that flags if times,concs, or treatments are unexpected values
        treatments = frame.Treatment.unique()
        if treatments[0] == 't':
            treatments = treatments[::-1]
        concs = ['1', '1.5', '2']

        n_colors = np.linspace(0.4, 0.8, 2)
        blues = plt.cm.Blues(n_colors)
        reds = plt.cm.Reds(n_colors)
        greens = plt.cm.Greens(n_colors)
        cmap = [blues, reds, greens]
        T = '50'
        plt.title("Comparison of Erastin and Radiation Treated HT1080 Cells")
        for j, (Tr, state) in enumerate(zip(treatments, ['-', '+'])):
            xbar = []
            ybar = []
            yerr = []
            for x in concs:
                y_samples = np.asarray(
                    frame['Area Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr) & (
                            frame['Concentration'] == x)], dtype=float)
                if y_samples.any():
                    xbar.append(x)
                    ybar.append(y_samples.mean())
                    yerr.append(y_samples.std())
            if ybar:
                plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
                             yerr=np.asarray(yerr, dtype=float), capsize=8,
                             label="{}{} {}".format(exp_name[0], state, exp_name[1]), color=cmap[i][j])
        plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
        plt.ylabel("Ratio of Green to Red Intensity")
        plt.legend(loc='best')
    if not show:
        inputbase = inp.split('_')[0]
        plt.savefig("Erastin_Radiation_Comparison.png")

    #     plt.figure()
    #     for i, T in enumerate(times):
    #         plt.title("Average Ratio of Green to Red Intensity Peak Areas")
    #         for j, Tr in enumerate(treatments):
    #             xbar = []
    #             ybar = []
    #             yerr = []
    #             x_samples = frame['Concentration'][(frame['Time'] == T) & (frame['Treatment'] == Tr)]
    #             for x in x_samples.unique():
    #                 y_samples = np.asarray(frame['Area Ratio'][(frame['Time'] == T) & (frame['Treatment'] == Tr) & (
    #                         frame['Concentration'] == x)], dtype=float)
    #                 xbar.append(x)
    #                 ybar.append(y_samples.mean())
    #                 yerr.append(y_samples.std())
    #                 area_per_exp.append([x, y_samples.mean(), T, Tr, inp[5:11]])
    #             plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
    #                          yerr=np.asarray(yerr, dtype=float),
    #                          label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
    #         plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
    #         plt.ylabel("Ratio of Green to Red Intensity")
    #         # plt.legend(loc='lower right')
    #     if not show:
    #         plt.savefig(inputbase + "_AreaRatio.png")
    #
    # if len(inputfiles) > 1:
    #     peaks = pd.DataFrame(peak_per_exp,
    #                          columns=['Concentration', 'Ratio', 'Time', 'Treatment', 'Experiment']).sort_values(
    #         by=['Concentration'])
    #     areas = pd.DataFrame(area_per_exp,
    #                          columns=['Concentration', 'Ratio', 'Time', 'Treatment', 'Experiment']).sort_values(
    #         by=['Concentration'])
    #     plt.figure()
    #     treatments = peaks.Treatment.unique()
    #     experiments = peaks.Experiment.unique()
    #     concs = peaks['Concentration'][(peaks['Experiment']=='190328')].unique()
    #     blues = plt.cm.Blues(np.linspace(0.25, 0.75, 3))
    #     reds = plt.cm.Reds(np.linspace(0.25, 0.75, 3))
    #     greens = plt.cm.Greens(np.linspace(0.25,0.75, 3))
    #     cmap = [blues, reds, greens]
    #     treatment_names = ["Untreated", "Erastin", "Radiation"]
    #     experiment_names = ["Well Plate","Well Plate","Cytospin"]
    #     T = '50'
    #     for i, ex in enumerate(experiments):
    #         plt.title("Average Ratio of Green to Red Intensity Peak Heights Across Experiments")
    #         for j, (Tr, name) in enumerate(zip(treatments,treatment_names)):
    #             xbar = []
    #             ybar = []
    #             yerr = []
    #             for x in concs:
    #                 y_samples = np.asarray(
    #                     peaks['Ratio'][(peaks['Time'] == T) & (peaks['Treatment'] == Tr) & (
    #                             peaks['Concentration'] == x) & (peaks['Experiment'] == ex)], dtype=float)
    #                 if y_samples:
    #                     xbar.append(x)
    #                     ybar.append(y_samples.mean())
    #                     yerr.append(y_samples.std())
    #                 else:
    #                     break
    #             if ybar:
    #                 plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
    #                              yerr=np.asarray(yerr, dtype=float),
    #                              label="{},{}".format(name,ex), color=cmap[j][i])
    #     plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
    #     plt.ylabel("Ratio of Green to Red Intensity")
    #     plt.legend(loc='best')
    #     if not show:
    #         plt.savefig("data/Comparison_PeakRatio.png")
    #
    #     plt.figure()
    #     plt.title("Average Ratio of Green to Red Intensity Peak Heights Across Experiments")
    #     for i, ex in enumerate(experiments):
    #         for j, Tr in enumerate(treatments):
    #             xbar = []
    #             ybar = []
    #             yerr = []
    #             for x in concs:
    #                 y_samples = np.asarray(
    #                     areas['Ratio'][(areas['Time'] == T) & (areas['Treatment'] == Tr) & (
    #                             areas['Concentration'] == x) & (areas['Experiment'] == ex)], dtype=float)
    #                 if y_samples:
    #                     xbar.append(x)
    #                     ybar.append(y_samples.mean())
    #                     yerr.append(y_samples.std())
    #                 else:
    #                     break
    #             if ybar:
    #                 plt.errorbar(np.asarray(xbar, dtype=float), np.asarray(ybar, dtype=float),
    #                          yerr=np.asarray(yerr, dtype=float),
    #                          label="Time = {}min, Treatment = {}".format(T, Tr), color=cmap[j][i])
    #     plt.xlabel("Concentration of C11BODIPY ($\mu$M)")
    #     plt.ylabel("Ratio of Green to Red Intensity")
    #     plt.legend(loc='best')
    #     if not show:
    #         plt.savefig("data/Comparison_AreaRatio.png")
    #
    if show:
        plt.show()
