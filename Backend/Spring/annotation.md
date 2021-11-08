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
