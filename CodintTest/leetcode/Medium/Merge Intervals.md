### 소모 시간
- 25분 28초

### 통과 여부
- 100%

### 접근법
- 

### 문제점
- 새로운 리스트를 만들지 않고 기존 리스트를 pop해서 정답을 얻으려고 했는데 길이가 들쑥날쑥이어서 `list index out of range` 에러가 나서 났다. pop을 하면서 index를 이용하지 말아야겠다.
- `answer`의 마지막 원소가 아니라 `intervals[i]`로 비교해서 merge가 제대로 되지 않았다.
- `answer`를 굳이 pop을 안 하고 마지막에 원소만 수정했으면 됐을 것 같다.

### my solution
```
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) == 0:
            return []
        
        intervals.sort()
        answer = [intervals.pop(0)]
        for i in range(len(intervals)):
            if answer[-1][1] >= intervals[i][0]:
                popped = answer.pop()
                answer.append([popped[0], 
                               max(popped[1], intervals[i][1])])
            else:
                answer.append(intervals[i])

        return answer
```

### other solution
- 출처: https://leetcode.com/problems/merge-intervals/discuss/21227/7-lines-easy-Python
```
def merge(self, intervals):
    out = []
    for i in sorted(intervals, key=lambda i: i.start):
        if out and i.start <= out[-1].end:
            out[-1].end = max(out[-1].end, i.end)
        else:
            out += i,
    return out
```