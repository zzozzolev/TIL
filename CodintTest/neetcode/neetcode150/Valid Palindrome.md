### 소모 시간
- 6분 51초

### 통과율
- 100%

### my solution
```python
import re

class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = re.sub("[^a-z0-9]", "" ,s.lower())
        
        left, right = 0, len(cleaned) - 1
        while left < right:
            if cleaned[left] != cleaned[right]:
                return False
            left += 1
            right -= 1
        
        return True
```

### other solution
- https://leetcode.com/problems/valid-palindrome/solutions/350929/solution-in-python-3-beats-100-two-lines-o-1-solution-as-well/
```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
    	s = [i for i in s.lower() if i.isalnum()]
    	return s == s[::-1]
```
