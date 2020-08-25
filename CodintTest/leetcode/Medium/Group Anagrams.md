### 소모 시간
- 6분

### 통과 여부
- 100%

### 접근법
- 딕셔너리의 key를 `str`로 value를 `list`로 한다.
- 리스트로 바꾼 단어를 정렬하고 빈 문자열로 `join`을 한 것을 key로 하고 해당 단어를 list에 append한다.
- 딕셔너리의 values를 리턴한다.

### 문제점
- `tuple`을 key로 사용하면 굳이 `join`을 안 써도 된다.

### my solution
```
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        
        for word in strs:
            groups["".join(sorted(list(word)))].append(word)
        
        return groups.values()
```
