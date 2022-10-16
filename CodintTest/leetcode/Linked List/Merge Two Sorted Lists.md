### 소모 시간
- 19분 19초

### 통과율
- 100%

### my solution
```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1 or not list2:
            return list1 or list2
        
        cur1, cur2 = list1, list2
        new_head = ListNode(val=-101)
        new_cur = new_head
        
        while cur1 and cur2:
            if cur1.val <= cur2.val:
                new_cur.next = cur1
                cur1 = cur1.next
            else:
                new_cur.next = cur2
                cur2 = cur2.next

            new_cur = new_cur.next
        
        
        while cur1:
            new_cur.next = cur1
            cur1 = cur1.next
            new_cur = new_cur.next
        
        while cur2:
            new_cur.next = cur2
            cur2 = cur2.next
            new_cur = new_cur.next
        
        return new_head.next
```
- `new_head`를 새로운 노드를 안 만들고 기존 노드 포인팅하게 해서 다 꼬였음.
- 새로운 리스트에 대한 노드는 새롭게 만들어주자 ㅠ

### other solution
- https://leetcode.com/problems/merge-two-sorted-lists/discuss/1826693/Python3-MERGING-Explained
```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()
        while list1 and list2:               
            if list1.val < list2.val:
                cur.next = list1
                list1, cur = list1.next, list1
            else:
                cur.next = list2
                list2, cur = list2.next, list2
                
        if list1 or list2:
            cur.next = list1 if list1 else list2
            
        return dummy.next
```
- `list1` 혹은 `list2`가 남았을 때, `next`로 하나만 지정해주면 나머지는 이미 `next` 다음에 있음.
- 따라서 `while`로 할 필요 없음.
