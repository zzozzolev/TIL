### 소요 시간
- 28분
    - 문제 이해: 7분
    - 코드 작성: 14분
    - 테스트 케이스 성공: 1분
    - 포기하기 까지: 6분

### 통과율
- 100%

### 접근법
- union 이용. 
- parents를 자기 자신으로 초기화하고 rank를 1로 초기화. 
- 연결돼 있다면 rank가 더 높은 쪽으로 자기 자신과 자식의 부모 업데이트. 
- rank가 같다면 더 높은 index로 업데이트.
- unique한 parents 개수 반환.

### 문제점
- 필요 없는 ranks 사용
- element 값이 아닌 인덱스를 사용해 건너건너 연결된 경우 잘못된 부모 값을 가짐.
    - 1-3, 3-5 일 때 3번의 부모를 1로 바꿨다가 나중에 3번이랑 5번이 연결 돼있길래 5번의 부모를 1로 바꿔야 하는데 인덱스로 하면 3으로 바뀜


### my solution
```
def solution(n, computers):
    # 자기 자신으로 부모 초기화
    parents = list(range(n))
    
    for i in range(len(computers)):
        for j in range(len(computers[i])):            
            # 자기 자신
            if i == j:
                continue
            else:
                if computers[i][j]:
                    update_child(parents, i, j)

    return len(set(parents))
        
def update_child(parents, old, new):
    old_parents = parents[old]
    for idx, p in enumerate(parents):
        if p == old_parents:
            parents[idx] = parents[new]
    return parents
```

### other solution
- https://geonlee.tistory.com/54#google_vignette 에서 가져옴.
```
def solution(n, computers):
    answer = 0
    visited = [0 for i in range(n)]
    def dfs(computers, visited, start):
        stack = [start]
        while stack:
            j = stack.pop()
            if visited[j] == 0:
                visited[j] = 1
            for i in range(0, len(computers)):
                if computers[j][i] ==1 and visited[i] == 0:
                    stack.append(i)
    i=0
    while 0 in visited:
        if visited[i] ==0:
            dfs(computers, visited, i)
            answer +=1
        i+=1
    return answer
``` 