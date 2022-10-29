### 통과율
- 0%

### my solution
```python
class Solution:
    def flatten(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return head
        
        new_head = head
        new_cur = new_head
        stack = [head]
        while stack:
            cur = stack.pop()
            
            if not cur:
                break
            
            if cur.child:
                if cur.next:
                    stack.append(cur.next)
                new_cur.next = cur.child
                stack.append(cur.child)
                cur.next = cur.child
                cur.child.prev = cur
            else:
                new_cur.next = cur.next
                if cur.next:
                    stack.append(cur.next)
            
            new_cur = new_cur.next
                
        
        return new_head
```
- 스택을 쓰긴 썼음. 쓴 건 잘했음.
- 굳이 새로운 head를 만들 필요 없었음. 기존 리스트의 연결을 변경하는 것이기 때문임.
- while 조건이 stack이 아니라 cur이어야 함.
- child의 마지막은 child의 parent의 next를 next로 해야하고, parent의 next는 prev를 child로 해야됨.
- child의 마지막은 next가 `None`이고 parent의 next가 스택에 있을테니 stack이 비어있을 수 없음. 이 조건을 이용하면 됨.

### other solution
- https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/discuss/150321/Easy-Understanding-Java-beat-95.7-with-Explanation/837400
```java
class Solution {
    public Node flatten(Node node) {
        Stack<Node> stk = new Stack<>();
        Node cur = node;
        while(cur != null) {
            if(cur.child != null) {
                Node next = cur.next;
                if(next != null)
                    stk.add(next);
                cur.next = cur.child;
                if(cur.next != null)
                    cur.next.prev = cur;
                cur.child = null;
            } else if(cur.next == null && !stk.isEmpty()) {
                cur.next = stk.pop();
                cur.next.prev = cur;
            }
            cur = cur.next;
        }
        return node;
    }
}
```