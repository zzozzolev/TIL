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

## 연관관계의 주인(Owner)
- 객체의 두 관계중 하나를 연관관계의 주인으로 지정.
- 연관관계의 주인만이 FK를 관리. (등록, 수정)
- **주인이 아닌 쪽은 읽기만 가능.**
- 주인은 `mappedBy` 속성 사용 X.
- 주인이 아니면 `mappedBy` 속성으로 주인 지정.

## 연관관계 주의점
- 연관관계의 주인에 값을 입력하지 않으면 업데이트 쿼리가 나가지 않아서 FK가 설정되지 않음.
- 연관관계의 주인이 아닌 곳에 값을 입력하지 않고 연관관계의 주인을 조회하면 1차 캐시에 있는 게 그대로 사용돼서 조회가 안 됨.
- 양방향 연관관계를 설정하는 편의 메서드를 생성해야함. setter로 하기보다는 별도 이름을 쓰는 게 좋음. 한 곳만 선언해야함.
  ```java
  public void changeTeam(Team team) {
    this.team = team;
    team.getMembers().add(this);
  }

  public void addMember(Member member) {
    member.setTeam(this);
    members.add(member);
  }
  ```
- 양방향 매핑시에 무한 루프 조심해야함.
  - `toString()`, lombok, json 생성 라이브러리

## 양방향 매핑 정리
- 단방향 매핑만으로도 이미 연관관계 매핑은 완료.
  - 처음에는 단방향 매핑으로 설계를 끝내야함.
- 양방향 매핑은 반대 방향으로 조회 기능이 추가된 것 뿐.
- JPQL에서 역방향으로 탐색할 일이 많음.
- 단방향 매핑을 잘 하고 양방향은 필요할 때 추가해도 됨.

## 일대일 정리
### 주 테이블에 외래 키
- 주 객체가 대상 객체의 참조를 가지는 것처럼 주 테이블에 외래 키를 두고 대상 테이블을 찾음.
- 객체지향 개발자 선호.
- JPA 매핑 편리.
- 장점: 주 테이블만 조회해도 대상 테이블에 데이터가 있는지 확인 가능.
- 단점: 값이 없으면 외래 키에 null 허용.

### 대상 테이블에 외래 키
- 대상 테이블에 외래 키가 존재.
- 전통적인 DB 개발자 선호.
- 장점: 주 테이블과 대상 테이블을 일대일에서 일대다 관계로 변경할 때 테이블 구조 유지.
- 단점: 프록시 기능의 한계로 지연 로딩으로 설정해도 항상 즉시 로딩됨.

## 상속 관계 매핑
### 조인 전략
- 정석. 비즈니스적으로 중요함.
- 장점
  - 테이블 정규화
  - 외래 키 참조 무결성 제약조건 활용가능
  - 저장공간 효율화
- 단점
  - 조회시 조인을 많이 사용 -> 성능 저하
  - 조회 쿼리가 복잡함
  - 데이터 저장시 INSERT SQL 2번 호출

### 단일 테이블 전략
- 단순하고 확장 가능성 없음.
- 장점
  - 조인이 필요 없으므로 일반적으로 조회 성능이 빠름.
  - 조회 쿼리가 단순함.
- 단점
  - 자식 엔티티가 매핑한 컬럼은 모두 null 허용.
  - 단일 테이블에 모든 것을 저장하므로 테이블이 커질 수 있어 상황에 따라서 조회 성능이 오히려 느려질 수 있음.

### 구현 클래스마다 테이블 전략
- 이 전략은 DB 설계자와 ORM 전문가 둘 다 추천하지 않음.
- 여러 자식 테이블을 함께 조회할 때 성능이 느림. (UNION ALL)
- 자식 테이블을 통합해서 쿼리하기 어려움.

## 프록시의 특징
- 프록시 객체는 처음 사용할 때 한 번만 초기화.
- 프록시 객체를 초기화 할 때, **프록시 객체가 실제 엔티티로 바뀌는 것은 아님.**
- 초기화되면 프록시 객체를 통해서 실제 엔티티에 접근 가능함.
- 프록시 객체는 원본 엔티티를 상속 받음.
- 따라서 타입 체크시 주의해야함. (instance of 사용해야함)
- 영속성 컨텍스트에 찾는 엔티티가 이미 있으면 `em.getReference()`를 호출해도 실제 엔티티를 반환함.
  - 동일한 영속성 컨텍스트에서 같은 PK를 가지면 JPA는 항상 같다고 해야함.
- 영속성 컨텍스트의 도움을 받을 수 없는 준영속 상태일 때, 프록시 초기화하면 문제 발생함.
  - ex: `em.clear()`, `em.detach()`
  - 트랜잭션과 영속성 컨텍스트의 라이프사이클이 같아서 트랜잭션이 끝난 뒤 레이지 초기화를 하려고 할 때 에러가 발생함.

## 고아 객체
- 고아 객체 제거: 부모 엔티티와 연관 관계가 끊어진 자식 엔티티를 자동으로 삭제함.
- `orphanRemoval = true`
- 자식 엔티티를 컬렉션에서 제거
  ```java
  Parent parent1 = em.find(Parent.class, id);
  parent1.getChildren().remove(0);

  // DELETE FROM CHILD WHERE ID = ?
  ```

## 영속성 전이 + 고아 객체, 생명 주기
- `CascadeType.ALL` + `orphanRemoval = true`
- 스스로 생명주기를 관리하는 엔티티는 `em.persist()`로 영속화, `em.remove()`로 제거.
- 두 옵션을 모두 활성화하면 부모 엔티티를 통해서 자식의 생명 주기를 관리할 수 있음.
- DDD의 Aggregate Root 개념을 구현할 때 유용함.
- 주의 사항은 자식 엔티티가 하나의 부모에만 속해야됨. 여러 곳에서 참조하면 사용하면 안 됨.

## 값 타입 공유 참조
- 임베디드 타입 같은 값 타입을 여러 엔티티에서 공유하면 위험함.
- 하나의 엔티티의 값 타입을 변경해도 같이 변경되는 부작용 발생함.
- 대신 값을 복사해서 사용해야함.
- 직접 정의한 값 타입은 자바의 기본 타입이 아니라 객체 타입임.
- 객체 타입은 참조 값을 직접 대입하는 것을 막을 방법이 없음.

## 불변 객체
- 객체 타입을 수정할 수 없게 만들면 부작용을 원천 차단함.
- 값 타입은 불변 객체로 설계해야함.
- 불변 객체: 생성 시점 이후 절대 값을 변경할 수 없는 객체.
- 생성자로만 값을 설정하고 setter를 만들지 않으면 됨.

## 값 타입 컬렉션의 제약사항
- 값 타입은 엔티티와 다르게 식별자 개념이 없음.
- 값 타입 컬렉션에 변경 사항이 발생하면, 주인 엔티티와 연관된 모든 데이터를 삭제하고, 값 타입 컬렉션에 있는 현재 값을 모두 다시 저장함.
- 값 타입 컬렉션을 매핑하는 테이블은 모든 컬럼을 묶어서 기본키를 구성해야함 -> not nullable, unique
- 값 타입 컬렉션은 변경을 추적할 필요가 없는 스트링 정도를 저장할 때 써야함.
  - ex: 좋아하는 메뉴들을 작성.

## 값 타입 컬렉션 대안
- 값 타입 컬렉션 대신에 일대다 관계를 고려해야함.
- 일대다 관계를 위한 엔티티를 만들고, 여기에서 값 타입을 사용함.
- 영속성 전이 + 고아 객체 제거를 사용해서 값 타입 컬렉션처럼 사용함.
- 주인 엔티티가 One이지만 `JoinColumn` 사용함.

## JPQL 소개
- 테이블을 대상으로 쿼리하는 게 아니라 엔티티 객체를 대상으로 쿼리한다.
- SQL을 추상화해서 특정 데이터베이스 SQL에 의존하지 않는다.
- JPQL은 결국 SQL로 변환된다.

## JPA 서브 쿼리 한계
- JPA는 WHERE, HAVING 절에서만 서브 쿼리 사용 가능함.
- SELECT 절도 가능 (하이버네이트에서 지원)
- FROM 절의 서브 쿼리는 현재 JPQL에서 불가능
  - 조인으로 풀 수 있으면 풀어서 해결

## 경로 표현식 용어 정리
- 상태 필드: 단순히 값을 저장하기 위한 필드
- 연관 필드: 연관관계를 위한 필드
  - 단일 값 연관 필드: `@ManyToOne`, `@OneToOne` 대상이 엔티티.
  - 컬렉션 값 연관 필드: `@OneToMany`, `@ManyToMany`, 대상이 컬렉션.

## 경로 표현식 특징
- 상태 필드: 경로 탐색의 끝, 탐색 X
- 단일 값 연관 경로: inner join 발생, 탐색 O
- 컬렉션 값 연관 경로: inner join 발생, 탐색 X
  - FROM 절에서 명시적 조인을 통해 별칭을 얻으면 별칭을 통해 탐색 가능.
    ```
    SELECT m.username FROM Team t JOIN t.members m;
    ```

## 명시적 조인, 묵시적 조인
- 명시적 조인: join 키워드 직접 사용 -> `SELECT m FROM Member m JOIN m.team t`
- 묵시적 조인: 경로 표현식에 의해 묵시적으로 SQL 조인 발생 (inner join만 가능) -> `SELECT m.team FROM Member m`

## 실무 조건
- 가급적 묵시적 조인 대신에 **명시적 조인 사용.**
- 조인은 SQL 튜닝에 중요 포인트.
- 묵시적 조인은 조인이 일어나는 상황을 한눈에 파악하기 어려움.

## 페치 조인과 DISTINCT
- SQL에 DISTINCT를 추가하지만 데이터가 다르므로 SQL 결과에서 중복제거 실패.
- DISTINCT가 추가로 애플리케이션에서 중복 제거 시도.
- 같은 식별자를 가진 엔티티 제거.

## 페치 조인과 일반 조인의 차이
- 일반 조인 실행시 연관된 엔티티를 함께 조회하지 않음.
- JPQL은 결과를 반환할 때 연관관계 고려 안 함. 단지 `SELECT` 절에 지정한 엔티티만 조회할 뿐.
- 페치 조인을 사용할 때만 연관된 엔티티도 함께 조회 (eager loading)
- 페치 조인은 객체 그래프를 SQL 한 번에 조회하는 개념.