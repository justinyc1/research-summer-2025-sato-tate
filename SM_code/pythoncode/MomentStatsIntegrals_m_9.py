import numpy as np
from scipy import integrate


# m = 9, p = 3

def generate_integrand(n):
    def integrand(theta1, theta2, theta3):
        return (np.cos(theta1) + np.cos(theta2) + np.cos(theta3) + np.cos(-theta1 + theta2 + theta3))**n
    return integrand

def f(n):
    def function(theta3):
        return np.cos(theta3)**n
    return function

def main():
    p = 3
    normal_relations = ((p ** 2 - 1) // 2) - ((p - 1) // 2)
    total_moment_stats = []
    for b in range(6):
        moment_stats = [1]
        if b == 0:
            for n in range(1, 13):
                if n % 2 != 0:
                    moment_stats.append(0)
                    continue
                integrand = generate_integrand(n)
                limits = [(0, 2*np.pi), (0, 2*np.pi), (0, 2*np.pi)]
                result, _ = integrate.nquad(integrand, limits)
                result *= ((2 ** n) / (2 * np.pi) ** normal_relations)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)
        elif b%2 != 0:
            for n in range(1, 13):
                moment_stats.append(0)
            total_moment_stats.append(moment_stats)
        elif b==2:
            for n in range(1, 13):
                if n%2 != 0:
                    moment_stats.append(0)
                    continue
                function = f(n)
                limits = [(0, 2*np.pi)]
                result, _ = integrate.nquad(function, limits)
                result *= (2 ** n) / (2 * np.pi)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)
        else:
            for n in range(1, 13):
                if n%2 != 0:
                    moment_stats.append(0)
                    continue
                function = f(n)
                limits = [(0, 2*np.pi)]
                result, _ = integrate.nquad(function, limits)
                result *= ((-2) ** n) / (2 * np.pi)
                moment_stats.append(result)
            total_moment_stats.append(moment_stats)

    for item in total_moment_stats:
        print(f"{item} \n")

    arr = np.array(total_moment_stats)
    column_averages = np.mean(arr, axis=0)
    print([f"{float(x):.0f}" for x in column_averages])


main()