### 소모 시간
- 15분 45초

### 통과율
- 100%
- 하지만 Wrong Answer보고 고쳐서 100%임.

### my solution
```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        index = 0
        for i in range(len(haystack)):
            if haystack[i:i+len(needle)] == needle:
                return i
        
        return -1
```

### other solution
```java
public int strStr(String haystack, String needle) {
    // empty needle appears everywhere, first appears at 0 index
    if (needle.length() == 0)
        return 0;
    if (haystack.length() == 0)
        return -1;
    
    
    for (int i = 0; i < haystack.length(); i++) {
        // no enough places for needle after i
        if (i + needle.length() > haystack.length()) break;
        
        for (int j = 0; j < needle.length(); j++) {
            if (haystack.charAt(i+j) != needle.charAt(j))
                break;
            if (j == needle.length()-1)
                return i;
        }
    }
    
    return -1;
}
```