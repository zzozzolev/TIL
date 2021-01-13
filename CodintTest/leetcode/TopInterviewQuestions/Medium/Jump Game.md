### 소모 시간
- 19분 19초

### 통과 여부
- 96%

### 접근법
- 재귀적으로 접근하기 위해 재귀 함수를 만든다.
- 현재 index가 `len(nums)-1`보다 크거나 같다면 `True`를 반환하고 `nums[cur_index]`가 0이라면 `False`를 반환한다.
- 위의 경우에 해당되지 않는 경우 `nums[cur_index]`부터 1까지 range를 얻으면서 함수에 `cur_index + i`를 넘겨준다. 만약 재귀 함수가 `True`를 반환하면 `True`를 반환한다. 모든 순회에서 `False`인 경우 `False`를 반환한다.

### 문제점
- `Time Limit Exceeded`가 발생했다.
- 솔루션을 보니 비효율적인 Backtracking을 사용했다. memoization을 쓰면 더 효율적으로 할 수 있었다.
- 무조건 0에서 시작한다고 그렇게 가정하지 않고 이미 도착했다고 가정하고 문제를 풀었으면 더 효율적으로 문제를 풀 수 있었다.

### my solution
```
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        return self.jump(nums, 0)        
        
    def jump(self, nums, cur_idx):
        if cur_idx >= len(nums) - 1:
            return True
        elif nums[cur_idx] == 0:
            return False
        else:
            for i in range(nums[cur_idx], 0, -1):
                if self.jump(nums, cur_idx+i):
                    return True
            return False
```

### other solution
- 출처: https://leetcode.com/problems/jump-game/solution/
```
public class Solution {
    public boolean canJump(int[] nums) {
        int lastPos = nums.length - 1;
        for (int i = nums.length - 1; i >= 0; i--) {
            if (i + nums[i] >= lastPos) {
                lastPos = i;
            }
        }
        return lastPos == 0;
    }
}
```