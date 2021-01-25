# 소모 시간
- 17분 46초

# 통과율
- 100%

# 문제점
- in-place로 하라고 해서 0 아닌 것만 따로 못 골라내나 이렇게 생각했는데 그냥 덮어쓰면 끝이었다..

# my solution
```
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        idx = 0
        zero_count = nums.count(0)
        
        if zero_count != 0:
            while sum(nums[-zero_count:]) != 0:
                if nums[idx] == 0:
                    nums.pop(idx)
                    nums.append(0)
                else:
                    idx += 1
```

# other solution
- https://leetcode.com/problems/move-zeroes/discuss/72011/Simple-O(N)-Java-Solution-Using-Insert-Index
```
// Shift non-zero values as far forward as possible
// Fill remaining space with zeros

public void moveZeroes(int[] nums) {
    if (nums == null || nums.length == 0) return;        

    int insertPos = 0;
    for (int num: nums) {
        if (num != 0) nums[insertPos++] = num;
    }        

    while (insertPos < nums.length) {
        nums[insertPos++] = 0;
    }
}
```