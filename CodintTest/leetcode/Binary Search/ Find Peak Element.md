### 소모 시간
- 12분 6초

### 통과율
- 100%

### 문제 분석
- peak의 방향에 맞춰서 바이너리 서치를 하면 됨.
- peak가 왼쪽에 있는 경우 high를 mid로 지정하고 왼쪽을 탐색하면 되고, 오른쪽에 있는 경우 low를 mid + 1로 지정하고 오른쪽을 탐색하면 됨.

### My Solution
```java
public int findPeakElement(int[] nums) {
        if (nums.length >= 2) {
            if (nums[0] > nums[1])
                return 0;
            
            if (nums[nums.length - 2] < nums[nums.length - 1])
                return nums.length - 1;
        }
        
        for (int i = 1; i < nums.length - 1; i++) {
            if (nums[i - 1] < nums[i] && nums[i] > nums[i + 1])
                return i;
        }

        return 0;
    }
```
- 문제에서는 O(log N)으로 풀라고 했는데 그렇게 안 풀고 O(N)으로 풀었음.

### Other Solution
- https://leetcode.com/problems/find-peak-element/solutions/127550/find-peak-element/?orderBy=most_votes
```java
public class Solution {
    public int findPeakElement(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int mid = (l + r) / 2;
            if (nums[mid] > nums[mid + 1])
                r = mid;
            else
                l = mid + 1;
        }
        return l;
    }
}
```