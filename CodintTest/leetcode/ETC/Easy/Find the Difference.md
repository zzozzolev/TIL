### 소모 시간
- 17분

### 통과율
- 100%

### My Solution
```java
class Solution {
    public char findTheDifference(String s, String t) {
        String sortedS = sortStr(s);
        String sortedT = sortStr(t);

        for (int i = 0; i < s.length(); i++) {
            if (sortedS.charAt(i) != (sortedT.charAt(i))) {
                return sortedT.charAt(i);
            }
        }
        return sortedT.charAt(t.length() - 1);
    }

    public String sortStr(String str) {
        char[] chars = str.toCharArray();
        Arrays.sort(chars);
        return String.valueOf(chars);
    }
}
```
