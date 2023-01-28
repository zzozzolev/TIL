## Testing the Web Layer
- [공식 문서](https://spring.io/guides/gs/testing-web/)
  - `MockMvc`를 통한 테스트 방법 가이드
- [블로그](https://shinsunyoung.tistory.com/52)
  - GET, POST 테스트 방법을 예제를 통해 설명

## `@WebMvcTest` vs `@AutoConfigureMockMvc`
### 공통점
- `MockMvc`를 사용할 때 필요하다.
### `@WebMvcTest`
- 컨트롤러 테스트에 사용한다.
- `@SpringBootTest`와 같이 사용할 수 없다.

### `@AutoConfigureMockMvc`
- 컨트롤러 뿐만 아니라 테스트 대상이 아닌 `@Service`나 `@Repository`가 붙은 객체들도 모두 메모리에 올린다.

### 참고
- https://we1cometomeanings.tistory.com/65

## MockMvcResult
- `MockMvcResult`에서는 응답에서 쿠키를 받을 수 없다. [참고](https://stackoverflow.com/questions/26142631/why-does-spring-mockmvc-result-not-contain-a-cookie)
- 따라서 로그아웃을 제대로 테스트할 수 없다.
- 리퀘스트 세션에 스프링 시큐리티 컨텍스트가 들어가나 응답 세션에 넣어도 잘 동작하지 않는다.

## `@Transactional`이 적용된 테스트 동작 방식
1. 테스트에 `@Transactional`이 테스트 메서드나 클래스에 있으면 먼저 트랜잭션을 시작한다.
2. 테스트 로직을 실행한다. 테스트가 끝날 때 까지 모든 로직은 트랜잭션 안에서 수행된다.
  - 트랜잭션은 기본적으로 전파되기 때문에, 레포지토리에서 사용하는 JdbcTemplate도 같은 트랜잭션을 사용한다.
3. 테스트 실행 중에 INSERT SQL을 사용해서 로우를 데이터베이스에 저장한다.
4. 검증을 위해서 SELECT SQL로 데이터를 조회한다.
  - SELECT SQL도 같은 트랜잭션을 사용하기 때문에 저장한 데이터를 조회할 수 있다. 다른 트랜잭션에서는 해당 데이터를 확인할 수 없다.
5. `@Transactional`이 테스트에 있으면 테스트가 끝날 때 트랜잭션을 강제로 롤백한다.
6. 롤백에 의해 앞서 데이터베이스에 저장한 로우가 제거된다.
