import time, os
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import integrate
from numpy import cos, pi
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 100

from formulas_for_scipy import get_scipy_formula
from formulas_for_sympy import eval_integral_using_sympy

# default values:

ZEROTH_MOMENT_RESULT = 1
ODD_MOMENT_RESULT = 0

P = 7

B = 0 # leave as is
B_START, B_END = 0, 0

N = 0 # leave as is
N_START, N_END = 6, 22

print_info = True # print info on every M_n calculation
print_time = False
p = P

m = p*p
d = round((p+1)/2)

def round_to_int(unrounded):
    if isinstance(unrounded, int):
        return unrounded
    result = Decimal(unrounded).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    result = abs(result) if result == -0.0 else result
    return result

def enriched_time(time):
    date_time = datetime.fromtimestamp(time)

    return date_time.strftime('%Y-%m-%d %H:%M:%S')

"""
takes in p, b, n, gets the limits, prefix, function to evaluate the integral (if not an edge case)
returns the result (unrounded)
"""
def eval_integral_scipy(p, b, n):
    limits, prefix, function = get_scipy_formula(p, b, n)

    if n == 0:
        return ZEROTH_MOMENT_RESULT
    if n % 2 == 1:
        return ODD_MOMENT_RESULT
    if limits is None or prefix is None or function is None:
        return 0
    
    integral_output = integrate.nquad(function, limits, full_output=True)
    result = prefix * Decimal(integral_output[0])
    
    return result

def eval_integral_sympy(p, b, n):
    result = eval_integral_using_sympy(p, n)
    result = float(result)
    if result is None:
        print(f"error occurred when trying to evaluate integral for p = {p}, b = {b}, n = {n}")
    
    return result

"""
takes in p, b, n, n_start, n_end, evaluate results for a U*gamma^b function given b, from n_start to n_end (inclusive) 
uses sympy when p != 3 and b = 0, otherwise uses scipy
returns a dictionary where keys = n = {n_start, ..., n_end}, values = {U*gamma^b(n_start), ..., U*gamma^b(n_end)}
"""
def eval_moments_with_n_range(p, b, n, n_start=N_START, n_end=N_END, skip_odd_n=False, print_info=False, print_time=False):
    n_moments = {}
    
    for n in range(n_start, n_end+1):
        if skip_odd_n and n % 2 == 1:
            n_moments[n] = ODD_MOMENT_RESULT
            print(f"M_n for n={n} evaluates to 0 (skipped)")
            continue
        
        start_time = time.time()
        print(f"evaluating for p={p} b={b} n={n} starting at {enriched_time(start_time)}")
        result = eval_integral_sympy(p, b, n) if b == 0 and p != 3 else eval_integral_scipy(p, b, n)
        n_moments[n] = result
    
        if print_info:
            print(f"M_n for n={n} evaluates to {round_to_int(result)} (rounded from {result:.10f}){f", after {round((time.time() - start_time), 3):.3f} seconds" if print_time else ""}")

    return n_moments

"""
takes in p, b, n, b_start, b_end, evaluates results for all b functions in for U*gamma^b, from from b_start to b_end (inclusive)
by default, [b_start, b_end] covers the possible range of b
returns a dictionary where keys = b = {b_start, ..., b_end}, values = {dict(U*gamma^b_start(n)), ..., dict(U*gamma^b_end(n))}
"""
def eval_UGammaB_with_b_range(p, b, n, b_start=0, b_end=-1, skip_odd_n=False, print_info=False, print_time=False):
    if b_end == -1:
        b_end = p*(p-1)-1
        
    b_moments = {}
    for b in range(b_start, b_end+1):
        start_time = time.time()
        n_moments = eval_moments_with_n_range(p, b, n, N_START, N_END, skip_odd_n, print_info, print_time)
        b_moments[b] = n_moments
        
        if print_info:
            print(f"Moments for b = {b} evaluated){f" after {round((time.time() - start_time), 3):.3f} seconds" if print_time else ""}")
    
    return b_moments

"""
takes in the b_moments = {b, {n, nth_moment}} dict to compute averages
returns dict averages = {n, nth_moment_average}
"""
def eval_average_moment_stats_for_b(b_moments):
    count = len(b_moments.keys())
    
    sums = {}
    for n_moments in b_moments.values():
        for n, moment in n_moments.items():
            sums[n] = sums.get(n, 0) + moment
    
    averages = {}
    for n, sum in sums.items():
        averages[n] = round_to_int(sum) / count
    
    return averages

"""
takes in a 2d dictionary and averages, format print the data in neat columns
"""
def pretty_print(dict_of_dict, averages):
    print("=========")
    keys = set()
    for inner_dict in dict_of_dict.values():
        keys.update(inner_dict.keys())
    keys = sorted(keys)

    max_widths = {}
    for key in keys:
        max_width = max(len(str(round_to_int(dict_of_dict[outer].get(key, 0)))) for outer in dict_of_dict)
        max_widths[key] = max_width

    b = B_START
    for outer_key, inner_dict in dict_of_dict.items():
        print(f"b = {b:<3}:    ", end="")
        for key in keys:
            val = round_to_int(inner_dict.get(key, 0))
            width = max_widths[key]
            print(f"{key}: {str(val):<{width}}    ", end="")
        b += 1
        print()
    print()
    
    print("Average:    ", end="")
    for key in keys:
        val = round_to_int(averages.get(key, 0))
        width = max_widths[key]
        print(f"{key}: {str(val):<{width}}    ", end="")
    print()
        
"""
takes in p, evaluate and get all moments
returns a dict = {b = [b_start=0, b_end=p*(p-1)], {n = [n_start, n_end], nth_moment = [n_start, n_end]}}
"""
def moment_stats(p):
    unrounded_results = eval_UGammaB_with_b_range(p, B, N, B_START, B_END, True, True, True)
    averages = eval_average_moment_stats_for_b(unrounded_results)
    pretty_print(unrounded_results, averages)
    
moment_stats(P)
    

