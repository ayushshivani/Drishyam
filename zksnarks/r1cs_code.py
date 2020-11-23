import ast
if 'arg' not in dir(ast):
    ast.arg = type(None)

def parser(code):
    return ast.parse(code).body

def extio(code):
    o = []
    if len(code) != 1 :
        raise Exception("function not declaration")
    if not isinstance(code[0], ast.FunctionDef):
        raise Exception("function not declaration")
    inputs = []
    for arg in code[0].args.args:
        if isinstance(arg, ast.arg):
            assert isinstance(arg.arg, str)
            inputs.append(arg.arg)
        elif isinstance(arg, ast.Name):
            inputs.append(arg.id)
        else:
            raise Exception("Invalid arg: %r" % ast.dump(arg))
    body = []
    returned = False
    for c in code[0].body:
        if not isinstance(c, (ast.Assign, ast.Return)):
            raise Exception("Expected variable assignment or return")
        if returned:
            raise Exception("Cannot do stuff after a return statement")
        if isinstance(c, ast.Return):
            returned = True
        body.append(c)
    return inputs, body


def bd_flat(body):
    o = []
    for c in body:
        o.extend(stmt_flat(c))
    return o

next_symbol = [0]
def mksymbol():
    next_symbol[0] += 1
    return 'sym_'+str(next_symbol[0])


def stmt_flat(stmt):
    if isinstance(stmt, ast.Assign):
        assert len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name)
        target = stmt.targets[0].id
    elif isinstance(stmt, ast.Return):
        target = '~out'
    return exp_flat(target, stmt.value)

def exp_flat(target, expr):
    if isinstance(expr, ast.Name):
        return [['set', target, expr.id]]
    elif isinstance(expr, ast.Num):
        return [['set', target, expr.n]]
    elif isinstance(expr, ast.BinOp):
        if isinstance(expr.op, ast.Add):
            op = '+'
        elif isinstance(expr.op, ast.Mult):
            op = '*'
        elif isinstance(expr.op, ast.Sub):
            op = '-'
        elif isinstance(expr.op, ast.Div):
            op = '/'
        elif isinstance(expr.op, ast.Pow):
            assert isinstance(expr.right, ast.Num)
            if expr.right.n == 0:
                return [['set', target, 1]]
            elif expr.right.n == 1:
                return exp_flat(target, expr.left)
            else: 
                if isinstance(expr.left, (ast.Name, ast.Num)):
                    nxt = base = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
                    o = []
                else:
                    nxt = base = mksymbol()
                    o = exp_flat(base, expr.left)
                for i in range(1, expr.right.n):
                    latest = nxt
                    nxt = target if i == expr.right.n - 1 else mksymbol()
                    o.append(['*', nxt, latest, base])
                return o
        else:
            raise Exception("Bad operation: " % ast.dump(stmt.op))
        if isinstance(expr.left, (ast.Name, ast.Num)):
            var1 = expr.left.id if isinstance(expr.left, ast.Name) else expr.left.n
            sub1 = []
        else:
            var1 = mksymbol()
            sub1 = exp_flat(var1, expr.left)
        if isinstance(expr.right, (ast.Name, ast.Num)):
            var2 = expr.right.id if isinstance(expr.right, ast.Name) else expr.right.n
            sub2 = []
        else:
            var2 = mksymbol()
            sub2 = exp_flat(var2, expr.right)
        return sub1 + sub2 + [[op, target, var1, var2]]
    else:
        raise Exception("Unexpected statement value: %r" % stmt.value)

def intvar(arr, varz, var, used, reverse=False):
    if isinstance(var, str):
        if var not in used:
            raise Exception("Using a variable before it is set!")
        arr[varz.index(var)] += (-1 if reverse else 1)
    elif isinstance(var, int):
        arr[0] += var * (-1 if reverse else 1)

def gvplace(inputs, flatcode):
    return ['~one'] + [x for x in inputs] + ['~out'] + [c[1] for c in flatcode if c[1] not in inputs and c[1] != '~out']
    

def ftcs(inputs, flatcode):
    varz = gvplace(inputs, flatcode)
    A, B, C = [], [], []
    used = {i: True for i in inputs}
    for x in flatcode:
        a, b, c = [0] * len(varz), [0] * len(varz), [0] * len(varz)
        if x[1] in used:
            raise Exception("Variable already used: %r" % x[1])
        used[x[1]] = True
        if x[0] == 'set':
            a[varz.index(x[1])] += 1
            intvar(a, varz, x[2], used, reverse=True)
            b[0] = 1
        elif x[0] == '+' or x[0] == '-':
            c[varz.index(x[1])] = 1
            intvar(a, varz, x[2], used)
            intvar(a, varz, x[3], used, reverse=(x[0] == '-'))
            b[0] = 1
        elif x[0] == '*':
            c[varz.index(x[1])] = 1
            intvar(a, varz, x[2], used)
            intvar(b, varz, x[3], used)
        elif x[0] == '/':
            intvar(c, varz, x[2], used)
            a[varz.index(x[1])] = 1
            intvar(b, varz, x[3], used)
        A.append(a)
        B.append(b)
        C.append(c)
    return A, B, C

def gv(varz, assignment, var):
    if isinstance(var, str):
        return assignment[varz.index(var)]
    elif isinstance(var, int):
        return var
    else:
        raise Exception("What kind of expression is this? %r" % var)

def ass_var(inputs, input_vars, flatcode):
    varz = gvplace(inputs, flatcode)
    assignment = [0] * len(varz)
    assignment[0] = 1
    for i, inp in enumerate(input_vars):
        assignment[i + 1] = inp
    for x in flatcode:
        if x[0] == 'set':
            assignment[varz.index(x[1])] = gv(varz, assignment, x[2])
        elif x[0] == '+':
            assignment[varz.index(x[1])] = gv(varz, assignment, x[2]) + gv(varz, assignment, x[3])
        elif x[0] == '-':
            assignment[varz.index(x[1])] = gv(varz, assignment, x[2]) - gv(varz, assignment, x[3])
        elif x[0] == '*':
            assignment[varz.index(x[1])] = gv(varz, assignment, x[2]) * gv(varz, assignment, x[3])
        elif x[0] == '/':
            assignment[varz.index(x[1])] = gv(varz, assignment, x[2]) / gv(varz, assignment, x[3])
    return assignment
                

def ctrvi(code, input_vars):
    inputs, body = extio (parser(code))
    print( 'Inputs')
    print( inputs)
    print( 'Body')
    print( body)
    flatcode = bd_flat(body)
    print( 'Flatcode')
    print( flatcode)
    print( 'Input var assignment')
    print( gvplace(inputs, flatcode))
    A, B, C = ftcs(inputs, flatcode)
    r = ass_var(inputs, input_vars, flatcode)
    return r, A, B, C

r, A, B, C = ctrvi("""
def qeval(x):
    y = x**2
    return y + x + 3
""", [3])
print( 'r')
print( r)
print( 'A')
for x in A:
    print( x)
print( 'B')
for x in B: 
    print( x)
print( 'C')
for x in C: 
    print( x)