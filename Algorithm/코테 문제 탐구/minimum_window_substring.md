# 문제
- leetcode 문제이다.
```
Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).
```

# 정리한 이유
- 이진 탐색 이런 거는 아니지만 종종 많이 나오는 left, right pointer를 이용해 O(n)으 시간으로 탐색 문제를 해결할 수 있다.

# 코드
- https://leetcode.com/problems/minimum-window-substring/solution/
- 위에 들어가보면 기본적인 접근 방법은 알 수 있다.
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

# 주목할 점
- 목표 카운트가 있어서 그걸 맞춰야 된다면 똑같이 dict로 만들어서 해당 key 값의 값이 목표 카운트랑 같은지 체크한다.
    ```
    if window_counts[character] == dict_t[character]:
        formed += 1
    ```
- 정답에서 요구하는 상태임을 확인하고 하나씩 줄여나간다. 그니까 변경은 나중에 해야한다.
    ```
    # Save the smallest window until now.
    end = filtered_s[r][0]
    start = filtered_s[l][0]
    if end - start + 1 < ans[0]:
        ans = (end - start + 1, start, end)

    window_counts[character] -= 1
    if window_counts[character] < dict_t[character]:
        formed -= 1
    l += 1
    ```

# Reference
- https://leetcode.com/problems/minimum-window-substring/solution/