### 소모 시간
- 36분 20초

### 통과 여부
- 100%

### 문제점
- left보다 right가 클 때 return을 안 해주면 최대 recursion을 초과해서 에러가 난다. limit을 풀면 memroy limit 에러가 난다.
- recursion을 쓰다보니 recursion이 아닌 것보다 속도도 느리고 memory도 더 많이 차지한다.

### my solution
```
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        answer = [-1, -1]
        self.binary_search(nums, 0, len(nums)-1, target, answer)
        
        return answer
        
    def binary_search(self, nums, left, right, target, answer):
        mid = (left + right) // 2
        
        # 매우매우 중요함.. 이거 하나 안 넣어서 하나도 통과 못 하다가 넣으니까 100% 나옴.
        if left > right:
            return

        if nums[mid] == target:
            if mid > 0:
                if nums[mid-1] == target:
                    self.binary_search(nums, left, mid-1, target, answer)
                elif nums[mid-1] != target:
                    answer[0] = mid
            
            if mid < len(nums)-1:
                if nums[mid+1] == target:
                    self.binary_search(nums, mid+1, right, target, answer)
                elif nums[mid+1] != target:
                    answer[1] = mid
            
            if mid == 0:
                answer[0] = mid
            
            if mid == len(nums) - 1:
                answer[1] = mid
        
        elif nums[mid] > target:
            self.binary_search(nums, left, mid-1, target, answer)
        
        elif nums[mid] < target:
            self.binary_search(nums, mid+1, right, target, answer)
```

### other solution
- 출처: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/discuss/15012/Python-easy-solution
- 중복되는 부분을 수정했음.
```
class Solution:
    def searchRange(self, A, target):
        lmost = self.search(A,target,"left")
        rmost = self.search(A,target, "right")
        return[lmost,rmost]
                        
    def search(self,A,tar,mode):
        l = 0
        r = len(A)-1
        tarI = -1 #target index
        while l <= r:
            mid = (l+r)//2
            if A[mid] > tar:
                r = mid - 1
            elif A[mid] < tar:
                l = mid + 1
            else:
                tarI = mid
                if mode =="left":
                    r = mid - 1
                else:
                    l = mid+1
        return tarI
```