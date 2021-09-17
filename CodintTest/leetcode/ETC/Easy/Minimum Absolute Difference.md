### 소모 시간
- 10분 47초

### 통과율
- 100%

### my solution
```
from collections import defaultdict

class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        diff_to_lists = defaultdict(list)
        
        for i in range(len(arr) - 1):
            diff_to_lists[arr[i+1] - arr[i]].append([arr[i], arr[i+1]])
        
        min_key = min(diff_to_lists.keys())
        
        return diff_to_lists[min_key]
```

### other solution
- https://leetcode.com/problems/minimum-absolute-difference/discuss/387580/Python3-3-liner/498076
```
def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
    arr.sort()
    mad = min(arr[i] - arr[i-1] for i in range(1, len(arr)))
    results = [[arr[i-1], arr[i]] for i in range(1, len(arr)) if arr[i] - arr[i-1] == mad]
    return results
```