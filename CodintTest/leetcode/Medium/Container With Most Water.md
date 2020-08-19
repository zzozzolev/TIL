### 소모 시간
- 30분

### 통과 여부
- 86%

### 문제점
- brute force는 input이 많을 때 시간 초과로 통과하지 못한다.

### my solution
```
from itertools import combinations

class Solution:
    def maxArea(self, height: List[int]) -> int:
        coords = [(i, e) for i,e in enumerate(height, 1)]
        comb = combinations(coords, 2)
        results = [self.get_result(p[0], p[1]) for p in comb]
        return max(results)
    
    def get_result(self, e1, e2):
        return abs(e1[0]-e2[0]) * min(e1[1],e2[1])
```

### other solution
```
public class Solution {
    public int maxArea(int[] height) {
        int maxarea = 0, l = 0, r = height.length - 1;
        while (l < r) {
            maxarea = Math.max(maxarea, Math.min(height[l], height[r]) * (r - l));
            if (height[l] < height[r])
                l++;
            else
                r--;
        }
        return maxarea;
    }
}
```
- We take two pointers, one at the beginning and one at the end of the array constituting the length of the lines.
- Futher, we maintain a variable `maxarea` to store the maximum area obtained till now.
- At every step, we find out the area formed between them, update `maxarea` and move the pointer pointing to the shorter line towards the other end by one step.
- Now, to maximize the area, we need to consider the area between the lines of larger lengths.
- Now, to maximize the area, we need to consider the area between the lines of larger lengths.
- If we try to move the pointer at the longer line inwards, we won't gain any increase in area, since it is limited by the shorter line. But moving the shorter line's pointer could turn out to be beneficial, as per the same argument, despite the reduction in the width.
- This is done since a relatively longer line obtained by moving the shorter line's pointer might overcome the reduction in area caused by the width reduction.
