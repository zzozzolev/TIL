### 소모 시간
- 34분 55초

### 통과 여부
- sol1: non-pass (시간 초과)
- sol2: non-pass (틀렸습니다.)

### 문제점
- DP인 걸 전혀 몰랐다...현재의 최소는 결국 이전의 최소에 현재의 최소를 더한 것이니 DP문제 였다.
- 모든 케이스를 볼 필요가 없다.
- DP인 걸 알고 나름 DP로 풀어봤는데 처음 시작도 최솟값으로 해서 다른 케이스에 대해서 처리하지 못했다.
- 단순히 값 하나로 결정되는게 아니라 선택할 수 없는 색에 대해서 모두 봐야하므로 이차원 or 일차원 리스트가 필요하다.

### my solution
```
n = int(input())
inputs = []
for _ in range(n):
    inputs.append( sorted( [ (int(e), i) for i, e in enumerate(input().split()) ] ) )

# 선택, 비용
# [([0, 1], 10), ]

targets = [([i], cost) for cost, i in inputs[0]]

while len(targets[0][0]) != len(inputs):
    nums, cur_cost = targets.pop(0)
    for costs in inputs[1:]:
        # cost 오름차순으로 정렬돼있음
        for cost, i in costs:
            if nums[-1] != i:
                targets.append( (nums+[i], cur_cost + cost) )
                break

print(min([cost for nums, cost in targets]))
```

### my solution2
```
n = int(input())

answer = 0
prev_idx = -1
for _ in range(n):
    costs = [int(e) for e in input().split()]

    min_cost, min_idx = float("inf"), -1
    for i, cost in enumerate(costs):
        if i == prev_idx:
            continue
        
        # min이 하나만 있나?
        if cost < min_cost:
            min_cost = cost
            min_idx = i
        
    answer += min_cost
    prev_idx = min_idx

print(answer)
```

### other solution
- https://hongku.tistory.com/266