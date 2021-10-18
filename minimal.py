def print_dp(M):
    surrounding = ''
    for i in range(M + 1):
        surrounding += 'case |a| = ' + str(i) + ' ->\n'
        surrounding += '  return B {}'.format(i) + '\n'

    surrounding += 'case |a| > ' + str(M) + ' ->\n'
    surrounding += '  mx = -\u221e\n'
    dpvars = ''
    vs = ''
    for i in range(M):
        surrounding += '  ' + ('  ' * i) + 'for i{} in []:\n'.format(i)
        dpvars += 'a[i{}]'.format(i)
        vs += 'v{}'.format(i)

    recargs = 'v[e]'
    for i in range(0, M - 1):
        recargs += ' v{}'.format(i)
    surrounding += '  ' + ('  ' * M) + 'mx = max(mx, DP a[:i{0}) {1})'.format(M - 1, dpvars) + '\n'
    surrounding += '  return mx\n'
    surrounding += '\n'
    surrounding += 'def DP v {0}'.format(vs) + ' =\n'
    aargs = []
    for i in range(0, M):
        aargs.append('v[{}]'.format(i))
    aargs.append('v0')
    surrounding += '  case |v| = ' + str(M) + ' ->\n'
    surrounding += '    return f({})\n'.format(', '.join(aargs))
    surrounding += '  case |v| > 1 ->\n'
    surrounding += '    max [1, |v| - 1] (\u03bb e. (DP v[:e) {1}) + f(v[e], {2}))'.format(vs, recargs, vs) + '\n\n'
    print(surrounding)

print_dp(1)
