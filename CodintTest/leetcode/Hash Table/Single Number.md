### 소모 시간
- 6분 52초

### 통과율
- 100%

### my solution
```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        count = {num: 0 for num in nums}
        for num in nums:
            count[num] += 1
        
        for num in nums:
            if count[num] == 1:
                return num
```
