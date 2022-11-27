### 소모 시간
- 25분 13초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public boolean isValid(String s) {
        char[] chars = s.toCharArray();
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : chars) {
            if (c == '(' || c == '{' || c == '[') {
                stack.addFirst(c);
            }
            else {
                // Open brackets is needed.
                if (stack.isEmpty()) {
                    return false;
                }
                
                Character stackChar = stack.removeFirst();
                if (stackChar.equals('(') && c != ')' || stackChar.equals('{') && c != '}' || stackChar.equals('[') && c != ']')
                    return false;
            }
        }
        return stack.isEmpty();
    }
}
```

### Other Solution
```java
public boolean isValid(String s) {
	Stack<Character> stack = new Stack<Character>();
	for (char c : s.toCharArray()) {
		if (c == '(')
			stack.push(')');
		else if (c == '{')
			stack.push('}');
		else if (c == '[')
			stack.push(']');
		else if (stack.isEmpty() || stack.pop() != c)
			return false;
	}
	return stack.isEmpty();
}
```
- Open일 때 그대로 넣는게 아니라 Close를 넣는다.
- Close일 때 같은지 비교하면 훨씬 간단하게 비교할 수 있다.
