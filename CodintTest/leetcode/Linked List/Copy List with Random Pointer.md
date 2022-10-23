### 소모 시간
- 25분 24초

### 통과율
- 100%

### my solution
```python
class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        id2node = {}
        
        cur = head
        new_head = Node(0)
        new_cur = new_head
        
        # Make new nodes
        while cur:
            new_node = Node(cur.val, next=None, random=cur.random)
            new_cur.next = new_node
            id2node[id(cur)] = new_node
            cur = cur.next
            new_cur = new_cur.next
        
        # Link random nodes
        new_cur = new_head.next
        while new_cur:
            if new_cur.random:
                new_cur.random = id2node[id(new_cur.random)]
            new_cur = new_cur.next
        
        return new_head.next
```

### other solution
- https://leetcode.com/problems/copy-list-with-random-pointer/discuss/43491/A-solution-with-constant-space-complexity-O(1)-and-linear-time-complexity-O(N)
- [그림 설명](https://leetcode.com/problems/copy-list-with-random-pointer/discuss/43491/A-solution-with-constant-space-complexity-O(1)-and-linear-time-complexity-O(N)/42652)
```java
public RandomListNode copyRandomList(RandomListNode head) {
  RandomListNode iter = head, next;

  // First round: make copy of each node,
  // and link them together side-by-side in a single list.
  while (iter != null) {
    next = iter.next;

    RandomListNode copy = new RandomListNode(iter.label);
    iter.next = copy;
    copy.next = next;

    iter = next;
  }

  // Second round: assign random pointers for the copy nodes.
  iter = head;
  while (iter != null) {
    if (iter.random != null) {
      iter.next.random = iter.random.next;
    }
    iter = iter.next.next;
  }

  // Third round: restore the original list, and extract the copy list.
  iter = head;
  RandomListNode pseudoHead = new RandomListNode(0);
  RandomListNode copy, copyIter = pseudoHead;

  while (iter != null) {
    next = iter.next.next;

    // extract the copy
    copy = iter.next;
    copyIter.next = copy;
    copyIter = copy;

    // restore the original list
    iter.next = next;

    iter = next;
  }

  return pseudoHead.next;
}
```
- cur.next에 새로운 노드를 만들면 해쉬테이블 필요 없음.
- random도 원래 random.next를 포인팅하게 하면 됨.
- 마지막에 2단계씩 건너뛰면 원래 링크로 만들 수 있음.
