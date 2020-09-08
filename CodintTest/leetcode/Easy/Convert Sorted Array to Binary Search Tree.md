### 소모 시간
- 10분 50초

### 통과율
- 100%

### 접근 방법
- 중앙값을 root로 하고 재귀적으로 left subtree와 right subtree의 root들을 지정해나간다.

### my solution
```
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        def set_root(subtree):
            if subtree:
                root = TreeNode()
                idx = len(subtree) // 2
                root.val = subtree[idx]
                root.left = set_root(subtree[:idx])
                root.right = set_root(subtree[idx+1:])
            
                return root
            
        root = set_root(nums)
        
        return root
```
