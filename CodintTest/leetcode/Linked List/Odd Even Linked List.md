### 소모 시간
- 14분 27초

### 통과율
- 100%

### my solution
```python
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next or not head.next.next:
            return head
        
        odd_cur = head
        even_head = head.next
        even_cur = even_head
        
        while odd_cur.next and even_cur.next:
            odd_cur.next = even_cur.next
            even_cur.next = even_cur.next.next
            
            odd_cur = odd_cur.next
            even_cur = even_cur.next
        
        odd_cur.next = even_head
        
        return head
```

### other solution
- 리트코드에서 표 제일 많이 받은 거랑 거의 똑같이 풀었다 히힣.
