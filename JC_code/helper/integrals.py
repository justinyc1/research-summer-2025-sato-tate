import time
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import integrate

from numpy import cos
from numpy import pi

# func = lambda x0,x1,x2,x3 : x0**2 + x1*x2 - x3**3 + np.sin(x0) + (
#                                 1 if (x0-.2*x3-.5-.25*x1>0) else 0)

# def opts0(*args, **kwargs):
#     return {'points':[0.2*args[2] + 0.5 + 0.25*args[0]]}

# result = integrate.nquad(func, [[0,1], [-1,1], [.13,.8], [-.15,1]],
#                 opts=[opts0,{},{},{}], full_output=True)

# print(result)

"""
variables
"""
def get_results(function, limits, start, end, skip_odd_n=False):
    for n in range(start, end):
        if skip_odd_n and n % 2 == 1:
            results.append(0)
            print(f"M_n for n={n} evaluates to 0")
            continue
        prefix = ((2**n)/((2*pi)**3))

        start_time = time.time()

        integral_results = integrate.nquad(function, limits, full_output=True)
        area = integral_results[0]

        result = prefix * area
        result = round(result, 5)

        result = 0.0 if result == -0.0 else result
        result = int(result) if result.is_integer() else result
        
        elapsed_time = time.time() - start_time

        results.append(result)
        print(f"M_n for n={n} evaluates to {result} after {round(elapsed_time, 3):.3f} seconds")

    print(results)

def output_data(full_path):
    data = pd.read_csv(full_path).columns.values
    array = [None] * len(data)

    for i in range(0, len(data)):
        array[i] = int(data[i])

    print(array)

func_example = lambda d1,d2,d3 : (cos(d1) + cos(d2) + cos(d3))**n
limits_example = [[0,2*pi], [0,2*pi], [0,2*pi]]

func_p_3 = lambda d1,d2,d3 : (cos(d1) + cos(d2) + cos(d3) + cos(-d1 + d2 + d3))**n
limits_p_3 = [[0,2*pi], [0,2*pi], [0,2*pi]]

p = 3
m = p*p
d = round((p+1)/2)
file_path = "../outputs/max_relation_csvs/"
file_subpath = "p_0_to_100/"
file_name = f"p_{p}_m_{m}_d_{d}.csv"
results = []

# get_results(func_p_3, limits_p_3, 0, 21, True)

output_data(file_path + file_subpath + file_name)