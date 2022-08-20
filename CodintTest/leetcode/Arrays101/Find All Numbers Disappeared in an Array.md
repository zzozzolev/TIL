### 소모 시간
- 27분 10초

### 통과율
- 100%

### my solution
```python
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        n = len(nums)
        idx = 0
        
        # 자신의 위치에 놓음
        while idx < len(nums):
            # 자신의 자리에 있거나 이미 중복 원소가 제자리에 있음.
            if nums[idx] == idx + 1 or nums[nums[idx] - 1] == nums[idx]:
                idx += 1
            else:
                # Swap each elem.
                nums[nums[idx] - 1], nums[idx] = nums[idx], nums[nums[idx] - 1]
            
        answer = []
        for i in range(len(nums)):
            if nums[i] != i + 1:
                answer.append(i + 1)
        
        return answer
```

### other solution
```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        # For each number i in nums,
        # we mark the number that i points as negative.
        # Then we filter the list, get all the indexes
        # who points to a positive number
        for i in xrange(len(nums)):
            index = abs(nums[i]) - 1
            nums[index] = - abs(nums[index])

        return [i + 1 for i in range(len(nums)) if nums[i] > 0]
```
