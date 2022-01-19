### 소모 시간
- 11분 7초

### 통과율
- 100%

### 접근법
- 0번째가 0이 아니거나 마지막이 n이 아니면 해당 숫자를 리턴한다.
- 숫자를 오름차순으로 정렬하고 `(i + 1) - i`의 차이가 1이 아니면 `i`번째에서 1을 더한 것을 리턴한다.

### my solution
```java
class Solution {
    public int missingNumber(int[] nums) {
        Arrays.sort(nums);
        
        if (nums[0] != 0)
            return 0;
        
        if (nums[nums.length - 1] != nums.length)
            return nums.length;
        
        for (int i = 0; i < nums.length - 1; ++i) {
            if (nums[i + 1] - nums[i] != 1) {
                return nums[i] + 1;
            }
        }
        
        return -1;
    }
}
```

### other solution
- https://leetcode.com/problems/missing-number/discuss/69791/4-Line-Simple-Java-Bit-Manipulate-Solution-with-Explaination/71891
```java
public static int missingNumber(int[] nums) {
    int sum = nums.length;
    for (int i = 0; i < nums.length; i++)
        sum += i - nums[i];
    return sum;
}
```
- `nums`는 `[0, n]`까지의 합이여야하므로 인덱스로 총합을 더한다.
- 엘리먼트를 하나씩 빼서 값이 없는 걸 얻는다.
