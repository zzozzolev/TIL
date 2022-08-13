### 소모 시간
- 7분 24초

### 통과율
- 100%

### my solution
```java
class Solution {
    public int[] replaceElements(int[] arr) {
        if (arr.length == 1){
            arr[0] = -1;
            return arr;
        }
        
        // Don't include the last elem.
        for (int i = 0; i < arr.length - 1; i++) {
            // 1 <= arr[i]
            int maxValue = 0;
            // right
            for (int j = i + 1; j < arr.length; j++) {
                maxValue = Math.max(maxValue, arr[j]);
            }
            // Replace
            arr[i] = maxValue;
        }
        
        // Assign -1 to the last elem.
        arr[arr.length - 1] = -1;
        
        return arr;
    }
}
```

### other solution
```java
public int[] replaceElements(int[] arr) {
    for (int i = arr.length - 1, max = -1; i >= 0; --i) {
        int tmp = arr[i];
        arr[i] = max;
        max = Math.max(max, tmp);
    }
    return arr;
}
```
- Scan from right to left.
