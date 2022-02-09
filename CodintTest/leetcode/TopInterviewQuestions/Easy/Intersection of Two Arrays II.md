### 소모 시간
- 37분

### 통과율
- 100%

### 문제점
- 쓸데없이 복잡한 것 같다.

### my solution
```java
class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        Set<Integer> set1 = getSet(nums1);
        Set<Integer> set2 = getSet(nums2);
        
        set1.retainAll(set2);
        
        Map<Integer, Long> count1 = getCount(nums1);
        Map<Integer, Long> count2 = getCount(nums2);
        
        List<Integer> result = new ArrayList<>();
        for (Integer num : set1) {
            long minCount = Math.min(count1.get(num), count2.get(num));
            for (long i = 0; i < minCount; i++) {
                result.add(num);
            }
        }
        
        int[] arrayResult = new int[result.size()];
        for (int i = 0; i < result.size(); i++)
            arrayResult[i] = result.get(i);
        
        return arrayResult;
    }
    
    private Set<Integer> getSet(int[] nums){
        Set<Integer> set = new HashSet<>();
        for (int num : nums) {
            set.add(num);
        }
        return set;
    }
    
    private Map<Integer, Long> getCount(int[] nums) {
        List<Integer> list = new ArrayList<>();
        
        for (int num : nums)
            list.add(num);
        
        return list.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
    }
}
```

### other solution
- https://leetcode.com/problems/intersection-of-two-arrays-ii/discuss/82241/AC-solution-using-Java-HashMap
```java
public class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
        ArrayList<Integer> result = new ArrayList<Integer>();
        for(int i = 0; i < nums1.length; i++)
        {
            if(map.containsKey(nums1[i])) map.put(nums1[i], map.get(nums1[i])+1);
            else map.put(nums1[i], 1);
        }
    
        for(int i = 0; i < nums2.length; i++)
        {
            if(map.containsKey(nums2[i]) && map.get(nums2[i]) > 0)
            {
                result.add(nums2[i]);
                map.put(nums2[i], map.get(nums2[i])-1);
            }
        }
    
       int[] r = new int[result.size()];
       for(int i = 0; i < result.size(); i++)
       {
           r[i] = result.get(i);
       }
    
       return r;
    }
}
```
- map에 하나의 어레이에 대한 카운트를 하고 다른 어레이를 순회하면서 값을 감소시키면 교집합을 겹치는 개수만큼 얻을 수 있다.
- map으로 카운트를 만들고 다른 어레이를 순회할 때, 값이 양수라면 `nums1`에 카운트가 더 많은 것이고 값이 음수라면 `nums2`에 카운트가 더 많은 것이다.
