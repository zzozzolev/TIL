### 소모 시간
- 16분 47초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public String sortSentence(String s) {
        // Split by space
        String[] split = s.split(" ");
        String[] sentence = new String[split.length];

        // Get last index and store word at that index.
        for (String word : split) {
            int index = Character.getNumericValue(word.charAt(word.length() - 1));
            sentence[index - 1] = word.substring(0, word.length() - 1);
        }

        return String.join(" ", sentence);
    }
}
```
