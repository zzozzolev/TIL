### 소모 시간
- 18분 25초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int firstUniqChar(String s) {
        Map<Character, List<Integer>> charToInx = new HashMap<>();

        // Put char indices.
        for (int i = 0; i < s.length(); i ++) {
            Character c = s.charAt(i);
            if (!charToInx.containsKey(c)) {
                charToInx.put(c, new ArrayList<>(List.of(i)));
            }
            else {
                List<Integer> value = charToInx.get(c);
                value.add(i);
            }
        }

        int answer = Integer.MAX_VALUE;
        for (Map.Entry<Character, List<Integer>> entry : charToInx.entrySet()) {
            List<Integer> value = entry.getValue();
            if (value.size() == 1) {
                if (value.get(0) < answer)
                    answer = value.get(0);
            }
        }

        return (answer == Integer.MAX_VALUE) ? -1 : answer;
    }
}
```

### Other Solution
- https://leetcode.com/problems/first-unique-character-in-a-string/solutions/203359/first-unique-character-in-a-string/?orderBy=hot
```java
class Solution {
    public int firstUniqChar(String s) {
        HashMap<Character, Integer> count = new HashMap<Character, Integer>();
        int n = s.length();
        // build hash map : character and how often it appears
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            count.put(c, count.getOrDefault(c, 0) + 1);
        }
        
        // find the index
        for (int i = 0; i < n; i++) {
            if (count.get(s.charAt(i)) == 1) 
                return i;
        }
        return -1;
    }
}
```
