#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
data_proc.py
Processing data for kirigami touch sensor

Handles the primary functions
"""

import sys
import argparse
import numpy as np
import rampy
from scipy import signal
import matplotlib.pyplot as plt
import os

SUCCESS = 0
IO_ERROR = 2
DEFAULT_DATA_FILE_NAME = 'data.csv'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def data_process(data_array):

    """
    1. Remove first 500 and last 600 value for each data
    and make a new matrix - useful_data
    2. correct base line - corrected_data
    3. using filter, smooth the graph - filtered_data
    """
    num_data, num_sensor = data_array.shape
    # print("data array is ", num_data, num_sensor)

    time = data_array[500:num_data - 600, 0]
    kiri_1 = data_array[500:num_data - 600, 1]
    kiri_2 = data_array[500:num_data - 600, 2]
    kiri_3 = data_array[500:num_data - 600, 3]
    kiri_4 = data_array[500:num_data - 600, 4]
    kiri_5 = data_array[500:num_data - 600, 5]
    kiri_6 = data_array[500:num_data - 600, 6]
    roi = np.array([[1, 2], [5, 5.5], [9.5, 10]])

    useful_data = np.column_stack((kiri_1, kiri_2, kiri_3, kiri_4, kiri_5, kiri_6))
    # print("useful_data is ", useful_data.shape, type(useful_data))

    y1, base1 = rampy.baseline(time, kiri_1, roi, 'poly', polynomial_order=1)
    y2, base2 = rampy.baseline(time, kiri_2, roi, 'poly', polynomial_order=1)
    y3, base3 = rampy.baseline(time, kiri_3, roi, 'poly', polynomial_order=1)
    y4, base4 = rampy.baseline(time, kiri_4, roi, 'poly', polynomial_order=1)
    y5, base5 = rampy.baseline(time, kiri_5, roi, 'poly', polynomial_order=1)
    y6, base6 = rampy.baseline(time, kiri_6, roi, 'poly', polynomial_order=1)

    base = np.column_stack((base1, base2, base3, base4, base5, base6))

    corrected_data = np.zeros((len(time), 6))
    filtered_data = np.zeros((len(time), 6))
    for x in range(6):
        corrected_data[:, x] = useful_data[:, x] - base[:, x]
        filtered_data[:, x] = signal.savgol_filter(corrected_data[:, x], 11, 5)

    processed_data = np.column_stack((time, filtered_data))

    return processed_data


def peak_find(processed_data):

    peaks1, _ = signal.find_peaks(processed_data[:, 1], distance=200)
    peaks2, _ = signal.find_peaks(processed_data[:, 2], distance=200)
    peaks3, _ = signal.find_peaks(processed_data[:, 3], distance=200)
    peaks4, _ = signal.find_peaks(processed_data[:, 4], distance=200)
    peaks5, _ = signal.find_peaks(processed_data[:, 5], distance=200)
    peaks6, _ = signal.find_peaks(processed_data[:, 6], distance=200)

    peaks = np.column_stack((peaks1, peaks2, peaks3, peaks4, peaks5, peaks6))
    np.savetxt('peaks.csv', peaks, delimiter=',')
    print("Wrote file: {}".format('peaks.csv'))

    return peaks


def plot_processed(base_f_name, processed_data, peaks):

    x_axis = processed_data[:, 0]
    plt.plot(x_axis, processed_data[:, 1], 'r',
             x_axis[peaks[:, 0]], processed_data[:, 1][peaks[:, 0]], "o", markeredgecolor='r', markerfacecolor='None')
    plt.plot(x_axis, processed_data[:, 2], 'b',
             x_axis[peaks[:, 1]], processed_data[:, 2][peaks[:, 1]], "o", markeredgecolor='b', markerfacecolor='None')
    plt.plot(x_axis, processed_data[:, 3], 'g',
             x_axis[peaks[:, 2]], processed_data[:, 3][peaks[:, 2]], "o", markeredgecolor='g', markerfacecolor='None')
    plt.plot(x_axis, processed_data[:, 4], 'y',
             x_axis[peaks[:, 3]], processed_data[:, 4][peaks[:, 3]], "o", markeredgecolor='y', markerfacecolor='None')
    plt.plot(x_axis, processed_data[:, 5], 'c',
             x_axis[peaks[:, 4]], processed_data[:, 5][peaks[:, 4]], "o", markeredgecolor='c', markerfacecolor='None')
    plt.plot(x_axis, processed_data[:, 6], 'k',
             x_axis[peaks[:, 5]], processed_data[:, 6][peaks[:, 5]], "o", markeredgecolor='k', markerfacecolor='None')

    plt.title('Kirigami Touch Sensor')
    plt.xlabel('Time')
    plt.ylabel('Sensor Intensity')
    out_name = base_f_name + ".png"
    plt.savefig(out_name)
    print("Wrote file: {}".format(out_name))


def parse_cmdline(argv):

    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv_data_file", help="The location of csv file with data to analyze",
                        default=DEFAULT_DATA_FILE_NAME)
    args = None
    try:
        args = parser.parse_args(argv)
        args.csv_data = np.loadtxt(fname=args.csv_data_file, delimiter=',')
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR

    return args, SUCCESS


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret

    processed_data = data_process(args.csv_data)
    peaks = peak_find(processed_data)

    # get the name of the input file without the directory it is in, if one was specified
    base_out_fname = os.path.basename(args.csv_data_file)
    # get the first part of the file name (omit extension) and add the suffix
    base_out_fname = os.path.splitext(base_out_fname)[0] + '_processed'
    # add suffix and extension
    out_fname = base_out_fname + '.csv'
    np.savetxt(out_fname, processed_data, delimiter=',')
    print("Wrote file: {}".format(out_fname))
    # send the base_out_fname and data to a new function that will plot the data

    plot_processed(base_out_fname, processed_data, peaks)

    return SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
