### 소모 시간
- 8분 25초

### 통과율
- 100%

### 접근법
- `s`에 대한 카운트는 1을 더하고 `t`에 대한 카운트는 1을 뺀다.
- 모든 char둘의 차이가 모두 0인 경우 anagram으로 판단한다.

### my solution
```
from collections import defaultdict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_count = defaultdict(int)
        for char in s:
            s_count[char] += 1
        
        for char in t:
            s_count[char] -= 1
        
        for value in s_count.values():
            if value != 0:
                return False
        
        return True
```
