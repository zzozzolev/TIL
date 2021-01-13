### 소모 시간
- 34분 38초

### 통과율
- 40%

### 문제점
- 문제 자체를 제대로 이해 못한 것 같다. 앞이랑 뒤랑 같으면 되는 건 줄...

### my solution
```
from collections import defaultdict

class Solution:
    def longestPalindrome(self, s: str) -> str:
        d = defaultdict(list)
        
        if len(s) == 0:
            return s
        
        for i, char in enumerate(s):
            d[char].append(i)
        
        answer = ""
        for value in d.values():
            if value[-1] - value[0] > len(answer):
                answer = s[value[0]:value[-1]+1]
        
        if answer == "":
            answer = s[0]
            
        return answer
```

### other solution
```
class Solution:
    def longestPalindrome(self, s: str) -> str:
        m = ''  # Memory to remember a palindrome
        for i in range(len(s)):  # i = start, O = n
            for j in range(len(s), i, -1):  # j = end, O = n^2
                if len(m) >= j-i:  # To reduce time
                    break
                elif s[i:j] == s[i:j][::-1]:
                    m = s[i:j]
                    break
        return m
```