### 소모 시간
- 21분 4초

### 통과율
- 100%

### 문제점
- `put`을 할 때 기존 key이든 새로운 key이든 결과가 똑같아서 비슷하게 처리하다 보니 full 조건과 key 개수 조건을 이상하게 했다. 하나에 꽂혀서 너무 당연한건데 생각을 못했다...
- `get`과 `put`에서 O(1)이 보장되지 않는다.

### my solution
```
class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        # index가 key
        self.key_num = 0
        self.pairs = [-1] * 3001
        self.stack = []
        
    def get(self, key: int) -> int:
        if self.pairs[key] != -1:
            if key in self.stack:
                self.stack.remove(key)
            self.stack.append(key)     
        return self.pairs[key]
        
    def put(self, key: int, value: int) -> None:
        if self.pairs[key] == -1:
            if self.key_num == self.capacity:
                evicted = self.stack[0]
                self.stack = self.stack[1:]
                self.key_num -= 1
                self.pairs[evicted] = -1
            self.key_num += 1
        else:
            if key in self.stack:
                self.stack.remove(key)
        
        self.pairs[key] = value
        self.stack.append(key)
```

### other solution
- 출처: https://leetcode.com/problems/lru-cache/discuss/45911/Java-Hashtable-%2B-Double-linked-list-(with-a-touch-of-pseudo-nodes)
```
import java.util.Hashtable;


public class LRUCache {

class DLinkedNode {
  int key;
  int value;
  DLinkedNode pre;
  DLinkedNode post;
}

/**
 * Always add the new node right after head;
 */
private void addNode(DLinkedNode node) {
    
  node.pre = head;
  node.post = head.post;

  head.post.pre = node;
  head.post = node;
}

/**
 * Remove an existing node from the linked list.
 */
private void removeNode(DLinkedNode node){
  DLinkedNode pre = node.pre;
  DLinkedNode post = node.post;

  pre.post = post;
  post.pre = pre;
}

/**
 * Move certain node in between to the head.
 */
private void moveToHead(DLinkedNode node){
  this.removeNode(node);
  this.addNode(node);
}

// pop the current tail. 
private DLinkedNode popTail(){
  DLinkedNode res = tail.pre;
  this.removeNode(res);
  return res;
}

private Hashtable<Integer, DLinkedNode> 
  cache = new Hashtable<Integer, DLinkedNode>();
private int count;
private int capacity;
private DLinkedNode head, tail;

public LRUCache(int capacity) {
  this.count = 0;
  this.capacity = capacity;

  head = new DLinkedNode();
  head.pre = null;

  tail = new DLinkedNode();
  tail.post = null;

  head.post = tail;
  tail.pre = head;
}

public int get(int key) {

  DLinkedNode node = cache.get(key);
  if(node == null){
    return -1; // should raise exception here.
  }

  // move the accessed node to the head;
  this.moveToHead(node);

  return node.value;
}


public void put(int key, int value) {
  DLinkedNode node = cache.get(key);

  if(node == null){

    DLinkedNode newNode = new DLinkedNode();
    newNode.key = key;
    newNode.value = value;

    this.cache.put(key, newNode);
    this.addNode(newNode);

    ++count;

    if(count > capacity){
      // pop the tail
      DLinkedNode tail = this.popTail();
      this.cache.remove(tail.key);
      --count;
    }
  }else{
    // update the value.
    node.value = value;
    this.moveToHead(node);
  }
}

}
```
- One interesting property about double linked list is that the node can remove itself without other reference.
- It takes constant time to add and remove nodes from the head or tail.
- One particularity about the double linked list that I implemented is that I create a pseudo head and tail to mark the boundary, so that we don't need to check the NULL node during the update.