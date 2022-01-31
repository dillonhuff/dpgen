import os

class DPSpec:

    def __init__(self, name, base_cases, L, f, R, parameters=[], maximize=True, fixed_length=False):
        self.name = name
        self.base_cases = base_cases
        self.L = L
        self.f = f
        self.R = R
        self.parameters = parameters
        self.maximize = maximize
        self.fixed_length = fixed_length;

    def worst(self):
        return 'NEG_INF' if self.maximize else 'INF'

    def direction(self):
        return 'max' if self.maximize else 'min'

    def M(self):
        return len(self.base_cases) - 1

    def callf(self, a, b):
        paramstr = '' if len(self.parameters) == 0 else ', ' + ', '.join(self.parameters)
        return 'M(a, {0}, {1} {2})'.format(a, b, paramstr)

def print_dp(dpspec, filename, test_cases):
    M = dpspec.M()

    txt = ''
    txt += 'import math\n\n'
    txt += 'NEG_INF = -1000000000\n\n'
    txt += 'INF = 1000000000\n\n'
    for bf in dpspec.base_cases:
        txt += bf + '\n'
    txt += dpspec.L + '\n'
    txt += dpspec.f + '\n'
    txt += dpspec.R + '\n\n'

    paramstr = '' if len(dpspec.parameters) == 0 else ', ' + ', '.join(dpspec.parameters)

    txt += 'class Solution(object):\n'

    txt += '  def {0}(self, a {1}):\n'.format(dpspec.name, paramstr)
    txt += '    if len(a) == ' + str(0) + ':\n'
    txt += '      return A_{}(a)'.format(0) + '\n'
    txt += '    if len(a) == ' + str(1) + ':\n'
    txt += '      return A_{}(a, 0)'.format(1) + '\n'

    txt += '    if len(a) > ' + str(M) + ':\n'
    txt += '      mx = {}\n'.format(dpspec.worst())
    txt += '      memo = {}\n'
    if dpspec.fixed_length:
        txt += '      if k == 1:\n'
        txt += '        for i in range(len(a)):\n'
        txt += '          mx = {}(mx, L(a, i) + R(a, i))\n'.format(dpspec.direction())
        txt += '      else:\n'
        txt += '        ' + ('  ' * 0) + 'for i{} in range(1, len(a)):\n'.format(0)
        dpvars = 'i{}'.format(0)
        vs = 'v{}'.format(0)

        txt += '        ' + ('  ' * M) + 'mx = {3}(mx, self.DP(a, {1}, memo {2}) + R(a, {1}))'.format(M - 1, dpvars, paramstr, dpspec.direction()) + '\n'
        txt += '      return mx\n'
    else:
        txt += '      for i in range(len(a)):\n'
        txt += '        mx = {}(mx, L(a, i) + R(a, i))\n'.format(dpspec.direction())
        txt += '      ' + ('  ' * 0) + 'for i{} in range(1, len(a)):\n'.format(0)
        dpvars = 'i{}'.format(0)
        vs = 'v{}'.format(0)

        txt += '      ' + ('  ' * M) + 'mx = {3}(mx, self.DP(a, {1}, memo {2}) + R(a, {1}))'.format(M - 1, dpvars, paramstr, dpspec.direction()) + '\n'
        txt += '      return mx\n'
    txt += '\n'

    txt += '  def DP(self, a, {0}, memo {1}):'.format(vs, paramstr) + '\n'
    txt += '    if ({0} {1}) in memo:\n'.format(vs, paramstr)
    txt += '      return memo[({0} {1})]\n'.format(vs, paramstr)
    aargs = []
    aargs.append('{}'.format(0))
    aargs.append('v0')
    if dpspec.fixed_length:
        txt += '    mx = {}\n'.format(dpspec.worst())
        txt += '    if k == 2:\n'
        txt += '      for e in range(v0):\n'
        txt += '        mx = {1}(mx, L(a, e) + {0})\n'.format(dpspec.callf('e', 'v0'), dpspec.direction())
        txt += '    else:\n'
        txt += '      for e in range(k, v0):\n'
        txt += '        mx = {5}(mx, {4} + self.DP(a, {1}, memo {3} - 1))'.format(vs, 'e', vs, paramstr, dpspec.callf('e', vs), dpspec.direction()) + '\n\n'
    else:
        txt += '    mx = {}\n'.format(dpspec.worst())
        txt += '    for e in range(v0):\n'
        txt += '      mx = {1}(mx, L(a, e) + {0})\n'.format(dpspec.callf('e', 'v0'), dpspec.direction())
        txt += '    for e in range(1, v0):\n'
        txt += '      mx = {5}(mx, {4} + self.DP(a, {1}, memo {3}))'.format(vs, 'e', vs, paramstr, dpspec.callf('e', vs), dpspec.direction()) + '\n\n'
    txt += '    memo[(v0 {})] = mx\n'.format(paramstr)
    txt += '    return mx\n'

    txt += '\n\n'
    for case in test_cases:
        if isinstance(case[0], tuple):
            txt += 'assert(Solution().{2}({0}, {3}) == {1})\n'.format(case[0][0], case[1], dpspec.name, case[0][1])
        else:
            txt += 'assert(Solution().{2}({0}) == {1})\n'.format(case[0], case[1], dpspec.name)
    open(filename, 'w').write(txt)

def run_cmd(cmd):
    res = os.system(cmd)
    assert(res == 0)

test_cases = [([], 0), ([1], 0), ([0, 200], 200)]
print_dp(DPSpec('maxAbs', ['def A_0(a): return 0', 'def A_1(a, e): return 0'], 'def L(a, v): return 0', 'def M(a, v0, v1): return abs(a[v0] - a[v1])', 'def R(a, v): return 0'), 'dp.py', test_cases)
run_cmd('python dp.py')

test_cases = [([1, 0], 1), ([-1, 2], 2), ([10,9,2,5,3,7,101,18], 4), ([2,15,3,7,8,6,18], 5)]
lis_base_cases = ['def A_0(a): return 0', 'def A_1(a, e): return 1']
lis = DPSpec('lengthOfLIS', lis_base_cases, 'def L(a, v): return 1', 'def M(a, v0, v1): return 1 if a[v0] < a[v1] else NEG_INF', 'def R(a, v): return 0')
print_dp(lis, 'lengthOfLIS.py', test_cases)
run_cmd('python lengthOfLIS.py')

name = 'constrainedSubsetSum'
test_cases = [(([1], 1), 1), (([10,2,-10,5,20], 2), 37), (([10,2], 2), 12) , (([-1,-2,-3], 1), -1)]

lis_base_cases = ['def A_0(a): return 0', 'def A_1(a, e): return a[e]']
lis = DPSpec(name, lis_base_cases, 'def L(a, v): return a[v]', 'def M(a, v0, v1, k): return a[v1] if v1 - v0 <= k else NEG_INF', 'def R(a, v): return 0', ['k']) 
print_dp(lis, name + '.py', test_cases)
run_cmd('python ' + name + '.py')

# IOI post office: https://ioinformatics.org/page/ioi-2000/26
name = 'postOffice'
large_post = list(map(int, '7 96 113 143 191 243 384 421 444 465 469 513 522 602 622 660 702 781 800 811 820 853 879 952 996 1005 1011 1041 1086 1102 1123 1151 1162 1169 1172 1190 1201 1207 1247 1345 1410 1424 1438 1445 1476 1477 1592 1603 1662 1681 1701 1736 1858 1880 1896 1973 2012 2030 2046 2077 2095 2103 2148 2201 2203 2272 2303 2308 2355 2398 2425 2481 2502 2510 2559 2594 2663 2712 2752 2761 2811 2819 2869 3007 3016 3034 3049 3137 3214 3254 3305 3340 3363 3387 3471 3559 3565 3614 3629 3791 3814 3824 3870 3872 3898 3927 3947 4006 4106 4146 4178 4188 4267 4330 4371 4389 4448 4487 4523 4556 4606 4643 4644 4707 4738 4740 4774 4785 4786 4827 4829 4863 4870 4888 4970 4975 5072 5075 5090 5160 5204 5301 5339 5368 5376 5472 5489 5494 5499 5534 5540 5542 5563 5623 5640 5715 5724 5743 5833 5834 5854 5876 5880 5932 5941 5955 6046 6065 6067 6081 6100 6104 6181 6214 6215 6225 6226 6255 6260 6354 6371 6395 6425 6444 6512 6579 6616 6646 6693 6730 6841 6909 6926 6955 7007 7042 7043 7055 7092 7185 7224 7232 7240 7260 7359 7417 7473 7503 7551 7563 7604 7645 7653 7657 7666 7712 7718 7747 7766 7769 7780 7806 7841 7842 7846 7858 7871 7922 7933 7968 7982 7983 7996 8016 8031 8081 8141 8226 8268 8334 8358 8361 8407 8417 8448 8512 8540 8570 8685 8690 8760 8820 8899 8901 8919 8934 8937 9000 9082 9105 9134 9150 9191 9209 9215 9228 9255 9321 9336 9361 9364 9370 9386 9391 9417 9431 9453 9546 9557 9575 9607 9618 9761 9777 9782 9814 9869 9877 9893 9897'.split(' ')))
test_cases = [(([], 0), 0), (([1, 2, 3, 4, 5], 1), 6), (([1, 2, 3, 6, 7, 9, 11, 22, 44, 50], 5), 9), ((list(map(int, '1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765'.split(' '))), 3), 5026), ((large_post, 25), 24780)]
lis_base_cases = ['def A_0(a): return 0', 'def A_1(a, e): return a[e]']
M = 'def M(a, v0, v1, k): return sum(map(lambda x: min(abs(a[v0] - x), abs(a[v1] - x)), a[v0:v1]))'
lis = DPSpec(name, lis_base_cases, 'def L(a, v): return sum(map(lambda x: a[v] - x, a[0:v]))', M, 'def R(a, v): return sum(map(lambda x: x - a[v], a[v+1:]))', parameters=['k'], maximize=False, fixed_length=True)
print_dp(lis, name + '.py', test_cases)
run_cmd('python ' + name + '.py')


