### 소모 시간
- 20분 25초

### 통과율
- 100%

### 접근법
- 새로운 노드를 만들어서 노드의 next를 이전 것으로 한다.

### 문제점
- 기존 노드의 next를 이전 것으로해서 next 정보가 다 날라갔다.

### my solution
```java
class Solution {
    public ListNode reverseList(ListNode head) {
        // 0개 혹은 1개
        if (head == null || head.next == null)
            return head;
        
        ListNode cur = head;
        ListNode answer = new ListNode(head.val);
        
        while (true) {
            ListNode prev = answer;
            cur = cur.next;
            if (cur == null)
                break;
            answer = new ListNode(cur.val);
            answer.next = prev;
        }
        
        return answer;
    }
}
```

### other solution
- https://leetcode.com/problems/reverse-linked-list/discuss/58125/In-place-iterative-and-recursive-Java-solution/59714
```java
public ListNode reverseList(ListNode head) {
        ListNode prevHead = null;
        while(head != null){
            ListNode recordNext = head.next;
            head.next = prevHead;
            prevHead = head;
            head = recordNext;
        }
        return prevHead;
    }
```