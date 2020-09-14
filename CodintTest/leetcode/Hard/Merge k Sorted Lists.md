### 소모 시간
- 19분 30초

### 통과율
- 100%

### 접근법
- 각각의 linked list를 순회하면서 현재 포인터의 값을 얻어낸다.
- 그 중 가장 작은 값만 결과 linked list에 새로운 노드로 추가한다.
- 가장 작은 값에 해당하는 linked list의 현재 포인터를 `next`로 바꿔준다.

### 문제점
- 반복문을 돌 때마다 sort를 하므로 `O(N^2logN)`으로 시간 복잡도가 매우 비효율적이다.

### my solution
```
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        root = ListNode()
        cur = root
        curs = lists
        while True:
            cur_values = [(cur.val, i) for i, cur in enumerate(curs) if cur]
            
            if len(cur_values) == 0:
                break
            else:
                cur_values.sort()
                min_value = cur_values[0][0]
                for value, index in cur_values:
                    if value != min_value:
                        break
                    cur.next = ListNode(value)
                    cur = cur.next
                    curs[index] = curs[index].next
        
        return root.next
```

### other solution
- https://leetcode.com/problems/merge-k-sorted-lists/solution/
```
# heapq
class Solution:
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        h = [(l.val, idx) for idx, l in enumerate(lists) if l]
        heapq.heapify(h)
        head = cur = ListNode(None)
        while h:
            val, idx = heapq.heappop(h)
            cur.next = ListNode(val)
            cur = cur.next
            node = lists[idx] = lists[idx].next
            if node:
                heapq.heappush(h, (node.val, idx))
        return head.next

# Merge with Divide And Conquer
class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        # 이거 넣어줘야 empty input 처리 가능
        if len(lists) == 0:
            return None
        amount = len(lists)
        interval = 1
        while interval < amount:
            for i in range(0, amount - interval, interval * 2):
                lists[i] = self.merge2Lists(lists[i], lists[i + interval])
            interval *= 2
        return lists[0] if amount > 0 else lists

    def merge2Lists(self, l1, l2):
        head = point = ListNode(0)
        while l1 and l2:
            if l1.val <= l2.val:
                point.next = l1
                l1 = l1.next
            else:
                point.next = l2
                # 이 부분 내가 수정한 건데 이렇게 해도 다 통과함.
                l2 = l2.next
            point = point.next
        if not l1:
            point.next=l2
        else:
            point.next=l1
        return head.next
```