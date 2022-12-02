### 소모 시간
- 5분 44초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int maximumWealth(int[][] accounts) {
        int m = accounts.length;
        int n = accounts[0].length;

        int maxSum = 0;
        for (int i = 0; i < m; i++) {
            int sum = 0;
            for (int j = 0; j < n; j++)
                sum += accounts[i][j];
            maxSum = Math.max(maxSum, sum);
        }

        return maxSum;
    }
}
```