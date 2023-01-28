### 소모 시간
- 9분 18초

### 통과율
- 100%
  
### My Solution
```java
class Solution {
    public int[] minOperations(String boxes) {
        int[] answer = new int[boxes.length()];
        for (int i = 0; i < boxes.length(); i++) {
            for (int j = 0; j < boxes.length(); j++) {
                if (i == j)
                    continue;
                
                if (boxes.charAt(j) == '1')
                    answer[i] += Math.abs(i - j);
            }
        }

        return answer;
    }
}
```

### Other Solution
```java
class Solution {
    public int[] minOperations(String boxes) {
        int[] res = new int[boxes.length()];
        
        for (int i = 0, ops = 0, cnt = 0; i < boxes.length(); ++i) {
            res[i] += ops;
            cnt += boxes.charAt(i) == '1' ? 1 : 0;
            ops += cnt;
        }
        
        for (int i = boxes.length() - 1, ops = 0, cnt = 0; i >= 0; --i) {
            res[i] += ops;
            cnt += boxes.charAt(i) == '1' ? 1 : 0;
            ops += cnt;
        }
        return res;
    }
}
```
- 오른쪽으로 옮길 때와 왼쪽으로 옮길 때를 각각 계산함.