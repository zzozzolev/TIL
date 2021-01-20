# 소모 시간
- 10분 11초

# 통과율
- 100%

# my solution
```
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        else:
            first, second = 1, 2
            answer = first + second
        
            for i in range(3, n):
                first = second
                second = answer
                answer = first + second
                
            return answer
```