# 소모 시간
- 12분 50초

# 통과율
- 100%

# 문제점
- 불필요한 딕셔너리 사용함.
- 26 base인 거 처음에 몰랐음.

# my solution
```
class Solution:
    def titleToNumber(self, s: str) -> int:
        # 각 자릿수마다 (자릿수) * 26 * A,B..
        mapping = {chr(e): i + 1 for i, e in enumerate(range(ord("A"), ord("Z") + 1))}
        
        answer = 0
        for i, char in enumerate(s[:-1]):
            pos = len(s) - i - 1
            answer += (26 ** pos) * mapping[char]
        
        answer += mapping[s[-1]]
        
        return answer
```

# other solution
- https://leetcode.com/problems/excel-sheet-column-number/discuss/52289/Explanation-in-Python
```
def titleToNumber(s):
    return sum((ord(char) - 64) * (26 ** exp) for exp, char in enumerate(s[::-1]))
```