### 소모 시간
- 23분 27초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        boolean[][] visited = new boolean[image.length][image[0].length];
        Queue<List<Integer>> queue = new LinkedList<>();
        visited[sr][sc] = true;
        queue.offer(List.of(sr, sc));

        List<List<Integer>> neighbors = List.of(
            List.of(0, 1),
            List.of(1, 0),
            List.of(-1, 0),
            List.of(0, -1)
        );
        
        while (!queue.isEmpty()) {
            List<Integer> point = queue.poll();
            int x = point.get(0), y = point.get(1);
            
            for (List<Integer> neighbor: neighbors) {
                int i = x + neighbor.get(0), j = y + neighbor.get(1);

                // boundary.
                if (i >= 0 && j >= 0 && i < image.length && j < image[0].length) {
                    // unvisited and same color.
                    if (!visited[i][j] && image[i][j] == image[sr][sc]) {
                        image[i][j] = color;
                        visited[i][j] = true;
                        queue.offer(List.of(i, j));
                    }
                }
            }
        }
        image[sr][sc] = color;

        return image;
    }

```

### Other Solution
- https://leetcode.com/problems/flood-fill/solutions/473494/java-dfs-bfs-solutions-space-complexity-analysis-clean-concise/?orderBy=most_votes
```java
class Solution {
    int[] DIRS = {0, 1, 0, -1, 0};
    public int[][] floodFill(int[][] image, int sr, int sc, int newColor) {
        if (image[sr][sc] == newColor) return image; // same color -> no need to replace

        int m = image.length, n = image[0].length;
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{sr, sc});
        int oldColor = image[sr][sc];
        image[sr][sc] = newColor;
        while (!q.isEmpty()) {
            int[] top = q.poll();
            for (int i = 0; i < 4; i++) {
                int nr = top[0] + DIRS[i];
                int nc = top[1] + DIRS[i + 1];
                if (nr < 0 || nr == m || nc < 0 || nc == n || image[nr][nc] != oldColor) continue;
                image[nr][nc] = newColor; // also mean we marked it as visited!
                q.offer(new int[]{nr, nc});
            }
        }
        return image;
    }
}
```
- 방향 더하는 걸 굳이 2D로 하지 않고 1D로 할 수 있음.
- 이미 새로운 색깔이면 방문한 것이므로 `visited` 필요 없음.
