### 소모 시간
- 5분 43초

### 통과율
- 100%

### my solution 1
- sort: O(NlogN)
```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)
```

### my solution 2
- dict: O(N)
```python
from collections import defaultdict

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        d = defaultdict(int)
        
        # Increase counts of char
        for char in s:
            d[char] += 1
        
        # Increase counts of char
        for char in t:
            d[char] -= 1

        return all([e == 0 for e in d.values()])
```

### my solution3
- counter: O(N)
```python
from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        c = Counter(s)
        
        # Decrease counts of char
        for char in t:
            c[char] -= 1

        return all([e == 0 for e in c.values()])
```
