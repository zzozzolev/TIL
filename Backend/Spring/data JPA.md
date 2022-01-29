## JpaRepository 인터페이스
- `JpaRepository` 인터페이스를 상속한 인터페이스를 이용하면 구현체를 스프링 data jpa에서 만들어서 인젝션 해준다.
- 그래서 클래스를 출력해보면 프록시 객체가 들어있다.

## 쿼리 메서드
- 메서드 이름만으로 쿼리를 생성할 수 있다.
- 단, 정해진 규칙에 따라서 메서드 이름을 작성해야한다.
  - 자세한 건 [공식 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.query-methods) 참고
- 엔티티 이름을 변경해도 애플리케이션 로딩 시점에 오류가 나서 잘못된 것을 알 수 있다.
- 하지만 파라미터나 로직이 조금만 들어가도 메서드 이름이 복잡해진다. 따라새 파라미터 2~3개까지만 해당 방법을 사용하도록 한다.

## @Query
- `JpaRepository` 인터페이스에 `@Query`로 JPQL을 작성해서 이용할 수 있다.
  ```java
    @Query("select m from Member m where m.username = :username and m.age = :age")
    List<Member> findUser(@Param("username") String username, @Param("age") int age);
  ```
- 애플리케이션 로딩 시점에 잘못된 쿼리가 있다면 에러가 난다는 장점이 있다.

## 조회 사이즈
- 단건 조회시 조회 결과가 없다면 `null`이 된다. 만약 조회 결과가 2개 이상이면 `IncorrectResultSizeDataAccessException`이 발생한다.
- 컬렉션 조회시 조회 결과가 없다면 사이즈가 0인 컬렉션이 반환된다.
- 하지만 `Optional`을 사용하면 클라이언트가 `null`로 처리하지 않아도 된다.

## 쿼리 리턴타입
- [Supported Query Return Types](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repository-query-return-types)

## Page vs Slice
- 페이지는 0부터 시작인 것을 주의한다.
### Page
- `size`만큼만 `limit`으로 지정한다.
- `count` 쿼리를 날리기 때문에 전체 페이지, 전체 엘리먼트 개수를 알 수 있다.
  - 페이징 쿼리가 조인을 사용한다면 기본적으로 카운트 쿼리도 조인을 사용한다. 하지만, 조인은 필요없기 때문에 `@Query`에서 `countQuery`를 설정해주는 게 좋다.
    ```java
    @Query(value = "select m from Member m left join m.team t", countQuery = "select count(m) from Member m")
    ```

### Slice
- `size + 1`만큼 `limit`으로 지정한다.
- `count` 쿼리를 날라지 않기 때문에 전체 페이지, 전체 엘리먼트 개수를 알 수 없다. 단, 인터페이스 리턴 타입을 `Page`로 하면 `count` 쿼리가 나가니 조심해야한다.

## Page to DTO
- 처음 페이지를 생성하면 엔티티의 페이지이다. 그대로 노출하면 안 된다.
- 따라서 페이지 인스턴스의 `map` 메서드를 이용해 엔티티 페이지를 DTO 페이지로 변환한다.
```java
Page<Member> page = memberRepository.findByAge(10, pageRequest);
Page<MemberDto> dtoPage = page.map(m -> new MemberDto());
```

## Pageable 파라미터
- page
- size
- sort: 정렬 조건 ex) `sort=id,desc`
- `application.yml`에 `data.web.pageable.default-page-size`와 `data.web.pageable.max-page-size`를 설정할 수 있다.
- 혹은 `@PageableDefault`를 통해 설정할 수도 있다.
- `@Qualifier`를 통해 여러 페이징 정보를 받을 수도 있다. ex) `merber_page=0&order_page=1`

## 벌크성 업데이트
- 단 건이 아닌 여러 건을 한 번에 업데이트해야하는 경우 벌크 업데이트를 하면 성능이 더 잘 나올 수 있다.
- 단, 주의해야할 점은 persistent context를 무시하고 바로 DB에 업데이트 요청하는 하기 때문에, 이후에 엔티티를 조회하면 벌크 업데이트 이전의 상태가 조회된다.
  ```java
  memberRepository.save(new Member("member5", 40));

  // bulk update
  // age >= 20 이상의 멤버들의 age를 1씩 증가

  // Member(... , age=40)
  List<Member> result = memberRepository.findByUsername("member5").get(0); 
  ```
- 따라서 persistent context를 꼭 `clear`해야한다. 중간에 JPQL을 실행하면 `flush`를 알아서 호출한다.
  ```java
  // bulk update
  // age >= 20 이상의 멤버들의 age를 1씩 증가
  
  em.clear();

  // Member(... , age=40)
  List<Member> result = memberRepository.findByUsername("member5").get(0);
  ```
- bulk 쿼리에 `@Modifying(clearAutomatically = true)`로 하면 위의 과정을 알아서해준다.

## `@Modifying`
- INSERT, UPDATE, DELETE, DDL statements를 날릴 때 필요한 어노테이션이다.
- 변경 쿼리에 해당 어노테이션을 추가하지 않으면 hibernate에서 `QueryExecutionRequestException`이, spring에서 `InvalidDataAccessApiUsageException`이 발생한다.

## `@EntityGraph`
- fetch join을 간단하게 적용하고 싶을 때 사용한다.
- 아래와 같이 fetch join할 attributes를 명시하면 된다.
  ```java
  @Override
  @EntityGraph(attributePaths = {"team"})
  List<Member> findAll();

  // 다음의 JPQL과 같음.
  @Query("select m from Member m left join fetch m.team")
  List<Member> findMemberFetchJoin();
  ```
- `@NamedEntityGraph`도 있으나 실무에서는 거의 사용하지 않는다. 간단하게 위에처럼 쓰거나 JPQL을 쓰면 된다.

## `@Lock`
- row를 잠구기 위한 lock을 제공한다.
- 쿼리로 `SELECT ~ FOR UPDATE`가 나가서 한 세션의 업데이트가 종료될 때까지 다른 세션은 접근하지 못한다.

## 사용자 정의 리포지토리
- 인터페이스의 메서드를 직접 구현하고 싶을 때 사용한다.
- 주로 QueryDSL을 쓰고 싶을 때 쓴다.
- 단, 구현 클래스는 `JpaRepository`를 확장한 인터페이스 이름에 `Impl`을 붙여야한다.
  ```java
  public interface MemberRepository extends JpaRepository<Member, Long>, MemberRepositoryCustom {
    ...
  }

  public interface MemberRepositoryCustom {
    List<Member> findMemberCustom();

  }

  public class MemberRepositoryImpl implements MemberRepositoryCustom {
     List<Member> findMemberCustom() {

     }
  }
  ```
- 모든 곳에 사용자 정의 리포지토리를 써야하는 건 아니다. 복잡한 쿼리는 별도의 클래스로 분리하는 게 낫다.

## Auditing
- [공식 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#auditing)
- data JPA는엔티티를 누가 변경했는지 언제 변경했는지에 대해 트랙킹할 수 있도록 도와준다. 이걸 `auditing`이라고 한다.
- 이 기능을 활용하기 위해서는 엔티티에 애노테이션을 붙이거나 인터페이스를 구현해야한다.

## @MappedSuperclass
- 엔티티에서 공통 매핑 정보가 필요할 때 사용한다.
- 공통 매핑 정보가 있는 부모 클래스에 해당 애노테이션을 달아주면 된다.
- 실무에서는 생성자, 생성 시간, 수정자, 수정 시간을 공통적으로 써야할 때 사용하면된다.
- 애노테이션을 달지 않으면 자식 엔티티에 대한 테이블을 만들 때 부모의 정보가 들어가지 않는다.

## @CreatedBy, @LastModifiedDate
- JPA 이벤트 어노테이션(`@PrePersist`, `@PreUpdate`)를 사용하지 않고도 생성일, 수정일을 등록할 수 있도록 해준다.

## 등록, 수정 관련 정보 저장하기
- 보통 등록일, 수정일은 모든 엔티티에 필요한 정보이다.
- 하지만 등록자, 수정자는 엔티티에 따라 필요하지 않을 수도 있다.
- 그래서 베이스 엔티티에 등록자, 수정자를 모두 집어넣는 것 보다는 등록일, 수정일은 별도의 엔티티로 따로 빼는 게 좋다.
- 등록일, 수정일은 `BaseTimeEntity`로 등록자, 수정자는 `BaseEntity`로 만들고 `BaseTimeEntity`를 상속받게 하면 된다.
  ```java
  public class BaseTimeEntity {
      @CreatedDate
      @Column(updatable = false)
      private LocalDateTime createdDate;

      @LastModifiedDate
      private LocalDateTime lastModifiedDate;
  }

  public class BaseEntity extends BaseTimeEntity {

    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String lastModifiedBy;
  }
  ```

## SimpleJpaRepository
- data JPA의 구현체이다.
- 클래스에 `@Repository`, `@Transactional` 어노테이션이 붙어있다.
1. `@Repository`
  - 컴포넌트 스캔의 대상
  - 영속성 계층의 예외들을(JDBC, JPA) 스프링 예외로 바꿔준다.
  - 그래서 하부 기술을 바꿔도 예외 처리 매커니즘이 동일하다.
2. `@Transactional(readOnly = true)`
  - data JPA의 모든 기능은 트랜잭션을 걸고 시작한다.
  - 서비스 계층에서 트랜잭션을 걸고 들어오면, 별다른 옵션이 없으면 해당 트랜잭션을 이어서 동작한다.
  - 트랜잭션이 없어도 data JPA에서는 repository에서 기본적으로 걸고 시작한다.
  - `save` 이런 메서드들은 메서드에 `@Transactional` 어노테이션이 있다.
  - 단, 해당 메서드가 끝나면 트랜잭셩이 끝나므로 영속성 컨텍스트가 없어진다. 
  - `readOnly = true`이면 트랜잭션이 끝나도 플러시를 생략한다.

## 새로운 엔티티를 구별하는 방법
-  `save()` 메서드
  - 새로운 엔티티면 저장 (`persist`)
  - 새로운 엔티티가 아니면 병합 (`merge`)
    - DB에 select 쿼리가 나간다.
- 새로운 엔티티 판단 전략
  - 식별자가 객체일 때 `null`로 판단
    - 식별자가 `GeneratedValue`가 아닐 때, 식별자를 넣어서 객체를 만들면 새로운 엔티티로 판단하지 않는다.
    - 그래서 `merge`가 호출되는데, 불필요한 select 쿼리가 나가게 된다.
  - 식별자가 자바 기본 타입일 때 `0`으로 판단
  - `Persistable` 인터페이스를 구현해서 판단 로직 변경 가능
    - 만약 `GeneratedValue`를 쓰지 못한다면 이 인터페이스를 사용하면 된다.
    - `isNew`에 새로운 인스턴스인지 아닌지를 판단하는 로직을 넣는다.
    - 판단 로직은 `@CreatedDate`를 이용하면 된다. `@CreatedDate`가 `null`이라면 JPA를 통해 값이 들어가지 않은 것이기 때문이다.
      ```java
      @CreatedDate
      private LocalDateTime createdDate;

      @Override
      public boolean isNew() {
          return createdDate == null;
      }
      ```

## Projections
- 엔티티 대신에 DTO를 편리하게 조회할 때 사용한다.
- 전체 필드가 아닌 일부 필드만 조회화고 싶을 때 사용한다.
- 프로젝션 종류
  - open projection
    - DB에서 모든 필드를 가져온 후, 애플리케이션에서 필요한 필드만 지정
    ```java
    @Value("#{target.username + ' ' + target.age}")
    String getUsername();
    ```
  - close projection
    - DB에서 지정한 필드만 가져옴
    ```java
    String getUsername();
    ```
- 인터페이스가 아닌 DTO 클래스를 이용하는 방법도 있다. 이때 생성자에 넘겨지는 파라미터 이름을 보고 가져올 필드를 판단한다.
  ```java
  private final String username;

    public UsernaemOnlyDto(String username) {
        this.username = username;
    }

    public String getUsername() {
        return username;
    }
  ```
