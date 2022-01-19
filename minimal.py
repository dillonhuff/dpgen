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
    surrounding += '      memo = {}\n'
    dpvars = ''
    vs = ''
    for i in range(M):
        surrounding += '      ' + ('  ' * i) + 'for i{} in range(1, len(a)):\n'.format(i)
        dpvars += 'i{}'.format(i)
        vs += 'v{}'.format(i)

    recargs = 'e'
    for i in range(0, M - 1):
        recargs += ' v{}'.format(i)
    surrounding += '      ' + ('  ' * M) + 'mx = max(mx, self.DP(a, {1}, memo))'.format(M - 1, dpvars) + '\n'
    surrounding += '      return mx\n'
    surrounding += '\n'

    surrounding += '  def DP(self, a, {0}, memo):'.format(vs) + '\n'
    surrounding += '    if {0} in memo:\n'.format(vs)
    surrounding += '      return memo[{0}]\n'.format(vs)
    surrounding += '    v = {0} - 1\n'.format(vs)
    aargs = []
    for i in range(0, M):
        aargs.append('{}'.format(i))
    aargs.append('v0')
    surrounding += '    if v + 1 == ' + str(M) + ':\n'
    surrounding += '      return max(B_0([]) + B_1([v0]), B_0([]) + B_1(v) + f(a, v, v0))\n'
    surrounding += '    if v + 1 > 1:\n'
    surrounding += '      mx = 0\n'
    surrounding += '      for e in range(v + 1):\n'
    surrounding += '        mx = max(mx, B_0([]) + B_1([e]) + f(a, e, v0))\n'
    surrounding += '      for e in range(1, v + 1):\n'
    surrounding += '        mx = max(mx, self.DP(a, {1}, memo) + f(a, e, {2}))'.format(vs, recargs, vs) + '\n\n'
    surrounding += '      memo[v0] = mx\n'
    surrounding += '      return mx\n'

    surrounding += '\n\n'
    for case in test_cases:
        surrounding += 'assert(Solution().{2}({0}) == {1})\n'.format(case[0], case[1], dpspec.name)
    open(filename, 'w').write(surrounding)

class DPSpec:

    def __init__(self, name, base_cases, f, parameters=[]):
        self.name = name
        self.base_cases = base_cases
        self.f = f
        self.parameters = parameters

    def M(self):
        return len(self.base_cases) - 1

test_cases = [([], 0), ([1], 0), ([0, 200], 200)]
print_dp(DPSpec('maxAbs', ['def B_0(a): return 0', 'def B_1(a): return 0'], 'def f(a, v0, v1): return abs(a[v0] - a[v1])'), 'dp.py', test_cases)
run_cmd('python dp.py')

test_cases = [([1, 0], 1), ([-1, 2], 2), ([10,9,2,5,3,7,101,18], 4), ([2,15,3,7,8,6,18], 5)]
lis_base_cases = ['def B_0(a): return 0', 'def B_1(a): return 1']
lis = DPSpec('lengthOfLIS', lis_base_cases, 'def f(a, v0, v1): return 1 if a[v0] < a[v1] else NEG_INF')
print_dp(lis, 'lengthOfLIS.py', test_cases)
run_cmd('python lengthOfLIS.py')

name = 'constrainedSubsetSum'
test_cases = [] # [([1, 0], 1), ([-1, 2], 2), ([10,9,2,5,3,7,101,18], 4), ([2,15,3,7,8,6,18], 5)]
lis_base_cases = ['def B_0(a): return 0', 'def B_1(a): return 1']
lis = DPSpec(name, lis_base_cases, 'def f(a, v0, v1): return 1 if a[v0] < a[v1] else NEG_INF', ['k'])
print_dp(lis, name + '.py', test_cases)
run_cmd('python ' + name + '.py')

