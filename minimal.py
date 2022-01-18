import os

def run_cmd(cmd):
    res = os.system(cmd)
    assert(res == 0)

def print_dp(dpspec, filename, test_cases):
    M = dpspec.M()

    surrounding = ''
    surrounding += 'import math\n\n'
    surrounding += 'NEG_INF = -1000000000\n\n'
    for bf in dpspec.base_cases:
        surrounding += bf + '\n'
    surrounding += dpspec.f + '\n\n'

    surrounding += 'class Solution(object):\n'

    surrounding += '  def {0}(self, a):\n'.format(dpspec.name)
    for i in range(M + 1):
        surrounding += '    if len(a) == ' + str(i) + ':\n'
        surrounding += '      return B_{}(a)'.format(i) + '\n'

    surrounding += '    if len(a) > ' + str(M) + ':\n'
    surrounding += '      mx = NEG_INF\n'
    dpvars = ''
    vs = ''
    for i in range(M):
        surrounding += '      ' + ('  ' * i) + 'for i{} in range(1, len(a)):\n'.format(i)
        dpvars += 'a[i{}]'.format(i)
        vs += 'v{}'.format(i)

    recargs = 'v[e]'
    for i in range(0, M - 1):
        recargs += ' v{}'.format(i)
    surrounding += '      ' + ('  ' * M) + 'mx = max(mx, self.DP(a, a[:i{0}], {1}))'.format(M - 1, dpvars) + '\n'
    surrounding += '      return mx\n'
    surrounding += '\n'

    surrounding += '  def DP(self, a, v, {0}):'.format(vs) + '\n'
    aargs = []
    for i in range(0, M):
        aargs.append('v[{}]'.format(i))
    aargs.append('v0')
    surrounding += '    if len(v) == ' + str(M) + ':\n'
    surrounding += '      return max(B_0([]) + B_1([v0]), B_0([]) + B_1(v) + f(a, {}))\n'.format(', '.join(aargs))
    surrounding += '    if len(v) > 1:\n'
    surrounding += '      mx = 0\n'
    surrounding += '      for e in range(len(v)):\n'
    surrounding += '        mx = max(mx, B_0([]) + B_1([v[e]]) + f(a, v[e], v0))\n'
    surrounding += '      for e in range(1, len(v)):\n'
    surrounding += '        mx = max(mx, self.DP(a, v[:e], {1}) + f(a, v[e], {2}))'.format(vs, recargs, vs) + '\n\n'
    surrounding += '      return mx\n'

    surrounding += '\n\n'
    for case in test_cases:
        surrounding += 'assert(Solution().{2}({0}) == {1})\n'.format(case[0], case[1], dpspec.name)
    open(filename, 'w').write(surrounding)

class DPSpec:

    def __init__(self, name, base_cases, f):
        self.name = name
        self.base_cases = base_cases
        self.f = f

    def M(self):
        return len(self.base_cases) - 1

test_cases = [([], 0), ([1], 0), ([0, 200], 200)]
print_dp(DPSpec('maxAbs', ['def B_0(a): return 0', 'def B_1(a): return 0'], 'def f(a, v0, v1): return abs(v0 - v1)'), 'dp.py', test_cases)
run_cmd('python dp.py')

test_cases = [([1, 0], 1), ([-1, 2], 2), ([10,9,2,5,3,7,101,18], 4), ([2,15,3,7,8,6,18], 5)]
lis_base_cases = ['def B_0(a): return 0', 'def B_1(a): return 1']
lis = DPSpec('lengthOfLIS', lis_base_cases, 'def f(a, v0, v1): return 1 if v0 < v1 else NEG_INF')
print_dp(lis, 'lengthOfLIS.py', test_cases)
run_cmd('python lengthOfLIS.py')




