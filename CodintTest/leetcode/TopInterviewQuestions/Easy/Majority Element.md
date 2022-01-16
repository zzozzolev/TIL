### 소모 시간
- 9분 40초

### 통과율
- 100%

### 접근법
- `O(N)`으로 풀기 위해 솔팅을 사용하지 않았다.
- `nums`를 반복문으로 한 번 돌면서 엘리먼트 개수를 카운트하고 최대 카운트를 얻는다.
- value가 최대 카운트인 element를 반환한다.

### my solution
```java
class Solution {
    public int majorityElement(int[] nums) {
        Map<Integer, Integer> numToCount = new HashMap<>();
        
        int max = 0;
        for (int num : nums) {
            // 초기화
            if (!numToCount.containsKey(num))
                numToCount.put(num, 0);
            
            numToCount.put(num, numToCount.get(num) + 1);
            
            max = Math.max(max, numToCount.get(num));
        }
        
        int answer = -1;
        for (Map.Entry<Integer, Integer> elem : numToCount.entrySet()) {
            if (elem.getValue() == max) {
                answer = elem.getKey();
                break;
            }
                
        }
        return answer;
    }
}
```

### other solution
- https://leetcode.com/problems/majority-element/discuss/51613/O(n)-time-O(1)-space-fastest-solution
```java
public class Solution {
    public int majorityElement(int[] num) {

        int major=num[0], count = 1;
        for(int i=1; i<num.length;i++){
            if(count==0){
                count++;
                major=num[i];
            }else if(major==num[i]){
                count++;
            }else count--;
            
        }
        return major;
    }
}
```
- 반드시 어레이에서 과반 이상 있으니 위와 같은 방식으로 계산하면 최대 개수 엘리먼트가 `major`에 저장되는 걸 가정하는 것 같다.
