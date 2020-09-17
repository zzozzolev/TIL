### 소모 시간
- 54분

### 통과율
- 0%(영점 몇 퍼 통과했는데 안 한 거랑 마찬가지이지 ^^...)

### 문제점
- 좀 더 일반적으로 짜야하는데 새로운 케이스 나올때마다 다 걸려버린다.
- 로직이 더럽다.
- DP인 걸 전혀 생각하지 못했다.

### my solution
```
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        if len(p) == 0:
            return len(s) == 0
        
        if len(s) == 0:
            return set(p).pop() == "*"
        
        if "*" not in p:
            if len(s) != len(p):
                return False
            if "?" in p:
                for s_c, p_c in zip(s, p):
                    if p_c == "?":
                        continue
                    if s_c != p_c:
                        return False
                return True
            else:
                return s == p
        # "*" in p
        else:
            for i in range(len(p)-1):
                if p[i] == "*":
                    if p[i+1] == "?" and len(s) > 1:
                        continue
                    elif p[i+1] == "*":
                        continue
                    else:
                        if "?" in p[i+1:]:
                            ex_idx = (i+1) + p[i+1:].index("?")
                        elif "*" in p[i+1:]:
                            ex_idx = (i+1) + p[i+1:].index("*")
                        else:
                            ex_idx = len(p)
                        
                        target_patt = p[i+1:ex_idx]
                        while len(target_patt) > 0:
                            if target_patt in s:
                                target_idx = s.index(target_patt)
                                s = s[target_idx:]
                                break
                            else:
                                target_patt = target_patt[:-1]
                        
                        if len(target_patt) == 0:
                            return False
                                
                else:
                    if p[i] == "?":
                        if len(s) == 0:
                            return False
                    else:
                        if s[0] != p[i]:
                            return False
                    s = s[1:]
            # 끝처리
            if p[-1] != "*":
                if p[-1] == "?":
                    if len(s) == 0:
                        return False
                else:
                    if p[-1] != s[0]:
                        return False
                
            return True
```

### other solution
- https://leetcode.com/problems/wildcard-matching/discuss/17845/Python-DP-solution
```
def isMatch(s, p):
    length = len(s)
    if len(p) - p.count('*') > length:
        return False
    dp = [True] + [False]*length
    for i in p:
        if i != '*':
            for n in reversed(range(length)):
                # dp[n+1]에 dp[n]까지 맞았는지 저장
                dp[n+1] = dp[n] and (i == s[n] or i == '?')
        else:
            for n in range(1, length+1):
                # '*'인 경우 이전까지만 맞았으면 상관없음
                # dp[n]이 있는 이유는 dp[0] == False인 경우를 핸들링하기 위함인 듯.
                dp[n] = dp[n-1] or dp[n]
        # 첫 글자가 안 맞는 경우 이걸로 체크
        dp[0] = dp[0] and i == '*'
    return dp[-1]
```