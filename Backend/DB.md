# 헷갈리는 것들

## 트랜잭션의 Isolation Level이 READ COMMITED일 때, 왜 커밋되지 않은 업데이트를 읽을 수 있을까?
### 상황
- Spring 테스트 클래스에 `@Transactional`을 추가해주면 변경 사항을 커밋하지 않고 롤백해줬다.
- DB는 H2를 사용했고 디폴트 Isolation Level이 READ COMMITED 였다.
- 테스트 케이스에서는 DB에 row를 insert하고 select로 읽어와 검증을 했다.
  - 구체적으로는 회원가입을 검증하는 테스트 케이스 였다.
  - 회원 정보를 insert하고 select로 해당 회원 정보를 읽어왔다.

### 질문
- 커밋하지 않았는데 어떻게 해당 트랜잭션은 insert한 row를 읽을 수 있을까?

### 대답
- READ COMMITED라면 insert된 row는 해당 연산을 수행했던 트랜잭션에게만 visible 하다. 다른 트랜잭션들은 not visible하다.
- 즉, READ COMMITED가 연산을 수행한 트랜잭션을 기준으로 한 게 아니라 다른 트랜잭션을 기준으로 한 것이다.
- 다른 트랜잭션은 Undo 영역에 백업된 레코드에서 값을 가져온다고 한다. 아래 참고에서 Database-Transaction-isolation의 그림을 보면 이해가 된다.

### 참고
- https://stackoverflow.com/questions/58201324/h2-transactions-always-automatically-commit-why
- https://nesoy.github.io/articles/2019-05/Database-Transaction-isolation