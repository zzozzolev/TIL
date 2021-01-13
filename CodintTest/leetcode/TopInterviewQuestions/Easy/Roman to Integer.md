### 소모 시간
- 12분 30초

### 통과 여부
- 100%

### 접근법
- 로마자와 숫자에 대한 맵핑을 만든다.
- input `s`를 reverse하고 list로 만든다.
- `0`부터 `len(s)-2`까지 인덱스를 얻으면서 다음의 조건을 확인한다.
    - `s[i]`와 `s[i+1]`이 같다면 정답에 `s[i]`에 대한 mapping 값을 더한다.
    - `s[i]`와 `s[i+1]`가 다르다면 두 경우에 대해서 검사한다.
        - `s[i]`의 mapping 값이 `s[i+1]`에 대한 mapping 값보다 작다면 정답에 `s[i]`에 대한 mapping 값을 더한다. ex) VI -> IV
        - 그렇지 않다면 정답에 `s[i]`에 대한 mapping 값에서 `s[i+1]`에 대한 mapping 값을 빼고 한 번 더 계산하지 않기 위해 `s[i+1]`를 None으로 만든다.

### 문제점
- list로 변환하는 과정에서 시간이 오래 걸렸을 것 같다. 그냥 string 자체로 했어도 충분했을 듯.

### my solution
```
class Solution:
    def romanToInt(self, s: str) -> int:
        mapping = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }
        
        s = list(reversed(s))
        answer = 0
        for i in range(len(s)-1):
            if s[i] is None:
                continue
                
            if s[i] == s[i+1]:
                answer += mapping[s[i]]
            
            elif s[i] != s[i+1]:
                if mapping[s[i]] < mapping[s[i+1]]:
                    answer += mapping[s[i]]
                else:
                    answer += mapping[s[i]] - mapping[s[i+1]]
                    s[i+1] = None
        
        if s[-1] is not None:
            answer += mapping[s[-1]]
        
        return answer
```

### other solution
```
def romanToInt(self, s):

    romans = {'M': 1000, 'D': 500 , 'C': 100, 'L': 50, 'X': 10,'V': 5,'I': 1}

    prev_value = running_total = 0
    
    for i in range(len(s)-1, -1, -1):
        int_val = romans[s[i]]
        if int_val < prev_value:
            running_total -= int_val
        else:
            running_total += int_val
        prev_value = int_val
    
    return running_total
```