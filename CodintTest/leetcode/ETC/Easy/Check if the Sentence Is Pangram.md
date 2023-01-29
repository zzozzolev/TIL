### 소모 시간
- 5분 39초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public boolean checkIfPangram(String sentence) {
        int numAlphabets = ('z' - 'a') + 1;
        boolean[] isPresent = new boolean[numAlphabets];
        
        // Set true for present char.
        for (char c : sentence.toCharArray()) {
            isPresent[c - 'a'] = true;
        }

        for (boolean flag : isPresent) {
            if (!flag)
                return false;
        }

        return true;
    }
}
```

### Other Solution
- https://leetcode.com/problems/check-if-the-sentence-is-pangram/solutions/1164047/java-c-python-set-solution/?orderBy=most_votes
```java
    public boolean checkIfPangram(String sentence) {
        Set<Character> s = new HashSet<>();
        for (int i = 0; i < sentence.length(); ++i)
            s.add(sentence.charAt(i));
        return s.size() == 26;
    }
```
