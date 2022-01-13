### 소모 시간
- 27분 8초

### 통과율
- 100%

### 접근법
- 알파벳의 자리수가 높아질 때 `26^(자리수) * (알파벳)`인 것을 이용한다.

## my solution
```java
class Solution {
    public int titleToNumber(String columnTitle) {
        Map<Character, Integer> alphaToNum = new HashMap<>();
        
        int num = 0;
        for (char c = 'A'; c <= 'Z'; ++c) {
            alphaToNum.put(c, ++num);
        }
        
        int answer = 0;
        int base = 26;
        for (int i = 0; i < columnTitle.length() - 1; ++i) {
            int b = columnTitle.length() - 1 - i;
            answer += Math.pow(base, b) * alphaToNum.get(columnTitle.charAt(i));
        }
        
        // 일의 자리
        char lastChar = columnTitle.charAt(columnTitle.length() - 1);
        answer += alphaToNum.get(lastChar);
       
        return answer;
    }
}
```
