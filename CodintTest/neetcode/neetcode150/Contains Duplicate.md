### 소모 시간
- 3분 15초

### 통과율
- 100%

### my solution
```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return not(len(nums) == len(set(nums)))
```
