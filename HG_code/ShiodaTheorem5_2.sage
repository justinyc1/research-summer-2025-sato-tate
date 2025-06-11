##########################################################################
# This package contains code used to compute Hodge classes of Jacobians J_m of hyperelliptic curves of the form
# C_m: y^2=x^m-1, where m is any odd positive integer.
#
# The algorithms are based on [1] Shioda, T. "Algebraic Cycles on Abelian Varieties of Fermat Type" Math. Ann., 258(1):65–80, 1981/82. Equations 1 and 2, Theorem 5.2, and some explanations in Section 6.
#
# When using this code in your research, please cite as:
# "the software of [2], which is based on the theoretical work of [1]"
# where [1] is as above and [2] is
# [2] Goodson, H., "An Exploration of Degeneracy in Abelian Varieties of Fermat Type" arXiv 2022 (or the most recent citation once it is published) 
#
# This package contains the following functions:
# For the family y^2 = x^m-1, m odd:
#    -RestrictedU
#    -Bset
#    -Exceptional
#    -Exceptionalrelprime
#
# #TODO
#    -Exceptional function for d=4 or new for loop in old one
#    




##########################################################################
#
# Some utilities we will need
#

def tuplesize(alpha,m):
    sum=0
    for i in [0..len(alpha)-1]:
        sum+=alpha[i]/m
    return sum

def scalarproduct(alpha,t,m):
    tlist=[]
    for i in [0..len(alpha)-1]:
        tlist.append((t*alpha[i])%m)
    return tlist



##########################################################################
#
# Functions for y^2 = x^m-1
#

def RestrictedU(m,d):
    """
    Computes the elements we need from U^n_m in Equation 1.1 of [1]. This is the slowest of the functions.

    INPUT:
    - ``m`` -- an integer. The degree in C_m: y^2=x^m-1
    - ``d`` -- an integer satisfying n=2d-2. range of d: 0<= d <=dim(J_m)

    OUTPUT:
    - A list, containing 2d-tuples contained in U^n_m.

    """
    size=2*d
    maxvalue=size*m-d*(size+1) 
    Ulist=[] 
    integerlist=[]
    for i in [m..maxvalue]:
        if i%m==0:
            Ulist.append(i)
    upperbound=[]
    lowerbound=[]
    for i in [1..d]:
        upperbound.append((m-1)/2)
        lowerbound.append(i)  
    for i in [d+1..size]:
        upperbound.append((m-1))
        lowerbound.append(i)
    compositionlist=[]
    for k in Ulist:
        K=Compositions(k, min_slope=1, length=2*d, outer=upperbound, inner=lowerbound)
        for i in [0..len(K)-1]:
            compositionlist.append(list(K[i])) 
    return compositionlist


def Bset(m,d,Ufile):
    '''
    Computes the elements we need from B^n_m in Equation 1.2 of [1]

    INPUT:
    - ``m`` -- an integer. The degree in C_m: y^2=x^m-1
    - ``d`` -- an integer satisfying n=2d-2. range of d: 0<= d <=dim(J_m)
    -``Ufile`` -- this is the associated U^n_m subset that we obtain in the RestrctedU program. Ufile needs to be a saved sobj file

    OUTPUT:
    -  A list, containing 2d-tuples contained in B^n_m.
    '''
    g=(m-1)/2
    Blist=load(Ufile)
    #print(Blist)
    Badlist=[]
    for alpha in Blist:
        for t in [1..g]: 
            if gcd(t,m)==1:
                size=tuplesize(scalarproduct(alpha,t,m),m)
                if size!=d: #(2*d-2)/2+1:
                    if alpha not in Badlist:
                        Badlist.append(alpha)
                    break
    for beta in Badlist:
        Blist.remove(beta)
    Blistset=[]
    for j in [0..len(Blist)-1]:
        Blistset.append(Set(Blist[j])) #change the type from List to Set to remove duplicates
    return Blistset


def Exceptional(m,d,divclass,Bset2, Bset3):
    '''
    Computes the exceptional cycles of J_m in codimension d. These are the cycles not coming from divisor classes (d=1).
    Only works for d=2 and d=3 right now.

    INPUT:
    - ``m`` -- an integer. The degree in C_m: y^2=x^m-1
    - ``d`` -- an integer satisfying n=2d-2. range of d: 0<= d <=dim(J_m)
    - ``divclass`` -- these are the divisor classes computed as Bset(m,1). Bset needs to be a saved sobj file.
    - ``Bset2`` -- these are the codimension 2 classes computed as Bset(m,2). Bset needs to be a saved sobj file.
    - ``Bset3`` -- these are the codimension 3 classes computed as Bset(m,3). Bset needs to be a saved sobj file.

    OUTPUT:
    -  A list, containing exceptional Hodge cycles in codimension d, expressed as 2d-tuples.
    '''
    divisor_classes1=load(divclass)
    numero=len(divisor_classes1)-1
    divisor_classes2=[]
    divisor_classes3=[]
    exceptional2=load(Bset2)
    for i in [0..numero]:
        for j in [i+1..numero]:
            divisor_classes2.append(Set(divisor_classes1[i]+divisor_classes1[j]))
    for divisor in divisor_classes2:
            exceptional2.remove(divisor)
    if d==3:
        exceptional3=load(Bset3)
        for m in [0..numero]:
            for k in [0..len(divisor_classes2)-1]:
                divisor_classes3.append(Set(divisor_classes2[k]+divisor_classes1[m]))
            for n in [0..len(exceptional2)-1]:
                divisor_classes3.append(exceptional2[n]+Set(divisor_classes1[m]))
        for divisor in divisor_classes3:
            if divisor in exceptional3:
                exceptional3.remove(divisor)
    if d==2:
        return(exceptional2)
    if d==3:
        return(exceptional3)



def Exceptionalrelprime(m,d,exceptionalset):
    '''
    This computes the Exceptional classes whose entries are relatively prime to m.
    Useful for determining if the simple ab var factor of J_m is degenerate (i.e., does it have exceptional cycles?).

    INPUT:
    - ``m`` -- an integer. The degree in C_m: y^2=x^m-1
    - ``d`` -- an integer satisfying n=2d-2. range of d: 0<= d <=dim(J_m)
    - ``exceptionalset`` -- these are the codimension d exceptional cycles computed as Exceptional(m,d,divclass,Bset2, Bset3). Exceptional(m,d,divclass,Bset2, Bset3) needs to be a saved sobj file.

    OUTPUT:
    -  A list, containing exceptional Hodge cycles in codimension d whose entries are relatively prime to m, expressed as 2d-tuples.
    '''
    exceptionalBlist=load(exceptionalset)
    badlist=[]
    for List in exceptionalBlist:
        bad=[]
        for element in List:
            if gcd(element, m)>1:
                bad=List
        badlist.append(Set(bad))
        if [] in badlist:
            badlist.remove([])
    for i in badlist:
        if i in exceptionalBlist:
            exceptionalBlist.remove(i)
    return exceptionalBlist







