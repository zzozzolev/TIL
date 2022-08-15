### 소모 시간
- 20분 48초

### 통과율
- 100%

### my solution
```java
class Solution {
    public int[] sortArrayByParity(int[] nums) {
        int evenCount = 0;
        for(int num: nums){
            if (num % 2 == 0)
                evenCount += 1;
        }
        
        // Nothing to work.
        if (evenCount == 0 || nums.length == evenCount)
            return nums;
        
        // Start from last index searching even number.
        int j = nums.length - 1;
        
        for (int i = 0; i < evenCount; i++) {
            // odd
            if (nums[i] % 2 != 0) {
                while (nums[j] % 2 != 0) {
                    j--;
                }
                
                int tmp = nums[i];
                nums[i] = nums[j];
                nums[j] = tmp;
                j--;
            }
        }
        return nums;
    }
}
```

### other solution
```java
public int[] sortArrayByParity(int[] A) {
        int i = 0;
        int j = A.length - 1;
        while (i < j) {
            if(A[i] % 2 == 0) {
                // Even first
                i++;
            }
            else {
                if(A[j] % 2 != 0) {
                    // Both odd
                    j--;
                }
                if (A[j] % 2 == 0) {
                    // Odd, Even
                    swap(A, i, j);
                    i++;
                    j--;
                }
            }
        }


        return A;
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
```
