## 영속성 컨텍스트의 이점
- 1차 캐시
  - `find` 했을 때, 1차 캐시에서 먼저 찾고 없으면 DB에서 조회해서 1차 캐시에 저장함.
  - 하지만 1차 캐시는 트랜잭션 단위로 만들기 때문에 큰 도움은 안 됨.
- 영속 엔티티의 동일성(identity) 보장
  - 1차 캐시로 repeatable read 등급의 트랜잭션 격리 수준을 애플리케이션 차원에서 제공함.
- 트랜잭션을 지원하는 쓰기 지연 (transactional write-behind)
  - 쓰기 지연 SQL 저장소에 INSERT SQL을 저장했다가 커밋하는 순간 데이터베이스에 INSERT SQL을 보냄. (flush + commit)
- 변경 감지 (Dirty Checking)
  - 1차 캐시에는 처음 값을 가져온 시점의 엔티티 스냅샷을 저장함.
  - 현재 엔티티 상태와 스냅샷을 비교해서 바꼈으면 쓰기 지연 SQL 저장소에 업데이트 쿼리를 만듦.
- 지연 로딩 (Lazy Loading)

## 플러시 발생
- 변경 감지.
- 수정된 엔티티를 쓰기 지연 SQL 저장소에 등록함.
- 쓰기 지연 SQL 저장소의 쿼리를 데이터베이스에 전송함.
- 커밋이랑 다름.
- 호출 방법
  - `em.flush()`: 직접 호출
  - 트랜잭션 커밋: 자동 호출
  - JPQL 쿼리 실행: 자동 호출
    - JPQL은 DB 쿼리를 실행하는 것이므로 DB에 반영이 안 된 상태라면 문제가 있을 수 있음.
- 영속성 컨텍스트를 비우지 않음.
- 영속성 컨텍스트의 변경 내용을 DB에 동기화.
- 트랜잭션이라는 작업 단위가 중요함.

## `@GeneratedValue`
### IDENTITY
- PK 생성을 DB에 위임함.
- 주로 MySQL, PostgreSQL, SQL Server에서 사용.
  - MySQL의 `AUTO_INCREMENT`
- JPA는 트랜잭션 커밋 시점에 INSERT SQL 실행함.
- `AUTO_INCREMENT`는 데이터베이스에 INSERT SQL을 실행한 이후에 ID 값을 알 수 있음.
- `IDENTITY` 전략은 `em.persiste()` 시점에 즉시 INSERT SQL 실행하고 DB에서 식별자를 조회함.

### SEQUENCE
- 유일한 값을 순서대로 생성하는 특별한 DB 오브젝트.
- 오라클, PostgreSQL, H2 데이터베이스에서 사용.

### TABLE 전략
- 키 생성 전용 테이블을 하나 만들어서 DB 시퀀스를 흉내내는 전략.
- 모든 DB에 적용 가능하지만 성능이 안 좋음.

## 권장하는 식별자 전략
- PK 제약 조건
  - not null
  - unique
  - 변하면 안 됨.
- 자연키 말고 대체키 사용해야함.
- 권장: Long + 대체키 + 키 생성 전략 사용
