### 소모 시간
- 11분 12초

### 통과율
- 100%

### 접근법
- 전체 합에서 set을 이용해 중복되지 않은 합을 빼면 하나만 있는 수를 제외한 나머지 수들의 중복되지 않은 합이 나온다는 것을 이용했다. 중복되지 않은 합에서 이 합을 빼면 하나만 있는 수가 나온다.
    - ex) [4,1,2,1,2]
        - total_sum = 10
        - set_sum = 7
        - no_dup_sum = total_sum - set_sum = 10 - 7 = 3
        - single = set_sum - no_dup_sum = 7 - 3 = 4

### my solution
```
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        
        unique_sum = sum(set(nums))
        dup_sum = sum(nums)
        no_dup_sum = dup_sum - unique_sum
        return unique_sum - no_dup_sum
```