"""
author -- Sabeeha Malikah
last updated -- 7/22/25
description -- This program will compute the moment statistics for our data. Currently, this is for b = 0 where b is the
               power of the component group matrix.

"""

# IMPORTS

# files stuff
import re
from pathlib import Path

# integrals stuff
import math
import numpy as np
from sympy import symbols, cos, integrate, lambdify
from scipy import integrate

# This is used to sort the filenames in ascending order based on m value.
def extract_m_value(filename):
    match = re.search(r'm_(\d+)_raw_output', filename)
    if match:
        return int(match.group(1))
    else:
        return float('inf')


def generate_integrand(normal_relations, extra_relations, n):
    theta_variables = symbols(f'th_1:{normal_relations+1}')

    integrand = 0
    for i in range(len(theta_variables)):
        integrand += cos(theta_variables[i])

    # extra relations
    for relation in extra_relations:
        indices = list(map(int, relation.strip().split()))
        sum = 0
        for index in indices:
            if index > 0:
                sum += theta_variables[abs(index)-1]
            else:
                sum += -theta_variables[abs(index)-1]
        integrand += cos(sum)
    integrand = integrand**n
    function = lambdify(theta_variables, integrand, modules='numpy')

    return function, theta_variables


def main():
    moment_stats = [1]

    directory = Path(r'C:\Users\sabee\PycharmProjects\research-summer-2025-sato-tate\SM_code\output\raw data')

    files = list(directory.iterdir())
    # Sorts files based on m value so that we compute moment stats in order.
    files_sorted = sorted(files, key=lambda f: extract_m_value(f.name))

    for f in files_sorted:
        with open(f, "r") as file:
            lines = file.readlines()
        m = int(lines[0])
        p = int(math.sqrt(m))
        extra_relations = lines[1:]

        # We know the following:
        # total number of blocks = p^2-1/2
        # total number of blocks from extra relations= p-1/2
        # it follows that
        normal_relations = ((p**2 - 1) // 2) - ((p - 1) // 2)

        for i in range(1, 13):
            if i%2 != 0:
                moment_stats.append(0)
                continue
            integrand, theta_variables = generate_integrand(normal_relations, extra_relations, i)
            limits = [(0, 2 * np.pi) for _ in theta_variables]
            result, _ = integrate.nquad(integrand, limits)
            result *= ((2**i) / (2*np.pi)**normal_relations)
            moment_stats.append(result)

        print(f"m = {m}: {moment_stats}\n")

main()