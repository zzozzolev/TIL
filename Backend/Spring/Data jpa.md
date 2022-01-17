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
