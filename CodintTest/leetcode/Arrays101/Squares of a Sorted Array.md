### 소모 시간
- 31분

### 통과율
- 100%

### my solution
```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        i = 0
        j = len(nums) - 1
        
        answer = list(nums)
        idx = len(nums) - 1
        
        while i <= j:
            if abs(nums[i]) ** 2 <= abs(nums[j]) ** 2:
                answer[idx] = abs(nums[j]) ** 2
                j -= 1
            else:
                answer[idx] = abs(nums[i]) ** 2
                i += 1
            
            idx -= 1
        
        return answer
```

### other solution
```java
class Solution {
    public int[] sortedSquares(int[] A) {
        int n = A.length;
        int[] result = new int[n];
        int i = 0, j = n - 1;
        for (int p = n - 1; p >= 0; p--) {
            if (Math.abs(A[i]) > Math.abs(A[j])) {
                result[p] = A[i] * A[i];
                i++;
            } else {
                result[p] = A[j] * A[j];
                j--;
            }
        }
        return result;
    }
}
```