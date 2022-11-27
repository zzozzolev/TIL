### 소모 시간
- 20분

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int numIslands(char[][] grid) {
        boolean[][] visited = new boolean[grid.length][grid[0].length];
        
        int count = 0;
        List<List<Integer>> addedCoords = List.of(List.of(0, -1), List.of(0, 1), List.of(-1, 0), List.of(1, 0));

        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                // unvisited land. Do BFS.
                if (grid[i][j] != '0' && !visited[i][j]) {
                    Queue<List<Integer>> queue = new LinkedList<>();
                    visited[i][j] = true;
                    queue.offer(List.of(i, j));

                    while (!queue.isEmpty()) {
                        List<Integer> pair = queue.poll();
                        int x = pair.get(0);
                        int y = pair.get(1);

                        for (List<Integer> added: addedCoords) {
                            int alpha = x + added.get(0);
                            int beta = y + added.get(1);
                            
                            if (alpha >= 0 && alpha < grid.length && beta >= 0 && beta < grid[0].length) {
                                if (grid[alpha][beta] == '1' && !visited[alpha][beta]) {
                                    visited[alpha][beta] = true;
                                    queue.offer(List.of(alpha, beta));
                                }
                            }
                        }
                    }
                    count++;
                }
            }
        }

        return count;
    }
}
```
