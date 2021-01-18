# 소모 시간
- 43분 47초

# 통과율
- 68%

# 문제점
- 여러 개가 중첩된 것을 처리하지 못했음.
- 코드가 너무 더러움.
- 다른 사람도 똑같이 스택썼는데 왜 제대로 풀지 못했을까...

# my solution
```
class Node:
    def __init__(self, k):
        self.k = k
        self.enc_str = ""
        self.suffix = ""
    
    def __repr__(self):
         return str(self.k) + self.enc_str
    
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []
        string = ""
        answer = ""
        num = ""
        for i, char in enumerate(s):
            # k
            if '0' <= char <= '9':
                num += char
                if i < len(s) - 1 and '0' <= s[i+1] <= '9':
                    continue
                
                if string != "":
                    stack[-1].enc_str = string
                    string = ""
                node = Node(int(num))
                stack.append(node)
                num = ""
            
            elif char == '[':
                if string != "":
                    answer += string
                    string = ""
                
            elif char == ']':
                if string != "":
                    stack[-1].enc_str = string
                popped = stack.pop()
                if len(stack) != 0:
                    stack[-1].suffix = popped.k * popped.enc_str
                else:
                    answer += popped.k * (popped.enc_str + popped.suffix)
                string = ""
                
            else:
                if len(stack) == 0:
                    answer += char
                else:
                    string += char
        
        return answer
```

# other solution
- https://leetcode.com/problems/decode-string/discuss/87662/Python-solution-using-stack
```
def stacky(s):
    """
    When we hit an open bracket, we know we have parsed k for the contents of the bracket, so 
    push (current_string, k) to the stack, so we can pop them on closing bracket to duplicate
    the enclosed string k times.
    """
    stack = []
    current_string = ""
    k = 0
    
    for char in s:
        if char == "[":
            # Just finished parsing this k, save current string and k for when we pop
            stack.append((current_string, k))
            # Reset current_string and k for this new frame
            current_string = ""
            k = 0
        elif char == "]":
            # We have completed this frame, get the last current_string and k from when the frame 
            # opened, which is the k we need to duplicate the current current_string by
            last_string, last_k = stack.pop(-1)
            current_string = last_string + last_k * current_string
        elif char.isdigit():
            k = k * 10 + int(char)
        else:
            current_string += char
    
    return current_string
```
- stack에 저장할 때 원래 string과 k를 저장하는 게 아니라 앞에 나왔던 string과 현재 k를 저장한다.
- 이렇게 하면 괄호가 중첩돼있는 경우 무난하게 처리할 수 있다.
- k가 앞의 자리수부터 나오므로 10씩 곱해주면 앞에서 나온수를 핸들링할 수 있다.