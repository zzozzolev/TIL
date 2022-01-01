
### 소모 시간
- 32분 14초

### 통과율
- 100%

### 문제점
- 같은 iter에 queue에 담기면 같은 level이므로 map으로 따로 저장할 필요가 없다.

### my solution
```java
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        // zero node
        if (root == null)
            return new ArrayList<>();
        
        int level = 0;
        Queue<Pair> queue = new LinkedList<>();
        queue.offer(new Pair(level, root));
        Map<Integer, List<Integer>> level2values = new HashMap<>();
        
        while (!queue.isEmpty()) {
            Pair p = queue.poll();
            
            if (p.node == null)
                continue;
            
            if (!level2values.containsKey(p.level))
                level2values.put(p.level, new ArrayList<>());
            
            level2values.get(p.level).add(p.node.val);
            
            // left
            queue.offer(new Pair(p.level + 1, p.node.left));
            // right
            queue.offer(new Pair(p.level + 1, p.node.right));
        }
        
        List<List<Integer>> answer = new ArrayList<>();
        for (List<Integer> values : level2values.values())
            answer.add(values);
        
        return answer;
    }
    
    static class Pair {
        public int level;
        public TreeNode node;
        
        public Pair(int level, TreeNode node) {
            this.level = level;
            this.node = node;
        }
    }
}
```

### other solution
- https://leetcode.com/problems/binary-tree-level-order-traversal/discuss/33450/Java-solution-with-a-queue-used
```java
public class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        Queue<TreeNode> queue = new LinkedList<TreeNode>();
        List<List<Integer>> wrapList = new LinkedList<List<Integer>>();
        
        if(root == null) return wrapList;
        
        queue.offer(root);
        while(!queue.isEmpty()){
            int levelNum = queue.size();
            List<Integer> subList = new LinkedList<Integer>();
            for(int i=0; i<levelNum; i++) {
                if(queue.peek().left != null) queue.offer(queue.peek().left);
                if(queue.peek().right != null) queue.offer(queue.peek().right);
                subList.add(queue.poll().val);
            }
            wrapList.add(subList);
        }
        return wrapList;
    }
}
```

---

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