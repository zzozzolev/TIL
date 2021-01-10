# 소모 시간
- 20분 56초

# 통과율
- 100%

# 문제점
- 나누기를 쓰지 말라고 했지만 써버렸다.
- 0으로 나누는 경우를 고려하지 못했다.
- 왼쪽 오른쪽으로 나눠서 생각해봤으면 굳이 나누기가 필요 없고 0 처리도 안 해도 됐다.

# my solution
```
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if not nums:
            return []
        
        if 0 in nums and nums.count(0) > 1:
            return [0] * len(nums)
        
        total = 1
        zero_idx = None
        for i in range(len(nums)):
            if nums[i] == 0:
                zero_idx = i
                continue
            total *= nums[i]
        
        if zero_idx is not None:
            nums = [0] * len(nums)
            nums[zero_idx] = total        
        else:
            for i in range(len(nums)):
                nums[i] = total // nums[i]
        
        return nums
```

# other solution
- https://leetcode.com/problems/product-of-array-except-self/discuss/65622/Simple-Java-solution-in-O(n)-without-extra-space
```
public class Solution {
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] res = new int[n];
    res[0] = 1;
    for (int i = 1; i < n; i++) {
        res[i] = res[i - 1] * nums[i - 1];
    }
    int right = 1;
    for (int i = n - 1; i >= 0; i--) {
        res[i] *= right;
        right *= nums[i];
    }
    return res;
}
```
- 설명은 맨 위 댓글 참고