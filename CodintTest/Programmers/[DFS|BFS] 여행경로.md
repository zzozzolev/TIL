### 소요 시간
- 40분
    - 문제 이해: 13분
    - 코드 작성: 16분
    - 테스트 케이스 성공: 6분
    - 포기하기 까지: 3분

### 통과율
- 50%

### 접근법
- tickets의 출발점을 key로 하고 도착점을 list of element로 하는 dictionary `source_to_dest` 선언.
- `source_to_dest`의 각각의 value를 알파벳 순으로 정렬.
- `source_to_dest`의 모든 value의 length가 0이 될 때 까지, 첫번째 원소를 pop해서 `dest`로 지정.
- `start`에 `dest` 할당.

### 문제점
- 처음에 `pop(0)`가 아니라 `pop()`으로 해서 원하는 순서대로 `dest`를 얻지 못했음.
- *만일 가능한 경로가 2개 이상일 경우 알파벳 순서가 앞서는 경로를 return 합니다.* 라는 문제 조건을 잘못 이해해서 무조건 앞서는 거 선택하라는 줄 알았다...

### my solution
```
from collections import defaultdict

def solution(tickets):
    source_to_dest = sort_dest(get_source_to_dest(tickets))
    start = "ICN"
    paths = [start]
    # 주어진 항공권 모두 사용
    while not is_empty(source_to_dest):
        dest = source_to_dest[start].pop(0)
        paths.append(dest)
        start = dest
    return paths

def get_source_to_dest(tickets):
    source_idx, dest_idx = 0, 1
    source_to_dest = defaultdict(list)
    for ticket in tickets:
        source, dest = ticket[source_idx], ticket[dest_idx]
        source_to_dest[source].append(dest)
    return source_to_dest

def sort_dest(source_to_dest):
    # 알파벳 순서가 앞서는 경로
    return {key: sorted(value) for key, value in source_to_dest.items()}

def is_empty(source_to_dest):
    return all([len(value) == 0 for value in source_to_dest.values()])
```

### other solution
```
def solution(tickets):
    routes = {}
    for t in tickets:
        # 출발 공항이 키, value는 갈 수 있는 공항 들어있는 리스트
        routes[t[0]] = routes.get(t[0], []) + [t[1]]
    for r in routes:
        routes[r].sort(reverse=True)
    stack = ["ICN"]  # 빈 걸로 초기화할 수도 있지만 무조건 ICN은 넣어서 시작하므로
    path = []  # 가려고 하는 경로 표현
    while len(stack) > 0:  # stack이 다 없어질 때까지
        top = stack[-1]
        # 어떤 공항에서 출발하는 표가 한장도 없다면 또는 있었는데, 다 써버렸다면
        if top not in routes or len(routes[top]) == 0:
            path.append(stack.pop())
        else:
            stack.append(routes[top][-1])  # 역순으로 정렬을 해놨으니, 가장 앞서는
            # -1 직전까지 슬라이스를 해서, 떼어낸다. pop을 적용해도 된다.
            routes[top] = routes[top][:-1]
    return path[::-1]  # 역순- [start,end,step]이므로
```