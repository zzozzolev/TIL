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
