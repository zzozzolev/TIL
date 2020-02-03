### 소요 시간
- 28분
    - 문제 이해: 7분
    - 코드 작성: 14분
    - 테스트 케이스 성공: 1분
    - 포기하기 까지: 6분

### 통과율
- 23.1%

### 접근법
- union 이용. 
- parents를 자기 자신으로 초기화하고 rank를 1로 초기화. 
- 연결돼 있다면 rank가 더 높은 쪽으로 자기 자신과 자식의 부모 업데이트. 
- rank가 같다면 더 높은 index로 업데이트.
- unique한 parents 개수 반환.

### 문제점
- 왜 안 될까 ㅠㅜ...?

### my solution
```
def solution(n, computers):
    # 자기 자신으로 부모 초기화
    parents = list(range(n))
    ranks = [1] * n
    
    for i in range(len(computers)):
        for j in range(len(computers[i])):            
            # 자기 자신
            if i == j:
                continue
            else:
                if computers[i][j]:
                    if ranks[i] < ranks[j]:
                        parents, ranks = update(parents, i, j, ranks)
                    elif ranks[i] > ranks[j]:
                        parents, ranks = update(parents, j, i, ranks)
                    else:
                        if i < j:
                            parents, ranks = update(parents, i, j, ranks)
                        else:
                            parents, ranks = update(parents, j, i, ranks)
    
    return len(set(parents))
        
def update(parents, old, new, ranks):
    parents, count = update_child(parents, old, new)
    ranks[new] += count
    return parents, ranks

def update_child(parents, old, new):
    count = 0
    for idx, p in enumerate(parents):
        if p == old:
            parents[idx] = new
            count += 1
    return parents, count
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