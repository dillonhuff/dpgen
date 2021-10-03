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

class BigOp:

    def __init__(self, binop, local_cost, memory):
        self.binop = binop
        self.local_cost = local_cost
        self.memory = memory

class DPProblem:

    def __init__(self, name, accum, obj):
        self.name = name
        self.accum = accum
        self.obj = obj

    def cpp_program(self):
        body = '\n  const int N = a.size();\n'
        body += '\n  vector<int> dp(N, 0);\n'
        body += '  int mx = ' + str(objective[0]) + ';\n'
        body += '  for (int i = 0; i < N; i++) {\n'
        body += '    dp[i] = ' + '{1}(a[i]);\n'.format(objective[-1].binop, objective[-1].local_cost)
        body += '    for (int j = 0; j < i; j++) {\n'
        body += ('  ' * 3) + 'dp[i] = max(dp[i], dp[j] {0} {1}(a[i]));\n'.format(objective[-1].binop, objective[-1].local_cost)
        body += '    }\n'
        body += '  }\n'
        # TODO support argmin or min
        body += '  return max(mx, *max_element(begin(dp), end(dp)));\n'
        return 'int {0}(const vector<int>& a)'.format(self.name) + '{ ' + body + '}'

objective = [0, BigOp('+', 'f', 0)]
dpprob = DPProblem('maxsum', 'max', objective)
print(dpprob.cpp_program())
