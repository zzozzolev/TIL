### 소모 시간
- 7분 25초

### 통과율
- 100%

### My Solution 1
- for each 사용
```java
class Solution {
    public int countMatches(List<List<String>> items, String ruleKey, String ruleValue) {
        int idx = -1;
        if (ruleKey.equals("type"))
            idx = 0;
        else if (ruleKey.equals("color"))
            idx = 1;
        else
            idx = 2;

        int answer = 0;
        for (List<String> item: items) {
            if (item.get(idx).equals(ruleValue))
                answer += 1;
        }

        return answer;
    }
}
```

### My Solution 2
- lambda 사용
```java
class Solution {
    public int countMatches(List<List<String>> items, String ruleKey, String ruleValue) {
        return (int) items.stream()
            .filter(
                item -> item.get(ruleKey.equals("type") ? 0 : ruleKey.equals("color") ? 1 : 2)
                    .equals(ruleValue)
            ).count();
    }
}
```
