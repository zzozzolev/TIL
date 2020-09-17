### 소모 시간
- 49분 48초

### 통과율
- 54%

### 문제점
- 나중에 있는 인덱스를 우선 취하는 전략을 택했는데 꼭 나중에 있다고 해서 minimum은 아니다.
- 시작 지점을 하나씩 옮기면 `O(n^2)`이 나올 거라 생각해서 인덱스를 직접 옮기는 방법으로 풀지 않았는데 이게 잘못된 것 같다.

### my solution
```
from collections import defaultdict
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t) or set(t).intersection(set(s)) != set(t):
            return ""
        else:
            idx_dic = defaultdict(list)
            char_id = 0
            for i,c in enumerate(s):
                if c in t:
                    idx_dic[c].append(i)
            
            min_idx = len(s) + 1
            max_idx = -1
            t = list(t)
            for c in idx_dic:
                for idx in reversed(idx_dic[c]):
                    if c in t:
                        t.remove(c)
                        if idx < min_idx:
                            min_idx = idx
                        if idx > max_idx:
                            max_idx = idx
            return s[min_idx:max_idx+1]
```

### other solution
- https://leetcode.com/problems/minimum-window-substring/solution/
```
def minWindow(self, s, t):
    """
    :type s: str
    :type t: str
    :rtype: str
    """
    if not t or not s:
        return ""

    dict_t = Counter(t)

    required = len(dict_t)

    # Filter all the characters from s into a new list along with their index.
    # The filtering criteria is that the character should be present in t.
    filtered_s = []
    for i, char in enumerate(s):
        if char in dict_t:
            filtered_s.append((i, char))

    l, r = 0, 0
    formed = 0
    window_counts = {}

    ans = float("inf"), None, None

    # Look for the characters only in the filtered list instead of entire s. This helps to reduce our search.
    # Hence, we follow the sliding window approach on as small list.
    while r < len(filtered_s):
        character = filtered_s[r][1]
        window_counts[character] = window_counts.get(character, 0) + 1

        if window_counts[character] == dict_t[character]:
            formed += 1

        # If the current window has all the characters in desired frequencies i.e. t is present in the window
        while l <= r and formed == required:
            character = filtered_s[l][1]

            # Save the smallest window until now.
            end = filtered_s[r][0]
            start = filtered_s[l][0]
            if end - start + 1 < ans[0]:
                ans = (end - start + 1, start, end)

            window_counts[character] -= 1
            if window_counts[character] < dict_t[character]:
                formed -= 1
            l += 1    

        r += 1    
    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]
```