### 소모 시간
- 9분 43초

### 통과율
- 100%

### 접근법
- `root`가 `None`이면 빈 리스트를 반환한다.
- tree를 순회하는 재귀함수에 dictionary와 level을 넘겨줘서 level을 key로 left와 right의 값을 저장한다.

### 문제점
- dictionary를 쓰지 않고 queue를 사용했으면 더 많은 공간을 아낄 수 있었다.

### my solution
```
from collections import defaultdict
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        def visit(root, d, level):
            if root:
                if root.left:
                    d[level].append(root.left.val)
                if root.right:
                    d[level].append(root.right.val)
                
                if root.left:
                    visit(root.left, d, level+1)
                
                if root.right:
                    visit(root.right, d, level+1)
        
        if root is None:
            return []
        
        d = defaultdict(list)
        d[0].append(root.val)
        visit(root, d, 1)
        
        return [value for value in d.values()]
```

### other solution
- https://leetcode.com/problems/binary-tree-level-order-traversal/discuss/197348/Python-or-BFS-Queue-tm-(102)
```
from collections import deque
class Solution:
    def levelOrder(self, root):
        if not root: return []
        queue, res = deque([root]), []
        
        while queue:
            cur_level, size = [], len(queue)
            for i in range(size):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                cur_level.append(node.val)
            res.append(cur_level)
        return res
```