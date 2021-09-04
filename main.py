class Expr:

    def __init__(self):
        None

class MatchCase:

    def __init__(self, pattern, expr):
        self.pattern = pattern
        self.expr = expr

    def pp(self, level):
        tl = '  ' * level
        return '{0}{1} -> {2}'.format(tl, self.pattern, self.expr)

class Match:

    def __init__(self, target, cases):
        self.cases = cases
        self.target = target

    def pp(self, level):
        tl = '  ' * level
        ss = ''
        for c in self.cases:
            ss += c.pp(level + 1) + '\n'
        return '{0}match {1} with\n'.format(tl, self.target) + ss

class FunctionDef:

    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        al = ''
        for arg in self.args:
            al += str(arg)
        return self.name + ' {} '.format(al) + '\n' + self.body.pp(1)

e = Match('a', [MatchCase('[]', '0'), MatchCase('(k:s)', 'k + sumf s')])
sumf = FunctionDef('sumf', ['a'], e)

print(sumf)
