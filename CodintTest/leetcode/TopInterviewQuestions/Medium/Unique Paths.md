### 소모 시간
- 14분 48초

### 통과 여부
- 100%

### 접근법
- `n`만큼의 row를 가지고 `m`만큼의 col을 가지는 2D list를 순회하면서 위와 왼쪽 인덱스의 값을 더해 반복문을 끝내고 마지막 인덱스의 값을 반환한다.

### 문제점
- 어차피 같은 위치에 있는 걸 다음에 더하므로 굳이 2D일 필요가 없다.

### my solution
```
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        way = [[0] * m for _ in range(n)]
        way[0][0] = 1
        
        for i in range(n):
            for j in range(m):
                if i == 0 and j == 0:
                    continue
                else:
                    if j == 0:
                        way[i][j] = way[i-1][j]
                    elif i == 0:
                        way[i][j] = way[i][j-1]
                    else:
                        way[i][j] = way[i-1][j] + way[i][j-1]
        
        return way[-1][-1]
```

### other solution
- https://leetcode.com/problems/unique-paths/discuss/23234/Accpeted-simple-Python-DP-solution. comment
```
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for i in range(1, m):
            for j in range(1, n):
                dp[j] = dp[j - 1] + dp[j]
        return dp[-1] if m and n else 0
```