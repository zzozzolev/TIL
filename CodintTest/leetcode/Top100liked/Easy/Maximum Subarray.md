# 소모 시간
- 13분 30초

# 통과율
- 100%

# 문제점
- `max_sum`을 0으로 해놔서 길이가 1이고 0보다 클 때 제대로 되지 않았다.
- 최대 합을 기록하는 것을 하나만 만들어 중간에 최대가 나올 때 값이 갱신돼 정답이 제대로 나오지 않았다.

# my solution
```
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]
        local_max_sum = nums[0]
        for i in range(1, len(nums)):
            local_max_sum = max(local_max_sum + nums[i], nums[i])
            max_sum = max(max_sum, local_max_sum)
            
        return max_sum
```