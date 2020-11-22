### 소모 시간
- 43분 41초

### 통과율
- 77%

### 문제점
- 애초에 Time Limit Exceeded에 걸릴 거라고 생각했는데 짧은 인풋에도 걸려버렸다.
- 수정 전에 첫글자만 보고 무조건 더했는데 길이 때문에 에러가 났다. 문자열 다룰 때는 길이 조심...!

### my solution
```
from collections import defaultdict

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        first_letter = defaultdict(list)
        
        for w in wordDict:
            first_letter[w[0]].append(w)
        
        # 첫글자가 없는 경우
        if s[0] not in first_letter:
            return False
        
        words = [w for w in first_letter[s[0]] if len(w) <= len(s)]
        while len(words) != 0:
            new_words = []
            for word in words:
                if word == s:
                    return True
                else:
                    if len(word) == len(s):
                        continue
                    first = s[len(word):][0]
                    for added in first_letter[first]:
                        if len(word + added) > len(s):
                            continue
                        new_words.append(word + added)

            words = new_words  
```

### other solution
- 출처: https://leetcode.com/problems/word-break/discuss/43790/Java-implementation-using-DP-in-two-ways
```
public class Solution {
    public boolean wordBreak(String s, Set<String> dict) {
        
        boolean[] f = new boolean[s.length() + 1];
        
        f[0] = true;

        for(int i=1; i <= s.length(); i++){
            for(int j=0; j < i; j++){
                if(f[j] && dict.contains(s.substring(j, i))){
                    f[i] = true;
                    break;
                }
            }
        }
        
        return f[s.length()];
    }
}
```
- `f[i]` stands for whether `subarray(0, i)` can be segmented into words from the dictionary. So `f[0]` means whether `subarray(0, 0)` (which is an empty string) can be segmented, and of course the answer is yes.
- The default value for boolean array is false. Therefore we need to set `f[0]` to be true.