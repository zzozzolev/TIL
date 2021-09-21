### 소모 시간
- 7분 26초

### 통과율
- 100%

### my solution
```
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        highest_altitude = 0
        cur = 0
        
        for g in gain:
            cur += g
            highest_altitude = max(cur, highest_altitude)
        
        return highest_altitude
```

### other solution
```
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        curr_alt=0
        max_alt=0
        for i in range(0,len(gain)):
            curr_alt+=gain[i]
            max_alt=max(max_alt,curr_alt)
        return max_alt
```