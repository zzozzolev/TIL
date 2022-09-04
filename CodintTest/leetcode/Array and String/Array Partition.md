### 소모 시간
- 7분 8초

### 통과율
- 100%

### my solution
```python
class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        nums.sort()
        return sum(nums[::2])
```
