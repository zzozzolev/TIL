## JpaRepository 인터페이스
- `JpaRepository` 인터페이스를 상속한 인터페이스를 이용하면 구현체를 스프링 data jpa에서 만들어서 인젝션 해준다.
- 그래서 클래스를 출력해보면 프록시 객체가 들어있다.

## 쿼리 메서드
- 메서드 이름만으로 쿼리를 생성할 수 있다.
- 단, 정해진 규칙에 따라서 메서드 이름을 작성해야한다.
  - 자세한 건 [공식 문서](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#repositories.query-methods) 참고
- 엔티티 이름을 변경해도 애플리케이션 로딩 시점에 오류가 나서 잘못된 것을 알 수 있다.
