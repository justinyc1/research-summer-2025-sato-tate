#USING SYMPY INTEGRATION

from sympy import symbols, cos, pi, integrate, simplify, expand
import numpy as np

def compute_initial_integral(n):
    theta = symbols('theta1:22')  # theta1 to theta21

    integrand = sum(cos(t) for t in theta)
    integrand += cos(-theta[0] + theta[7] + theta[8] - theta[9] + theta[14] - theta[16] + theta[21])
    integrand += cos(-theta[3] + theta[6] - theta[10] + theta[13] + theta[15] - theta[17] + theta[20])
    integrand += cos(-theta[4] + theta[5] - theta[11] + theta[12] - theta[18] + theta[19] + theta[22])

    integrand_power = expand(integrand**n)

    for t in reversed(theta):
        integrand_power = integrate(integrand_power, (t, 0, 2 * pi))

    return simplify(integrand_power)


def compute_other_integrals(n):
    theta7, theta14, theta21 = symbols('theta7 theta14 theta21')
    integrand = (cos(theta7) + cos(theta14) + cos(theta21))**n
    integrand = expand(integrand)
    integrand = integrate(integrand, (theta7, 0, 2 * pi))
    integrand = integrate(integrand, (theta14, 0, 2 * pi))
    integrand = integrate(integrand, (theta21, 0, 2 * pi))
    return simplify(integrand)


def main():
    p = 7
    normal_relations = ((p ** 2 - 1) // 2) - ((p - 1) // 2)
    total_moment_stats = []

    for b in range(p*(p-1)):
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
        elif b % 6 == 0 and b % 12 != 0:
            for n in range(1, 9):
                if n % 2 != 0:
                    moment_stats.append(0)
                    continue
                result = compute_other_integrals(n)
                result *= (2 ** n) / (2 * pi)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)
        elif b % 12 == 0:
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

    arr = np.array([[float(x) for x in row] for row in total_moment_stats])
    column_averages = np.mean(arr, axis=0)
    print([f"{float(x):.0f}" for x in column_averages])


main()
