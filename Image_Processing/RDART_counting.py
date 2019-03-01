import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import rampy
import warnings
import csv

PLOT = False
RED_LABEL = 'CY3(1)'
GREEN_LABEL = 'FITC(1)'
PINK_LABEL = 'CY5(1)'
COLUMN_TITLES = ["Index", "Peak Ratio", "Green Test", "Red Test", "Pink Background", "Pink Max"]

# filename = 'data/RDART004baseline_testcase.xlsx'
filename = 'data/RDART004baseline.xlsx'


data = pd.ExcelFile(filename)
s = pd.read_excel(data, sheet_name=None)
ind_list = []
distance_list = []
blue_list = []
green_list = []
red_list = []
pink_list = []
results = {}
for sheet in data.sheet_names:
    # TODO: combine individual lists into a single dataframe for more efficient manipulation
    ind_list.append(s[sheet]['No.'])
    distance_list.append(s[sheet]['Distance [µm]'])
    blue_list.append(s[sheet]['DAPI(1)'])
    green_list.append(s[sheet]['FITC(1)'])
    red_list.append(s[sheet]['CY3(1)'])
    pink_list.append(s[sheet]['CY5(1)'])
ind = pd.concat(ind_list)
distance = pd.concat(distance_list)
blue = pd.concat(blue_list)
green = pd.concat(green_list)
red = pd.concat(red_list)
pink = pd.concat(pink_list)
globalmaxgreen = green.max()

cols = [blue, green, red, pink]
colors = ['mediumblue', 'limegreen', 'crimson', 'hotpink']
edges = np.argwhere(ind == 1)
for i, num in enumerate(edges):
    if PLOT:
        plt.figure()
    if len(edges) > i + 1:
        end = edges[i + 1]
    else:
        end = [len(distance)]
    x = distance[num[0]:end[0]]
    for col, color in zip(cols, colors):
        raw = col[num[0]:end[0]]
        n = len(raw)
        bound = np.array([[x.iloc[0], 50], [50, x.iloc[-1]]])
        if col.name == RED_LABEL:
            maxred = raw.max()
            ratio = maxgreen / maxred
            if maxgreen < globalmaxgreen / 3:
                greentest = True
            else:
                greentest = False
            if maxred > maxgreen + 100:
                redtest = True
            else:
                redtest = False
        if col.name == GREEN_LABEL:
            maxgreen = raw.max()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y, background = rampy.baseline(np.asarray(x), np.asarray(raw), bound, "arPLS")
        if col.name == PINK_LABEL:
            pinkbackground = background.mean()
            pinkmax = y.max()
        if PLOT:
            plt.plot(x, y, color=color)
    if PLOT:
        plt.show()
    results[i] = [ratio, greentest, redtest, pinkbackground, pinkmax]

w = csv.writer(open("RDART_counting_summary_test.csv", "w"))
w.writerow(COLUMN_TITLES)
for key, val in results.items():
    w.writerow([key, val])
