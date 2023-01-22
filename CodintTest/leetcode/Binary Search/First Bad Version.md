### 소모 시간
- 11분 46초

### 통과율
- 46%

### 문제 분석
- binary serch 이용
- mid 구할 때 오버플로우 에러 조심해야됨.

### My Solution
```java
public class Solution extends VersionControl {
    public int firstBadVersion(int n) {
        int low = 1, high = n;
        
        while (low <= high) {
            int mid = (low + high) / 2;
            
            // Index which is before first bad version should be false.
            if (isBadVersion(mid) && !isBadVersion(mid - 1))
                return mid;
            else if (!isBadVersion(mid))
                low = mid + 1;
            else
                high = mid - 1;
                
        }
        return -1;
    }
}
```

### Other Solution
- https://leetcode.com/problems/first-bad-version/solutions/71296/o-lgn-simple-java-solution/
```java
public int firstBadVersion(int n) {
    int start = 1, end = n;
    while (start < end) {
        int mid = start + (end-start) / 2;
        if (!isBadVersion(mid)) start = mid + 1;
        else end = mid;            
    }        
    return start;
}
```
