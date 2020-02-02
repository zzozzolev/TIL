### 소요 시간
- 50분
    - 문제 이해: 22분
    - 코드 작성: 14분
    - 테스트 케이스 성공: 9분
    - 포기하기 까지: 5분  

### 통과율
- 0%

### 접근법
- 인덱스를 1씩 증가시키며 numbers에 하나씩 - 곱해줌. 이때 sub의 인덱스를 1씩 증가시키면서 - 곱해줄 numbers 포함.
```
numbers: [1, 2, 3, 4, 5]

1, 2
1, 2, 3
1, 2, 3, 4
1, 2, 3, 4, 5

1, 3
1, 3, 4
1, 3, 4, 5

...

5
```

### 문제점
- 위와 같이 하면 인덱스가 떨어져 있는 경우가 포함되지 않음. ex) `[-1, -2, 3, 4, -5]`
- DFS/BFS 인데 조합과 비슷하게 접근함.

### 느낀 점
- 아래로 순차적으로 내려가는 이런 문제(DFS, BFS)가 나오면 재귀로 접근해보자.

### my solution
```
def solution(numbers, target):
    if sum(numbers) == target:
        return 1
    
    answer = 0
    # i는 외부 인덱스
    for i in range(len(numbers)):
        result = sum(numbers) - (2 * numbers[i])
        if result == target:
            answer += 1
    
        # 마지막 엘리멘트
        if i == len(numbers) - 1:
            break
                                    
        # j는 sub의 start 인덱스
        for j in range(i+1,len(numbers)):
            # j에서 1씩 증가
            for k in range(1,len(numbers)-j):
                result =  \
                - numbers[i] - sum(numbers[j:j+k]) + sum(numbers[j+k:])
                if result == target:
                    answer += 1
    
    return answer
```

### other solution
- https://ihatecucumber.tistory.com/54 에서 가져옴.
```
def dfs(idx, numbers, result, target):
    global answer
    if idx == len(numbers):
        if result == target:
            answer += 1
        return
    dfs(idx+1, numbers, result+numbers[idx], target)
    dfs(idx+1,numbers, result-numbers[idx], target)


answer = 0  
def solution(numbers, target):
    dfs(0, numbers, 0, target)
    return answer
```