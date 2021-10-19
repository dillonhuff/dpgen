import os

def run_cmd(cmd):
    res = os.system(cmd)
    assert(res == 0)

def print_dp(dpspec, filename, test_cases):
    M = dpspec.M()

    surrounding = ''
    surrounding += 'import math\n\n'
    for bf in dpspec.base_cases:
        surrounding += bf + '\n'
    surrounding += dpspec.f + '\n\n'

    surrounding += 'NEG_INF = -1000000000\n\n'

    surrounding += 'def driver(a):\n'
    for i in range(M + 1):
        surrounding += '  if len(a) == ' + str(i) + ':\n'
        surrounding += '    return B_{}(a)'.format(i) + '\n'

    surrounding += '  if len(a) > ' + str(M) + ':\n'
    surrounding += '    mx = NEG_INF\n'
    dpvars = ''
    vs = ''
    for i in range(M):
        surrounding += '    ' + ('  ' * i) + 'for i{} in range(1, len(a)):\n'.format(i)
        dpvars += 'a[i{}]'.format(i)
        vs += 'v{}'.format(i)

    recargs = 'v[e]'
    for i in range(0, M - 1):
        recargs += ' v{}'.format(i)
    surrounding += '    ' + ('  ' * M) + 'mx = max(mx, DP(a[:i{0}], {1}))'.format(M - 1, dpvars) + '\n'
    surrounding += '    return mx\n'
    surrounding += '\n'
    surrounding += 'def DP(v, {0}):'.format(vs) + '\n'
    aargs = []
    for i in range(0, M):
        aargs.append('v[{}]'.format(i))
    aargs.append('v0')
    surrounding += '  if len(v) == ' + str(M) + ':\n'
    surrounding += '    return f({})\n'.format(', '.join(aargs))
    surrounding += '  if len(v) > 1:\n'
    surrounding += '    mx = NEG_INF\n'
    surrounding += '    for e in range(1, len(v)):\n'
    surrounding += '      mx = max(mx, DP(v[:e], {1}) + f(v[e], {2}))'.format(vs, recargs, vs) + '\n\n'
    surrounding += '    return mx\n'

    surrounding += '\n\n'
    for case in test_cases:
        surrounding += 'assert(driver({0}) == {1})\n'.format(case[0], case[1])
    open(filename, 'w').write(surrounding) # rint(surrounding)

class DPSpec:

    def __init__(self, base_cases, f):
        self.base_cases = base_cases
        self.f = f

    def M(self):
        return len(self.base_cases) - 1

test_cases = [([], 0), ([1], 0), ([0, 200], 200)]
print_dp(DPSpec(['def B_0(a): return 0', 'def B_1(a): return 0'], 'def f(v0, v1): return abs(v0 - v1)'), 'dp.py', test_cases)
run_cmd('python dp.py')

