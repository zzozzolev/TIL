### 소요 시간
- 40분
    - 문제 이해: 19분
    - 코드 채점 및 제출: 14분 15초
    - 포기까지: 6분 45초

### 통과율
- 85.0%

### 접근법
- 

### 문제점
- 왜 DP인지 이해하지 못했다.
- `left`의 max가 오른쪽 카드보다 큰 게 있더라도 오른쪽 카드를 버리는 게 이득인 경우가 처리되지 않은 것 같다.

### my solution
```
def solution(left, right):
    score = 0
    
    while not(len(left) == 0 or len(right) == 0):
        # TODO: update idx
        if right[0] < left[0]:
            score += right.pop(0)
        else:
            left_max = max(left)
            # 두 카드 모두 버림
            if left_max <= right[0]:
                left.pop(0)
                right.pop(0)
            else:
                left.pop(0)
            
    return score
```

### other solution
- https://copy-driven-dev.tistory.com/entry/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-ProgrammersPython-%EC%B9%B4%EB%93%9C-%EA%B2%8C%EC%9E%84 에서 가져옴.
```
def solution(left, right):
    # 각각의 위치에서의 점수를 저장하기 위한 배열. axis 0은 오른쪽에 대한 정보 axis 1은 왼쪽으로 대한 정보. index가 커질수록 아래에 있는 카드.
    # 아래 반복문에서 `index-1`로 접근하기 때문에 len보다 1크게 만든다.
    arr = [[0 for _ in range(len(left)+1)] for _ in range(len(right)+1)]

    # 반복문을 돌면서 각각의 경우일 때의 점수를 저장
    for i in range(len(right)):
        for j in range(len(left)):
            # 왼쪽이 큰 경우, 이전 값 + 현재 오른쪽
            if left[j] > right[i]:
                arr[i][j] = arr[i-1][j] + right[i]
            # 모두 버리는 경우 or 왼쪽을 버리는 경우
            else:
                arr[i][j] = max(arr[i-1][j-1], arr[i][j-1])

    # array의 가장 마지막
    return arr[len(right)-1][len(left)-1]
```