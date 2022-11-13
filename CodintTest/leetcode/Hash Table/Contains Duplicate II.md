### 소모 시간
- 12분 41초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Map<Integer, Integer> numToLatestIdx = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            // Compare latest index to i.
            if (numToLatestIdx.containsKey(nums[i]) && Math.abs(i - numToLatestIdx.get(nums[i])) <= k) {
                return true;
            }

            numToLatestIdx.put(nums[i], i);
        }

        return false;
    }
}
```

### Other Solution
- https://leetcode.com/problems/contains-duplicate-ii/solutions/61372/simple-java-solution/?orderBy=most_votes
```java
public boolean containsNearbyDuplicate(int[] nums, int k) {
        Set<Integer> set = new HashSet<Integer>();
        for(int i = 0; i < nums.length; i++){
            if(i > k) set.remove(nums[i-k-1]);
            if(!set.add(nums[i])) return true;
        }
        return false;
 }
```
- 윈도우 밖에 있는 건 제거.
- 이미 set에 있다면 k 인덱스 내에 있는 것이므로 `ture` 반환.
