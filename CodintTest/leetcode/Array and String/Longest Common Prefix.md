### 소모 시간
- 12분 3초

### 통과율
- 100%

### my solution
```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 1:
            return strs[0]
        
        min_length = min([len(s) for s in strs])
        
        answer = ""
        for i in range(min_length):
            for j in range(0, len(strs) - 1):    
                if strs[j][i] != strs[j + 1][i]:
                    return answer
            
            # 1개는 무조건 있음
            answer += strs[0][i]
        
        return answer
```

### other solution
```python
def longestCommonPrefix(self, strs):
    """
    :type strs: List[str]
    :rtype: str
    """
    if not strs:
        return ""
    shortest = min(strs,key=len)
    for i, ch in enumerate(shortest):
        for other in strs:
            if other[i] != ch:
                return shortest[:i]
    return shortest 
```
- 최대 길이의 공통 프리픽스는 제일 짧은 스트링이다.
- 굳이 별도의 스트링을 만들지 않고 제일 짧은 스트링에서 슬라이싱만 해도 된다.
