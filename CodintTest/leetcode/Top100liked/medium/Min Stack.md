# 소모 시간
- 15분 35초

# 통과율
- 100%

# 문제점
- `pop`에서 constant time이 아니라 `O(n)`이 나온다.

# my solution
```
class MinStack:

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.min_stack = []
        self.min_value = float("inf")
        

    def push(self, x: int) -> None:
        self.min_value = min(x, self.min_value)
        self.min_stack.append(x)

    def pop(self) -> None:
        popped = self.min_stack.pop()
        if popped == self.min_value:
            if len(self.min_stack) != 0:
                self.min_value = min(self.min_stack)
            else:
                self.min_value = float("inf")

    def top(self) -> int:
        return self.min_stack[-1]

    def getMin(self) -> int:
        return self.min_value
```

# other solution
- https://leetcode.com/problems/min-stack/discuss/49010/Clean-6ms-Java-solution
```
class MinStack {
    private Node head;
    
    public void push(int x) {
        if(head == null) 
            head = new Node(x, x);
        else 
            head = new Node(x, Math.min(x, head.min), head);
    }

    public void pop() {
        head = head.next;
    }

    public int top() {
        return head.val;
    }

    public int getMin() {
        return head.min;
    }
    
    private class Node {
        int val;
        int min;
        Node next;
        
        private Node(int val, int min) {
            this(val, min, null);
        }
        
        private Node(int val, int min, Node next) {
            this.val = val;
            this.min = min;
            this.next = next;
        }
    }
}
```
- 계속 `min`을 비교해서 유지한다.
- 해당 `Node`까지의 `min`이 해당 노드의 `min`으로 돼있을 것이다.