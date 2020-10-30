### 소모 시간
- 1시간

### 통과율
- 60%

### 문제점
- 원래 좌표가 인덱싱이라 반대여서 좌표 때문에 좀 헤맸다. 문제에서 좌표가 주어지면 원래 인덱싱과 맞는지 맞지 않는다면 어떻게 처리해야되는지 꼭 생각하자.
- 못 푼 문제 모두 Runtime Error가 났다. 인덱싱 때문에 나는 거 같은데 도저히 왜 나는지 모르겠다.
- 결국 가장 가까운 것을 찾으면 되는 게 아닌가 싶었서 나는 퀸의 위치부터 O(n)으로 서치를 했는데 다른 솔루션을 보니 장애물을 기준으로 그냥 찾아버린다. 이게 메모리도 안 들고 O(k)로 속도도 더 빠르니 더 좋은 접근 같다.

### my solution
```
def queensAttack(n, k, r_q, c_q, obstacles):
    board = [ [False] * n for _ in range(n) ]
    check_obstacles(board, obstacles)
    r_q, c_q = n - r_q, n - c_q
    answer = 0
    # plus direction
    direction = [ (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1) ]
    for dr, dc in direction:
        answer += get_count(board, dr, dc, r_q, c_q)
    
    return answer


def check_obstacles(board, obstacles):
    for obs in obstacles:
        raw_row, raw_col = obs
        row, col = n - raw_row, n - raw_col
        board[row][col] = True


def get_count(board, dr, dc, r_q, c_q):
    cur_row, cur_col = r_q + dr, c_q + dc
    count = 0
    
    while 0 <= cur_row < len(board) and \
            0 <= cur_col < len(board) and \
            not board[cur_row][cur_col]:
        count += 1
        cur_row, cur_col = cur_row + dr, cur_col + dc

    return count
```

### other solution
- 출처: https://github.com/RyanFehr/HackerRank/blob/master/Algorithms/Implementation/Queen%27s%20Attack%20II/Solution.java
- 그냥 조건 다 따져서 8 방향에서 가장 가까운 걸 찾는다.