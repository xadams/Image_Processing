import pandas as pd
import sys
import numpy as np
import rampy
from scipy import signal
import csv
from plotting import plot_FA, PlotComparison
import os
import matplotlib.pyplot as plt
import warnings

# Dictionary Keywords
PEAK_RATIO_AVG = 'Average Peak Ratio'
PEAK_RATIO_STD = 'Peak Ratio Standard of Deviation'
AREA_RATIO = 'Area Ratio'
TIME = 'Time'
CONC = 'Concentration'
TREATMENT = 'Treatment'
REPLICA = 'Replica'
DATE = 'Date'
ENV = 'Environment'
FIELD_NAMES = [CONC, TIME, TREATMENT, ENV, DATE, REPLICA, PEAK_RATIO_AVG, PEAK_RATIO_STD,
                                       AREA_RATIO]

def proc_sheet(filename, outname, plot_peaks=False):
    data = pd.ExcelFile(filename)
    results = []
    # for title in ["60min 1uL Treated"]:
    for title in data.sheet_names:
        s = pd.read_excel(data, title).dropna(thresh=3)
        if 'CY3(1)' in s.columns:
            red = s['CY3(1)'].values
            green = s['FITC(1)'].values
        elif 'Ch1' in s.columns:
            if int(s['Ch1'].mean()) > int(s['Ch2'].mean()):
                red = s['Ch1'].values
                green = s['Ch2'].values
            else:
                green = s['Ch1'].values
                red = s['Ch2'].values
        else:
            print("Neither 'CY3(1)' nor 'Ch1' columns detected. Exiting")
            exit(2)
            # TODO: Make this exit in a more pythonic way
        n = len(red)
        xval = np.linspace(0, n - 1, n)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            bounds = np.array([[0, 1500], [1500, 1600]])
            red_corrected, red_background = rampy.baseline(xval, red, bounds, "arPLS")
            green_corrected, green_background = rampy.baseline(xval, green, bounds, "arPLS")
            red_peaksx, red_peaksy = signal.find_peaks(red_corrected[:, 0], width=10, distance=1, height=1)
            green_peaksx, green_peaksy = signal.find_peaks(green_corrected[:, 0], width=10, distance=1, height=1)
        if len(red_peaksx) != len(green_peaksx):
            # print("Mismatch in number of peaks: {} red peaks vs {} green peaks\nWill attempt to align".format(n_red_peaks,n_green_peaks))
            aligned_green_peaks = []
            for i, red_peak in enumerate(red_peaksx):
                min = 20
                for j, green_peak in enumerate(green_peaksx):
                    difference = abs(red_peak - green_peak)
                    if difference < min:
                        min = difference
                        index = j
                if min == 20:
                    aligned_green_peaks.append([red_peaksx[i], green_corrected[red_peaksx[i]]])
                else:
                    aligned_green_peaks.append([green_peaksx[index], green_peaksy['peak_heights'][index]])
            garray = np.asarray(aligned_green_peaks)
            green_peaksy['peak_heights'] = garray[:, 1]
            green_peaksx = garray[:, 0]

        peak_ratio = green_peaksy['peak_heights'] / red_peaksy['peak_heights']
        area_ratio = np.trapz(green_corrected, axis=0) / np.trapz(red_corrected, axis=0)
        # Variable region for each experiment sheet naming scheme
        sheetname = title.split(' ')
        conc = sheetname[0]
        treatment_code = sheetname[2][0]
        if  treatment_code == 'u':
            tr = 'Radiation-'
        elif treatment_code == 'z':
            tr = 'Radiation+'
        rep = sheetname[-1]
        date = filename[5:11]
        ti = sheetname[3]
        env = "Cytospin"
        result = {CONC: conc, TIME: ti, TREATMENT: tr, ENV: env, DATE: date, REPLICA: rep,
                  PEAK_RATIO_AVG: peak_ratio.mean(), PEAK_RATIO_STD: peak_ratio.std(), AREA_RATIO: area_ratio[0], }
        results.append(result)
        # PLOT_RAW = True
        if plot_peaks:
            fig, ax = plt.subplots()
            try:
                if PLOT_RAW:
                    ax.plot(red, color='red')
                    ax.plot(green, color='green')
            except NameError:
                ax.set_title(title)
                ax.plot(red_corrected, color='red')
                ax.scatter(red_peaksx, red_peaksy['peak_heights'], color=plt.cm.Reds([0.75]), marker='o')
                ax.plot(green_corrected, color='green')
                ax.scatter(green_peaksx, green_peaksy['peak_heights'], color='darkgreen', marker='o')
                ax.set_xlabel("Length (μm)")
                ax.set_ylabel("Intensity")
                # textstr = '\n'.join((
                #     'Average peak ratio=%.2f' % (peak_ratio.mean(),),
                #     'Peak ratio std=%.2f' % (peak_ratio.std(),),
                #     'Area ratio=%.2f' % (area_ratio[0],)))
                # ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
                #          fontsize=14, verticalalignment='top')
        plt.show()

    with open(outname, "w") as csvfile:
        w = csv.DictWriter(csvfile,
                           fieldnames=FIELD_NAMES)
        w.writeheader()
        for result in results:
            w.writerow(result)


def main():
    filename = "data/190328cytospin.xlsx"
    outname = os.path.splitext(filename)[0] + "_result_summary.csv"
    # Comment following line in for peak graphs and debugging
    # proc_sheet(filename,outname, True)
    if not os.path.isfile(outname):
        proc_sheet(filename, outname, False)
    # plot_FA([outname], show=False)
    # PlotComparison(["data/erastin_result_summary.csv","data/190321zappedinwells_result_summary.csv",outname], show=False)


if __name__ == "__main__":
    status = main()
    sys.exit(status)
