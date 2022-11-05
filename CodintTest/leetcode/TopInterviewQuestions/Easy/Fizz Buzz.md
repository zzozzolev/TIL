### 소모 시간
- 5분 27초

### 통과율
- 100%

### my solution
```java
class Solution {
    public List<String> fizzBuzz(int n) {
        List<String> answer = new ArrayList<>();
        for (int i = 1; i < n + 1; i++) {
            if (i % 3 == 0 && i % 5 == 0)
                answer.add("FizzBuzz");
            else if (i % 3 == 0)
                answer.add("Fizz");
            else if (i % 5 == 0)
                answer.add("Buzz");
            else
                answer.add(Integer.toString(i));
        }
        return answer;
    }
}
```
