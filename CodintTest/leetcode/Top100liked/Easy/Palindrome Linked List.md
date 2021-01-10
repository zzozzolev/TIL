# 소모 시간
- 15분

# 통과율
- 100%

# 문제점
- `cur != None`으로 조건을 걸어야 하는데 `cur.next != None` 이렇게 해버렸다.

# my solution
```
class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        cur = head
        count = 0
        while cur != None:
            count += 1
            cur = cur.next
        
        if count <= 1:
            return True
        
        stack = []
        cur = head
        half_num = count // 2
        
        while len(stack) != half_num:
            stack.append(cur.val)
            cur = cur.next
        
        # odd num
        if count % 2 != 0:
            cur = cur.next
        
        while cur != None:
            if stack.pop() != cur.val:
                return False
            cur = cur.next
        
        return True
```

# other solution
- https://leetcode.com/problems/palindrome-linked-list/discuss/64500/11-lines-12-with-restore-O(n)-time-O(1)-space
```
def isPalindrome(self, head):
    rev = None
    fast = head
    while fast and fast.next:
        fast = fast.next.next
        rev, rev.next, head = head, rev, head.next
    tail = head.next if fast else head
    isPali = True
    while rev:
        isPali = isPali and rev.val == tail.val
        head, head.next, rev = rev, head, rev.next
        tail = tail.next
    return isPali
```
- 옮기는 동시에 홀수인지 확인할 수 있게 함.. 이런 거 어떻게 생각하냐..
- 댓글에 시각화한 거 있는데 그거 보면 좀 이해가 감.