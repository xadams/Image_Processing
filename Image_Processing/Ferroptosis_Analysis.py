import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import numpy as np
import rampy
from scipy import signal
import os

#ReadExcel = pd.read_excel ('Ferroptosis Data/1810006 RT+- Data.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
data = pd.ExcelFile ('data/180808ferropdata.xlsm')
#overview = pd.read_excel(data, 'Summary')
s1 = pd.read_excel(data, '60min 5uL Treated').dropna(thresh=3)
s2 = pd.read_excel(data, '60min 5uL No Treatment').dropna(thresh=3)
s1 = s1.iloc[:,:].values
s2 = s2.iloc[:,:].values
# red = s1[:,6]
# green = s1[:,7]
red = s2[:,6]
green = s2[:,5]

n = len(red)
xval = np.linspace(0,n-1,n)

reddata= np.c_[xval,red]
greendata = np.c_[xval,green]
bounds = np.array([[0,1500],[1500,1600]])
red_corrected, red_background = rampy.baseline(xval,red,bounds,"arPLS")
green_corrected, green_background = rampy.baseline(xval, green,bounds,"arPLS")
red_peaksx,red_peaksy = signal.find_peaks(red_corrected[:,0],height=300,distance=32)
green_peaksx,green_peaksy = signal.find_peaks(green_corrected[:,0],height=300,distance=32)


n_red_peaks = len(red_peaksx)
n_green_peaks = len(green_peaksx)
if n_red_peaks != n_green_peaks:
    print("Mismatch in number of peaks: {} red peaks vs {} green peaks\nWill attempt to align".format(n_red_peaks,n_green_peaks))
    aligned_green_peaks = []
    for i, red_peak in enumerate(red_peaksx):
        min = 50
        for j, green_peak in enumerate(green_peaksx):
            difference = abs(red_peak-green_peak)
            if difference < min:
                min = difference
                index = j
        aligned_green_peaks.append([green_peaksx[index],green_peaksy['peak_heights'][index]])
    garray = np.asarray(aligned_green_peaks)
    green_peaksx = garray[:,0]
    green_peaksy['peak_heights'] = garray[:,1]
    if n_red_peaks == len(green_peaksx):
        print("Found equal number of red and green peaks.")
    else:
        print("Could not select an appropriate set of green peaks.")

peak_ratio = red_peaksy['peak_heights'] / green_peaksy['peak_heights']
# print("Peak ratio average: {}\nPeak ratio std: {}".format(peak_ratio.mean(), peak_ratio.std()))
area_ratio = np.trapz(red_corrected,axis=0)/np.trapz(green_corrected,axis=0)
# print("Peak area average: {}".format(area_ratio[0]))

# PLOT_RAW = True
fig, ax = plt.subplots()
try:
    if PLOT_RAW:
        plt.plot(red, color='red')
        plt.plot(green, color='green')
except:
    plt.plot(red_corrected, color='red')
    plt.scatter(red_peaksx,red_peaksy['peak_heights'], color='blue', marker='o')
    plt.plot(green_corrected, color='green')
    plt.scatter(green_peaksx,green_peaksy['peak_heights'], color='orange', marker='o')
    textstr = '\n'.join((
        'Average peak ratio=%.2f' % (peak_ratio.mean(),),
        'Peak ratio std=%.2f' % (peak_ratio.std(),),
        'Area ratio=%.2f' % (area_ratio[0],)))
    plt.text(0.05, 0.95, textstr, transform=ax.transAxes,
             fontsize=14, verticalalignment='top')
    # for i in range(n_red_peaks-1):
    #     vline = (red_peaksx[i]+red_peaksx[i+1])/2
    #     plt.axvline(x=vline, color='blue')
plt.show()

