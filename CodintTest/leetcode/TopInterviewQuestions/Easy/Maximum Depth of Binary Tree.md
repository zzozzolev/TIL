### 소모 시간
- 5분 28초

### 통과율
- 100%

### 문제점
- 첫번째 순회와 두번째 재귀에서 level을 세는 것이 달라 좀 헤맸다.
- traversal이나 순회를 쓰지 않고도 왼쪽과 오른쪽에 대한 재귀만으로 해결할 수 있다.


### my solution1
```
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        queue = [root]
        level = 0
        while len(queue) != 0:
            length = len(queue)
            for _ in range(length):
                node = queue.pop(0)
                if node.left or node.right:
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
            
            if length > 0:
                level += 1
                
        return level
```

### my solution2
```
class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        def traversal(root, level, answer):
            if root:
                if level not in answer:
                    answer.append(level)
                traversal(root.left, level+1, answer)
                traversal(root.right, level+1, answer)
        
        answer = []
        traversal(root, 1, answer)
        
        return max(answer)
```

### other solution
- https://leetcode.com/problems/maximum-depth-of-binary-tree/discuss/34212/1-line-Ruby-and-Python comment
```
def maxDepth(self, root: TreeNode) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```