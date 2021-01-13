# 소모 시간
- 1시간

# 통과율
- 40%

# 문제점
- 그냥 reversed도 되지 않았다.
- 총체적 난국
- dummy node 없이 풀려고 해서 엉망진창이 된 것 같다.
- 왜 `next.next`에 꽂힌 거지..

# my solution
```
class Solution:
    def reverseBetween(self, head: ListNode, m: int, n: int) -> ListNode:
        if m == n:
            return head
        
        prev = None
        first = None
        last = None
        pos = 1
        cur = head
        
        while pos <= n and cur is not None:
            if pos < m:
                if pos + 1 == m:
                    prev = cur
                pos += 1
                cur = cur.next
                continue
            
            if first is None:
                first = cur   
            
            next = cur.next
            if pos + 1 == n:
                last = next
                
            pos_2 = None
            if next is not None:
                pos_2 = cur.next.next
                next.next = cur
                if pos + 2 == n:
                    last = pos_2
                
                
            # (pos + 2) node 존재
            if pos_2 != None:
                pos_3 = pos_2.next
                pos_2.next = next
                # set cur to (pos + 3) node
                cur = pos_3
                pos += 3
                if pos == n:
                    last = cur
                
            if last is not None:
                break
        
        if first == head:
            head = first.next
            first.next = None
        else:
            first.next = cur
        if prev is not None:
            prev.next = last
        
        return head
```

# other solution
- https://github.com/monkeys-code/save-the-monkey-2A/blob/master/week4_20200119_92_damian.md
```
class Solution {
    public ListNode reverseBetween(ListNode head, int m, int n) {
        if (head == null || head.next == null || m == n) {
            return head;
        }
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode prev = dummy;
        for (int i = 0; i < m - 1; i ++) {
            prev = prev.next;
        }
        // prev의 next를 n번 노드로 한다.
        prev.next = doReverseBetween(prev.next, m, n);
        return dummy.next;
    }
    
    // 함수는 reverse 한 뒤 head를 반환한다. 결과적으로 n번 노드를 반환하는 것이다.
    private ListNode doReverseBetween(ListNode head, int m, int n) {
        if (head == null || head.next == null || m == n) {
            return head;
        }
        ListNode prev = null;
        ListNode curr = head;
        ListNode next = null;
        for (int i = 0; i < n - m + 1; i++) {
            next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        // m번 노드의 next를 n번 노드의 next로 한다.
        head.next = next;
        return prev;
    }   
}
```
- `dummy`를 이용해 `head` 부터가 아니라 이전부터 시작할 수 있도록 한다.
- `prev`, `curr`, `next` node로 포인터를 관리한다.