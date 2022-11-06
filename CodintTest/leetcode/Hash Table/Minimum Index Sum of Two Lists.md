### 소모 시간
- 36분 32초

### 통과율
- 100%

### my solution
```java
class Solution {
    public String[] findRestaurant(String[] list1, String[] list2) {
        Map<String, Integer> idxSum = new HashMap<>();

        // Get common elems.
        Set<String> common = new HashSet<>(List.of(list1));
        Set<String> list2Set = new HashSet<>(List.of(list2));
        common.retainAll(list2Set);

        if (common.size() == 0)
            return new String[0];

        // Put list1 elem idx
        for (int i = 0; i < list1.length; i++) {
            if (common.contains(list1[i]))
                idxSum.put(list1[i], i);
        }

        // Put list2 elem idx
        for (int i = 0; i < list2.length; i++) {
            if (common.contains(list2[i]))
                idxSum.put(list2[i], idxSum.get(list2[i]) + i);
        }

        // Sort by the sum of index.
        List<Map.Entry<String, Integer>> entries = new ArrayList<>(idxSum.entrySet());
        entries.sort(Map.Entry.comparingByValue());

        // Find min values.
        Integer minValue = entries.get(0).getValue();
        List<String> result = new ArrayList<String>(List.of(entries.get(0).getKey()));
        for (int i = 1; i < entries.size(); i++){
            if (entries.get(i).getValue().equals(minValue))
                result.add(entries.get(i).getKey());
        }

        return result.toArray(String[]::new);
    }
}
```

### other solution
- https://leetcode.com/problems/minimum-index-sum-of-two-lists/solutions/127548/minimum-index-sum-of-two-lists/
```java
public class Solution {
    public String[] findRestaurant(String[] list1, String[] list2) {
        HashMap < String, Integer > map = new HashMap < String, Integer > ();
        for (int i = 0; i < list1.length; i++)
            map.put(list1[i], i);
        List < String > res = new ArrayList < > ();
        int min_sum, sum = Integer.MAX_VALUE;
        for (int j = 0; j < list2.length && j <= min_sum; j++) {
            if (map.containsKey(list2[j])) {
                sum = j + map.get(list2[j]);
                if (sum < min_sum) {
                    res.clear();
                    res.add(list2[j]);
                    min_sum = sum;
                } else if (sum == min_sum)
                    res.add(list2[j]);
            }
        }
        return res.toArray(new String[res.size()]);
    }
}
```
- 결과에 min 값일 때만 넣으면 굳이 set으로 공통을 알 필요가 없음.
