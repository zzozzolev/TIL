### 소모 시간
- 28분 35초

### 통과율
- 98%

### 접근법
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)랑 비슷하다고 생각했다.
- `range(len(heights))`를 이용해 left, right를 시작할 인덱스를 얻는다.
    - `left`와 `right`를 각각 `i`로 초기화한다.
    - `left`가 `1`보다 클 때까지 `heights[left-1]`이 `heights[i]`보다 크거나 같은지 검사한다. 
        - 만약 그렇다면 `left`를 1 감소 시킨다.
        - 그렇지 않다면 break 한다.
    - `right`도 `len(heights)-2`보다 작을 때까지 1씩 증가하면서 똑같은 과정을 반복한다.
    - 만약 `left`와 `right`가 `i`와 같다면 `heights[i]`를 정답과 비교하고 그렇지 않다면 `(r - l + 1) * heights[i]`를 비교해 더 큰 경우 정답으로 업데이트한다.

### 문제점
- 시간 초과에 걸렸다.
- left, right를 구하는 방식이 이상했다. 이거 때문에 좀 헤맸다. left가 조건을 만족하면 하나씩 left를 줄여나갔다. 하지만 문제는 그 줄인 left는 조건을 만족하지 않을 수 있기 때문에 width가 2가 더 나와버렸다. 예를 들면 `[2,1,5,6,2,3]`이면 `5`에서 자기 자신은 만족하기 때문에 left는 2에서 1이 되는데 1은 만족하지 않는다. 그래서 계산에 포함하거나 특정 조건을 만족하는 인덱스로 하는 경우 그 조건을 만족한 게 포함되도록 만들어야 겠다.

### my solution1
```
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        if not heights:
            return 0
        
        answer = 0
        for i in range(len(heights)):
            # 포함 인덱스
            l, r = i, i
            while l >= 1:
                if heights[l-1] >= heights[i]:
                    l -= 1
                else:
                    break
            
            while r <= len(heights)-2:
                if heights[r+1] >= heights[i]:
                    r += 1
                else:
                    break
            
            # handle l == r
            if l == i and r == i:
                if heights[i] > answer:
                    answer = heights[i]
            else:
                cur = (r - l + 1) * heights[i]
                if cur > answer:
                    answer = cur
        return answer
```

### my solution2
```
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        if not heights:
            return 0
        
        answer = 0
        for i in range(len(heights)):
            # 포함 인덱스
            l, r = i, i
            while -1 < l:
                if heights[l] >= heights[i]:
                    l -= 1
                else:
                    break
            
            while r < len(heights):
                if heights[r] >= heights[i]:
                    r += 1
                else:
                    break
            
            l += 1
            r -= 1
            
            # handle l == r
            if l == i and r == i:
                if heights[i] > answer:
                    answer = heights[i]
            else:
                cur = (r - l + 1) * heights[i]
                if cur > answer:
                    answer = cur
        return answer
```

### other solution
- 출처: https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28917/AC-Python-clean-solution-using-stack-76ms
```
def largestRectangleArea(self, height):
    height.append(0)
    stack = [-1]
    ans = 0
    for i in xrange(len(height)):
        while height[i] < height[stack[-1]]:
            h = height[stack.pop()]
            w = i - stack[-1] - 1
            ans = max(ans, h * w)
        stack.append(i)
    height.pop()
    return ans
```