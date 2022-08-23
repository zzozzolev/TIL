### 소모 시간
- 20분

### 통과율
- 100%

### my solution
```python
class Solution:
    def dominantIndex(self, nums: List[int]) -> int:
        answer = -1
        max_num = -1
        
        for i in range(len(nums)):
            if nums[i] * 2 > max_num:
                answer = -1
            
            if max_num < nums[i]:
                if max_num * 2 <= nums[i]:
                    answer = i
                else:
                    answer = -1
                max_num = nums[i]
        
        return answer
```

### other solution
- https://leetcode.com/explore/learn/card/array-and-string/201/introduction-to-array/1147/discuss/110120/Python-O(n)-time-and-O(1)-space-without-fancy-builtins/483223
```python
def dominantIndex(self, nums: List[int]) -> int:
        max1 = max2 = maxi = -1 
        for i, num in enumerate(nums):
            if num > max1:
                max2 ,max1, maxi  = max1 , num , i 
            elif num > max2:
                max2 = num
        return maxi if max1 >= 2 * max2 else -1
```
- 제일 큰 수는 그 다음으로 큰 수의 2배 보다 크기만 하면 된다.
- 따라서 제일 큰 수와 그 다음으로 큰 수를 찾으면 된다.
