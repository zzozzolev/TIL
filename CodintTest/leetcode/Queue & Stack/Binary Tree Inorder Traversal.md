### 소모 시간
- 6분 6초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> values = new ArrayList<>();
        visit(values, root);
        return values;
    }

    private void visit(List<Integer> values, TreeNode node) {
        if (node == null)
            return;
        
        if (node.left != null)
            visit(values, node.left);
        
        values.add(node.val);

        if (node.right != null)
            visit(values, node.right);
    }
}
```
