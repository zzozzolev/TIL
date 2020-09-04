### 소모 시간
- 5분 41초

### 통과율
- 100%

### my solution
```
class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        def inorder(node, answer):
            if node == None:
                return
            inorder(node.left, answer)
            answer.append(node.val)
            inorder(node.right, answer)
        answer = []
        
        inorder(root, answer)
        
        return answer
```

### other solution
- https://leetcode.com/problems/binary-tree-inorder-traversal/discuss/31381/Python-recursive-and-iterative-solutions.
```
# iteratively       
def inorderTraversal(self, root):
    res, stack = [], []
    while True:
        while root:
            stack.append(root)
            root = root.left
        if not stack:
            return res
        node = stack.pop()
        res.append(node.val)
        root = node.right
```