### 소모 시간
- 10분

### 통과율
- 100%

### my solution
```java
class Solution {
    public int heightChecker(int[] heights) {
        int[] expected = heights.clone();
        Arrays.sort(expected);
        
        int answer = 0;
        for(int i = 0; i < heights.length; i++) {
            if (expected[i] != heights[i])
                answer += 1;
        }
        
        return answer;
    }
}
```

### other solution
- https://leetcode.com/problems/height-checker/discuss/369999/Help-you-to-understand-this-question-and-also-the-optimal-O(N)-solution!
```java
class Solution {
    public int heightChecker(int[] heights) {
        int[] map = new int[101]; // heights go from 1 to 100
        for(int h: heights) ++map[h];
        
        int res = 0;
        int h_ptr = 1;
        
        for(int h: heights) {
            while(map[h_ptr] == 0) ++h_ptr;
            
            if(h_ptr != h) {
                ++res;
            }
            
            --map[h_ptr];
        }
        
        return res;
    }
}
```
- a bucket/counting sort which only takes O(100n) = O(n) time.
