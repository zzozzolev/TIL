## @Configuration
### 사용하는 이유
- singleton을 보장하기 위해서

### 원리
- CGLIB를 이용해 해당 클래스를 상속받은 클래스를 만들어준다.
- 원래 클래스에서는 새로운 객체를 만들었지만, 만들어진 클래스에서는 이미 스프링 컨테이너로 등록돼있다면 등록된 컨테이너를 사용하고 그렇지 않을 때만 새로 객체를 만든다.

## @ComponentScan
- `@ComponentScan`은 해당 config 파일이 놓여진 경로 이하를 스캔한다.
- 따라서 경로 이하에 없는 클래스들은 스프링 bean으로 등록할 수 없다.
- `@SpringBootApplication`에서 component scan을 하기 때문에 따로 사용할 필요는 없다.

## @Autowired
- 생성자가 하나만 있을 때는 해당 생성자로 자동으로 Autowired를 수행한다.
- 하지만 2개 이상이면 특정 생성자 즉, 자신이 원하지 않는 생성자를 사용할 수 있다.
- 스프링 빈에서만 적용된다.
- optional한 인자에는 `@Nullable` 혹은 자바8의 문법인 `Optional<T>`를 이용한다.

## @Primary
### 사용하는 이유
- 같은 타입의 스프링 빈이 여러 개일 때, 특정 빈에 우선 순위를 주기 위해서
  - 실전 사용 예제: 메인 DB와 서브 DB의 커넥션이 있을 때 `@Qualifier` 지정 없이 편리하게 획득.

### 기타
- `@Qualifier`보다 우선 순위가 낮다.

## @Qualifier
### 사용하는 이유
- 같은 타입의 스프링 빈이 여러 개일 때, 구분하기 위해서
  - 실전 사용 예제: 메인 DB와 서브 DB의 커넥션이 있을 때, 명시적으로 획득.

### 한계
- 하지만 `@Qualifier("A")` 이런 식으로 사용할 때, 컴파일 타임에 `"A"`를 인식하지 못한다.
- 따라서 annotation을 만들어서 사용하는 게 좋다.

## @Bean
### 초기화, 종료
- 기본적으로 `@ComponentScan`과 잘 어울리는 `@PostConstruct`, `@PreDestroy`를 사용하자.
- 만약 외부라이브러리를 사용해야한다면 다음을 참고하자.
    - `initMethod`와 `destoryMethod`로 초기화 메서드와 종료 메서드를 지정해줄 수 있다.
    - `destroyMethod`를 지정하지 않으면 `close`, `shutdown`이라는 이름의 메서드를 자동으로 호출해준다. 이건 추론 기능때문이다.
    - 자동으로 호출되는 게 싫다면 `destroyMethod=""`으로 하면 된다.

## @Mapping
### 미디어 타입 조건 매핑
- `headers`를 써도 되긴 하지만 스프링에서 해당 파라미터로 처리하는 것이 있기 때문에 `consumes`을 권장한다.
- `consumes`: request `Content-Type`에 해당 조건이 명시돼 있는 경우.
- `produeces`: request `Accept`와 맞아야한다.

## @RequestParam
### 생략
- 요청 파라미터 이름과 변수 이름이 같으면 `name`을 직접 지정해주지 않아도 된다.
```java
// GET /test?name=jam

public String requestParam(@RequestParam String name)
```
- 또한 `String`, `int`, `Integer` 등 단순한 타입이면 `@RequestParam`도 생략할 수 있다. 하지만 어노테이션을 붙이면 명확하게 요청 파라미터에서 데이터를 읽는 다는 것을 알 수 있다. (단순한 타입은 자바가 정의한 클래스나 Primitive 타입을 말하는 것 같음)
- 나머지는 `@ModelAttribute`로 처리한다.

### null과 ""을 구분하자.
- `required = true`로 줬을 때는 파라미터를 넘겨주지 않았을 때 400 에러가 난다.
- 하지만 파라미터에 빈 값을 넘겨주면 400 에러가 나지 않는다.
```
name이 required

GET /test? -> 400 에러
GET /test?name= -> 200 OK
```

### 기본형에는 null을 입력할 수 없다.
- `required = false`인 파라미터의 타입은 기본형으로 선언하면 안 된다.
- 파라미터가 주어지지 않았을 때 `null`이 들어오는데 기본형은 `null`로 선언할 수 없기 때문이다.

### 기본값 설정
- `defaultValue`로 기본값을 설정할 수 있다.
- `required = true`일지라도 무시되고 기본값이 적용된다.
- 빈문자의 경우에도 설정한 기본값이 적용된다.

## @ModelAttribute
- 지정한 객체를 생성한 뒤 알맞은 프로퍼티 setter를 호출해서 파라미터 값을 바인딩한다.
  - 예를 들어 파라미터가 `name`이면 `setName`을 호출해 `name` 값을 설정해준다.

### 생략
- `@RequestParam`과 마찬가지로 생략할 수 있다.

### 바인딩 오류
- 타입에 맞지 않는 값이 파라미터로 들어오면 `BindException`이 발생한다.

## @RequestBody
### 원리
- HTTP 메세지 컨버터가 HTTP 메세지 바디의 내용을 우리가 원하는 문자나 객체 등으로 변환해준다.
  - 조금 더 자세하게 말하면 `MappingJackson2HttpMessageConverter`라는 게 동작한다.
  - 컨텐트 타입이 `application/json`이면 메세지 바디에서 값을 파싱해 원하는 객체를 만드는 걸 대신 해준다. -> 컨텐트 타입 주의.
- json -> (HTTP 메세지 컨버터) -> 객체

### 생략
- `@RequestBody`를 생략하면 `@ModelAttribute`가 적용된다.

## @ResponseBody
### 원리
- HTTP 메세지 컨버터가 반환한 객체를 json으로 변환해준다.
  - `Accept`에 `application/json`이 있어야 한다.
- 객체 -> (HTTP 메세지 컨버터) -> json
