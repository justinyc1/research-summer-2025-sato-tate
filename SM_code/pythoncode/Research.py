"""
author -- Sabeeha Malikah
date -- 3/23/25
Description -- Post Meeting on 3/17/25
    Changes:
    - using product function from itertools library to compute cartesian product of half_tuples_list
      and reverse_half_tuples_list instead of using a nested for-loop
    - using multiprocessing library to speed up verify_v_property() function
"""

# IMPORTS:
import time
import math
import os
from itertools import combinations
from itertools import product
from multiprocessing import Pool


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
    half_tuples_list = []
    reverse_half_tuples_list = []
    v_list = []
    print("These are the half tuple(s) in the V set: ")
    for combo in combinations(range(1, ((m-1)//2)+1), d):
        half_tuples_list.append(combo)
        reverse_half_tuples_list.append(tuple(m-alpha for alpha in reversed(combo)))
        print(combo)
        count += 1
    print(len(half_tuples_list))

    # this creates a list containing tuples that represent the parameters sent to verify_v_property() for each i
    params = product(half_tuples_list, reverse_half_tuples_list, [m], [d], [z_star])
    # using multiprocessing for more efficiency
    with Pool() as pool:
        results = pool.starmap(verify_v_property, params)
    print("These are the tuple(s) in the V set: ")
    for result in results:
        bool_result, new_tuple = result
        if bool_result:
            print(new_tuple)
            v_list.append(new_tuple)

    # for param in params:
    #     bool_result, new_tuple = verify_v_property(param[0], param[1], param[2], param[3], param[4])
    #     if bool_result:
    #         print(new_tuple)
    #         v_list.append(new_tuple)


    # for half_tuple in half_tuples_list:
    #     params1.append((half_tuple, reverse_half_tuples_list))
    # with Pool() as pool1:
    #     results1 = pool1.starmap(combine_tuples, [(ht, reverse_half_tuples_list) for ht in half_tuples_list])
    #     # for half_tuple in half_tuples_list:
    #     #     results1 = pool1.starmap(combine_tuples, params1)
    #
    # for result in results1:
    #     for new_tuple in result:
    #         params2.append((new_tuple[0], new_tuple[1], m, d, z_star))

    # params = []
    # for half_tuple in half_tuples_list:
    #     for reverse_tuple in reverse_half_tuples_list:
    #         params.append((half_tuple, reverse_tuple, m, d, z_star))


    #

    print("The number of tuple(s) is ", len(v_list))
    print()
    return v_list


# def v_set(m, d, z_star):
#     count = 0
#     half_tuples_list = []
#     reverse_half_tuples_list = []
#     v_list = []
#     print("These are the half tuple(s) in the U set: ")
#     for combo in combinations(range(1, ((m-1)//2)+1), d):
#         half_tuples_list.append(combo)
#         reverse_half_tuples_list.append(tuple(m-alpha for alpha in reversed(combo)))
#         print(combo)
#         count += 1
#
#
#     print("These are the tuple(s) in the V set: ")
#     for half_tuple in half_tuples_list:
#         i = 0
#         while i < len(reverse_half_tuples_list):
#             if sum(half_tuple) + sum(reverse_half_tuples_list[i]) == m*d:
#                 if verify_v_property(half_tuple, reverse_half_tuples_list[i], m, d, z_star):
#                     if verify_not_all_pairs(half_tuple, reverse_half_tuples_list[i], m, d):
#                         print(half_tuple+reverse_half_tuples_list[i])
#                         v_list.append(half_tuple+reverse_half_tuples_list[i])
#             i+=1

    # ATTEMPT 1
    # for half_tuple in half_tuples_list:
    #     i = 0
    #     while i < len(half_tuples_list):
    #         new_tuple = half_tuple + tuple(m-alpha for alpha in reversed(half_tuples_list[i]))
    #         if sum(new_tuple) == m*d:
    #             if verify_v_property(new_tuple, m, d, z_star):
    #                 print(new_tuple)
    #                 v_list.append(new_tuple)
    #         i += 1

    # ATTEMPT 2
    # for i in range(0, len(half_tuples_list)):
    #     for j in range(0, len(half_tuples_list)):
    #         new_tuple = tuple(m-alpha for alpha in reversed(half_tuples_list[j]))
    #         if sum(half_tuples_list[i] + new_tuple) == m*d:
    #             if verify_v_property(half_tuples_list[i], new_tuple, m, d, z_star):
    #                 print(half_tuples_list[i] + new_tuple)
    #                 v_list.append(half_tuples_list[i] + new_tuple)
    # print("These are the tuple(s) in the V set: ")
    # print(tuple_list)
    # print("The number of tuple(s) is ", len(v_list))
    # print()
    # return v_list

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

# def verify_not_all_pairs(tuple_1, tuple_2, m, d):
#     i = 0
#     j = d-1
#     pair_count = 0
#     while i < d and j > -1:
#         if tuple_1[i] + tuple_2[j] == m:
#             pair_count += 1
#         i += 1
#         j -= 1
#
#     if pair_count == d:
#         return False
#     return True
def combine_tuples(half_tuple, reverse_half_tuples_list):
    return [(half_tuple, reverse_tuple) for reverse_tuple in reverse_half_tuples_list]


def verify_v_property(half_tuple_one, half_tuple_two, m, d, z_star):
    t_count = 0
    new_tuple = half_tuple_one + half_tuple_two
    for t in z_star:
        i = 0
        sum = 0
        while i < 2 * d:
            sum += ((new_tuple[i] * t) % m)
            i += 1
        if (sum / m) == d:
            t_count = t_count + 1
    if t_count == len(z_star):
        return True, new_tuple
    return False, new_tuple


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
        if pair_count == int(len(v_tuple) / 2):
            count -= 1
            tuple_list.remove(v_tuple)
        elif pair_count == 0:
            no_pairs.append(v_tuple)
        else:
            some_pairs.append(v_tuple)
    print("These are the tuple(s) in the E set: ")
    print(tuple_list)
    print("The number of tuple(s) is ", count)
    print("These tuples have no pairs that add to m =", m, )
    print(no_pairs)
    print("The number of tuple(s) is ", len(no_pairs))
    print("These tuples have some (but not all) pairs that add to m =", m, )
    print(some_pairs)
    print("The number of tuple(s) is ", len(some_pairs))
    print()
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


def indecomposable(m, d, no_pairs):
    tuple_list = no_pairs[:]
    for e_tuple in no_pairs:
        for i in range(2, d, 2):
            if e_tuple in no_pairs:
                for combo in combinations(e_tuple, i):
                    if sum(combo) % m == 0:
                        tuple_list.remove(e_tuple)
                        break

    print("These are the exceptional tuple(s) that are indecomposable: ")
    print(tuple_list)
    print("The number of tuple(s) is ", len(tuple_list))
    return tuple_list


def main():
    m = 7**2
    for d in range(1, ((m-1)//2)+1):
        start_time = time.time()
        save_path = r'C:\Users\sabee\PycharmProjects\research-spring-2025\SM_code\output'
        filename = f"m_{m}_d_{d}_output.txt"
        full_path = os.path.join(save_path, filename)
        # with open(filename, "w") as file:
        #     file.write(f"These are the tuples for m = {m} and d = {d}")
        z_star = zmodmzstarset(m)
        with open(full_path, "w") as file:
            file.write(f"For m = {m} and d = {d}\n")
            file.write(f"These are integers in the z mod m z star set for m = {m}\n {z_star}\n")
        v_tuple_list = v_set(m, d, z_star)
        e_tuple_list, no_pairs = e_set(m, v_tuple_list)
        indecomposable_list = indecomposable(m, d, no_pairs)
        end_time = time.time() - start_time

        # print summary & tuples
        with open(full_path, "a") as file:
            # printing summary
            file.write(f"The program took {end_time} seconds to complete.\n")
            file.write(f"The number of tuple(s) in the V set is: {len(v_tuple_list)}\n")
            file.write(f"The number of tuple(s) in the E set is: {len(e_tuple_list)}\n")
            file.write(f"The number of tuple(s) with no pairs is: {len(no_pairs)}\n")
            # file.write(no_pairs)
            file.write(f"The number of indecomposable tuple(s) is: {len(indecomposable_list)}\n\n")

            # printing tuples
            file.write(f"The tuples in the V set are:\n")
            for x in v_tuple_list:
                file.write(f"{x}\n")
            file.write(f"The number of tuple(s) in the V set is: {len(v_tuple_list)}\n")
            file.write(f"\n")
            # file.write(f"The tuples in the E set are:\n")
            # for x in e_tuple_list:
            #     file.write(f"{x}\n")
            # file.write(f"The number of tuple(s) in the E set is: {len(e_tuple_list)}\n")
            # file.write(f"The number of tuple(s) with no pairs is: {len(no_pairs)}\n")
            # file.write(no_pairs)
            file.write(f"The indecomposable tuples are:\n")
            for x in indecomposable_list:
                file.write(f"{x}\n")
            file.write(f"The number of indecomposable tuple(s) is: {len(indecomposable_list)}\n")

if __name__ == "__main__":
    main()


