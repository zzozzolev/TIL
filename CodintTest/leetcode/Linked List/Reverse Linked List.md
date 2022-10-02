### 소모 시간
- 18분 13초

### 통과율
- 100%

### my solution
```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        prev = head
        cur = head.next
        head.next = None
        
        while cur is not None:
            original_next = cur.next
            cur.next = prev
            prev = cur
            cur = original_next
            
        return prev
```

### other solution
- https://leetcode.com/problems/reverse-linked-list/discuss/803955/C%2B%2B-Iterative-vs.-Recursive-Solutions-Compared-and-Explained-~99-Time-~85-Space
```c++
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *nextNode, *prevNode = NULL;
        while (head) {
            nextNode = head->next;
            head->next = prevNode;
            prevNode = head;
            head = nextNode;
        }
        return prevNode;
    }
};
```
- 내가 풀은 거랑 거의 비슷함.
- 근데 처음에 `None`, `None`으로 시작한 게 좀 다름.
