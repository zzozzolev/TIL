### 소모 시간
- 9분 22초

### 통과율
- 100%

### my solution
```python
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        answer = [[1]]
        for i in range(1, numRows):
            tmp = []
            
            for j in range(i+1):
                if j == 0 or j == i:
                    tmp.append(1)
                else:
                    tmp.append(answer[i-1][j-1] + answer[i-1][j])
            
            answer.append(tmp)
        
        return answer
```