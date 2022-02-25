## Tracking Modes
- 서버가 처음에는 브라우저의 쿠키 지원 여부를 판단하지 못하므로 쿠키와 URL에 `jessionid`도 함께 전달한다.
- URL 전달 방식을 끄고 항상 쿠키를 통해서만 세션을 유지하고 싶다면 다음과 같이 하면 된다.
```yaml
server:
    servlet:
        session:
            tracking-modes: cookie
```
