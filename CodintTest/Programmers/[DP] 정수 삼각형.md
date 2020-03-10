### 소요 시간
- 78분
    - 문제 이해: 11분
    - 코드 채점 및 제출: 49분
    - 포기까지: 18분

### 통과율
- 32.1% (효율성 0% ...)

### 접근법
- 경로에 따른 합을 저장할 dict를 만든다. (`[depth][index]`, dict of dict of list)
- `[0][0]`에 삼각형 꼭대기를 추가해 초기화한다.
- `1`번째 index부터 `len(triangle)-1`번째 index를 순회하면서 다음을 반복한다.
- 현재 depth의 index(`j`)를 순회하면서 이전 depth 좌측(`j-1`)의 합과 우측(`j`)의 합에 각각 `triangle[i][j]`을 더해 `sum_dict[i][j]`에 append한다. 
- 위의 반복문이 끝났을 때 마지막 depth에서 max 값을 얻는다.

### 문제점
- 저장하는 자료형을 너무 복잡하게 설정했다.
- 이전 depth에서 최대만 가져오면 되는데 모든 경우를 다 계산해서 시간을 낭비했다.

### my solution
```
from collections import defaultdict

def solution(triangle):
    sum_dict = defaultdict(lambda: defaultdict(list))
    sum_dict[0][0].append(triangle[0][0])
    
    for i in range(1, len(triangle)):
        for j in range(len(triangle[i])):
            # 상위 depth 좌측 우측
            for k in [j-1, j]:
                # 맨 처음 왼쪽, 맨 끝 오른쪽 처리
                if k < 0 or k >= len(triangle[i-1]):
                    continue
                for value in sum_dict[i-1][k]:
                    sum_dict[i][j].append(triangle[i][j] + value)
    
    last_depth = len(triangle) - 1
    max_value = 0
    for j in range(len(sum_dict[last_depth])):
        local_max = max(sum_dict[last_depth][j])
        if local_max > max_value:
            max_value = local_max
        
    return max_value
```

### other solution
- https://codedrive.tistory.com/49 에서 가져옴.
```
def solution(triangle):
    for i in range(1, len(triangle)):
        # 자기의 depth 만큼 index를 가짐.
        for j in range(i + 1):
            # 처음 index와 마지막 index는 하나 밖에 존재하지 않음.
            if j == 0:
                triangle[i][j] += triangle[i-1][j]
            elif j == i:
                triangle[i][j] += triangle[i-1][j-1]
            # 좌측과 우측 중 max 값을 고름.
            else:
                triangle[i][j] += max(triangle[i-1][j], triangle[i-1][j-1])
    return max(triangle[-1])
```