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

## Implementaion of Isolation
- DBMS는 isolation level을 다르게 구현했음.
- pessimistic
  - ex: row level locks, table locks, page locks
  - 바꿀거니까 건드리지 마라 ㅇㅇ
  - 락 관리 비용이 비쌈. 특히 row level lock.
- optimistic
  - 락을 사용하지 않음.
  - 단지 변화가 있다면 트랜잭션이 실패함.
  - 유저가 재시도해야함.
- repeatable read는 row를 잠금. 하지만 row를 많이 읽는다면 비용이 비쌈.
- postgres는 이걸 snapshot으로 구현했음. 그래서 repeatable read에서 phantom read 현상이 나타나지 않음.
- isolation은 다른 트랜잭션에만 적용됨. 따라서 같은 트랜잭션 내에서는 적용이 안 됨.

## Consistency
### Consistency in data
- enforced by the referential integrity
- 예를 들면, fk의 count를 바탕으로 한 컬럼 값이 맞지 않거나 존재하지 않는 fk를 가리킬 때.
- eventual consistency 없음.

### Consistency in reads
- 트랜잭션이 커밋됐다고 다른 트랜잭션에 바로 해당 변화를 볼 수 있는 건 아님.
- 예를 들면, 마스터에 변경 사항을 커밋했다고 해서 레플리카에서 바로 업데이트된 값을 볼 수 있지 않음.
- inconsistent 하지만 언젠간 consistent 해질거라는 eventual consistency가 있음.
- eventual consistency는 NoSQL용이 아님.

## Durability
- 커밋된 트랜잭션들에 의해 만들어진 변화들은 non-volatile 스토리지에서 durable하게 유지돼야함.
### 테크닉
- WAL(Write ahead log): 변경 내용에 대한 로그를 디스크에 먼저 저장하고, 일정 정도가 쌓이면 데이터 블록으로 만들어서 기록함.
- Asynchronous snapshot: 쓰는 모든 것을 메모리에 비동기 백그라운드를 이용해 유지함.
- AOF(Append Only File): 모든 명령을 파일에 기록함.

### OS Cache
- OS에 쓰기 요청을 하면 보통 OS 캐쉬로 감.
- 트랜잭션이 성공했지만 OS 캐쉬에만 쓰였고 그때 머신이 크래쉬 된다면 해당 데이터를 잃게됨.
- 그래서 DB는 OS cache를 건너뛰고 디스크에 바로 쓸 것을 요청함.
- 속도가 느림.

## 테이블과 인덱스가 디스크에 저장되고 쿼리되는 방법
### Row_ID
- 시스템에서 유지됨.
- mysql-innoDB 같은 특정 DB에서븐 pk와 같지만 포스트그레스 같은 다른 db에서는 시스템 컬럼 row_id(tuple_id)를 가짐.

### Page
- row들이 저장되는 곳, 고정된 크기의 메모리 로케이션임.
  - Postgres 8KB, MySQL 16KB
- DB는 row 하나를 읽지 않음. 한 번의 IO로 하나의 페이지 이상을 읽고 해당 IO로 많은 row들을 얻음.
  - 예를 들어, page 하나에 세 개의 row가 들어간다면, page0는 row 1,2,3을 page1은 row 4,5,6을 가지고 있음.

### IO
- 가능한한 많이 줄여야 됨.
- IO는 하나의 row를 읽을 수 없음.

### Heap
- 데이터 테이블을 가리키는 여러 page들의 컬렉션. 
- 자신의 page들과 함께 테이블이 저장되는 자료 구조.
- 모든 데이터를 저장하는 곳.

### Index
- heap의 어디를 봐야하는지 가리키는 heap과 별개의 자료 구조.
- 무언가를 빠르게 찾기 위해 사용됨.
- 하나 이상의 컬럼을 사용해서 만들 수 있음.
- heap에 있는 모든 페이지를 스캔하기보다는 heap에서 어떤 페이지를 fetch 해야하는지 정확히 알려줌.
- index도 pages에 저장되고 index 엔트리를 가져오기 위해 IO가 필요함.
- index가 작을 수록 메모리에 더 많이 올릴 수 있고 검색이 더 빨라짐.
- MySQL InnoDB는 항상 pk(clustered index)를 가지고 다른 index들은 pk의 값을 가리킴.
- Postgres는 secondary index들만 가지고 모든 index들은 heap내에 있는 row_id를 가리킴.
