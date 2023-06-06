## Session
- 같은 호스트에 여러 번 리퀘스트를 해도 기저의 TCP 커넥션은 재사용된다.
- `with`과 함께 사용하면 처리되지 않은 예외가 발생해도 세션이 닫히는 걸 보장한다.
  ```python
  with requests.Session() as s:
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
  ```
- `Session`을 사용하면 매 요청마다 커넥션을 만들지 않고 최초 1회에만 만들어 사용한다.

### Reference
- https://requests.readthedocs.io/en/latest/user/advanced/
- https://requests.readthedocs.io/en/latest/api/?highlight=Session#requests.Session
- https://asecurity.dev/entry/Python-HTTP-Keep-alive-%EB%A5%BC-%ED%86%B5%ED%95%9C-%EC%84%B1%EB%8A%A5-%ED%96%A5%EC%83%81
- https://asecurity.dev/entry/Python-HTTPAdapter-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9D%B8-Session-ConnectionPool-%EA%B4%80%EB%A6%AC