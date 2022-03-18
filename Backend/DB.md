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
- index에 있는 것만 select 하면 heap에서 가져오지 않음.
- MySQL은 pk를 모든 index마다 가지고 있어서 pk로 만든 index가 아니더라도 pk를 select 하는 게 느리지 않음.
- 표현식에 대해서는 index를 이용할 수 없음.
- 인덱스가 있다고 항상 쓰는 게 아니라 플래닝에 따라서 달라짐.
- `order by`도 역시 index가 있는 거에 해야 빠름.

### composite index
- composite index에서 첫번째 이후에 대해서만 `where`에 조건으로 추가하면 index를 사용하지 못함.
  - 예를 들어, `(a, b)` index가 있고 `where b = 100`이라면 index를 사용하지 못함.
- 여러 컬럼에 `and`로 조건을 걸어야 한다면, 각각에 대해 index를 만드는 것보다 composite로 하는 게 훨씬 빠름.
  - 예를 들어, `(a)`, `(b)`로 index를 만드는 것보다 `(a, b)`로 index를 만드는 게 `where a = 1 and b = 3`에서 더 빠름.
- 단, 여러 컬럼에 `or`로 조건을 걸어야 한다면, index를 사용할 수 없음. 
- 첫번째 이후의 컬럼에 index가 걸려있다면 composite index와 해당 index를 모두 사용함.
  - 예를 들어, `(a, b)`, `(b)` index가 있다면 `where a = 100 or b = 3`에서 `a`에 대해서는 `(a, b)` index를 `b`에 대해서는 `(b)` index를 사용함.

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
- table과도 별개의 자료구조임.
- 무언가를 빠르게 찾기 위해 사용됨.
- 하나 이상의 컬럼을 사용해서 만들 수 있음.
- heap에 있는 모든 페이지를 스캔하기보다는 heap에서 어떤 페이지를 fetch 해야하는지 정확히 알려줌.
- index도 pages에 저장되고 index 엔트리를 가져오기 위해 IO가 필요함.
- index가 작을 수록 메모리에 더 많이 올릴 수 있고 검색이 더 빨라짐.
- MySQL InnoDB는 항상 pk(clustered index)를 가지고 다른 index들은 pk의 값을 가리킴.
- Postgres는 secondary index들만 가지고 모든 index들은 heap내에 있는 row_id를 가리킴.

## Row-Oriented vs Column-Oriented Database
### Row-Oriented Database
- 테이블들이 디스크에 row로 저장돼있음.
- 한 번의 block IO로 여러 개의 row들과 row의 모든 컬럼들을 읽음.
- block에 row의 모든 컬럼이 있기 때문에 모든 컬럼을 얻는 비용이 비싸지 않음.
- 컬럼 하나가 필요해도 row의 모든 컬럼을 읽어야 됨.
- r/w에 최적화.
- OLTP(Online Transaction Processing)
- aggregation이 효과적이지 않음.
- 여러 컬럼에 걸친 쿼리에 효과적.

### Column-Oriented Database
- 테이블들이 디스크에 column으로 저장돼있음.
- 한 번의 block IO로 여러 개의 row들과 여러 개의 컬럼들을 읽음.
- 블록 하나에 더 많은 컬럼들을 저장함.
- 주어진 컬럼을 얻기 위해서 적은 IO를 사용하지만, 여러 컬럼들을 얻기 위해 더 많은 IO를 사용해야함.
- 각 컬럼이 row_id를 저장하고 있음.
- 단, row를 업데이트 하거나 삭제하면 row의 컬럼을 저장하고 있는 모든 블록의 내용을 지워야함.
- 일부 컬럼에 aggregate할 때 특히 좋음.
- 단, row의 모든 컬럼에 접근할 때 굉장히 좋지 않음.
- 쓰기가 느림.
- OLAP(Online Analytical Processing)
- aggregation에 효과적
- 여러 컬럼에 걸친 쿼리에 효과적이지 않음.

## PK vs Secondary Key
### PK
- 클러스터링은 해당 키를 중심으로 테이블을 구성하는 것임.
- clustered index를 구성하려면 pk 기준으로 순서가 유지돼야함.
- 예를 들어 pk가 id이고 id 1인 row가 들어오고 id 8인 row가 들어왔다면, 둘은 같은 페이지에 있지 않음. id 2 ~ 7의 자리를 비워둠.
- index에서 찾으면 바로 데이터가 있음.

### Secondary Key
- secondary key를 key를 중심으로 순서가 유지돼있지 않음.
- index에서 찾으면 바로 데이터가 있지 않고 데이터에 대한 포인터가 있음.
- 그래서 index에서 찾고 heap에서 다시 한 번 더 찾아야됨.

## index scan vs index only scan
- postgres term인 듯.
### index scan
- index를 타서 빠르게 찾았지만 table을 다시 한 번 뒤져서 원하는 컬럼을 가져와야함.

### index only scan
- index를 타서 빠르게 찾았고 index에 필요한 컬럼이 있어서 table을 다시 뒤질 필요가 없음.
- key 컬럼은 검색에 이용되는 것이고 non-key 컬럼은 fetch에 이용되는 것임.
- non-key 컬럼은 검색에 이용되지 않음.
- 단, index 사이즈가 너무 커지면 쿼리 속도가 느려짐. 더 많은 페이지들은 fetch 해야하기 때문임.

## 옵티마이저가 인덱스를 사용하는 방법
### 가정
- a, b 컬럼에 대해 각각 a_index, b_index가 존재함.

### 두 index의 검색 결과가 적당히 있는 경우
- a_index와 b_index를 모두 사용해 각각에 대해서 결과를 얻음.
- intersection 적용함.

### 한 index의 결과보다 다른 index 결과가 훨씬 많은 경우
- 더 적은 쪽의 index만 사용하고 다른 index는 사용하지 않음.
- table에서 해당 index로 얻은 row들이 조건에 맞는지 필터링함.

### index를 사용하지 않는 경우
- 반환 되는 row들이 너무 많아서 full table scan이 더 빠를 것이라고 판단함.
- row가 얼마 안 됐을 때 쿼리를 날리다가 배치로 확 넣어서 쿼리를 날리면 full table scan이 일어날 수 있음.

### 기타
- 데이터 베이스를 신뢰하지 않는다면 hint로 특정 index를 사용하도록 만들 수 있음.

## Bitmap Index Scan
- index에서 row를 찾고 바로 table로 가지 않음.
- 모든 index에서 검색하는 동안 검색한 값을 bitmap에 기록해둠.
  - ex) `[0, 0, 0, 0]` 이런 bitmap이 있을 때 첫번째 row를 찾아다면 `[0, 1, 0, 0]`으로 표시
- table에서 row를 꺼낼 때 해당 page에 조건을 만족하지 않는 row도 있음. 그래서 recheck해서 해당 row들을 제거함.
- and 조건일 경우 BitmapAnd 수행해서 모두 1인 것만 결과로 나오게 함.

## Bloom Filter
- 데이터의 양이 굉장히 많은 경우 특정 원소가 있는지 없는지 검사하는 것은 비용이 많이 듦.
- 그렇다고 캐쉬를 사용한 건 또 그만큼의 복잡도가 증가함.
- 이때 사용할 수 있는 게 Bloom Filter임.
- 특정 원소가 데이터에 존재하는지 검사하는데 사용할 수 있는 자료 구조.
- 원소를 hash해서 저장함.
- 따라서 다른 원소가 같은 해쉬 값을 가지는 collision에 의해 없는 원소를 있다고 할 수 있지만, 있는 원소를 없다고는 하지 않음.

## B-Tree vs B+Tree
### B-Tree
- 모든 노드에서 키와 밸류를 저장 -> 더 많은 공간 차지 -> 더 많은 IO 필요 -> 탐색이 느려짐
- 랜덤 액세스때문에 레인지 쿼리가 느림. 해당하는 값을 찾기 위해 불필요한 탐색도 이루어짐.
- 노드를 메모리에 올리는 게 어려워짐. 특히 pk가 UUID, string이면 더욱 어려움.

### B+Tree
- B-Tree랑 같지만 인터널 노드에 키만 저장함 -> 더 적은 공간 차지 -> 더 적은 IO 필요
- 밸류는 리프 노드에 저장함. 대신, 키가 중복될 수 있음.
- 인터널 노드가 차지하는 용량이 적다보니 페이지 하나에 더 많은 엘리먼트가 들어감.
- 리프 노드가 서로 연결돼있기 때문에 키를 찾으면 해당 키의 전후 값을 찾을 수 있음.
- 한 페이지에 여러 개의 리프 노드가 저장됨.

## B+Tree & DBMS Considerations
- 리프 포인터 비용은 쌈.
- 노드 하나는 하나의 DBMS 페이지에 맞음.
- 빠른 탐색을 위해 인터널 노드를 메모리에 쉽게 올릴 수 있음.
- 리프 노들들은 힙의 데이터 파일에 있을 수 있음.

## Storage Cost in Postgres vs MySQL
- B+Tree secondary index 값은 바로 튜플(포인터)을 가리킬 수도 있고 (Postgres) 혹은 pk를 가리킬 수도 있음 (MySQL)
- pk를 UUID로 하면 clustered index에서 randomness 때문에 insert 비용이 비쌈. 또한 모든 secondary index에서 가리키니 비용이 더 비쌈. (MySQL)
- MySQL은 clustered index이기 때문에 리프 노드들은 모든 로우를 포함한다.
