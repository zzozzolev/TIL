### 소모 시간
- 9분

### 통과 여부
- 100%

### 접근법
- `s`가 empty string이면 valid 하다고 여겨지므로 `len(s)`가 0인 경우 `True`를 리턴한다.
- `s`의 char를 하나씩 순회하면서 다음을 반복한다.
    - open bracket이면 stack에 char를 추가한다.
    - close bracket인데 `len(s)`가 0인 경우 `False`를 리턴하고 그렇지 않은 경우 stack에서 pop을 해서 open bracket을 얻었을 때 종류가 맞지 않으면 `False`를 리턴한다.
- 위의 반복문을 마치고나서 stack이 비어있다면 `True`를 반환하고 그렇지 않다면 `False`를 반환한다.

### my solution
```
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) == 0:
            return True

        push_chars = ["(", "[", "{"]
        mapping = {
            "(": ")",
            "[": "]",
            "{": "}"
        }
        
        stack = []
        for ch in s:
            if ch in push_chars:
                stack.append(ch)
            else:
                if len(stack) == 0:
                    return False
                else:
                    top = stack.pop()
                    if mapping[top] != ch:
                        return False
        
        if len(stack) == 0:
            return True
        else:
            return False
```

### other solution
```
def isValid(self, s):
    bracket_map = {"(": ")", "[": "]",  "{": "}"}
    open_par = set(["(", "[", "{"])
    stack = []
    for i in s:
        if i in open_par:
            stack.append(i)
        elif stack and i == bracket_map[stack[-1]]:
                stack.pop()
        else:
            return False
    return stack == []
```