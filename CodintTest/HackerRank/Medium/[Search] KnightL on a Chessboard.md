### 소모 시간
- 31분 54초

### 통과율
- 100%

### 접근법
- `(a, b)`와 `(b, a)`가 같으니 diagonal과 그 오른쪽만 구하고 왼쪽은 구하지 않는다.
- bfs를 이용한다.

### my solution
```
from collections import deque

def knightlOnAChessboard(n):
    nums = [ [-1] * n for _ in range(n) ]

    for i in range(1, n):
        for j in range(1, n):
            if i <= j:
                nums[i][j] = bfs(i, j, n)
    
    for i in range(1, n):
        for j in range(1, n):
            if j < i:
                nums[i][j] = nums[j][i]

    result = []
    for i in range(1, n):
        result.append(nums[i][1:n])
    return result


def bfs(a, b, n):
    visited = [ [False] * n for _ in range(n) ]
    queue = deque( [ [(0, 0), 0] ] )
    visited[0][0] = True

    while len(queue) > 0:
        coord, move = queue.popleft()
        x, y = coord
        possible_moves = get_pairs(a, b) + get_pairs(b, a)
        for dx, dy in possible_moves:
            new_x, new_y = x + dx, y + dy
            
            if new_x == n - 1 and new_y == n - 1:
                return move + 1
            
            if 0 <= new_x < n and 0 <= new_y < n \
                and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                queue.append( [(new_x, new_y), move + 1] )
    
    return -1

    
def get_pairs(i, j):
    return [ (i, j), (i, -j), (-i, j), (-i, -j) ]
```