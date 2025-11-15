#USING SYMPY INTEGRATION

from sympy import symbols, cos, pi, integrate, simplify, expand
import numpy as np

def compute_initial_integral(n):
    theta = symbols('theta1:11')  # theta1 to theta10

    integrand = sum(cos(t) for t in theta)
    integrand += cos(-theta[0] + theta[3] + theta[4] - theta[5] + theta[8])
    integrand += cos(-theta[1] + theta[2] - theta[6] + theta[7] + theta[9])

    integrand_power = expand(integrand**n)

    for t in theta:
        integrand_power = integrate(integrand_power, (t, 0, 2 * pi))

    return simplify(integrand_power)


def compute_other_integrals(n):
    theta5, theta10 = symbols('theta5 theta10')
    integrand = (cos(theta5) + cos(theta10))**n
    integrand = expand(integrand)
    integrand = integrate(integrand, (theta5, 0, 2 * pi))
    integrand = integrate(integrand, (theta10, 0, 2 * pi))
    return simplify(integrand)


def main():
    p = 5
    normal_relations = ((p ** 2 - 1) // 2) - ((p - 1) // 2)
    total_moment_stats = []

    for b in range(20):
        print(f"b = {b}\n")
        moment_stats = [1]

        if b == 0:
            for n in range(1, 9):
                print(f"n = {n}: ")
                if n % 2 != 0:
                    moment_stats.append(0)
                    continue
                result = compute_initial_integral(n)
                result *= ((2 ** n) / (2 * pi) ** normal_relations)
                print(f"{float(result):.4f}")
                moment_stats.append(result)
            print()
            total_moment_stats.append(moment_stats)
        elif b % 4 == 0 and b % 8 != 0:
            for n in range(1, 9):
                if n % 2 != 0:
                    moment_stats.append(0)
                    continue
                result = compute_other_integrals(n)
                result *= (2 ** n) / (2 * pi)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)
        elif b % 8 == 0:
            for n in range(1, 9):
                if n % 2 != 0:
                    moment_stats.append(0)
                    continue
                result = compute_other_integrals(n)
                result *= ((-2) ** n) / (2 * pi)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)
        else:
            for n in range(1, 9):
                moment_stats.append(0)
            total_moment_stats.append(moment_stats)

    for item in total_moment_stats:
        print(f"{item} \n")

    arr = np.array(total_moment_stats)
    column_averages = np.mean(arr, axis=0)
    print([f"{float(x):.0f}" for x in column_averages])


main()