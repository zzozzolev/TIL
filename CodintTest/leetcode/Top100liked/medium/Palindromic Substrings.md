# 소모 시간
- 44분 11초

# 통과율
- 100%

# 문제점
- 하나씩 위치를 이동할 때 window만큼 건너 뛰면서 시작해서 탐색하지 못하는 서브 스트링이 있었다.
- `left`, `right`를 구할 때 `s`가 아니라 `sub`로 해야되는데 `s`로 해버려서 이상하게 비교가 되고 있었다..

# my solution
```
class Solution:
    def countSubstrings(self, s: str) -> int:
        length = len(s)
        
        if length == 0:
            return 0
        
        if len(set(s)) == 1:
            return (length + 1) * length // 2
        
        answer = length
        for window in range(2, length + 1):
            # v
            for i in range(length):
                if len(s[i:i + window]) != window:
                    break
                sub = s[i:i + window]
                
                if window % 2 == 0:
                    left = sub[:window // 2]
                    right = sub[window//2:]
                else:
                    left = sub[:window // 2]
                    right = sub[window//2 + 1:]

                if left == right[::-1]:
                    answer += 1
        
        return answer
```

# other solution
- https://leetcode.com/problems/palindromic-substrings/discuss/105689/Java-solution-8-lines-extendPalindrome
```
public class Solution {
    int count = 0;
    
    public int countSubstrings(String s) {
        if (s == null || s.length() == 0) return 0;
        
        for (int i = 0; i < s.length(); i++) { // i is the mid point
            extendPalindrome(s, i, i); // odd length;
            extendPalindrome(s, i, i + 1); // even length
        }
        
        return count;
    }
    
    private void extendPalindrome(String s, int left, int right) {
        while (left >=0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            count++; left--; right++;
        }
    }
}
```
   