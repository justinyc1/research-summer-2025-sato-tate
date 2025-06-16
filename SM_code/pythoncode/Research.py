"""
author -- Sabeeha Malikah
last updated -- 6/10/25
description -- This program generates all indecomposable tuples for a given m and d value.
               The main method can be customized based on which m values we are interested in (i.e. m = p*q or m = p^2).
               The main method is currently written for m = p^2.
summary --
    1. The zmodmzstarset() function is called and the program generates this set for the given m value.
    2. The v_set() function is called and the program generates the V set for the given m and d value
       using the z_star set produced by zmodmzstar() function.
       This function calls other functions:
        - verify_not_all_pairs() that checks whether a tuple consists of all pairs. If this is true, the
          tuple is not an exceptional cycle and is not part of the exceptional cycles set. For efficiency, this tuple is
          not added to the V set either. This significantly reduces the number of tuples in the V set (which is now
          equivalent to the E set).
            * This means that there are fewer tuples that have to be checked with the verify_v_property() function, which
              requires a lot of mathematical computations.
        - verify_v_property() that checks if the tuple satisfies the B set property from our project summary document.
            * Our code treats the V and B set as the same set. (B set contains only ascending tuples from the V set).
    3. The e_set() function is called which finds all exceptional cycles in the V set. It separates the tuples into
       sum pairs and no pairs.
    4. The indecomposable_set() function is called which finds all tuples in the no pairs set that are indecomposable.

"""

# IMPORTS
import os
import math
import time
from itertools import combinations


"""
This function computes the z mod m z star set given an m value. This set contains integers ranging from [1,m).
The integers in this set satisfy the following property: gcd(i, m) == 1.

INPUT:
- ``m`` -- an odd integer which represents the degree in C_m: y^2=x^m-1

OUTPUT:
- ``z_star`` -- The set representing the z mod m z star set for the given m value.
"""


def zmodmzstarset(m):
    z_star = []
    for i in range(1, m):
        if math.gcd(i, m) == 1:
            z_star.append(i)
    return z_star


"""
This function computes the V set for a given m and d value. The function generates all d length "half tuples" whose
values range from [1, (m-1)/2]. It then combines each half tuple with every other half tuple, forming a tuple of length 
2*d. It checks if the tuple satisfies the properties for the U set and then for the V set. If it does, the tuple is 
appended to the list.  
Only the tuples that satisfy the following conditions are added to the list: 
    1. the elements of the tuple are ascending 
    2. the sum of the elements = m*d
    3. verify_v_property() returns True

INPUT:
- ``m`` -- an odd integer which represents the degree in C_m: y^2=x^m-1
- ``d``-- an integer whose range is [1, (m-1)/2]. This integer defines the length of the tuples produced.
          the tuples have length 2*d.
- ``z_star`` -- a list representing the z mod m z star set for the given m value that was returned by the zmodmzstar() function.


OUTPUT:
- ``v_list`` -- a list represent the V set for the given m and d values. 
"""


def v_set(m, d, z_star):
    count = 0
    small_tuple_list = []
    v_list = []
    print("These are the half tuple(s) in the U set: ")
    for combo in combinations(range(1, ((m-1)//2)+1), d):
        small_tuple_list.append(combo)
        print(combo)
        count += 1

    print("These are the tuple(s) in the V set: ")
    for half_tuple in small_tuple_list:
        i = 0
        while i < len(small_tuple_list):
            reverse_tuple = tuple(m-alpha for alpha in reversed(small_tuple_list[i]))
            if sum(half_tuple) + sum(reverse_tuple) == m*d:
                if verify_not_all_pairs(half_tuple, reverse_tuple, m, d):
                    new_tuple = half_tuple + reverse_tuple
                    if verify_v_property(new_tuple, m, d, z_star):
                        print(new_tuple)
                        v_list.append(new_tuple)
            i += 1
    # print("These are the tuple(s) in the V set: ")
    # print(tuple_list)
    print("The number of tuple(s) is", len(v_list))
    print()
    return v_list

"""
This function verifies whether a tuples meets the conditions necessary to be part of the V set.

INPUT:
- ``u_tuple`` -- a tuple that was generated in the v_set() function that satisfies the properties of the U set.
- ``m`` -- an odd integer which represents the degree in C_m: y^2=x^m-1
- ``d``-- an integer whose range is [1, (m-1)/2]. This integer defines the length of the tuples produced.
          the tuples have length 2*d.
- ``z_star`` -- a list representing the z mod m z star set for the given m value that was returned by the zmodmzstar() function.

OUTPUT:
- ``True`` -- if the tuple satisfies the necessary properties
- ``False`` -- if the tuple does not satisfy the necessary properties

"""

def verify_not_all_pairs(tuple_1, tuple_2, m, d):
    i = 0
    j = d-1
    pair_count = 0
    while i < d and j > -1:
        if tuple_1[i] + tuple_2[j] == m:
            pair_count += 1
        i += 1
        j -= 1

    if pair_count == d:
        return False
    return True

def verify_v_property(u_tuple, m, d, z_star):
    t_count = 0
    for t in z_star:
        i = 0
        sum = 0
        while i < 2 * d:
            sum += ((u_tuple[i] * t) % m)
            i += 1
        if (sum / m) == d:
            t_count = t_count + 1
    if t_count == len(z_star):
        return True
    return False


"""
This function computes the E set (set containing exceptional tuples). It creates the following lists:
    1. no_pairs -- represents the set with tuples that contain no pairs of elements that add to m.
    2. some_pairs -- represents the set with tuples that contain some but not all pairs of elements that add to m.

INPUT:
- ``m`` -- an odd integer which represents the degree in C_m: y^2=x^m-1
- ``v_list`` -- a list representing the V set for the given m and d values that was returned by the v_set() function.

OUTPUT:
- ``tuple_list`` -- a list representing the set of all tuples in the V set that are exceptional cycles
- ``no_pairs`` -- a list representing the subset of the exceptional cycles set that contains tuples containing no pairs 
"""


def e_set(m, v_list):
    tuple_list = v_list[:]
    no_pairs = []
    some_pairs = []
    count = len(v_list)
    # This checks for all possible pair combinations in the tuple.
    for v_tuple in v_list:
        pair_count = 0
        for combo in combinations(v_tuple, 2):
            if sum(combo) == m:
                pair_count += 1
        # if pair_count == int(len(v_tuple) / 2):
        #     count -= 1
        #     tuple_list.remove(v_tuple)
        if pair_count == 0:
            no_pairs.append(v_tuple)
        else:
            some_pairs.append(v_tuple)
    # PRINTING
    # print("These are the tuple(s) in the E set: ")
    # for e_tuple in tuple_list:
    #     print(e_tuple)
    # print("The number of tuple(s) is", count)
    # print("These tuples have no pairs that add to m =", m, )
    # for no_pairs_tuple in no_pairs:
    #     print(no_pairs_tuple)
    # print("The number of tuple(s) is", len(no_pairs))
    # print("These tuples have some (but not all) pairs that add to m =", m, )
    # for some_pairs_tuple in some_pairs:
    #     print(some_pairs_tuple)
    # print("The number of tuple(s) is", len(some_pairs))
    # print()
    return tuple_list, no_pairs


"""
This functions determines which tuples in the no_pairs set are indecomposable and returns a list of those tuples.

INPUT: 
- ``m`` -- an odd integer which represents the degree in C_m: y^2=x^m-1
- ``d``-- an integer whose range is [1, (m-1)/2]. This integer defines the length of the tuples produced.
          the tuples have length 2*d.
- ``no_pairs`` -- a list representing the subset of the exceptional cycles set that contains tuples containing no pairs
                  returned by the e_set() function

OUTPUT:
- ``tuple_list`` -- a list representing a subset of the no pairs set containing the tuples that are indecomposable
"""


def indecomposable_set(m, d, no_pairs):
    tuple_list = no_pairs[:]
    for e_tuple in no_pairs:
        for i in range(2, d, 2):
            if e_tuple in no_pairs:
                for combo in combinations(e_tuple, i):
                    if sum(combo) % m == 0:
                        tuple_list.remove(e_tuple)
                        break
    # PRINTING
    # print("These are the exceptional tuple(s) that are indecomposable: ")
    # for ind_tuple in tuple_list:
    #     print(ind_tuple)
    # print("The number of tuple(s) is", len(tuple_list))
    return tuple_list


def main():
    # Create a list of primes. This will be useful to loop through.
    list_of_primes = []
    primes_file = open(r'C:\Users\sabee\PycharmProjects\research-spring-2025\SM_code\primes.txt', "r")
    for prime in primes_file:
        list_of_primes.append(int(prime))

    for p in list_of_primes:
        m = p**2
        d = (p+1)/2
        start_time = time.time()
        save_path = r'C:\Users\sabee\PycharmProjects\research-spring-2025\SM_code\output'
        filename = f"m_{m}_d_{d}_output.txt"
        full_path = os.path.join(save_path, filename)
        z_star = zmodmzstarset(m)
        with open(full_path, "w") as file:
            file.write(f"For m = {m} and d = {d}\n")
            file.write(f"These are integers in the z mod m z star set for m = {m}\n {z_star}\n")
        v_tuple_list = v_set(m, d, z_star)
        e_tuple_list, no_pairs = e_set(m, v_tuple_list)
        indecomposable_list = indecomposable_set(m, d, no_pairs)
        end_time = time.time() - start_time

        # PRINTING
        with open(filename, "a") as file:
            # PRINTING SUMMARY
            file.write(f"The program took {end_time} seconds to complete.\n")
            file.write(f"The number of tuple(s) in the V set is: {len(v_tuple_list)}\n")
            file.write(f"The number of tuple(s) in the E set is: {len(e_tuple_list)}\n")
            file.write(f"The number of tuple(s) with no pairs is: {len(no_pairs)}\n")
            file.write(f"The number of indecomposable tuple(s) is: {len(indecomposable_list)}\n\n")

            # PRINTING TUPLES
            # V set
            file.write(f"The tuples in the V set are:\n")
            for x in v_tuple_list:
                file.write(f"{x}\n")
            file.write(f"The number of tuple(s) in the V set is: {len(v_tuple_list)}\n")
            file.write(f"\n")

            # E set
            file.write(f"The tuples in the E set are:\n")
            for x in e_tuple_list:
                file.write(f"{x}\n")
            file.write(f"The number of tuple(s) in the E set is: {len(e_tuple_list)}\n")

            # no pairs set
            file.write(f"The tuples in the no pairs set are:\n")
            for x in no_pairs:
                file.write(f"{x}\n")
            file.write(f"The number of tuple(s) in the no pairs set is: {len(no_pairs)}\n")

            # indecomposable set
            file.write(f"The indecomposable tuples are:\n")
            for x in indecomposable_list:
                file.write(f"{x}\n")
            file.write(f"The number of indecomposable tuple(s) is: {len(indecomposable_list)}\n")

main()


