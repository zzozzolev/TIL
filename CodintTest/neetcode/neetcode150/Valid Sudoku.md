### 소모 시간
- 29분 44초

### 통과율
- 100%

### my solution
```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # row
        for i in range(len(board)):
            counter = {str(k): 0 for k in range(1, 10)}
            for j in range(len(board[i])):
                if board[i][j] != ".":
                    counter[board[i][j]] += 1
                    if counter[board[i][j]] == 2:
                        return False

        # column
        for j in range(len(board[0])):
            counter = {str(k): 0 for k in range(1, 10)}
            for i in range(len(board)):
                if board[i][j] != ".":
                    counter[board[i][j]] += 1
                    if counter[board[i][j]] == 2:
                        return False

        # 3 * 3
        origin = (0, 0)
        for i in range(3):
            for j in range(3):
                start = (3 * i, 3 * j)
                counter = {str(k): 0 for k in range(1, 10)}
                for k in range(3):
                    for l in range(3):
                        x = start[0] + k
                        y = start[1] + l
                        if board[x][y] != ".":
                            counter[board[x][y]] += 1
                            if counter[board[x][y]] == 2:
                                return False
        return True
```

### other solution
- https://leetcode.com/problems/valid-sudoku/solutions/15472/short-simple-java-using-strings/
```java
public boolean isValidSudoku(char[][] board) {
    Set seen = new HashSet();
    for (int i=0; i<9; ++i) {
        for (int j=0; j<9; ++j) {
            if (board[i][j] != '.') {
                String b = "(" + board[i][j] + ")";
                if (!seen.add(b + i) || !seen.add(j + b) || !seen.add(i/3 + b + j/3))
                    return false;
            }
        }
    }
    return true;
}
```