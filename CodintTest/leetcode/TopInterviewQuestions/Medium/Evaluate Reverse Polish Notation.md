### 소모 시간
- 24분 12초

### 통과율
- 100%

### 문제점
- switch에서 break를 안해서 값이 이상하게 됐다.
- stack이므로 피연산자 순서가 반대인데 처음에 이를 고려하지 않았다.

### my solution
```java
class Solution {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String token : tokens) {
            if (token.equals("+")
                || token.equals("-")
                || token.equals("*")
                || token.equals("/")) {
                Integer o2 = stack.pop();
                Integer o1 = stack.pop();
                
                Integer result = null;
                switch (token) {
                    case "+":
                        result = o1 + o2;
                        break;
                    case "-":
                        result = o1 - o2;
                        break;
                    case "*":
                        result = o1 * o2;
                        break;
                    case "/":
                        result = (int)(o1 / o2);
                        break;
                    default:
                        break;
                }
                stack.push(result);
            }
            
            // Number
            else {
                stack.push(Integer.parseInt(token));
            }
        }
        
        return stack.pop().intValue();
    }
}
```

---

### 소모 시간
- 17분 29초

### 통과율
- 100%

### 접근법
- stack에 operand인 경우 push하고 operator인 경우 pop을 두 번 수행해 두 번째, 첫 번째 operand를 얻어내 연산을 한다.

### 문제점
- 나누기를 버림으로 해야되는데 //로 해서 내림으로 했더니 결과가 -일 때 잘못 나왔다.

### my solution
```
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operators = ["+", "-", "*", "/"]
        for t in tokens:
            if t in operators:
                second = int(stack.pop())
                first = int(stack.pop())
                
                if t == "+":
                    result = first + second
                elif t == "-":
                    result = first - second
                elif t == "*":
                    result = first * second
                else:
                    result = int(first / second)
                
                stack.append(result)
                
            else:
                stack.append(t)
        
        return stack[-1]
```
