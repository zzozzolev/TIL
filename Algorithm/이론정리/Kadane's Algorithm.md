# 무슨 알고리즘?
- DP의 일종

# 용도
- 최대 부분 합 구하기

# 핵심
- 부분의 최대 합, 즉 local maximum을 매번 업데이트하고 global maximum과 비교한다.

# pseudo code
```
Array a
local_maximum = 0
global_maximum = 0

for i from 0 to len(a) - 1
    local_maximum = max(a[i], local_maximum + a[i])
    global_maximum = max(local_maximum, global_maximum)
    i++

return global_maximum
```

# 시간 복잡도
- O(N)

# 응용
- 이전 인덱스와의 차이 중 최대가 되는 값
    - [max profit 문제](https://app.codility.com/programmers/lessons/9-maximum_slice_problem/max_profit/)
    - [max profit 해설](https://sustainable-dev.tistory.com/22)

# Reference
https://sustainable-dev.tistory.com/23?category=809125