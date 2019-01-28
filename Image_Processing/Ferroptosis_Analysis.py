import pandas as pd
import matplotlib.pyplot as plt
import sys
import argparse
import numpy as np
import rampy
from scipy import signal
import os

#ReadExcel = pd.read_excel ('Ferroptosis Data/1810006 RT+- Data.xlsx') #for an earlier version of Excel, you may need to use the file extension of 'xls'
data = pd.ExcelFile ('Ferroptosis Data/180808ferropdata.xlsm')
#overview = pd.read_excel(data, 'Summary')
s1 = pd.read_excel(data, '60min 5uL Treated')
s2 = pd.read_excel(data, '60min 5uL No Treatment')
s1 = s1.iloc[:,:].values
s2 = s2.iloc[:,:].values

red = s1[:,6]
green = s1[:,7]

n = len(red)

xval = np.linspace(0,n-1,n)

reddata= np.c_[xval,red]
greendata = np.c_[xval,green]

roi1 = reddata
roi2 = greendata

#ry, rbase = rampy.baseline(xval, reddata, roi1, 'poly', polynomial_order=1)
#gy, gbase = rampy.baseline(xval, greendata, roi2, 'poly', polynomial_order=1)


redno = s2[:,6]
greenno = s2[:,5]



#shift = np.divide(green,red)
#shiftno = np.divide(greenno,redno)

plt.plot(red, color='red')
plt.plot(green, color='green')
#plt.plot(shift)
#plt.plot(shiftno)
plt.show()


