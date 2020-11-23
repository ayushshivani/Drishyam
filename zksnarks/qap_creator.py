def mathematical_operations(a,b,oper=None):
    if oper == "mult":
        o = [0] * (len(a) + len(b) - 1)
        for i in range(len(a)):
            for j in range(len(b)):
                o[i + j] += a[i] * b[j]
    
    if oper == "add":
        o = [0] * max(len(a), len(b))
        for i in range(len(a)):
            o[i] += a[i]
        for i in range(len(b)):
            o[i] += b[i] 

    if oper == "div":
        o = [0] * (len(a) - len(b) + 1)
        remainder = a
        while len(remainder) >= len(b):
            leading_fac = remainder[-1] / b[-1]
            pos = len(remainder) - len(b)
            o[pos] = leading_fac
            remainder = mathematical_operations(remainder, mathematical_operations(b, [0] * pos + [leading_fac],oper="mult"),oper="sub")[:-1]
        return o,remainder

    if oper == "sub":
        o = [0] * max(len(a), len(b))
        for i in range(len(a)):
            o[i] += a[i]
        for i in range(len(b)):
            o[i] += b[i] * (-1 )
    
    return o



# Evaluate a polynomial at a point
def eval_poly(poly, x):
    return sum([poly[i] * x**i for i in range(len(poly))])

# Make a polynomial which is zero at {1, 2 ... total_pts}, except
# for `point_loc` where the value is `height`
def mk_singleton(point_loc, height, total_pts):
    fac = 1
    for i in range(0, total_pts ):
        if i + 1 != point_loc:
            fac *= point_loc - ( i + 1 )
    o = [height * 1.0 / fac]
    for i in range(0, total_pts ):
        if ( i + 1 ) != point_loc:
            o = mathematical_operations(o, [-(i+1), 1],oper="mult")
    return o

# Assumes vec[0] = p(1), vec[1] = p(2), etc, tries to find p,
# expresses result as [deg 0 coeff, deg 1 coeff...]
def lagrange_interp(vec):
    o = []
    for i in range(len(vec)):
        o = mathematical_operations(o, mk_singleton(i + 1, vec[i], len(vec)),oper="add")
    for i in range(len(vec)):
        assert abs(eval_poly(o, i + 1) - vec[i] < 10**-10), \
            (o, eval_poly(o, i + 1), i+1)
    return o

def transpose(matrix):
    return list(map(list, zip(*matrix)))
    
# A, B, C = matrices of m vectors of length n, where for each
# 0 <= i < m, we want to satisfy A[i] * B[i] - C[i] = 0
def r1cs_to_qap(A, B, C):
    A, B, C = transpose(A), transpose(B), transpose(C)
    new_A,new_B,new_C = [],[],[]

    for a in A:
        new_A.append(lagrange_interp(a))
    for b in B:
        new_B.append(lagrange_interp(b))
    for c in C:
        new_C.append(lagrange_interp(c))
    Z = [1]
    for i in range(1, len(A[0]) + 1):
        Z = mathematical_operations(Z, [-i, 1],oper="mult")
    return (new_A, new_B, new_C, Z)

def create_solution_polynomials(r, new_A, new_B, new_C):
    Apoly = []
    for rval, a in zip(r, new_A):
        Apoly = mathematical_operations(Apoly, mathematical_operations([rval], a, oper="mult"),oper="add")
    Bpoly = []
    for rval, b in zip(r, new_B):
        Bpoly = mathematical_operations(Bpoly, mathematical_operations([rval], b,oper="mult"),oper="add")
    Cpoly = []
    for rval, c in zip(r, new_C):
        Cpoly = mathematical_operations(Cpoly, mathematical_operations([rval], c,oper="mult"),oper="add")
    o = mathematical_operations(mathematical_operations(Apoly, Bpoly,oper="mult"), Cpoly,oper="sub")
    for i in range(1, len(new_A[0]) + 1):
        assert abs(eval_poly(o, i)) < 10**-10, (eval_poly(o, i), i)
    return Apoly, Bpoly, Cpoly, o

def create_divisor_polynomial(sol, Z):
    quot, rem = mathematical_operations(sol, Z,oper="div")
    for x in rem:
        assert abs(x) < 10**-10
    return quot

r = [1, 3, 35, 9, 27, 30]
A = [[0, 1, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [0, 1, 0, 0, 1, 0],
     [5, 0, 0, 0, 0, 1]]
B = [[0, 1, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0]]
C = [[0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 1],
     [0, 0, 1, 0, 0, 0]]

Ap, Bp, Cp, Z = r1cs_to_qap(A, B, C)
print('Ap')
for x in Ap: print (x)
print('Bp')
for x in Bp: print (x)
print( 'Cp')
for x in Cp: print( x)
print( 'Z')
print( Z)
Apoly, Bpoly, Cpoly, sol = create_solution_polynomials(r, Ap, Bp, Cp)
print( 'Apoly')
print( Apoly)
print( 'Bpoly')
print( Bpoly)
print( 'Cpoly')
print( Cpoly)
print( 'Sol')
print( sol)
print( 'Z cofactor')
print( create_divisor_polynomial(sol, Z))
