### 소모 시간
- 14분 42초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int countConsistentStrings(String allowed, String[] words) {
        int answer = 0;
        for (String word : words) {
            boolean isNotInChar = false;
            for (char c : word.toCharArray()) {
                if (allowed.indexOf(c) == -1) {
                    isNotInChar = true;
                    break;
                }
            }
            if (!isNotInChar)
                answer += 1;
        }
        return answer;
    }
}
```

### Other Solution
- https://leetcode.com/problems/count-the-number-of-consistent-strings/solutions/969570/java-python-3-2-codes-bit-manipulation-and-1-liners-w-brief-explanation-and-analysis/
```java
public int countConsistentStrings(String allowed, String[] words) {
    return Arrays.stream(words)
                    .mapToInt(w -> w.chars().allMatch(c -> allowed.contains((char)c + "")) ? 1 : 0)
                    .sum();
}
```
- 자바 스트림의 함수들을 잘 이용하면 바로 끝나는 듯...
