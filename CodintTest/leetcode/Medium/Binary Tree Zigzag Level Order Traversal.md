### 소모 시간
- 36분 24초

### 통과율
- 100%

### 문제점
- 처음에 추가되는 노드의 자식을 나중에 넣어야 된다 이런 거 없이 똑같이 append하고 나중에 순서만 바꿔주면 굳이 복잡하게 `insert` 0를 하거나 level에 따라 left와 right를 바꿀 필요가 없음.

### my solution
```
from collections import defaultdict

class Solution:
    def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
        level_dic = defaultdict(list)
        level_dic[0].append(root)
        level = 0
        answer = []
        
        while len(level_dic[level]) != 0:
            cur_level_vals = []
            queue = level_dic[level]
            
            while len(queue) != 0:
                node = queue.pop(0)
                if node is not None:
                    cur_level_vals.append(node.val)
                    
                    if level % 2 == 0:
                        level_dic[level+1].insert(0, node.left)
                        level_dic[level+1].insert(0, node.right)
                    else:
                        level_dic[level+1].insert(0, node.right)
                        level_dic[level+1].insert(0, node.left)    
                
            if cur_level_vals:
                answer.append(cur_level_vals)
            del level_dic[level]
            level += 1
            
        return answer
```

### other solution
- https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/discuss/749036/Python-Clean-BFS-solution-explained
```
class Solution:
    def zigzagLevelOrder(self, root):
        if not root: return []
        queue = deque([root])
        result, direction = [], 1
        
        while queue:
            level = []
            for i in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:  queue.append(node.left)
                if node.right: queue.append(node.right)
            result.append(level[::direction])
            direction *= (-1)
        return result
```