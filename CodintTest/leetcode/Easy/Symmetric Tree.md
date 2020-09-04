### 소모 시간
- 17분 59초

### 통과율
- 100%

### 접근법
- 

### 문제점

### my solution
```
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if root is None:
            return True
        
        result = []
        def inorder(root, result, direction):
            if root:
                inorder(root.left, result, "left")
                result.append((root.val, direction))
                inorder(root.right, result, "right")
        
        inorder(root, result, None)
        mid = len(result) // 2
        if result[mid][0] == root.val:
            left, right = 0, len(result)-1
            while left < right:
                if result[left][0] == result[right][0] \
                    and result[left][1] != result[right][1]:
                    left += 1
                    right -= 1
                else:
                    return False
            
            return True
        else:
            return False
```