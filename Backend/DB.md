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

## index
- https://sddev.tistory.com/157
- https://jojoldu.tistory.com/243

### 카티널리티와 인덱스
- 중복도가 낮은, 즉 카디널리티가 높은 것에 인덱스를 걸어야한다.
- 왜냐하면 인덱스를 통해 많은 부분을 거를 수 있어야하기 때문이다.

## Isolation - Read phenomena
### Dirty reads
- 아직 커밋되거나 플러쉬되지 않은 변경될 수 있는 내용을 읽음.

### Non-repeatable reads
- 한 트랜잭션 안에서 같은 종류의 읽기 쿼리를 수행했을 때 다른 값이 나옴.
- TX2가 TX1이 데이터를 다시 읽기 전에 TX1이 읽는 데이터를 수정하고 커밋했다면 TX1은 두 번째 read에서 다른 값을 봄.

### Phantom reads
- 한 트랜잭션 안에서 같은 종류의 읽기 쿼리를 수행했을 때 다른 값이 나옴.
- TX2가 TX1이 데이터를 다시 읽기 전에 새로운 row를 추가하고 커밋했다면 TX1은 첫 번째 read에서 읽지 않았던 row의 값을 얻음.

### Lost updates
- 여러 트랜잭션이 동시에 같은 row를 수정해서 일부 트랜잭션의 업데이트 내용을 잃게됨.
- 같은 row에 대해 TX1이 먼저 업데이트하고 TX2가 그 다음에 업데이트 후 커밋을 했다면, TX1은 TX2가 업데이트한 내용을 보게 됨.

## Isolation Level
- https://en.wikipedia.org/wiki/Isolation_(database_systems)
  - 맨 아래에 표 있음.
### Read uncommitted
- Isolation 없음
- 트랜잭션이 다른 트랜잭션이 수정중인 것을 볼 수 있음.

### Read committed
- 트랜잭션내의 쿼리는 커밋된 변경 사항만 볼 수 있음.
- 보통 DB의 디폴트

### Repeatable Read
- 트랜잭션 동안 로우를 읽을 때 변하지 않은 채 유지될 수 있음.

### Snapshot
- 트랜잭션 내의 각각의 쿼리는 트랜잭션이 시작할 때까지 커밋된 변경사항만 볼 수 있음.

### Serializable
- 트랜잭션이 순차적으로 수행됨.
- 가장 느림.
