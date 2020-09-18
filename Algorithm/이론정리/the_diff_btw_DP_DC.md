# 정리한 이유
- `DP`도 subproblems를 이용하는거고 `DC(divide-and-conquer)`도 subproblems를 이용하는 거여서 무슨 차이인지 헷갈렸다.

# 핵심
- `DP`는 `DC`의 extension(?)이다.
- `DC`에 overlapping subproblems + optimal substructure를 요구 조건으로 하고 `memoization`과 `tabulation` 중 선택하는 방식이랄까.

# 예시
- `binary search`는 `DC`이지만 `DP`가 될 수 없다. 왜냐면 overlapping subproblems가 없기 때문이다. 문제를 쪼갤 때마다 각각이 서로 독립적이다. decision graph가 아니라 decision tree이다.
- `minimum edit distance`는 `DP`이다. 특정 subproblem을 풀기 위해서는 그 subproblem을 잘게 나눈 subproblem을 풀어야 하기 때문이다. 또한 subproblem의 optimal solution이 다음 문제의 optimal solution과 같다.

# Reference
- https://www.geeksforgeeks.org/dynamic-programming-vs-divide-and-conquer/