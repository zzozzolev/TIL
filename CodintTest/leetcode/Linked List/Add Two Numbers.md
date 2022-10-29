### 소모 시간
- 23분 6초

### 통과율
- 100%

### my solution
```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:        
        new_head = ListNode(val=-1, next=None)
        new_cur = new_head
        l1_cur = l1
        l2_cur = l2
        
        carry = 0
        while l1_cur and l2_cur:
            node_sum = l1_cur.val + l2_cur.val + carry
            new_cur.next = ListNode(val=node_sum % 10)
            carry = node_sum // 10
            
            l1_cur = l1_cur.next
            l2_cur = l2_cur.next
            new_cur = new_cur.next
        
        while l1_cur:
            node_sum = l1_cur.val + carry
            new_cur.next = ListNode(val=node_sum % 10)
            carry = node_sum // 10
            
            l1_cur = l1_cur.next
            new_cur = new_cur.next
        
        while l2_cur:
            node_sum = l2_cur.val + carry
            new_cur.next = ListNode(val=node_sum % 10)
            carry = node_sum // 10
            
            l2_cur = l2_cur.next
            new_cur = new_cur.next
    
        if carry:
            new_cur.next = ListNode(val=carry)
    
        return new_head.next
```

### other solution
```java
public class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode c1 = l1;
        ListNode c2 = l2;
        ListNode sentinel = new ListNode(0);
        ListNode d = sentinel;
        int sum = 0;
        while (c1 != null || c2 != null) {
            sum /= 10;
            if (c1 != null) {
                sum += c1.val;
                c1 = c1.next;
            }
            if (c2 != null) {
                sum += c2.val;
                c2 = c2.next;
            }
            d.next = new ListNode(sum % 10);
            d = d.next;
        }
        if (sum / 10 == 1)
            d.next = new ListNode(1);
        return sentinel.next;
    }
}
```
- `while`문 조건으로 `or`을 하고, 각각에 대해 `null`을 검사하면 굳이 밖에서 `while`을 또 할 필요가 없다.
