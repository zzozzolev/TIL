### 소모 시간
- 9분 18초

### 통과 여부
- 100%

### 접근법
- `len(strs)`가 0이면 empty string을 반환한다.
- `strs`중 가장 짧은 길이를 얻는다.
- 가장 짧은 길이만큼의 range를 순회하면서 `strs`에 있는 모든 string의 `i`번째 char가 같은지 검사한다.
- 하나라도 다르다면 지금까지 저장한 정답을 반환한다.

### my solution
```
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return ""
        
        shortest_length = min([len(s) for s in strs])
        answer = ""
        for i in range(shortest_length):
            flag = True
            for j in range(len(strs)-1):
                if strs[j][i] != strs[j+1][i]:
                    flag = False
                    break
            
            if flag:
                answer += strs[-1][i]
            else:
                break
        
        return answer
```