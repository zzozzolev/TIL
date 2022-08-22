### 소모 시간
- 13분 52초

### 통과율
- 100%

### my solution
```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total_sum = sum(nums)
        left_sum = 0
        right_sum = total_sum - nums[0]
        
        if left_sum == right_sum:
            return 0
            
        
        for i in range(len(nums) - 1):
            left_sum += nums[i]
            right_sum -= nums[i + 1]
            
            if left_sum == right_sum:
                return i + 1
        
        return -1
```

### other solution
```python
class Solution(object):
    def pivotIndex(self, nums):
        # Time: O(n)
        # Space: O(1)
        left, right = 0, sum(nums)
        for index, num in enumerate(nums):
            right -= num
            if left == right:
                return index
            left += num
        return -1
```