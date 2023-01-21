### 소모 시간
- 36분 13초

### 통과율
- 52%

### 문제 분석
- 제한된 포인트 개수.
- 포인트 간의 거리를 구해야 됨.
- circular라는 특성이 있음.

### My Solution
```java
class Solution {
    public int findMinDifference(List<String> timePoints) {
        List<Integer> clockwise = new ArrayList<>();
        List<Integer> countclockwise = new ArrayList<>();
        Integer FULL_MINS = 24 * 60;

        for (String s : timePoints) {            
            Integer cwMins = 0;
            Integer ccwMins = 0;
            
            String[] split = s.split(":");
            
            cwMins += Integer.valueOf(split[0]) * 60; // hours
            cwMins += Integer.valueOf(split[1]); // minutes
            
            ccwMins = (s.equals("00:00")) ? 0 : FULL_MINS - cwMins;
            
            clockwise.add(cwMins);
            countclockwise.add(ccwMins);
        }

        clockwise.sort(Comparator.naturalOrder());
        countclockwise.sort(Comparator.naturalOrder());

        return Math.min(clockwise.get(1) - clockwise.get(0), countclockwise.get(1) - countclockwise.get(0));
    }
}
```
- 반시계 방향이 고려가 안 됨.

### Other Solution
```java
public int findMinDifference(List<String> timePoints) {
        boolean[] mark = new boolean[24 * 60];
        int min = Integer.MAX_VALUE, max = Integer.MIN_VALUE;
        for(String time : timePoints){
            String[] t = time.split(":");
            int h = Integer.parseInt(t[0]);
            int m = Integer.parseInt(t[1]);
            if(mark[h * 60 + m]){
                return 0;
            }
            min = Math.min(min, h * 60 + m);
            max = Math.max(max, h * 60 + m);
            mark[h * 60 + m] = true;
        }
        int minDiff = Integer.MAX_VALUE, prev = 0;
        for(int i = min; i <= max; i++){   //set the range from min to max as an optimization.
            if(mark[i]){
                if(i == min){   
                    //the min and max is the special case, it looks like :
                    //0---min----max-----1440, so we have two directions to calculate the distance
                    minDiff = Math.min(minDiff, Math.min(max - min, 1440 - max + min));
                }else{
                    //normal case: just one direction.
                    minDiff = Math.min(minDiff, i - prev);
                }
                prev = i;
            }
        }
        return minDiff;
    }
```
- `00:00 ~ 23:59`까지 있기 때문에 최대 `24 * 60`개의 포인트가 있음.
- 최대, 최소에 대해서 반시계 방향을 고려해주면 됨. (`1440 - max + min`)
- 현재 인덱스에서 바로 이전을 뺀 게 최소임.
