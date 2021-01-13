### 소모 시간
- 27분 4초

### 통과 여부
- 100%

### 접근법
- row, column, 3 x 3 sub-boxes에 대해 각각 for문으로 순회하면서 `.`을 제외한 count가 1보다 크면 `False`를 반환한다. 모두 통과하면 `True`를 반환한다.

### 문제점
- `Counter`를 사용하지 않고도 `set`만으로도 충분히 해결할 수 있었을 것 같다.

### my solution
```
from collections import Counter

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # row
        for i in range(9):
            nums = [e for e in board[i] if e != "."]
            if len(nums) == 0:
                continue
            if self.is_count_gt_one(nums):
                return False
        
        # col
        for j in range(9):
            nums = []
            for i in range(9):
                if board[i][j] != ".":
                    nums.append(board[i][j])
            if len(nums) == 0:
                continue
            if self.is_count_gt_one(nums):
                return False
        
        # 3 x 3
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                nums = []
                for i in range(3):
                    for j in range(3):
                        if board[row+i][col+j] != ".":
                            nums.append(board[row+i][col+j])
                if len(nums) == 0:
                    continue
                if self.is_count_gt_one(nums):
                    return False
        return True
    
    def is_count_gt_one(self, nums):
        c = Counter(nums)
        _, count = c.most_common(1)[0]
        return count > 1
```

### other solution
- 출처: https://leetcode.com/problems/valid-sudoku/discuss/15451/A-readable-Python-solution
```
def isValidSudoku(self, board):
    return (self.is_row_valid(board) and
            self.is_col_valid(board) and
            self.is_square_valid(board))

def is_row_valid(self, board):
    for row in board:
        if not self.is_unit_valid(row):
            return False
    return True

def is_col_valid(self, board):
    for col in zip(*board):
        if not self.is_unit_valid(col):
            return False
    return True
    
def is_square_valid(self, board):
    for i in (0, 3, 6):
        for j in (0, 3, 6):
            square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not self.is_unit_valid(square):
                return False
    return True
    
def is_unit_valid(self, unit):
    unit = [i for i in unit if i != '.']
    return len(set(unit)) == len(unit)
```