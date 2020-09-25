### 소모 시간
- 1시간 10분

### 통과 여부
- pass

### 접근법
- k - 1, k, k + 1 제약이 있으므로 팰린드롬처럼 거리가 대칭을 이루도록 만든다.
- n^2 (n >= 2)일 때, `1, 2, ..., (n - 1), n, (n - 1), ..., 2, 1`의 거리로 가야되는 것을 이용한다.
- 시작 지점과 도착 지점의 차이가 3이하라면 차이만큼을 정답으로 추가한다.
- 그렇지 않은 경우, `base`를 2부터 시작해서 `base ** 2`이라면 `(base-1) * 2 + 1`을 정답으로 추가한다.
- 사이에 있다면 `(base + 1) ** 2`와 거리의 차이가 대칭인 값을 합친것보다 작을 동안 정답을 하나씩 뺀다. 루프가 끝나면 정답으로 추가한다. 
    - 시작이 `4`, 끝이 `9`이어서 차이가 `5`만큼 난다면 `1211` or `1121`이렇게 가야한다. 
    - `2 ** 2 < 5 < 3 ** 2` -> `base = 2` -> `base + 1 = 3` -> `12321` -> `9 - 5 = 4` -> `3` < `5` -> `1221` -> `7` > `5` 이므로 멈춤. 

### 문제점
- 아래 부분에서 계산하다가 실수가 났다.
- 다른 솔루션을 보니 그냥 인풋, 아웃풋 이런 거 다 적어두고 더 일반적인 규칙을 찾았으면 좀 더 쉽게 풀었을 것 같다.


### my solution
```
def main():
    n = int(input())
    answers = []
    for _ in range(n):
        start, end = list( map( int, input().split() ) )
        
        if end - start <= 3:
            answers.append(end-start)
        
        else:
            dist = end - start
            base = 2
            while True:
                if base ** 2 == dist:
                    answers.append( (base-1) * 2 + 1 )
                    break

                elif base ** 2 < dist < (base + 1) ** 2:
                    answer = base * 2 + 1
                    value = base + 1
                    diff = (base + 1) ** 2 - dist
                    cur = base + 1

                    while value <= diff:
                        answer -= 1
                        value += (cur - 1) * 2
                            
                    answers.append(answer)
                    break
                else:
                    base += 1
        
    for ans in answers:
        print(ans)
    
if __name__ == "__main__":
    main()
```

### other solution
- 출처: https://leedakyeong.tistory.com/entry/%EB%B0%B1%EC%A4%80-1011%EB%B2%88-Fly-me-to-the-Alpha-Centauri-in-python
- 코드2