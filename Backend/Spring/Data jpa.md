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
