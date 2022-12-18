### 소모 시간
- 10분 1초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int balancedStringSplit(String s) {
        int l = 0, r = 0, count = 0;
        
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == 'L')
                l++;
            else
                r++;
            
            if (l == r) {
                count++;
                l = 0;
                r = 0;
            }
        }

        return count;
    }
}
```

### Other Solution
- https://leetcode.com/problems/split-a-string-in-balanced-strings/solutions/403836/c-java-python-easy-solution/
```java
public int balancedStringSplit(String s) {
    int res = 0, cnt = 0;
    for (int i = 0; i < s.length(); ++i) {
        cnt += s.charAt(i) == 'L' ? 1 : -1;
        if (cnt == 0) ++res;
    }
    return res;             
}    
```
- L, R 두 개 밖에 없으므로 각자 하지 않고 +, - 처리하면 변수 하나만 사용 가능함.
