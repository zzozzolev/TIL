### 소모 시간
- 44분 39초

### 통과율
- 100%

### 접근법
- BFS
- 특이한 점이라면 가능한 포인트를 바로 넣지 않고 일단 저장했다가 나중에 ways 계산해서 넣는다는 것이다.

### 문제점
- 일반 BFS랑 살짝 다르다보니 K를 count할 때 도착지가 바로 주변에 있으면 고려를 안 해서 틀렸었다.
- 너무 기존 알고리즘에 익숙해져서 일반적인 거에서 조그만 꼬아도 바로 헤매는 것 같다...

### my solution
```
from collections import deque

# Complete the countLuck function below.
def countLuck(matrix, k):
    maps, start_p, dest_p = parse_matrix(matrix)
    n, m = len(maps), len(maps[0])
    visited = [ [False] * m for _ in range(n) ]
    queue = deque( [ [start_p, 0] ] )
    visited[start_p[0]][start_p[1]] = True
    
    while len(queue) > 0:
        coord, ways = queue.popleft()
        row, col = coord
        count = 0
        cache = []

        for dr, dc in [ (0, 1), (1, 0), (0, -1), (-1, 0) ]:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < n \
                and 0 <= new_col < m \
                and not visited[new_row][new_col] \
                and maps[new_row][new_col] in [".", "*"]:
                    visited[new_row][new_col] = True
                    count += 1
                    cache.append( (new_row, new_col) )
        
        for coord in cache:
            if count == 1:
                queue.append( [coord, ways] )
            else:
                queue.append( [coord, ways+1] )
            
            if queue[-1][0] == dest_p:
                if queue[-1][1] == k:
                    return "Impressed"
                else:
                    return "Oops!"

def parse_matrix(matrix):
    maps = [ [None] * len(matrix[0]) for _ in range(len(matrix)) ]
    start_p, dest_p = None, None
    for row in range(len(matrix)):
        matrix[row] = matrix[row].strip()
        for col in range(len(matrix[row])):
            maps[row][col] = matrix[row][col]
            if maps[row][col] == "M":
                start_p = (row, col)
            if maps[row][col] == "*":
                dest_p = (row, col)

    return maps, start_p, dest_p
```
