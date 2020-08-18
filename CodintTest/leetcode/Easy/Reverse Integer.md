### 소모 시간
- 14분 57초

### 통과 여부
- 100%

### 접근법
- `x`를 slicing을 이용해 reverse한다.
- reverse한 것의 마지막이 `-`라면 마지막을 제외하고 마이너스를 곱하고 int로 변환한다. 그렇지 않은 경우 그대로 int로 변환한다.
- `-2 ** 31`보다 크거나 같고 `2 ** 31`보다 작다면 위에서 변환한 int를 반환하고 그렇지 않다면 0을 반환한다.

### my solution
```
class Solution:
    def reverse(self, x: int) -> int:
        reversed_str = str(x)[::-1]
        if reversed_str[-1] == "-":
            answer = - int(reversed_str[:-1])
        else:
            answer = int(reversed_str)
        
        if - 2 ** 31 <= answer and answer <= 2 ** 31 - 1:
            return answer
        else:
            return 0
```
