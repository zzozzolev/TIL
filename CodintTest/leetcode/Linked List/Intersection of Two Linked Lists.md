### 소모 시간
- 10분 52초

### 통과율
- 87%
- Time Limit Exceeded

### my solution
```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        target = headA
        
        while target is not None:
            comp = headB
            while comp is not None:
                if target == comp:
                    return target
                comp = comp.next
            
            target = target.next
        
        return None
```

### other solution
```java
public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    //boundary check
    if(headA == null || headB == null) return null;
    
    ListNode a = headA;
    ListNode b = headB;
    
    //if a & b have different len, then we will stop the loop after second iteration
    while( a != b){
    	//for the end of first iteration, we just reset the pointer to the head of another linkedlist
        a = a == null? headB : a.next;
        b = b == null? headA : b.next;    
    }
    
    return a;
}
```
- [visual solution](https://leetcode.com/problems/intersection-of-two-linked-lists/discuss/49785/Java-solution-without-knowing-the-difference-in-len!/165648)
- 서로 바꿔서 순회하면 같은 길이를 가질 수 밖에 없다.
