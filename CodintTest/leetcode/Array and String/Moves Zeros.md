### 소모 시간
- 21분

### 통과율
- 94%

### my solution
```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)-1):
            if nums[i] == 0:
                cur = i + 1
                while nums[cur] == 0 and cur < len(nums) - 1: cur += 1
                nums[i] = nums[cur]
                nums[cur] = 0
```

### other solution
- https://leetcode.com/problems/move-zeroes/discuss/172432/THE-EASIEST-but-UNUSUAL-snowball-JAVA-solution-BEATS-100-(O(n))-%2B-clear-explanation
```java
class Solution {
     public void moveZeroes(int[] nums) {
        int snowBallSize = 0; 
        for (int i=0;i<nums.length;i++){
	        if (nums[i]==0){
                snowBallSize++; 
            }
            else if (snowBallSize > 0) {
	            int t = nums[i];
	            nums[i]=0;
	            nums[i-snowBallSize]=t;
            }
        }
    }
}
```
- 0을 만나면 하나로 합치고 0이 아닌 것을 0 뭉텅이 앞으로 빼낸다.