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
        else:
            assert(len(self.args) == 0)
            return '{}'.format(self.tag)

def prim(name):
    return ASTNode(name, [])

def lam(var, expr):
    return ASTNode('lam', [var, expr])

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


