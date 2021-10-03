class ASTNode:

    def __init__(self, tag, args):
        self.tag = tag
        self.args = args

    def __repr__(self):
        if self.tag == 'call':
            return '({0} {1})'.format(self.args[0], self.args[1:])
        elif self.tag == 'lam':
            return '(lam {0}. {1})'.format(self.args[0], self.args[1:])
        else:
            print('Tag:', self.tag)
            assert(len(self.args) == 0)
            return '{}'.format(self.tag)

def prim(name):
    return ASTNode(name, [])

def lam(var, expr):
    return ASTNode('lam', [var, expr])

def call(fun, args):
    return ASTNode('call', [fun] + args)

ssa = call(prim('ss'), [prim('a')])
obj = lam(prim('s'), call('F', [prim('s')]))
nd = call(prim('max'), [ssa, obj])

print(nd)


