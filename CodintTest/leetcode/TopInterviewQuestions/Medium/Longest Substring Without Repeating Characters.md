### 소모 시간
- 17분 16초

### 통과 여부
- 100%

### 접근법
- 만약 `len(s)`가 0이면 0을 반환한다.
- `group`이라는 list를 만들어 고유한 char만 담기도록 한다. 처음에는 `s[0]`로 초기화를 하고 정답은 1로 초기화한다.
- `1`부터 `len(s)-1`까지의 인덱스를 얻으면서 `s[i]`가 `group`에 있으면 `group`내에서의 index를 얻고 `group`을 `group[index+1:]`로 설정한다. 
- `group`에 `s[i]`를 append한다.
- 정답을 정답과 `len(group)` 중 max 값으로 한다.

### 문제점
- 어떤 경우든 group에 append를 해야하는데 그렇지 않아서 케이스를 통과 못 했다.
- index를 써서 속도가 느렸다. 기존의 index를 dict에 캐쉬해두면 더 빠르게 가능하다.

### my solution
```
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0
        group = [s[0]]
        answer = 1
        for i in range(1, len(s)):
            if s[i] in group:
                idx =  group.index(s[i])
                group = group[idx+1:]
            group.append(s[i])
            answer = max(answer, len(group))
            
        return answer
```

### other solution
```
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        dct = {}
        max_so_far = curr_max = start = 0
        for index, i in enumerate(s):
            if i in dct and dct[i] >= start:
                max_so_far = max(max_so_far, curr_max)
                curr_max = index - dct[i]
                start = dct[i] + 1
            else:
                curr_max += 1
            dct[i] = index
        return max(max_so_far, curr_max)
```