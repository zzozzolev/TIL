### 소모 시간
- 9분 42초

### 통과율
- 100%

### 접근법
- `numRows`가 0이면 empty list를 반환한다.
- `answer`를 `[[1]]`로 초기화하고 `0`부터 `numRows-2`까지 순회를 하면서 index `i`를 얻는다. `i`는 이전 row에 대한 index이다. 
- 다음의 과정을 반복하면서 각 row를 얻는다.
    - `0`부터 `i+1`까지 index `j`를 얻는다.
    - `j`가 맨 처음 혹은 맨 마지막이라면 `1`을 추가한다. 그렇지 않다면 이전 row의 `j-1`과 `j`를 더한 값을 추가한다.
    - row를 `answer`에 추가한다.

### 문제점
- 이전 row의 index를 얻는 것보다 다른 솔루션처럼 현재 row의 index를 얻는 것이 더 직관적이다.

### my solution
```
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows == 0:
            return []
        
        answer = [[1]]
        for i in range(numRows-1):
            row = []
            for j in range(i+2):
                if j == 0 or j == i+1:
                    row.append(1)
                else:
                    row.append(answer[i][j-1]+answer[i][j])
            answer.append(row)
            
        return answer
```

### other solution
- https://leetcode.com/problems/pascals-triangle/solution/ comment
```
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
            if numRows   == 0: return []
            elif numRows == 1: return [[1]]
            Tri = [[1]]
            for i in range(1,numRows):
                row = [1]
                for j in range(1,i):
                    row.append(Tri[i-1][j-1] + Tri[i-1][j]) 
                row.append(1)
                Tri.append(row)
            return Tri
```