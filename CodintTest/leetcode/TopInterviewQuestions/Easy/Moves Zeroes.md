### 소모 시간
- 20분 56초

### 통과율
- 100%

### 문제점
- 0이 아닌 것의 위치만 트랙킹하면 굳이 두 번 for문을 돌릴 필요가 없다.

### my solution
```java
class Solution {
    public void moveZeroes(int[] nums) {
        for (int i = 0; i < nums.length; ++i) {
            if (nums[i] != 0)
                continue;
            
            for (int j = i; j < nums.length; ++j) {
                if (nums[j] != 0) {
                    nums[i] = nums[j];
                    nums[j] = 0;
                    break;
                }
            }
            
        }
    }
}
```

### other solution
- https://leetcode.com/problems/move-zeroes/discuss/72011/Simple-O(N)-Java-Solution-Using-Insert-Index/74623
```java
public void moveZeroes(int[] nums) {
    if (nums == null || nums.length == 0) {
        return;
    }
    
    int cur = 0;

    for (int i = 0; i < nums.length; ++i) {
        if (nums[i] != 0) {
            int temp = nums[cur];
            nums[cur++] = nums[i];
            nums[i] = temp;
        }
    }
}
```