## Singly Linked List

### 소모 시간
- 54분

### 통과율
- 100%

### My Solution
```python
class Node:
    def __init__(self, val: int, next_node = None):
        self.val = val
        self.next_node = next_node

class MyLinkedList:

    def __init__(self):
        self.length = 0
        self.head = None

    def get(self, index: int) -> int:
        cur = self.head
        for _ in range(self.length):
            cur = cur.next_node
        
        if index < 0 or index >= self.length:
            return -1
        
        cur = self.head
        for _ in range(index):
            cur = cur.next_node
        
        return cur.val

    def addAtHead(self, val: int) -> None:
        node = Node(val, self.head)
        self.head = node
        self.length += 1

    def addAtTail(self, val: int) -> None:
        if self.length == 0:
            self.addAtHead(val)
            return
        
        cur = self.head
        for _ in range(self.length - 1):
            cur = cur.next_node
        node = Node(val, None)
        cur.next_node = node 
        self.length += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index == 0:
            self.addAtHead(val)
            return
        
        if index > self.length:
            return
        
        cur = self.head
        for _ in range(index - 1):
            cur = cur.next_node
        node = Node(val, cur.next_node)
        cur.next_node = node
        self.length += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.length:
            return
        
        if index == 0:
            self.head = self.head.next_node
            self.length -= 1
            return
        
        cur = self.head
        # Get index - 1 Node.
        for _ in range(index - 1):
            cur = cur.next_node
        cur.next_node = cur.next_node.next_node
        self.length -= 1
```
- 길이가 1인 경우를 제대로 처리하지 못했다.

### Other Solution
- https://leetcode.com/problems/design-linked-list/discuss/778751/Very-Clean-Python-Solution
- `add`를 모두 `addAtIndex`로 통일한다.

---

## Doubly Linked List
### 소모 시간
- 45분

### 통과율
- 100%

### My Solution
```python
class Node:
    def __init__(self, val = 0, next = None, prev = None):
        self.val = val
        self.next = next
        self.prev = prev

class MyLinkedList:
    
    def __init__(self):
        self.head = None
        self.length = 0
        
    def get(self, index: int) -> int:
        if index >= self.length:
            return -1
        
        cur = self.__get_index_node(index)
        
        return cur.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.length, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.length:
            return None
        
        if index == 0:
            cur = self.head
        if index == self.length:
            cur = self.__get_index_node(index - 1)
        else:
            cur = self.__get_index_node(index)
        
        if index == 0:
            node = Node(val, next = self.head, prev = None)
            if self.head:
                self.head.prev = node
            self.head = node
        elif index == self.length:
            node = Node(val, next = None, prev = cur)
            cur.next = node
        else:
            node = Node(val, next = cur, prev = cur.prev)
            cur.prev.next = node
            cur.prev = node
                
        self.length += 1
        
        
    def deleteAtIndex(self, index: int) -> None:
        if index >= self.length:
            return None
        
        cur = self.__get_index_node(index)
        
        if index == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            
        elif index == self.length:
            if cur.prev:
                cur.prev.next = None
        else:
            if cur.next:
                cur.next.prev = cur.prev
            if cur.prev:
                cur.prev.next = cur.next
        
        self.length -= 1
    
    
    def __get_index_node(self, index) -> Node:
        cur = self.head
        for _ in range(index):
            cur = cur.next
        
        return cur
```