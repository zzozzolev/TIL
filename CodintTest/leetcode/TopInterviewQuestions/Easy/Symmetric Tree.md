### 소모 시간
- 17분 59초

### 통과율
- 100%

### 접근법
- `root`가 `None`이면 `True`를 리턴한다.
- inorder로 tree를 traversal한 결과에서 중앙값이 `root`의 값과 같고 왼쪽과 오른쪽의 서로 대칭되는 부분의 값이 같으면서 반대 방향인지를 검사한다.
- 만약 그렇다면 왼쪽을 1 늘리고 오른쪽을 1 줄인다. 왼쪽이 오른쪽보다 작을 때까지 반복한다.

### 문제점
- 추가적인 정보로 left와 right를 넣는 게 아니라 처음부터 left와 right를 비교하면 반복문을 한 번 더 돌 필요가 없다.

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

### other solution
- https://leetcode.com/problems/symmetric-tree/discuss/33068/6line-AC-python comment
```
class Solution(object):
    def isSymmetric(self, root):
        def isSym(L,R):
            if not L and not R: return True
            if L and R and L.val == R.val: 
                return isSym(L.left, R.right) and isSym(L.right, R.left)
            return False
        if root is None:
            return True
        return isSym(root.left, root.right)
```