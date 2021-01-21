# 소모 시간
- 의미 없음

# 통과율
- 32%

# my solution
```
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        if len(nums) == 0:
            return []
        
        origin_length = len(nums)
        nums = list(set(nums))
        nums.sort()
        answer = []
        
        for i in range(len(nums)):
            if nums[i] != i + 1:
                answer.append(i + 1)
        
        if nums[-1] != origin_length:
            for e in range(nums[-1] + 1, origin_length + 1):
                answer.append(e)
        
        return answer
```

# other solution
- https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/discuss/92955/Python-4-lines-with-short-explanation
```
# 댓글에 있는 거 가져옴.
```
For each number i in nums,
we mark the number that i points as negative.
Then we filter the list, get all the indexes
who points to a positive number.
Since those indexes are not visited.
```
def findDisappearedNumbers(self, nums):
    for num in nums:
        index = abs(num) - 1
        nums[index] = -abs(nums[index])
            
    return [i + 1 for i, num in enumerate(nums) if num > 0]
```
- `len(nums)`는 항상 원래 숫자에 해당 -> 해당 값의 인덱스에 있는 값을 음수로 만듦.
- 1 pass가 끝나고 음수가 아니라면 없는 것이므로 해당 값들만 넣어주면 됨.