### 소모 시간
- 38분 36초

### 통과율
- 85%

### 문제점
- `sliced`가 0인게 틀리는 거 같은데 대체 왜 이게 0이 되는지 모르겠다... `s`의 최소 길이가 1이니까 `row`랑 `col`도 최소 1이어서 아예 for문을 안 돌지는 않을 거 같은데..
- 

### my solution
```
import math
import re

def encryption(s):
    s = re.sub(" ", "", s)
    s = s.strip()
    row, col = get_row_col(s)
    
    sliced = []
    for i in range(row):
        sliced.append(s[i*col:(i+1)*col])
    
    if len(sliced) == 0:
        return s

    answer = []
    for j in range(len(sliced[0])):
        tmp = ""
        for i in range(len(sliced)):
            if j < len(sliced[i]):
                tmp += sliced[i][j]
        answer.append(tmp)
    
    return " ".join(answer)

def get_row_col(s):
    s_len_sqrt = math.sqrt(len(s))
    lower_bound = int(s_len_sqrt)
    upper_bound = int(s_len_sqrt) + 1
    
    row, col = 0, 0
    # 1 <= len(s) <= 81
    for i in range(1, 9):
        if lower_bound <= i and i + 1 <= upper_bound:
            row, col = i, i + 1
            break
    
    # 1
    if row * row >= len(s):
        col = row
    elif row * col < len(s) and col * col >= len(s):
        row = col
    
    return row, col
```

### other solution
- https://www.hackerrank.com/challenges/encryption/forum
```
def encryption(s):
    sm = s.replace(" ","")
    r = math.floor(math.sqrt(len(sm)))
    c = math.ceil(math.sqrt(len(sm)))
    
    answer = []
    for i in range(c):
        # i번째 부터 c칸씩 stride로 char 가져옴
        answer.append(sm[i::c]) 
    
    return " ".join(answer)
```