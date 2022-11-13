### 소모 시간
- 8분 20초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> group = new HashMap<>();

        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String sorted = String.valueOf(chars);

            if (!group.containsKey(sorted)) {
                group.put(sorted, new ArrayList<>(List.of(s)));
            }
            else {
                List<String> list = group.get(sorted);
                list.add(s);
            }
        }

        return new ArrayList<>(group.values());
    }
}
```

### Other Solution
- https://leetcode.com/problems/group-anagrams/solutions/19176/share-my-short-java-solution/?orderBy=most_votes
```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        if (strs == null || strs.length == 0) return new ArrayList<>();
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] ca = s.toCharArray();
            Arrays.sort(ca);
            String keyStr = String.valueOf(ca);
            if (!map.containsKey(keyStr)) map.put(keyStr, new ArrayList<>());
            map.get(keyStr).add(s);
        }
        return new ArrayList<>(map.values());
    }
}
```
