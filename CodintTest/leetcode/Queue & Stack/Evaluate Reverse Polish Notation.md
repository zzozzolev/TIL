### 소모 시간
- 19분 12초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        
        for (String token : tokens) {
            if (token.length() > 1 && token.charAt(0) == '-'  || Character.isDigit(token.charAt(0)))
                stack.push(Integer.parseInt(token));
            else {
                int right = stack.pop();
                int left = stack.pop();
                
                int result;
                if (token.equals("+"))
                    result = left + right;
                else if (token.equals("-"))
                    result = left - right;
                else if (token.equals("*"))
                    result = left * right;
                else
                    result = left / right;
                
                stack.push(result);
            }
        }
        
        return stack.pop();
    }
}
```
- `else`로 숫자를 처리하면 굳이 복잡하게 할 필요 없음.

### Other Solution
- https://leetcode.com/explore/learn/card/queue-stack/230/usage-stack/1394/discuss/47430/Java-Accepted-Code:-Stack-implementation.
```java
public class Solution {
    public int evalRPN(String[] tokens) {
        int a,b;
		Stack<Integer> S = new Stack<Integer>();
		for (String s : tokens) {
			if(s.equals("+")) {
				S.add(S.pop()+S.pop());
			}
			else if(s.equals("/")) {
				b = S.pop();
				a = S.pop();
				S.add(a / b);
			}
			else if(s.equals("*")) {
				S.add(S.pop() * S.pop());
			}
			else if(s.equals("-")) {
				b = S.pop();
				a = S.pop();
				S.add(a - b);
			}
			else {
				S.add(Integer.parseInt(s));
			}
		}	
		return S.pop();
	}
}
```