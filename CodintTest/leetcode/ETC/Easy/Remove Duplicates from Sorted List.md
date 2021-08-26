### 소모 시간
- 10분 30초

### 통과율
- 100%

### my solution
```
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        
        while cur != None and cur.next != None:
            # duplicated
            while cur != None and cur.next != None and cur.val == cur.next.val:
                # Remove cur.next
                cur.next = cur.next.next
            cur = cur.next
        
        return head
```