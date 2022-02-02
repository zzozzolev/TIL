## Bean Validation Basics
### `@Validated` and `@Valid`
- validator object를 만들지 않고도 밸리데이션을 할 수 있다.
- `@Validated`와 `@Valid` 어노테이션을 사용하면 특정 객체에 대해 밸리데이션이 필요한지 스프링에게 알려줄 수 있다.
- `@Validated`는 클래스 레벨 어노테이션이고 `@Valid`는 메서드 파라미터와 필드 레벨 어노테이션이다.

# Validating Input to a Spring MVC Controller
- 스프링 레스트 컨트롤러를 구현했고 클라이언트에 의해 전달되는 인풋을 밸리데이션하고 싶다고 해보자.
- 어떤 인커밍 HTTP 리퀘스트에 대해 밸리데이션을 할 수 있는 것이 세 가지가 있다.
  - 리퀘스트 바디
  - 패스 배리어블
  - 쿼리 파라미터

### Validating a Request Body
- POST, PUT 리퀘스트에서 json 페이로드를 리퀘스트 바디내에 전달하는 게 흔하다.
- 스프링은 알아서 인커밍 json을 자바 오브젝트로 맵핑한다.
- 이 맵핑된 오브젝트를 체크한다고 해보자.
- 클래스는 아래와 같다. (해당 글에서는 언급하지 않지만 DTO로 보면 될 거 같다.)
  ```java
  class Input {

    @Min(1)
    @Max(10)
    private int numberBetweenOneAndTen;

    @Pattern(regexp = "^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$")
    private String ipAddress;
    
    // ...
  }
  ```
- 리퀘스트 바디를 검증하기 위해서, 레스트 컨트롤러의 리퀘스트 바디에 `@Valid`을 붙이면 된다.
  ```java
  @RestController
  class ValidateRequestBodyController {

    @PostMapping("/validateBody")
    ResponseEntity<String> validateBody(@Valid @RequestBody Input input) {
        return ResponseEntity.ok("valid");
    }
  }
  ```
> 만약 `Input` 클래스가 또 다른 컴플렉스 타입을 가진 필드를 포함하고 있다면, 이 필드 역시 `@Valid`가 붙어있어야 한다.

- 만약 밸리데이션이 실패한다면, `MethodArgumentNotValidException`을 트리거할 것이다. 기본적으로 스프링은 이 예외를 404 스테이터스(Bad Request)로 바꾼다.

### Validating Path Variables and Request Parameters
- 패스 배리어블은 보통 `int`, `String` 같은 타입이기 때문에 복잡한 자바 오브젝트를 밸리데이션하지 않는다.
- 클래스 필드에 어노테이팅하지 않고 아래처럼 메서드 파라미터에 바로 붙인다.
  ```java
  @RestController
  @Validated
  class ValidateParametersController {

    @GetMapping("/validatePathVariable/{id}")
    ResponseEntity<String> validatePathVariable(
        @PathVariable("id") @Min(5) int id) {
        return ResponseEntity.ok("valid");
    }
    
    @GetMapping("/validateRequestParameter")
    ResponseEntity<String> validateRequestParameter(
        @RequestParam("param") @Min(5) int param) { 
        return ResponseEntity.ok("valid");
    }
  }
  ```
- 컨트롤러 클러스에 `@Validated` 어노테이션을 붙여야한다. 이렇게 스프링이 이밸류에이션을 할 수 있다.
- 리퀘스트 바디 밸리데이션과 달리 실패한 밸리데이션은 `ConstraintViolationException`을 트리거한다.
- 스프링은 이 예외에 대한 디폴트 예외 핸드러를 등록하지 않기 때문에 500 스테이터스(Internal Server Error)를 반환한다.
- 만약 400을 대신 리턴하고 싶다면 커스텀 예외 핸들러를 컨트롤러에 추가할 수 있다. (스프링 공식 튜토리얼에는 Advice를 사용하도록 안내하고 있다.)
  ```java
  @RestController
  @Validated
  class ValidateParametersController {

    // request mapping method omitted
    
    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    ResponseEntity<String> handleConstraintViolationException(ConstraintViolationException e) {
        return new ResponseEntity<>("not valid due to validation error: " + e.getMessage(), HttpStatus.BAD_REQUEST);
    }
  } 
  ```

## Validating Input to a Spring Service Method
- 컨트롤러 레벨에서 인풋을 밸리데이팅하는 대신, 어느 스프링 컴포넌트에서도 인풋을 밸리데이트할 수 있다.
- 이렇게 하기 위해서는 `@Validated`와 `@Valid` 어노테이션 조합을 사용한다.
  ```java
  @Service
  @Validated
  class ValidatingService{

    void validateInput(@Valid Input input){
        // do something
    }
  }
  ```
- `@Validated` 어노테이션은 클래스 레벨에서만 이벨류에이션되기 때문에 이런 사용예에서는 메서드에 넣으면 안 된다.

## Validating JPA Entities
- 밸리데이션을 위한 마지막 라인은 펄시스턴스 레이어이다.
- 기본적으로 스프링 데이터는 하이버네이트를 사용한다. 그리고 하이버네이트는 특별히 빈 밸리데이션을 지원한다.

> 펄시스턴스 레이어는 밸리데이션 하기에 적절한 곳일까?

> 보통 펄시스턴스 레이어에서만큼 늦게 밸리데이션 하는 걸 원하지 않는다. 왜냐하면 그 위의 비지니스 코드는 잠재적으로 인밸리드 오브젝트와 동작했고 발견하지 못한 에러들을 발생시켰을 수도 있기 때문이다. 자세한 건 [Bean Validation anti-patterns](https://reflectoring.io/bean-validation-anti-patterns/#anti-pattern-1-validating-only-in-the-persistence-layer)를 참고하자.
- `Input` 클래스 오브젝트를 데이터 베이스에 저장하고 싶다고 해보자.
  ```java
  @Entity
  public class Input {

    @Id
    @GeneratedValue
    private Long id;

    @Min(1)
    @Max(10)
    private int numberBetweenOneAndTen;

    @Pattern(regexp = "^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$")
    private String ipAddress;
    
    // ...
  }
  ```
- 다음은 테스트 코드이다.
  ```java
  public interface ValidatingRepository extends CrudRepository<Input, Long> {}
  
  @ExtendWith(SpringExtension.class)
  @DataJpaTest
  class ValidatingRepositoryTest {

    @Autowired
    private ValidatingRepository repository;

    @Autowired
    private EntityManager entityManager;

    @Test
    void whenInputIsInvalid_thenThrowsException() {
        Input input = invalidInput();

        assertThrows(ConstraintViolationException.class, () -> {
        repository.save(input);
        entityManager.flush();
        });
    }
  }
  ```
- 빈 밸리데이션은 하이버네이트가 일단 `EntityManager`를 `flush`하고 트리거된다.
- 만약 스프링 데이터 레파지토리에서 빈 밸리데이션을 비활성화하고 싶다면, 스프링 부트 프로퍼티에서 `spring.jpa.properties.javax.persistence.validation.mode`를 `none`으로 설정하면 된다.

## A Custom Validator with Spring Boot
- 만약 사용가능한 constraint annotations가 유즈 케이스들에 맞지 않는다면, 커스텀을 만들 수도 있다.
- 먼저 커스텀 컨스트레인트 어노테이션인 `IpAddress`를 생성한다.
  ```java
  @Target({ FIELD })
  @Retention(RUNTIME)
  @Constraint(validatedBy = IpAddressValidator.class)
  @Documented
    public @interface IpAddress {

    String message() default "{IpAddress.invalid}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
  }
  ```
  - `message`는 `ValidationMessages.properties`에 있는 프로퍼티 키를 가리킨다. 바이오레이션시 메시지를 리졸브할 때 사용된다.
  - `groups`는 어떤 상황에서 해당 밸리데이션이 트리거돼야하는지를 정의한다.
  - `payload`는 거의 안 쓰인다고 한다.
  - `@Constraint` 어노테이션은 `ConstraintValidator` 인터페이스의 구현이라는 것을 가리킨다.
- 밸리데이터 구현은 아래와 같다.
  ```java
  class IpAddressValidator implements ConstraintValidator<IpAddress, String> {

  @Override
  public boolean isValid(String value, ConstraintValidatorContext context) {
    ...
  ```
- 이제는 커스텀 애노테이션인 `@IpAddress`를 다른 constraint annotation 처럼 사용할 수 있다.

## Validating Programmatically
- 스프링의 빌트인 빈 밸리데이션 서포트에 의지하기 보다는 밸리데이션을 프로그래밍적으로 호출하길 원할 때가 있다.
- 이런 경우라면, 빈 밸리데이션 API를 직접 사용할 수 있다.
- 스프링 서포트 없이 아래와 같이 직접 팩토리로 validator를 만들수도 있다.
  ```java
  class ProgrammaticallyValidatingService {
  
    void validateInput(Input input) {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        Validator validator = factory.getValidator();
        Set<ConstraintViolation<Input>> violations = validator.validate(input);
        if (!violations.isEmpty()) {
        throw new ConstraintViolationException(violations);
        }
    } 
  }
  ```
- 하지만, 스프링 부트는 미리 설정된 `Validator` 인스턴스를 제공한다. 그래서 서비스 내에 해당 인스턴스를 주입하고 사용하면 된다.
  ```java
  @Service
  class ProgrammaticallyValidatingService {

    private Validator validator;

    ProgrammaticallyValidatingService(Validator validator) {
        this.validator = validator;
    }

    void validateInputWithInjectedValidator(Input input) {
        Set<ConstraintViolation<Input>> violations = validator.validate(input);
        if (!violations.isEmpty()) {
        throw new ConstraintViolationException(violations);
        }
    }
  }
  ```

## Using Validation Groups to Validate Objects Differently for Different Use Cases
- 종종, 특정 오브젝트들은 다른 유즈 케이스들 사이에서 공유된다. 하지만 같은 밸리데이션이 적용되지 않을 수 있다.
- 좀 더 구체적으로는 Create, Update에서 다른 밸리데이션을 사용할 수도 있다.
- 이럴 때, 밸리데이션 그룹을 사용하면 된다.
  ```java
  class InputWithGroups {

    @Null(groups = OnCreate.class)
    @NotNull(groups = OnUpdate.class)
    private Long id;
  
    // ...
  }
  ```
- 하지만, create랑 update가 동일하지 않을 때도 많고 공유할 바에 따른 DTO로 만드는 게 더 나을 것 같다. 그래서 이걸 쓸 일이 많을까 싶다;

## Handling Validation Errors
- 밸리데이션이 실패했을 때, 클라이언트에게 유의미한 에러 메세지를 리턴하고 싶다.
- 각각 실패한 밸리데이션에 대한 에러 메세지를 담고 있는 자료 구조들을 리턴해야한다.
- 자료 구조는 `Violation` 오브젝트들의 리스트를 포함한다.
  ```java
  public class ValidationErrorResponse {

    private List<Violation> violations = new ArrayList<>();

    // ...
  }

  public class Violation {

    private final String fieldName;

    private final String message;

    // ...
  }
  ```
- 그 다음, 컨트롤러 레벨까지 올라오는 모든 `ConstraintViolationExceptions`을 처리하는 글로벌 `ControllerAdvice`를 생성한다.
- 리퀘스트 바디에서 발생하는 밸리데이션 에러들을 잡기 위해서, `MethodArgumentNotValidExceptions`을 처리한다.
  ```java
  @ControllerAdvice
  class ErrorHandlingControllerAdvice {

    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    ValidationErrorResponse onConstraintValidationException(
        ConstraintViolationException e) {
        ValidationErrorResponse error = new ValidationErrorResponse();
        for (ConstraintViolation violation : e.getConstraintViolations()) {
        error.getViolations().add(
            new Violation(violation.getPropertyPath().toString(), violation.getMessage()));
        }
        return error;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ResponseBody
    ValidationErrorResponse onMethodArgumentNotValidException(
        MethodArgumentNotValidException e) {
        ValidationErrorResponse error = new ValidationErrorResponse();
        for (FieldError fieldError : e.getBindingResult().getFieldErrors()) {
        error.getViolations().add(
            new Violation(fieldError.getField(), fieldError.getDefaultMessage()));
        }
        return error;
    }
  }
  ```
- 위에서 한 것은 그냥 바이오레이션들에 대한 정보를 읽어서 정으한 자료 구조에 넣은 것이다.
- `@ControllerAdvice` 어노테이션을 잘 봐라. 해당 어노테이션은 예외 핸들러 메서드들이 어플리케이션 컨텍스트 내에 있는 모든 컨트롤러들에 글로벌하게 이용할 수 있도록 해준다.

## 참고
- https://reflectoring.io/bean-validation-with-spring-boot/