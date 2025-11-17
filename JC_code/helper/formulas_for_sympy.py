import sympy as sp

def eval_integral_using_sympy(p, n):
    match p:
        case 5:
            return p_equals_5(n)
        case 7:
            return p_equals_7(n)
        case _:
            return None
        
    
def p_equals_5(n):
    theta1, theta2, theta3, theta4, theta5, theta6, theta7, theta8, theta9, theta10 = sp.symbols('theta1 theta2 theta3 theta4 theta5 theta6 theta7 theta8 theta9 theta10')

    integrand = (
        sp.cos(theta1) + 
        sp.cos(theta2) + 
        sp.cos(theta3) + 
        sp.cos(theta4) + 
        sp.cos(theta5) + 
        sp.cos(theta6) + 
        sp.cos(theta7) + 
        sp.cos(theta8) + 
        sp.cos(theta9) + 
        sp.cos(theta10) + 
        sp.cos(-theta1 + theta4 + theta5 - theta6 + theta9) + 
        sp.cos(-theta2 + theta3 - theta7 + theta8 + theta10)
    )**n

    integral_result = sp.integrate(
        integrand, 
        (theta1, 0, 2*sp.pi), 
        (theta2, 0, 2*sp.pi), 
        (theta3, 0, 2*sp.pi), 
        (theta4, 0, 2*sp.pi), 
        (theta5, 0, 2*sp.pi), 
        (theta6, 0, 2*sp.pi), 
        (theta7, 0, 2*sp.pi), 
        (theta8, 0, 2*sp.pi), 
        (theta9, 0, 2*sp.pi), 
        (theta10, 0, 2*sp.pi)
    )

    constant_factor = (2**n) / (2*sp.pi)**10

    final_result = constant_factor * integral_result
    
    return final_result

def p_equals_7(n):
    theta1, theta2, theta3, theta4, theta5, theta6, theta7, theta8, theta9, theta10, theta11, theta12, theta13, theta14, theta15, theta16, theta17, theta18, theta19, theta20, theta21 = sp.symbols('theta1 theta2 theta3 theta4 theta5 theta6 theta7 theta8 theta9 theta10 theta11 theta12 theta13 theta14 theta15 theta16 theta17 theta18 theta19 theta20 theta21')

    integrand = (
        sp.cos(theta1) + 
        sp.cos(theta2) + 
        sp.cos(theta3) + 
        sp.cos(theta4) + 
        sp.cos(theta5) + 
        sp.cos(theta6) + 
        sp.cos(theta7) + 
        sp.cos(theta8) + 
        sp.cos(theta9) + 
        sp.cos(theta10) + 
        sp.cos(theta11) + 
        sp.cos(theta12) + 
        sp.cos(theta13) + 
        sp.cos(theta14) + 
        sp.cos(theta15) + 
        sp.cos(theta16) + 
        sp.cos(theta17) + 
        sp.cos(theta18) + 
        sp.cos(theta19) + 
        sp.cos(theta20) + 
        sp.cos(theta21) + 
        sp.cos(-theta1 + theta6 + theta7 - theta8 + theta13 - theta15 + theta20) + 
        sp.cos(-theta2 + theta5 - theta9 + theta12 + theta14 - theta16 + theta19) +
        sp.cos(-theta3 + theta4 - theta10 + theta11 - theta17 + theta18 + theta21)
    )**n

    integral_result = sp.integrate(
        integrand, 
        (theta1, 0, 2*sp.pi), 
        (theta2, 0, 2*sp.pi), 
        (theta3, 0, 2*sp.pi), 
        (theta4, 0, 2*sp.pi), 
        (theta5, 0, 2*sp.pi), 
        (theta6, 0, 2*sp.pi), 
        (theta7, 0, 2*sp.pi), 
        (theta8, 0, 2*sp.pi), 
        (theta9, 0, 2*sp.pi), 
        (theta10, 0, 2*sp.pi),
        (theta11, 0, 2*sp.pi),
        (theta12, 0, 2*sp.pi),
        (theta13, 0, 2*sp.pi),
        (theta14, 0, 2*sp.pi),
        (theta15, 0, 2*sp.pi),
        (theta16, 0, 2*sp.pi),
        (theta17, 0, 2*sp.pi),
        (theta18, 0, 2*sp.pi),
        (theta19, 0, 2*sp.pi),
        (theta20, 0, 2*sp.pi),
        (theta21, 0, 2*sp.pi),
    )

    constant_factor = (2**n) / (2*sp.pi)**21

    final_result = constant_factor * integral_result
    
    return final_result