### 소모 시간
- 9분 57초

### 통과 여부
- 100%

### 접근법
- `0`부터 시작해서 `len(s)-2`까지 index를 늘리면서 `i`번째에 pop한 결과를 insert한다.

### my solution
```
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        for i in range(len(s)-1):
            s.insert(i, s.pop())
```

### other solution
```
class Solution:
    def reverseString(self, s):
        s.reverse()
```