# Dynamic Programming Solution Generator

This repository contains a solver that generates
dynamic programs that solve optimization problems
of the following form:

Given an array, maximize (or minimize) an objective
function over all subsequences of the array.

If a is the original array and
s is the array of indices included in the subsequence
then the objective is of the form:

L(a, s[0]) + (Sum from i = 1 to len(a): M(a, s[i - 1], s[i])) + R(a, s[len(s) - 1])

Where L, M, and R are functions specified by the user.

The user can also optionally specify that they want to find
the optimal value of the objective function over all subsequences
of a given length, k.

The entire program is contained in `main.py`

Example problems included in `main.py` (The brute force solutions to these problems are O(2^N))
* Max abs - Maximize the sum of absolute values of
differences between adjacent entries of the subsequence
* [Longest increasing subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - dpgen produces an O(N^2) solution. The optimal solution is O(Nlog(N)).
* [Constrained subsequence sum](https://leetcode.com/problems/constrained-subsequence-sum/) - dpgen produces an O(N^2) solution. The optimal solution is O(Nlog(N)).
* [Post office (IOI 2000)](https://ioinformatics.org/page/ioi-2000/26) - dpgen produces an [O(N^2 K) solution](https://www.iarcs.org.in/inoi/online-study-material/problems/postoffice-soln.php#solution) that matches the one provided by the IOI.


To run the examples:

```
python main.py
```

This make take a while due to a large test case
for the post office problem.

