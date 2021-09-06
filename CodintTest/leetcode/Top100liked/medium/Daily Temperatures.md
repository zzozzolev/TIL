### 소모 시간
- 12분 5초

### 통과율
- 64%

### my solution
```
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        answer = []
        for i in range(len(temperatures)-1):
            count = 0
            for j in range(i+1, len(temperatures)):
                if temperatures[i] < temperatures[j]:
                    count = j - i
                    break
            answer.append(count)
            
        answer.append(0)
        
        return answer
```

### other solution
- https://leetcode.com/problems/daily-temperatures/discuss/136017/Elegant-Python-Solution-with-Stack
- Everytime a higher temperature is found, we update answer of the peak one in the stack.
- 다음 값이 크지 않으면 넘어감.
```
  def dailyTemperatures(self, T):
    ans = [0] * len(T)
    stack = []
    for i, t in enumerate(T):
      while stack and T[stack[-1]] < t:
        cur = stack.pop()
        ans[cur] = i - cur
      stack.append(i)

    return ans
```