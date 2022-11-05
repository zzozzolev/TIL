### 소모 시간
- 11분 12초

### 통과율
- 100%

### 접근법
- 전체 합에서 set을 이용해 중복되지 않은 합을 빼면 하나만 있는 수를 제외한 나머지 수들의 중복되지 않은 합이 나온다는 것을 이용했다. 중복되지 않은 합에서 이 합을 빼면 하나만 있는 수가 나온다.
    - ex) [4,1,2,1,2]
        - total_sum = 10
        - set_sum = 7
        - no_dup_sum = total_sum - set_sum = 10 - 7 = 3
        - single = set_sum - no_dup_sum = 7 - 3 = 4

### my solution
```
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        
        unique_sum = sum(set(nums))
        dup_sum = sum(nums)
        no_dup_sum = dup_sum - unique_sum
        return unique_sum - no_dup_sum
```

### my solution (java1)
```java
class Solution {
    public int singleNumber(int[] nums) {
        Map<Integer, Integer> counter = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            if (!counter.containsKey(nums[i]))
                counter.put(nums[i], 1);
            else
                counter.put(nums[i], counter.get(nums[i]) + 1);
        }

        for (Integer num: counter.keySet() ) {
            if (counter.get(num).equals(1))
                return num;
        }
        return 0;
    }
}
```

### my solution (java2)
```java
class Solution {
    public int singleNumber(int[] nums) {
        Integer uniqueSum = Arrays.stream(nums).boxed().collect(Collectors.toSet()).stream().reduce(0, Integer::sum);
        Integer dupSum = Arrays.stream(nums).boxed().reduce(0, Integer::sum);
        Integer noDupSum = dupSum - uniqueSum;

        return uniqueSum - noDupSum;
    }
}
```
