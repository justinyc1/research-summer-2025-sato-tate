import time
import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import integrate
from numpy import cos, pi
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 1000

print_info = True # print info on every M_n calculation
p = 3

m = p*p
d = round((p+1)/2)
file_path = "/outputs/max_relation_csvs/"
file_subpath = "p_0_to_100/"
file_name = f"p_{p}_m_{m}_d_{d}.csv"

def get_pattern(full_path):
    data = pd.read_csv(full_path).columns.values
    array = [None] * len(data)

    for i in range(0, len(data)):
        array[i] = int(data[i])

    return sorted(array, key=abs)

def eval_integral(pattern, n, print_info=False):
    signs = np.sign(pattern)
    prefix = ((Decimal(2)**Decimal(n))/((Decimal(2)*Decimal(pi))**Decimal((3))))
    function = lambda *d: (sum(cos(d_i) for d_i in d) + cos(sum(s * d_i for s, d_i in zip(signs, d))))**n
    limits = [(0, 2*pi)] * len(signs)

    start_time = time.time()
    integral_results = integrate.nquad(function, limits, full_output=True)
    unrounded_result = prefix * Decimal(integral_results[0])
    
    rounded_result = unrounded_result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    rounded_result = abs(rounded_result) if rounded_result == -0.0 else rounded_result
    
    if print_info:
        elapsed_time = time.time() - start_time
        print(f"M_n for n={n} evaluates to {rounded_result} (rounded from {unrounded_result:.16f}), after {round(elapsed_time, 3):.3f} seconds")

    return unrounded_result, rounded_result

def get_results(start, end, skip_odd_n=False):
    integer_results = []
    decimal_results = []

    for n in range(start, end+1):
        if skip_odd_n and n % 2 == 1:
            integer_results.append(0)
            decimal_results.append(Decimal(0))
            print(f"M_n for n={n} evaluates to 0 (skipped)")
            continue

        pattern = get_pattern("./JC_code" + file_path + file_subpath + file_name)
        unrounded, rounded = eval_integral(pattern, n, print_info)

        integer_results.append(int(rounded))
        decimal_results.append(rounded)

    return [integer_results, decimal_results]


integer_results, decimal_results = get_results(0, 10, True)

print(integer_results)
# print(decimal_results)