### 소모 시간
- 15분

### 통과율
- 100%

### my solution
```java
class Solution {
    public boolean validMountainArray(int[] arr) {
        if (arr.length < 3)
            return false;
        
        if (arr[0] > arr[1])
            return false;
        
        int prevValue = arr[0];
        int peakIdx = 0;
        for (int i = 1; i < arr.length; i++){
            if (prevValue == arr[i]) {
                return false;
            }
            else if (prevValue > arr[i]) {
                peakIdx = i - 1;
                break;
            }
            prevValue = arr[i];
        }
        
        // Last Index
        if (peakIdx == arr.length - 1)
            return false;
        
        prevValue = arr[peakIdx];
        for (int i = peakIdx + 1; i < arr.length; i++) {
            if (prevValue <= arr[i])
                return false;
            prevValue = arr[i];
        }
        
        return true;
    }
}
```

### other solution
```java
public boolean validMountainArray(int[] A) {
    int n = A.length, i = 0, j = n - 1;
    while (i + 1 < n && A[i] < A[i + 1]) i++;
    while (j > 0 && A[j - 1] > A[j]) j--;
    return i > 0 && i == j && j < n - 1;
}
```
- Two people climb from left and from right separately.
- If they are climbing the same mountain, they will meet at the same point.
