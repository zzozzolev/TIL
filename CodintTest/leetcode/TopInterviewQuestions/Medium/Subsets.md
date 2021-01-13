### 소모 시간
- 5분

### 통과율
- 100%

### my solution
```
from itertools import combinations

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        answer = [[]]
        
        for r in range(1, len(nums)+1):
            combs = combinations(nums, r)
            for comb in combs:
                answer.append(sorted(list(comb)))
        
        return answer
```

### other solution
- https://leetcode.com/problems/subsets/solution/
```
# Cascading
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        output = [[]]
        
        for num in nums:
            output += [curr + [num] for curr in output]
        
        return output

# Lexicographic Subsets
# 처음보는 신기한 방법
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        output = []
        
        for i in range(2**n, 2**(n + 1)):
            # generate bitmask, from 0..00 to 1..11
            bitmask = bin(i)[3:]
            
            # append subset corresponding to that bitmask
            output.append([nums[j] for j in range(n) if bitmask[j] == '1'])
        
        return output
```