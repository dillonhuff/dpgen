# Dynamic Programming Solution Generator

This repository contains a solver that generates
dynamic programs that solve optimization problems
on subsequences.

The entire program is contained in `main.py`

Example problems included in `main.py` (The brute force solutions to these problems are O(2^N))
* Max abs - Maximize the sum of absolute values of
differences between adjacent entries of the subsequence
* [Longest increasing subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - dpgen produces an O(N^2) solution. The optimal solution is O(Nlog(N)).
* [Constrained subsequence sum](https://leetcode.com/problems/constrained-subsequence-sum/) - dpgen produces an O(N^2) solution. The optimal solution is O(Nlog(N)).
* [Post office (IOI 2000)](https://ioinformatics.org/page/ioi-2000/26) - dpgen produces an [O(N^2 K) solution](https://www.iarcs.org.in/inoi/online-study-material/problems/postoffice-soln.php#solution) that is acceptable at the IOI


To run the examples:

```
python main.py
```

This make take a while due to a large test case
for the post office problem.

