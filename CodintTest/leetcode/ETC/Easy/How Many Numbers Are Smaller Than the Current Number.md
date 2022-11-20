### 소모 시간
- 29분 15초 ㅠ
- 뻘짓하다가 시간 다 날림...

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int[] smallerNumbersThanCurrent(int[] nums) {
        Map<Integer, Integer> valueToCount = new HashMap<>();
        
        int[] answer = new int[nums.length];
        for (int i = 0; i < nums.length; i++) {
            if (valueToCount.containsKey(nums[i])) {
                answer[i] = valueToCount.get(nums[i]);
                continue;
            }

            int count = 0;
            for (int j = 0; j < nums.length; j++) {
                if (i == j)
                    continue;
                
                if (nums[j] < nums[i]) {
                    count++;
                }
            }

            answer[i] = count;
            valueToCount.put(nums[i], count);
        }

        return answer;
    }
}
```

### Other Solution
- https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/solutions/524996/java-beats-100-o-n/
```java
class Solution {
    public int[] smallerNumbersThanCurrent(int[] nums) {
        int[] count = new int[101];
        int[] res = new int[nums.length];
        
        // Count the occurrence of nums.
        for (int i =0; i < nums.length; i++) {
            count[nums[i]]++;
        }
        
        // Accumulate the count of less than num.
        for (int i = 1 ; i <= 100; i++) {
            count[i] += count[i-1];    
        }
        
        // Assign the count.
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == 0)
                res[i] = 0;
            else 
                res[i] = count[nums[i] - 1];
        }
        
        return res;        
    }
}
```
- O(N) solution.
- 가능한 숫자가 0 ~ 100으로 개수가 작으므로 가능한 솔루션으로 보임.
- 인덱스를 `i`라고 했을 때, `0 < 1 < ... < i - 2 < i - 1 < i` 인 것을 이용함.
- 작은 숫자들의 카운트는 축적 가능함.
