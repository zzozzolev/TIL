# 문제
- leetcode 문제이다.
```
Given an unsorted integer array, find the smallest missing positive integer.
Your algorithm should run in O(n) time and uses constant extra space.
```

# 정리한 이유
- 추가 공간 없이 값 자체를 인덱스처럼 사용해 존재 여부를 파악할 수 있다. 신박하다...

# 코드
- https://leetcode.com/problems/first-missing-positive/discuss/231337/Python-solution 여기서 가져왔다.
```
class Solution:
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        for i, n in enumerate(nums):
            if n < 0:
                continue
            else:
                while n <= len(nums) and n > 0:
                    # 아래 3줄이 핵심 포인트
                    tmp = nums[n-1]
                    # 1을 봤다면 0에, 2를 봤다면 1에 이런 식으로 값 자체를 인덱스로 이용
                    nums[n-1] = float('inf')
                    # nums[n-1]에 있던 걸 n으로 함. 이때 만약 n이 lte 0 이라면 사라지게 됨.
                    # [-1, 0, 1, 2, 3] -> [inf, inf, inf, 2, 3]
                    n = tmp
        for i in range(len(nums)):
            if nums[i] != float('inf'):
                return i+1
            
        return len(nums)+1
```

# 복잡도
- 시간 복잡도: `O(n)`
- 공간 복잡도: `O(1)`

# Reference
- https://leetcode.com/problems/first-missing-positive/
- https://leetcode.com/problems/first-missing-positive/discuss/231337/Python-solution