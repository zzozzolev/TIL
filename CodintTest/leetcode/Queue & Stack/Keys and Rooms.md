### 소모 시간
- 12분 31초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public boolean canVisitAllRooms(List<List<Integer>> rooms) {
        boolean[] visited = new boolean[rooms.size()];
        Stack<Integer> stack = new Stack<>();
        visited[0] = true;
        stack.push(0);

        while (!stack.isEmpty()) {
            int visitRoom = stack.pop();

            for (int room : rooms.get(visitRoom)) {
                if (!visited[room]) {
                    visited[room] = true;
                    stack.push(room);
                }
            }
        }

        for (boolean visit : visited) {
            if (!visit)
                return false;
        }

        return true;
    }
}
```
