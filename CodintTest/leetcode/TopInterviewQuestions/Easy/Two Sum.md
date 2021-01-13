### 소모 시간
- 13분 39초

### 통과 여부
- 100%

### 접근법
- `len(nums)`까지 순회하는 이중 for문을 이용한다. 이때 outer loop는 `0`부터 시작하고 inner loop는 `i+1`부터 시작한다.
- 만약 두 수의 합이 `target`과 같다면 해당 인덱스들을 반환한다.

### my solution 1 (accepted)
```
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
```

### my solution 2 (wrong)
```
from itertools import combinations

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
    pairs = [(num, i) for i, num in enumerate(nums)]
        combs = list(combinations(pairs, 2))
        for comb in combs:
            comb_nums = [p[0] for p in comb]
            if sum(comb_nums) == target:
                return sorted([p[1] for p in comb])
```

### other solution
- hash table 이용
```
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (map.containsKey(complement)) {
            return new int[] { map.get(complement), i };
        }
        map.put(nums[i], i);
    }
    throw new IllegalArgumentException("No two sum solution");
}
```