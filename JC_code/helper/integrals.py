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
p = 5

m = p*p
d = round((p+1)/2)
file_path = "/outputs/max_relation_csvs/"
file_subpath = "p_0_to_100/"
file_name = f"p_{p}_m_{m}_d_{d}.csv"

def get_patterns(path, p, m, d):
    data = pd.read_csv(path + f"p_{p}_m_{m}_d_{d}.csv")

    header_numbers = [int(x) for x in list(data.columns)]
    patterns = [header_numbers] + data.values.tolist()

    for pattern in patterns:
        pattern.sort(key=abs)

    return patterns

# print(get_pattern("./JC_code" + file_path + file_subpath, p, m, d)) # DEBUG

def eval_integral(patterns, n, print_info=False):
    array_of_signs = [np.sign(pattern).tolist() for pattern in patterns]
    signs_dict = {}
    for pattern, signs in zip(patterns, array_of_signs):
        for val, sign in zip(pattern, signs):
            signs_dict[abs(val)] = sign

    prefix = ((Decimal(2)**Decimal(n))/((Decimal(2)*Decimal(pi))**Decimal((3))))

    num_normal = ((p-1)/2)*p
    num_total = ((p**2)-1)/2

    function = lambda *d: (
        sum(cos(d[i]) for i in range(0, num_normal+1)) + 
        sum(
            cos(sum(s * d[i] for s, i in signs))
        )
    )**n
    
# range(num_normal+1, num_total+1)

    # function = lambda *d: (
    #     sum(cos(d_i) for d_i in d) + 
    #     cos(sum(s * d_i for s, d_i in zip(signs, d)))
    # )**n

    limits = [(0, 2*pi)] * len(signs)

    start_time = time.time()
    integral_results = integrate.nquad(function, limits, full_output=True)
    unrounded_result = prefix * Decimal(integral_results[0])
    
    rounded_result = unrounded_result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    rounded_result = abs(rounded_result) if rounded_result == -0.0 else rounded_result
    
    if print_info:
        elapsed_time = time.time() - start_time
        print(f"M_n for n={n} evaluates to {rounded_result} (rounded from {unrounded_result:.10f}), after {round(elapsed_time, 3):.3f} seconds")

    return unrounded_result, rounded_result

def get_results(start, end, p, m, d, skip_odd_n=False):
    integer_results = []
    decimal_results = []

    for n in range(start, end+1):
        if skip_odd_n and n % 2 == 1:
            integer_results.append(0)
            decimal_results.append(Decimal(0))
            print(f"M_n for n={n} evaluates to 0 (skipped)")
            continue

        patterns = get_patterns("./JC_code" + file_path + file_subpath, p, m, d)
        unrounded, rounded = eval_integral(patterns, n, print_info)

        integer_results.append(int(rounded))
        decimal_results.append(rounded)

    return [integer_results, decimal_results]


integer_results, decimal_results = get_results(0, 10, p, m, d, True)

# print(integer_results)
# print(decimal_results)















# import time
# import os
# from pathlib import Path

# import numpy as np
# import pandas as pd
# from scipy import integrate

# from numpy import cos
# from numpy import pi

# from decimal import Decimal, ROUND_HALF_UP, getcontext
# getcontext().prec = 1000

# """
# variables
# """
# def get_results(start, end, skip_odd_n=False):
    
#     func_example = lambda d1,d2,d3 : (cos(d1) + cos(d2) + cos(d3))**n
#     limits_example = [[0,2*pi], [0,2*pi], [0,2*pi]]

#     func_p_3 = lambda d1,d2,d3 : (cos(d1) + cos(d2) + cos(d3) + cos(-d1 + d2 + d3))**n
#     limits_p_3 = [[0,2*pi], [0,2*pi], [0,2*pi]]

#     function = func_p_3
#     limits = limits_p_3

#     integer_results = []
#     decimal_results = []

#     for n in range(start, end+1):

#         if skip_odd_n and n % 2 == 1:
#             integer_results.append(0)
#             decimal_results.append(Decimal(0))
#             print(f"M_n for n={n} evaluates to 0 (skipped)")
#             continue
#         prefix = ((Decimal(2)**Decimal(n))/((Decimal(2)*Decimal(pi))**Decimal((3))))

#         start_time = time.time()

#         integral_results = integrate.nquad(function, limits, full_output=True)
#         area = Decimal(integral_results[0])
#         # print(integral_results[0], "OR", area) # DEBUG

#         result = prefix * area
#         rounded_result = result.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

#         rounded_result = abs(rounded_result) if rounded_result == -0.0 else rounded_result
#         # rounded_result = int(rounded_result) if rounded_result.is_integer() else rounded_result
        
#         elapsed_time = time.time() - start_time

#         integer_results.append(int(rounded_result))
#         decimal_results.append(rounded_result)
#         print(f"M_n for n={n} evaluates to {rounded_result} (rounded from {result:.32f}), after {round(elapsed_time, 3):.3f} seconds")

#     return [integer_results, decimal_results]

# def output_data(full_path):
#     data = pd.read_csv(full_path).columns.values
#     array = [None] * len(data)

#     for i in range(0, len(data)):
#         array[i] = int(data[i])

#     print(array)


# p = 3
# m = p*p
# d = round((p+1)/2)
# file_path = "../outputs/max_relation_csvs/"
# file_subpath = "p_0_to_100/"
# file_name = f"p_{p}_m_{m}_d_{d}.csv"

# integer_results, decimal_results = get_results(31, 100, True)

# print(integer_results)
# print(decimal_results)

# # output_data(file_path + file_subpath + file_name)


