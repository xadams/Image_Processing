import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import numpy as np
import rampy
from scipy import signal
import os
import csv

data = pd.ExcelFile ('data/180808ferropdata.xlsm')
results = {}
for title in data.sheet_names:
    s = pd.read_excel(data, title).dropna(thresh=3)
    red_len = []
    green_len = []
    if int(s['Ch1'].mean()) > int(s['Ch2'].mean()):
        red = s['Ch1'].values
        green = s['Ch2'].values
    else:
        green = s['Ch1'].values
        red = s['Ch2'].values
    n = len(red)
    xval = np.linspace(0,n-1,n)

    reddata= np.c_[xval,red]
    greendata = np.c_[xval,green]
    bounds = np.array([[0,1500],[1500,1600]])
    red_corrected, red_background = rampy.baseline(xval,red,bounds,"arPLS")
    green_corrected, green_background = rampy.baseline(xval, green,bounds,"arPLS")
    red_peaksx,red_peaksy = signal.find_peaks(red_corrected[:,0],width=10,distance=10,height=1)
    green_peaksx,green_peaksy = signal.find_peaks(green_corrected[:,0],width=10,distance=10,height=1)

    n_red_peaks = len(red_peaksx)
    n_green_peaks = len(green_peaksx)
    if n_red_peaks != n_green_peaks:
        # print("Mismatch in number of peaks: {} red peaks vs {} green peaks\nWill attempt to align".format(n_red_peaks,n_green_peaks))
        aligned_green_peaks = []
        for i, red_peak in enumerate(red_peaksx):
            min = 20
            for j, green_peak in enumerate(green_peaksx):
                difference = abs(red_peak-green_peak)
                if difference < min:
                    min = difference
                    index = j
            if min == 20:
                aligned_green_peaks.append([red_peaksx[i], green_corrected[red_peaksx[i]]])
            else:
                aligned_green_peaks.append([green_peaksx[index],green_peaksy['peak_heights'][index]])
        garray = np.asarray(aligned_green_peaks)
        green_peaksx = garray[:,0]
        green_peaksy['peak_heights'] = garray[:,1]
        # if n_red_peaks == len(green_peaksx):
        #     print("Found equal number of red and green peaks.")
        # else:
            # print("Could not select an appropriate set of green peaks.")

    peak_ratio = green_peaksy['peak_heights'] / red_peaksy['peak_heights']
    # print("Peak ratio average: {}\nPeak ratio std: {}".format(peak_ratio.mean(), peak_ratio.std()))
    area_ratio = np.trapz(green_corrected,axis=0)/np.trapz(red_corrected,axis=0)
    # print("Peak area average: {}".format(area_ratio[0]))
    results[title] = [peak_ratio.mean(),peak_ratio.std(),area_ratio[0]]
    # PLOT_RAW = True
    # try:
    #     if PLOT_RAW:
    #         ax.plot(red, color='red')
    #         ax.plot(green, color='green')
    # except:
    #     ax.set_title(title)
    #     ax.plot(red_corrected, color='red')
    #     ax.scatter(red_peaksx,red_peaksy['peak_heights'], color='blue', marker='o')
    #     ax.plot(green_corrected, color='green')
    #     ax.scatter(green_peaksx,green_peaksy['peak_heights'], color='orange', marker='o')
    #     textstr = '\n'.join((
    #         'Average peak ratio=%.2f' % (peak_ratio.mean(),),
    #         'Peak ratio std=%.2f' % (peak_ratio.std(),),
    #         'Area ratio=%.2f' % (area_ratio[0],)))
    #     ax.text(0.05, 0.95, textstr, transform=ax.transAxes,
    #              fontsize=14, verticalalignment='top')

# plt.show()

w = csv.writer(open("result_summary.csv", "w"))
for key, val in results.items():
    w.writerow([key, val])