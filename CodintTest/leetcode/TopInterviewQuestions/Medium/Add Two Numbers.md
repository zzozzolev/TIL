### 소모 시간
- 31분 57초

### 통과 여부
- 100%

### 접근법
- `l1`과 `l2`가 모두 `None`이 될 때까지 탐색하는 노드를 하나씩 늘려나가면서 다음의 과정을 반복한다.
    - `l1`과 `l2`에 대한 value를 0으로 초기화한다.
    - `l1`과 `l2`의 현재 node가 None이 아니라면 각각에 대한 value를 현재 node의 value로 한다.
    - `l1`과 `l2`의 현재 node의 value와 이전에 얻은 `carry`를 더해서 결과를 얻는다.
    - 만약 결과가 10이상이면 `carry`를 1로 하고 result를 mod 10으로 한다. 그렇지 않다면 `carry`를 0으로 한다.
    - root가 없다면 ListNode를 새로 만들어 root로 한다. 그렇지 않다면 결과 linked list의 현재 node의 next를 만들고 next를 현재 node로 한다.
    - `l1`과 `l2`의 현재 node가 None이 아니라면 각각에 대한 현재 node를 next로 한다.
- `root`를 반환한다.

### 문제점
- 처음에 root를 반환하지 않고 계속 변경되는 tail을 반환해서 계속 틀렸다.
- `divmod`를 잘 사용했으면 더 깔끔하게 짤 수 있을 것 같다.

### my solution
```
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        l1_cur, l2_cur = l1, l2
        carry = 0
        root = None
        cur_node = None
        while not(l1_cur is None and l2_cur is None):
            l1_val, l2_val = 0, 0
            
            if l1_cur is not None:
                l1_val = l1_cur.val
            
            if l2_cur is not None:
                l2_val = l2_cur.val
            
            result = l1_val + l2_val + carry
            
            if result >= 10:
                carry = 1
                result = result % 10
            else:
                carry = 0
            
            if root is None:
                root = ListNode(result)
                cur_node = root
            else:
                cur_node.next = ListNode(result)
                cur_node = cur_node.next
            
            if l1_cur is not None:
                l1_cur = l1_cur.next
            
            if l2_cur is not None:
                l2_cur = l2_cur.next
            
            if (l1_cur is None and l2_cur is None) \
                and carry == 1:
                cur_node.next = ListNode(1)
        
        return root
```

### other solution
```
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        result = ListNode(0)
        result_tail = result
        carry = 0
                
        while l1 or l2 or carry:            
            val1  = (l1.val if l1 else 0)
            val2  = (l2.val if l2 else 0)
            carry, out = divmod(val1+val2 + carry, 10)    
                      
            result_tail.next = ListNode(out)
            result_tail = result_tail.next                      
            
            l1 = (l1.next if l1 else None)
            l2 = (l2.next if l2 else None)
               
        return result.next
```