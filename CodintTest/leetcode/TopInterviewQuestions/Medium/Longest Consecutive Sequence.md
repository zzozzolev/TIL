### 소모 시간
- 21분 37초

### 통과율
- 96% (메모리 초과)

### 접근법
- (최대값 + 최솟값의 절대값 + 1) 길이의 어레이에 존재하면 `True`, 존재하지 않으면 `False`를 저장한다.
- 어레이를 순회하면서 가장 긴 `True`의 길이를 찾는다.

### my solution
```
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        
        constant = abs(min(nums))
        exist_checking = [False] * (max(nums) + constant + 1)
        
        # Mark existing num.
        for e in nums:
            exist_checking[e + constant] = True
        
        answer, count = 0, 0
        for checked in exist_checking:
            if checked:
                count += 1
            else:
                answer = max(answer, count)
                count = 0
        
        # for last element
        answer = max(answer, count)
        
        return answer
```

### other solution
- https://leetcode.com/problems/longest-consecutive-sequence/discuss/41202/Python-O(n)-solution-using-sets/39339
- 중복을 제거해서 불필요한 이터레이션을 줄임.
- 숫자 하나를 골라서 기준점을 잡고 작은 수, 큰 수를 각각 하나씩 찾아감.
```
class Solution:
    def longestConsecutive(self, nums):
        nums = set(nums)
        maxlen = 0
        while nums:
            first = last = nums.pop()
            while first - 1 in nums:
                first -= 1
                nums.remove(first)
            while last + 1 in nums:
                last += 1
                nums.remove(last)
            maxlen = max(maxlen, last - first + 1)
        return maxlen
```