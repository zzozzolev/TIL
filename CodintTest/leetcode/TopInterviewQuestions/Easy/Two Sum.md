### 소모 시간
- 18분 30초

### 통과율
- 100%

### 문제점
- 이미 해쉬 테이블 문제인 것을 알고있었지만 제대로 활용을 못했다.
- 매번 인덱스를 얻기보다는 값을 키로 밸류를 인덱스로 설정했으면 됐다.

### my solution
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        List<Integer> diff = new ArrayList<>();
        int[] answer = new int[2];
        for (int i = 0; i <nums.length; ++i) {
            int index = diff.indexOf(nums[i]);
            
            // 페어 존재
            if (index != -1) {
                answer[0] = index;
                answer[1] = i;
            }
                
            diff.add(target - nums[i]);
        }
        
        return answer;
    }
}
```

---

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