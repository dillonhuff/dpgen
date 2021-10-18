def is_binop(op):
    return op.tag in ['=', '>', '<', '+', '-']

class ASTNode:

    def __init__(self, tag, args):
        self.tag = tag
        self.args = args

    def __repr__(self):
        if self.tag == 'call':
            if self.args[0].tag == 'len':
                return '|{0}|'.format(self.args[1]) #, self.args[2])
            if self.args[0].tag == 'aref':
                return '{0}[{1}]'.format(self.args[1], self.args[2])
            if is_binop(self.args[0]):
                assert(len(self.args) == 3)
                return '({0} {1} {2})'.format(self.args[1], self.args[0], self.args[2])
            #' '.join(map(str, self.args[1:]))) 
            return '({0} {1})'.format(self.args[0], ' '.join(map(str, self.args[1:])))
        elif self.tag == 'lam':
            return '(\u03bb {0}. {1})'.format(self.args[0], ' '.join(map(str, self.args[1:])))
        elif self.tag == 'case':
            return '(case {0})'.format(' '.join(map(str, self.args)))
        elif self.tag == 'metavar':
            assert(len(self.args) == 1)
            return '{}'.format(self.args[0])
        else:
            if (len(self.args) != 0):
                print('ERROR: Error multiple arguments to primtive or metavar {}'.format(self.args))
            assert(len(self.args) == 0)
            return '{}'.format(self.tag)

def prim(name):
    return ASTNode(name, [])

def lam(var, expr):
    return ASTNode('lam', [var, expr])

def mv(name):
    return ASTNode('metavar', name)

def call(fun, args):
    return ASTNode('call', [fun] + args)

def case(cases):
    return ASTNode('case', cases)

def fc(fun, args):
    assert(isinstance(fun, str))
    return call(prim(fun), args)

def sub(a, b):
    return fc('-', [a, b])

ssa = call(prim('ss'), [prim('a')])
F = case([
    fc('=', [call(prim('len'), [prim('s')]), prim(0)]),
    prim(0),
    fc('>', [fc('len', [prim('s')]), prim(0)]),
    fc('sum', [0, sub(fc('len', [prim('s')]), prim(1)),
        lam(prim('i'), fc('aref', [prim('s'), prim('i')]))])
    ])
obj = lam(prim('s'), call(F, [prim('s')]))
nd = call(prim('max'), [ssa, obj])

print(nd)

def matchr(pattern, e, res):
    print('pat = ', pattern)
    print('e   = ', e)
    print('res =', res)
    if pattern.tag == 'metavar':
        res[pattern] = e
        print('  res = ', res)
    elif pattern.tag != e.tag or len(pattern.args) != len(e.args):
        print('Error: pattern tag {0} does not match {1}'.format(pattern, e))
        assert(False)
    else:
        for i in range(0, len(pattern.args)):
            matchr(pattern.args[i], e.args[i], res)
    return

def match(pattern, e):
    res = {}
    matchr(pattern, e, res)
    return res

def push_max(e):
    r = match(fc('max', [fc('ss', [mv('A')]), lam(mv('S'), mv('F'))]), e)
    print(r)
    print('Match res')
    for mvar in r:
        print('  ', mvar, ' -> ', r[mvar])
    return e

def convert_to_dp(problem):
    # Push max
    pl = push_max(problem)
    # Determine last M cases
    # Extract named function for innermost max (DP)
    # Pull last sum term out of max
    # Determine the last free variable needed
    # to move the sum term
    # Pull the last term out of the max
    # Unify the resulting expression with a call to DP
    return pl

print(convert_to_dp(nd))
