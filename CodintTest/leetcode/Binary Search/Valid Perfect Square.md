### 소모 시간
- 16분 48초

### 통과율
- 100%

### 문제 분석
- 바이너리 서치로 제곱근 구하기
- right에 mid를 할당하면서 제곱근을 찾으면 됨.

### My Solution
```java
class Solution {
    public boolean isPerfectSquare(int num) {
        if (num == 1)
            return true;
        
        int left = 1;
        int right = num;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            int other = num / mid;

            if (mid == other && mid * other == num) // 나누기에서 내림때문에 곱해서 num이 나오는지도 확인해야 됨.
                return true;
            else {
                left = other;
                right = mid;
            }
        }

        return false;
    }
}
```

### Other Solution
```java
public boolean isPerfectSquare(int num) {
        int low = 1, high = num;
        while (low <= high) {
            long mid = (low + high) >>> 1;
            if (mid * mid == num) {
                return true;
            } else if (mid * mid < num) {
                low = (int) mid + 1;
            } else {
                high = (int) mid - 1;
            }
        }
        return false;
    }
```
