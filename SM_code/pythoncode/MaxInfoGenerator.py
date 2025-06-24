import os
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
        base_output_path = Path(r'C:\Users\sabee\PycharmProjects\research-summer-2025-sato-tate\SM_code\output\max_element_info_output')
        filename = f"m_{m}_max_element_output.txt"
        full_path = base_output_path / filename

        if os.path.exists(full_path):
            print(f"Skipping m = {m}, d = {d} - file already exists.")
            continue

        ind_tuple_list = ind_tuple_generator(p, m)

        with open(full_path, "a") as file:
            file.write(f"Maximum values for m = {m} and d = {d}:\n")
            for ind_tuple in ind_tuple_list:
                max_value = max(ind_tuple, key=abs)
                new_tuple = tuple()
                for n in ind_tuple:
                    if n != max_value:
                        new_tuple = new_tuple + (-1*n,)
                file.write(f"{max_value} = {new_tuple}\n")

main()
