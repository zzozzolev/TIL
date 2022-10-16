### 소모 시간
- 13분 15초

### 통과율
- 100%

### my solution
```python
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        if head is None:
            return None
        
        dummy_head = ListNode(val=-1, next=head)
        cur = dummy_head

        while cur is not None and cur.next is not None:
            # Remove a node.
            while cur is not None and cur.next is not None and cur.next.val == val:
                cur.next = cur.next.next
            
            cur = cur.next
        
        return dummy_head.next
```

### other solution
- https://leetcode.com/problems/remove-linked-list-elements/discuss/158651/Simple-Python-solution-with-explanation-(single-pointer-dummy-head).
```python
class Solution:
    def removeElements(self, head, val):
        """
        :type head: ListNode
        :type val: int
        :rtype: ListNode
        """
        
        dummy_head = ListNode(-1)
        dummy_head.next = head
        
        current_node = dummy_head
        while current_node.next != None:
            if current_node.next.val == val:
                current_node.next = current_node.next.next
            else:
                current_node = current_node.next
                
        return dummy_head.next
```
- `cur.next`가 `None`이 아닌 걸 테스트하면 `cur`이 `None`인 것을 테스트할 필요가 없다.
- `cur`을 무조건 안 바꾸고 `val`이 아닐 때만 바꾸면 내부에서 또 `while`을 쓸 필요가 없다.
