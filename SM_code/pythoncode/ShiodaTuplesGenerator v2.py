"""
author -- Sabeeha Malikah
date created -- 6/23/25
last modified -- 6/23/25
description -- We noticed that for m = p^2 and d = (p+1)/2, the indecomposable tuples are the same tuples that are
               from Shioda's Lemma 5.5. This program will use the generalized equation to generate the necessary
               indecomposable tuples for m = p^2.
version -- This version generates the indecomposable tuples for all m values that satisfy m = p^2 for 2 < p < 1000.
           The tuples generated are modified so that elements i: i > m+1/2 are written as i - m.

"""

# IMPORTS
import os
import time
from pathlib import Path

def ind_tuple_generator(p, m):
    ind_tuple_list = []
    for i in range(1, p):
        ind_tuple = tuple()
        coeff = 0
        while coeff <= p-1:
            ind_tuple = ind_tuple + (i + coeff*p,)
            coeff = coeff + 1
        ind_tuple = ind_tuple + (m - (p*i),)
        ind_tuple = tuple(sorted(ind_tuple))
        new_tuple = tuple()
        for n in ind_tuple:
            if n > (m-1)/2:
                n = n - m
            new_tuple = new_tuple + (n,)
        ind_tuple_list.append(new_tuple)
    return ind_tuple_list

def main():
    # Create a list of primes. This will be useful to loop through.
    list_of_primes = []
    primes_file = open(r'C:\Users\sabee\PycharmProjects\research-summer-2025-sato-tate\SM_code\pythoncode\primes.txt', "r")
    for prime in primes_file:
        list_of_primes.append(int(prime))

    for p in list_of_primes:
        m = p**2
        d = (p+1)//2
        start_time = time.time()
        base_output_path = Path(r'/SM_code/output/modified_shioda_tuples_output')
        filename = f"m_{m}_ind_f_output.txt"
        full_path = base_output_path / filename

        if os.path.exists(full_path):
            print(f"Skipping m = {m}, d = {d} - file already exists.")
            continue

        with open(full_path, "w") as file:
            file.write(f"For m = {m} and d = {d}\n")

        ind_tuple_list = ind_tuple_generator(p, m)
        total_time = time.time() - start_time

        #PRINTING
        with open(full_path, "a") as file:
            # PRINTING SUMMARY
            file.write(f"The program took {total_time} seconds to complete. \n")
            file.write(f"The number of indecomposable tuple(s) is: {len(ind_tuple_list)}\n")

            # PRINTING TUPLES
            file.write("\nThe indecomposable tuples are:\n")
            for ind_tuple in ind_tuple_list:
                file.write(f"{ind_tuple} -> max value: {max(ind_tuple, key=abs)}\n")


main()