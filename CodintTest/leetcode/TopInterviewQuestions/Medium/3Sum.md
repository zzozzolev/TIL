### 소모 시간
- 49분 40초

### 통과 여부
- 96%

### 접근법
- `nums`를 오름차순으로 정렬한다.
- `nums`에서 0의 개수를 count한다.
- 만약 0의 개수가 3보다 크거나 같다면 `answer`에 `[0, 0, 0]`을 추가한다.
- 만약 `len(nums)`가 zero count보다 크다면 다음의 과정을 수행한다.
    - 음수와 양수 두 가지로 나눈 list를 얻어낸다.
    - zero count가 1보다 크거나 같다면 더 작은 길이를 가진 list의 원소 `n`을 얻어내면서 `-n`이 더 큰 길이를 가진 list에 존재하는지 확인한다. 존재하고 기존에 추가되지 않았다면 정답에 추가한다.
    - 양수와 음수를 모두 더해 r=3인 조합을 얻어낸다. 그 중 합이 0인 고유한 조합을 정답에 추가한다.

### 문제점
- 시간 초과로 100% 통과를 못 했다.
- 저번에도 그렇고 뭔가 특정 조건을 만족하는 문제에서 L, R pointer 접근을 많이 하는 것 같다.

### my solution
```
from itertools import combinations

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        answer = []
        nums.sort()
        
        zero_count = nums.count(0)
        if zero_count >= 3:
            answer.append([0, 0, 0])
        
        if len(nums) > zero_count:
            plus, minus = [], []
            for i, n in enumerate(nums):
                if n < 0:
                    minus.append(n)
                elif n == 0:
                    continue
                else:
                    plus = nums[i:]
                    break

            shorter = None
            if len(plus) <= len(minus):
                shorter = plus
                longer = minus
            else:
                shorter = minus
                longer = plus

            if zero_count >= 1:
                for n in shorter:
                    if -n in longer:
                        appended = [-n, 0, n]
                        if appended not in answer:
                            answer.append(appended)
            
            combs = combinations(plus+minus, 3)
            for comb in combs:
                if sum(comb) == 0:
                    sorted_comb = list(sorted(comb))
                    if sorted_comb not in answer:
                        answer.append(sorted_comb)
        
        return answer
```

### other solution
- 출처: https://leetcode.com/problems/3sum/discuss/799276/Clean-code-with-Easy-Explanation
```
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()
        
        for i, a in enumerate(nums):
            if i > 0 and a == nums[i - 1]:
                continue
            
            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = a + nums[l] + nums[r]
                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    # Handle same value ex) [-2, -2, 0, 0, 2, 2]
                    l += 1
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
        return res
```