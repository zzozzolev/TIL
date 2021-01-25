# 소모 시간
- 6분 19초

# 통과율
- 100%

# my solution
```
from collections import defaultdict

class Solution:
    def firstUniqChar(self, s: str) -> int:
        d = defaultdict(int)
        
        for char in s:
            d[char] += 1
        
        for key in d:
            if d[key] == 1:
                return s.index(key)
        
        return -1
```