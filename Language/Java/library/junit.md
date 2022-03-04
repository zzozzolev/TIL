## 기본 애노테이션
- [블로그](https://gracelove91.tistory.com/107)

## `@BeforeAll`에 `@Autowired` 넣기
- `@BeforeAll`은 스태틱 메서드이다. 하지만 보통 `@Autowired`는 인스턴스 변수로 선언한다.
- `@BeforeAll`에서 autowired 객체를 사용하고 싶다면 `@BeforeAll`에서 인자로 넘겨주면 된다.
  ```java
  public class LoginTest {
      @Autowired UserService userService;

      @BeforeAll
      public static void setUp(@Autowired UserService userService) {
  ```
