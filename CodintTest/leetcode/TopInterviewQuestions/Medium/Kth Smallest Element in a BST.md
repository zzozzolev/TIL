### 소모 시간
- 20분?

### 통과율
- 100%

### 문제점
- 마지막에 sort는 안 해야한다;

### my solution
```java
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Stack<TreeNode> stack = new Stack<>();
        List<Integer> list = new ArrayList<>();
        stack.push(root);
        
        while (!stack.empty()) {
            TreeNode node = stack.pop();
            list.add(node.val);
            
            if (node.right != null) {
                stack.push(node.right);
            }
            
            if (node.left != null) {
                stack.push(node.left);
            }
        }
        
        list.sort(Comparator.naturalOrder());
        
        return list.get(k-1);
    }
}
```

### other solution
- https://leetcode.com/problems/kth-smallest-element-in-a-bst/discuss/63660/3-ways-implemented-in-JAVA-(Python)%3A-Binary-Search-in-order-iterative-and-recursive
```java
public int kthSmallest(TreeNode root, int k) {
      Stack<TreeNode> st = new Stack<>();
      
      while (root != null) {
          st.push(root);
          root = root.left;
      }
          
      while (k != 0) {
          TreeNode n = st.pop();
          k--;
          if (k == 0) return n.val;
          TreeNode right = n.right;
          while (right != null) {
              st.push(right);
              right = right.left;
          }
      }
      
      return -1; // never hit if k is valid
}
```
- 제일 왼쪽은 가장 작은 수이므로 제일 왼쪽을 찾는다.
- 루트의 오른쪽의 왼쪽이 있다면 제일 왼쪽을 다시 찾는다.
