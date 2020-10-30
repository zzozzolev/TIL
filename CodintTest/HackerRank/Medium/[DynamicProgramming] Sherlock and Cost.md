### 소모 시간
- 30분 48초

### 통과율
- 17%

### 접근법
- 문제에서는 `A[i]`가 `1`과 `B[i]` 사이의 어떤 값이라도 가질 수 있다고 했지만, 차이가 최대가 되려면 결국 최소와 최대 차이를 이용해야 된다고 생각했다. 즉, `1` 아니면 `B[i]`가 될 거라고 가정했다.

### 문제점
- 위의 가정까지는 맞는데 무조건 `1` 다음에 `B[1]` 이런 식으로 번갈아 등장할거라고 잘못 생각했다.
- 사실 이상해서 제대로 될 거 같지가 않았다..

### my solution
```
# Complete the cost function below.
def cost(B):
    max_start = [0] * len(B)
    min_start = [0] * len(B)

    for i in range(1, len(B)):
        if i % 2 == 0:
            max_start[i] = max_start[i-1] + B[i] - 1
            min_start[i] = min_start[i-1] + abs(1 - B[i-1])
        else:
            max_start[i] = max_start[i-1] + abs(1 - B[i-1])
            min_start[i] = min_start[i-1] + B[i] - 1
    
    return max( max_start[-1], min_start[-1] )
```

### other solution
- https://nillk.tistory.com/44
- 현재 `1`을 선택해도 이전에 `1`을 선택할 수 있고 `B[i]`를 선택해도 이전에 `B[i]`를 선택할 수 있다.