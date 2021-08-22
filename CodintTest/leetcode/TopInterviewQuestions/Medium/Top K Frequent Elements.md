### 소모 시간
- 10분 40초

### 통과율
- 100%

### my solution
```
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        items = Counter(nums).most_common()
        return [pair[0] for pair in items][:k]
```

### other solution
- https://leetcode.com/problems/top-k-frequent-elements/discuss/81697/Python-O(n)-solution-without-sort-without-heap-without-quickselect/178522
- 최대 `len(nums)`개의 원소가 존재.
- 딕셔너리의 키를 카운트로해서 저장하고 높은 순으로 키의 값을 얻음.
```
    def topKFrequent(self, nums, k):
        frq = defaultdict(list)
        for key, cnt in Counter(nums).items():
            frq[cnt].append(key)

        res = []
        for times in reversed(range(len(nums) + 1)):
            res.extend(frq[times])
            if len(res) >= k: return res[:k]

        return res[:k]
```