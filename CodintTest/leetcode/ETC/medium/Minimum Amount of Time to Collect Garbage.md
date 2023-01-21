### 소모 시간
- 55분 3초

### 통과율
- 100%

### 문제 분석
- garbage의 마지막 인덱스를 알아내는 게 키포인트.
- 마지막 인덱스까지만 이동 거리를 더해주면 됨.

### My Solution
```java
class Solution {
    public int garbageCollection(String[] garbage, int[] travel) {
        char[] trucks = new char[] {'M', 'P', 'G'};

        int mins = 0;
        // Iterate by truck
        for (char type : trucks) {
            // Find last home
            int lastIdx = garbage.length; 
            for (int i = garbage.length - 1; i >= 0; i--) {
                if (garbage[i].indexOf(type) != -1) {
                    lastIdx = i;
                    break;
                }
            }

            // No garbage
            if (lastIdx == garbage.length)
                continue;

            // Iterate each garbage
            for (int i = 0; i < lastIdx + 1; i++) {
                int count = (int) garbage[i].chars().filter(ch -> ch == type).count();
                mins += count + (i == 0 ? 0 : travel[i - 1]);
            }
        }

        return mins;
    }
}
```

### Other Solution
```java
public int garbageCollection(String[] garbage, int[] travel) {
    // last size is the number of chars.
    int last[] = new int[128], res = 0;

    for (int i = 0; i < garbage.length; ++i) {
        res += garbage[i].length(); // 1 per unit.
        for (int j = 0; j < garbage[i].length(); ++j)
            last[garbage[i].charAt(j)] = i; // Store the last index.
    }

    // Get the prefix sum.
    for (int j = 1; j < travel.length; ++j)
        travel[j] += travel[j - 1];

    for (int c : "PGM".toCharArray())
        if (last[c] > 0)
            res += travel[last[c] - 1]; // Add travel distance.
    return res;
}
```
