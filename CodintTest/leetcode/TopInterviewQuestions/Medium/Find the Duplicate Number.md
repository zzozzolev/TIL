### 소모 시간
- 15분 36초

### 통과율
- 90%

### my solution
```
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        for i in range(len(nums) - 1):
            for j in range(i+1, len(nums)):
                if nums[i] == nums[j]:
                    return nums[i]
```

### other solution
- https://leetcode.com/problems/find-the-duplicate-number/discuss/72846/My-easy-understood-solution-with-O(n)-time-and-O(1)-space-without-modifying-the-array.-With-clear-explanation.
- 솔직히 이해 잘 못 함 ㅎㅎ;
```
int findDuplicate3(vector<int>& nums)
{
	if (nums.size() > 1)
	{
		int slow = nums[0];
		int fast = nums[nums[0]];
		while (slow != fast)
		{
			slow = nums[slow];
			fast = nums[nums[fast]];
		}

		fast = 0;
		while (fast != slow)
		{
			fast = nums[fast];
			slow = nums[slow];
		}
		return slow;
	}
	return -1;
}
```
