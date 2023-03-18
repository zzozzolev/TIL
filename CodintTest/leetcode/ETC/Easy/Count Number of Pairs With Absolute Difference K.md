### 소모 시간
- 5분 30초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int countKDifference(int[] nums, int k) {
        int answer = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (Math.abs(nums[i] - nums[j]) == k)
                    answer += 1;
            }
        }
        return answer;
    }
}
```

### Other Solution
```java
public int countKDifference(int[] nums, int k) {
    Map<Integer,Integer> map = new HashMap<>();
    int count = 0;
    for(int n : nums){
        count += map.getOrDefault(n - k, 0) + map.getOrDefault(n + k, 0);
        map.put(n, map.getOrDefault(n, 0) + 1);
    }
    return count;
}
```
