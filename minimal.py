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
    surrounding += dpspec.L + '\n'
    surrounding += dpspec.f + '\n\n'

    paramstr = '' if len(dpspec.parameters) == 0 else ', ' + ', '.join(dpspec.parameters)

    surrounding += 'class Solution(object):\n'

    surrounding += '  def {0}(self, a {1}):\n'.format(dpspec.name, paramstr)
    surrounding += '    if len(a) == ' + str(0) + ':\n'
    surrounding += '      return A_{}(a)'.format(0) + '\n'
    surrounding += '    if len(a) == ' + str(1) + ':\n'
    surrounding += '      return A_{}(a, 0)'.format(1) + '\n'

    surrounding += '    if len(a) > ' + str(M) + ':\n'
    surrounding += '      mx = NEG_INF\n'
    surrounding += '      memo = {}\n'
    surrounding += '      for i in range(len(a)):\n'
    surrounding += '        mx = max(mx, L(a, i))\n' # A_0(a) + A_1(a, i))\n'
    dpvars = ''
    vs = ''
    surrounding += '      ' + ('  ' * 0) + 'for i{} in range(1, len(a)):\n'.format(0)
    dpvars += 'i{}'.format(0)
    vs += 'v{}'.format(0)

    recargs = 'e'
    surrounding += '      ' + ('  ' * M) + 'mx = max(mx, self.DP(a, {1}, memo {2}))'.format(M - 1, dpvars, paramstr) + '\n'
    surrounding += '      return mx\n'
    surrounding += '\n'

    surrounding += '  def DP(self, a, {0}, memo {1}):'.format(vs, paramstr) + '\n'
    surrounding += '    if {0} in memo:\n'.format(vs)
    surrounding += '      return memo[{0}]\n'.format(vs)
    # surrounding += '    v = {0} - 1\n'.format(vs)
    aargs = []
    aargs.append('{}'.format(0))
    aargs.append('v0')
    surrounding += '    if v0 == ' + str(M) + ':\n'
    surrounding += '      return L(a, v0 - 1) + {}\n'.format(dpspec.callf('v0 - 1', 'v0'))
    surrounding += '    if v0 > 1:\n'
    surrounding += '      mx = NEG_INF\n'
    surrounding += '      for e in range(v0):\n'
    surrounding += '        mx = max(mx, A_0([]) + A_1(a, e) + {})\n'.format(dpspec.callf('e', 'v0'))
    surrounding += '      for e in range(1, v0):\n'
    surrounding += '        mx = max(mx, {4} + self.DP(a, {1}, memo {3}))'.format(vs, recargs, vs, paramstr, dpspec.callf('e', vs)) + '\n\n'
    surrounding += '      memo[v0] = mx\n'
    surrounding += '      return mx\n'

    surrounding += '\n\n'
    for case in test_cases:
        if isinstance(case[0], tuple):
            surrounding += 'assert(Solution().{2}({0}, {3}) == {1})\n'.format(case[0][0], case[1], dpspec.name, case[0][1])
        else:
            surrounding += 'assert(Solution().{2}({0}) == {1})\n'.format(case[0], case[1], dpspec.name)
    open(filename, 'w').write(surrounding)

class DPSpec:

    def __init__(self, name, base_cases, L, f, R, parameters=[]):
        self.name = name
        self.base_cases = base_cases
        self.L = L
        self.f = f
        self.R = R
        self.parameters = parameters

    def M(self):
        return len(self.base_cases) - 1

    def callf(self, a, b):
        paramstr = '' if len(self.parameters) == 0 else ', ' + ', '.join(self.parameters)
        return 'M(a, {0}, {1} {2})'.format(a, b, paramstr)

test_cases = [([], 0), ([1], 0), ([0, 200], 200)]
print_dp(DPSpec('maxAbs', ['def A_0(a): return 0', 'def A_1(a, e): return 0'], 'def L(a, v): return 0', 'def M(a, v0, v1): return abs(a[v0] - a[v1])', ''), 'dp.py', test_cases)
run_cmd('python dp.py')

test_cases = [([1, 0], 1), ([-1, 2], 2), ([10,9,2,5,3,7,101,18], 4), ([2,15,3,7,8,6,18], 5)]
lis_base_cases = ['def A_0(a): return 0', 'def A_1(a, e): return 1']
lis = DPSpec('lengthOfLIS', lis_base_cases, 'def L(a, v): return 1', 'def M(a, v0, v1): return 1 if a[v0] < a[v1] else NEG_INF', '')
print_dp(lis, 'lengthOfLIS.py', test_cases)
run_cmd('python lengthOfLIS.py')

name = 'constrainedSubsetSum'
test_cases = [(([1], 1), 1), (([10,2,-10,5,20], 2), 37), (([10,2], 2), 12) , (([-1,-2,-3], 1), -1)]

lis_base_cases = ['def A_0(a): return 0', 'def A_1(a, e): return a[e]']
lis = DPSpec(name, lis_base_cases, 'def L(a, v): return a[v]', 'def M(a, v0, v1, k): return a[v1] if v1 - v0 <= k else NEG_INF', '', ['k']) 
print_dp(lis, name + '.py', test_cases)
run_cmd('python ' + name + '.py')

# Q: How do I want to deal with non-emptiness constraints?
# IOI post office: https://ioinformatics.org/page/ioi-2000/26

