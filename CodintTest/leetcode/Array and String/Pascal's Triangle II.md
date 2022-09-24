### 소모 시간
- 24분 40초

### 통과율
- 100%

### my solution
```python
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        answer = [0] * (rowIndex + 1)
        
        for i in range(rowIndex + 1):
            prev, cur = answer[0], answer[0]
            for j in range(i + 1):
                cur = answer[j]
                if j == 0 or j == i:
                    answer[j] = 1
                else:
                    answer[j] = prev + answer[j]
                prev = cur
        
        return answer
```

### other solution
- https://leetcode.com/problems/pascals-triangle-ii/discuss/38420/Here-is-my-brief-O(k)-solutions
```java
class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<int> A(rowIndex+1, 0);
        A[0] = 1;
        for(int i=1; i<rowIndex+1; i++)
            for(int j=i; j>=1; j--)
                A[j] += A[j-1];
        return A;
    }
};
```
- `row[i][j] = row[i-1][j-1] + row[i-1][j]`이다.
- 따라서 `j`이후의 인덱스에 의존하지 않으니 뒤에서부터 업데이트하면 별도로 이전 것을 저장할 필요없이 쭉 업데이트하면 된다.
