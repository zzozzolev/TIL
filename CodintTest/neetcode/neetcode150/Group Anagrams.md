### 소모 시간
- 4분 26초

### 통과율
- 100%

### my solution
```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_dict = defaultdict(list)
        for word in strs:
            anagram_dict["".join(sorted(word))].append(word)
        
        return anagram_dict.values()
```