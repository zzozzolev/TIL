### 소모 시간
- 12분 9초

### 통과율
- 100%

### my solution
```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # sz == 1
        if head.next is None:
            return None
        
        length = 0
        cur = head
        
        # Get length of list
        while cur is not None:
            length += 1
            cur = cur.next
        
        # Remove
        remove_idx = length - n
        
        if remove_idx == 0:
            head = head.next
            return head
        
        idx = 0
        cur = head
        
        # Find prev idx
        while idx != remove_idx - 1:
            cur = cur.next
            idx += 1
        
        cur.next = cur.next.next
        
        return head
```

### other solution
- https://leetcode.com/problems/remove-nth-node-from-end-of-list/discuss/1164542/JS-Python-Java-C%2B%2B-or-Easy-Two-Pointer-Solution-w-Explanation
```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        fast, slow = head, head
        for _ in range(n): fast = fast.next
        if not fast: return head.next
        while fast.next: fast, slow = fast.next, slow.next
        slow.next = slow.next.next
        return head
```
- `fast`를 `n`번째로 위치시켜놓으면 남은 건 `len(list) - n`임.
- `slow`를 `len(list) - n`만큼 이동 시키면 `n`번째에 위치하게 됨.
