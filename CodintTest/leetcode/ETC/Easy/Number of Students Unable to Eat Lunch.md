### 소모 시간
- 40분

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int countStudents(int[] students, int[] sandwiches) {
        Deque<List<Integer>> queue = new ArrayDeque<>();
        
        for (int i = 0; i < students.length; i++)
            queue.offerLast(List.of(i, students[i]));

        // Check if each student visited sandwiches.
        boolean[][] visited = new boolean[students.length][sandwiches.length];

        int topIdx = 0;
        while (!queue.isEmpty()) {
            List<Integer> pair = queue.peekFirst();
            int seq = pair.get(0);
            int student = pair.get(1);

            // Student visit again.
            if (visited[seq][topIdx])
                break;

            visited[seq][topIdx] = true;
            queue.removeFirst();

            if (student == sandwiches[topIdx]) {
                topIdx += 1;
            }
            else {
                queue.offerLast(pair);
            }
        }

        System.out.println(queue);
        return queue.size();
    }
}
```
- deque에서 `offerFist`하면 나중에 넣은 게 제일 처음이 되므로 원래 순서 그대로 유지하고 싶으면 `offerLast`로 넣어야 됨.
- 방문 확인하지 않고 제거해버리면 정답보다 명수가 하나 적게 나옴.

### Other Solution
```java
public int countStudents(int[] A, int[] B) {
    int count[] = {0, 0}, n = A.length, k;
    for (int a: A)
        count[a]++;
    for (k = 0; k < n && count[B[k]] > 0; ++k)
        count[B[k]]--;
    return n - k;
}
```
- 순서 중요하지 않음. 어차피 언젠가는 stack의 top을 보기 때문임.
- 그냥 stack 순서대로 카운트를 감소 시켰을 때 0이면 끝남.
