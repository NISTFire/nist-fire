import os
import collections
import numpy as np
import pandas as pd
from pylab import *
import math
import inspect
# from sympy.solvers import solveset
# from sympy import Symbol
# V = Symbol('V')
import sys

exp_file = '../Data/UL_Exp_5_031116_arduino.csv'
data = pd.read_csv(exp_file)
data['HF voltage'] = ''
data['HF new'] = ''
data = pd.DataFrame(data, columns=['TimeStamp', 'Device', 'Plot Time', 
	'T old', 'HF old', 'HF voltage', 'HF new'])
V_T = []
V_HF = []

c1 = 2.508355 * 10**1
c2 = 7.860106 * 10**-2
c3 = -2.503131 * 10**-1
c4 = 8.315270 * 10**-2
c5 = -1.228034 * 10**-2
c6 = 9.804036 * 10**-4
c7 = -4.413030 * 10**-5
c8 = 1.057734 * 10**-6
c9 = -1.052755 * 10**-8 

m_old = 0.308857142857
b_old = 0.00142857142857
m_new = 3.23773867465
b_new = -0.00461250467989

zero_voltage = 0
HF_zero = []

for index, row in data.iterrows():
	T = row[3]
	HF_old = row['HF old']

	HF_voltage = (HF_old-b_old)/m_old

	if row['Plot Time'] == 0:
		HF_zero.append(HF_voltage)
		zero_voltage = np.mean(HF_zero)

	HF_new = (HF_voltage-zero_voltage)*m_new + b_new

	data.loc[index, 'HF new'] = HF_new
	data.loc[index, 'HF voltage'] = HF_voltage

data.to_csv('../Data/UL_Exp_5_031116_revised.csv')