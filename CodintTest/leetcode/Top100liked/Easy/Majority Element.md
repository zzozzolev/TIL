# 소모 시간
- 4분 55초

# 통과율
- 100%

# my solution
```
from collections import defaultdict

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        maj_elem = -1
        d = defaultdict(int)
        
        for n in nums:
            d[n] += 1
            if d[n] >= d[maj_elem]:
                maj_elem = n
        
        return maj_elem
```