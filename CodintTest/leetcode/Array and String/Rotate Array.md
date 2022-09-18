### 소모 시간
- 20분 53초

### 통과율
- 100%

### my solution
```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # Handle k exceeds len(nums)
        k = k % len(nums)
        if k == 0:
            return nums
        
        copy = list(nums)
        
        for i in range(0, k):
            nums[i] = copy[-k+i]
        
        for i in range(k, len(nums)):
            nums[i] = copy[i-k]
```

### other solution
- https://leetcode.com/problems/rotate-array/discuss/269948/4-solutions-in-python-(From-easy-to-hard)
```python
class Solution4:
    def rotate(self, nums, k) -> None:
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        k %= len(nums)
        self.reverse(nums,0,len(nums)-1)
        self.reverse(nums,0, k-1)
        self.reverse(nums,k, len(nums)-1)

    def reverse(self, nums, start, end) -> None:
        """
        :type nums: List[int]
        :type start: int
        :type end: int
        :rtype: None
        """
        while start < end: #
            temp = nums[start]
            nums[start] = nums[end]
            nums[end] = temp 
            start += 1
            end -= 1
```