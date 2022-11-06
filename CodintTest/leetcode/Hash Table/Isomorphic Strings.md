### 소모 시간
- 30분 30초

### 통과율
- 100%

### my solution
```java
class Solution {
    public boolean isIsomorphic(String s, String t) {
        List<List<Integer>> sVals = getSortedValues(s);
        List<List<Integer>> tVals = getSortedValues(t);
        
        return new HashSet(sVals).equals(new HashSet(tVals));
    }

    public List<List<Integer>> getSortedValues(String target) {
        Map<Character, List<Integer>> charToIdx = new HashMap<>();

        for (int i = 0; i < target.length(); i++) {
            if (!charToIdx.containsKey(target.charAt(i))) {
                List<Integer> indices = new ArrayList<Integer>(List.of(i));
                charToIdx.put(target.charAt(i), indices);
            }
            else {
                List<Integer> indices = charToIdx.get(target.charAt(i));
                indices.add(i);
            }
                
        }

        List<List<Integer>> values = new ArrayList<>(charToIdx.values());
        
        return values;
    }
}
```

### other solution
- https://leetcode.com/problems/isomorphic-strings/solutions/1261227/isomorphic-strings/
```java
class Solution {
    private String transformString(String s) {
        Map<Character, Integer> indexMapping = new HashMap<>();
        StringBuilder builder = new StringBuilder();
        
        for (int i = 0; i < s.length(); ++i) {
            char c1 = s.charAt(i);
            
            if (!indexMapping.containsKey(c1)) {
                indexMapping.put(c1, i);
            }
            
            builder.append(Integer.toString(indexMapping.get(c1)));
            builder.append(" ");
        }
        return builder.toString();
    }
    
    public boolean isIsomorphic(String s, String t) {
        return transformString(s).equals(transformString(t));
    }
}
```
- 그냥 인덱스로만 하면 `1 + 10` 과 `11 + 0`이 구분되지 않으니 공백을 넣는다.
