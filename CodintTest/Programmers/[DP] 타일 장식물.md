### 소요 시간
- 60분
    - 문제 이해: 9분
    - 코드 실행 및 채점: 40분
    - 코드 개선: 11분

### 통과율
- 100%

### 접근법

### 문제점
- 피보나치 이용하는 건 바로 알았지만 DP로 피보나치를 잘 짜지 못했다.
- 재귀로 짤 때 글로벌을 어떻게 처리할 지 모른다. -> [여기](https://shoark7.github.io/programming/algorithm/%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98-%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98%EC%9D%84-%ED%95%B4%EA%B2%B0%ED%95%98%EB%8A%94-5%EA%B0%80%EC%A7%80-%EB%B0%A9%EB%B2%95.html)를 참고해보니 fibo 함수 안에 재귀 함수를 정의하면 굳이 global을 쓰지 않아도 될 거 같다.
- for문을 이용해도 충분히 DP로 풀 수 있는데 `피보나치 == 재귀`로 고정시킨 거 같다.

### my solution
```
def solution(N):
    if N == 1:
        return 4
    
    prev, cur = fibonacci(N, {})
     
    return cur * 2 + (cur + prev) * 2

def fibonacci(n, fibo_answer):
    if n == 1:
        fibo_answer[1] = 1
        return 0, 1
    elif n == 2:
        fibo_answer[2] = 1
        return 1, 1
    
    answer = []
    for i in [n-2, n-1]:
        if i not in fibo_answer:
            _, used = fibonacci(i, fibo_answer)
            answer.append(used)
        else:
            answer.append(fibo_answer[i])
    
    fibo_answer[n] = sum(answer)
    
    return [fibo_answer[n-1], fibo_answer[n]]
```

### other solution
- https://geonlee.tistory.com/120 에서 가져옴.
```
def solution(N):
    # 첫번째, 두번째 초기화
    rad_array = [1,1]
    for i in range(2,N):
        rad_array.append(rad_array[-1] + rad_array[-2])
    answer = (rad_array[-2] + rad_array[-1]*2)*2
    return answer
```