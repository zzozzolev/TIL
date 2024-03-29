## 스프링 컨테이너
- 일반적으로 `ApplicationContext`를 지칭함.
- 파라미터로 넘어온 설정 클래스 정보를 사용해 스프링 빈을 등록한다.

## Singleton
- 스프링 컨테이너를 생성할 때 초기화 메서드가 실행된다.

## Singleton 방식의 주의점
- 여러 클라이언트가 하나의 같은 객체 인스턴스를 공유하기 때문에 stateful하게 설계하면 안 된다.
- stateless로 설계해야 한다.
  - 특정 클라이언트에 의존적인 필드가 있으면 안 된다.
  - 특정 클라이언트가 값을 변경할 수 있는 필드가 있으면 안 된다. (read-only)
  - 필드 대신에 자바에서 공유되지 않는 지역변수, 파라미터, `ThreadLocal`등을 사용해야한다.

## Prototype
- 스프링 컨테이너에서 bean을 얻을 때 생성 및 초기화 메서드가 실행된다.
- 스프링 DI 컨테이너가 요청시 생성과 DI만 하고 바로 클라이언트한테 리턴한다.
- 요청할 때 마다 다른 bean을 생성한다.
- 더 이상 스프링 DI 컨테이너가 관리하지 않는다.
- 따라서 `@PreDestroy` 같은 종료 메서드가 호출되지 않는다.

## 프로토타입, 싱글톤 스코프 빈을 함께 사용시 문제점
- 싱글톤 빈이 프로토타입 빈을 사용한다면, DI 시점에 프로토타입 빈을 주입받아 쭉 사용한다.
- 그러면 싱글톤 빈이 동일한 프로토타입 빈을 사용하게 된다.
- 프로토타입 빈이 stateful하다면 서로 다른 클라이언트가 상태를 공유하게 된다.

## Dependency Lookup
- 의존관계를 외부에서 주입받는 게 아니라 직접 필요한 의존관계를 찾는 것.

## ObjectProvider
- `getObject()`를 이용하면 어플리케이션 컨텍스트를 이용하지 않고도 스프링 컨테이너를 통해 원하는 bean을 얻을 수 있다.
- 즉, DL(Dependency Lookup)이 쉬워진다.
- `ObjectFactory`도 비슷한 기능을 하지만 `ObjectProvider`가 bean을 얻는 것 외에 더 많은 편의 기능을 제공한다.
- 다만 스프링에 의존적이다.
- java 표준인 javax의 `Provider`를 사용하면 스프링에 의존적이지 않으면서 똑같이 원하는 bean을 얻을 수 있다. 하지만 별도의 라이브러리가 필요하다.
- 추가적인 기능이 필요없고 다른 컨테이너가 추가될 가능성이 있다면 `Provider`를, 추가적인 기능이 필요하고 외부 라이브러리 추가가 번거롭다면 `ObjectProvider`를 사용하면 된다.

## RequestMappingHandlerMapping
- 가장 우선 순위가 높은 핸들러 매핑이다.
- 스프링 빈 중에서 `@RequestMapping` 또는 `@Controller`가 클래스 레벨에 있는 경우 매핑 정보로 인식한다.

## HttpMessageConverter
- HTTP 요청, HTTP 응답에 모두 사용된다.
- 요청에 있는 메세지를 읽어서 컨트롤러에 객체로 넘겨주거나 컨트롤러에 있는 리턴값을 응답 메세지에 넣는다.
- 기본 메세지 컨버터
  1. `ByteArrayHttpMessageConverter`
  2. `StringHttpMessageConverter`
    - 클래스 타입: `String`, 미디어타입: `*/*`
  3. `MappingJackson2HttpMessageConverter`
    - 클래스 타입: 객체 또는 `HashMap`, 미디어타입: `application/json` 관련
    - `@RequestBody`가 바이트도 아니고 스트링도 아니면서 `Content-Type`이 `application/json`일 때
    - 즉, `application/json`이 아니면 적용이 안 되니 주의해야한다.

### 요청 데이터 읽기
1. 대상 클래스 타입을 지원하는가.
  - `@RequestBody`의 대상 클래스
2. 요청 헤더의 `Content-Type`의 미디어 타입을 지원하는가.

### 응답 데이터 읽기
1. 대상 클래스 타입을 지원하는가.
  - `return`의 대상 클래스
2. `@RequestMapping`의 `produces`을 지원하는가.
3. (2가 없다면) 요청 헤더의 `Accept`의 미디어 타입을 지원하는가.

## ArgumentResolver
- `RequestMappingHandlerAdapter`에서 호출한다.
- 컨트롤러가 필요로 하는 다양한 파라미터(객체)를 생성한다.
- `@RequestBody`와 `HttpEntity`를 처리하는 `ArgumentResolver`들이 HTTP 메세지 컨버터를 사용한다.

## ReturnValueHandler
- `ArgumentResolver`와 비슷하다.
- 응답 값을 변환하고 처리한다.

## RedirectAttributes
- 리다이렉트를 할 때 지정한 것에 대해서 인코디을 알아서 해주고 나머지는 쿼리 파라미터로 넘겨준다.

## BindingResult
- 검증 오류를 저장하는 객체이다.
- 해당 객체의 메서드인 `hasError()`로 에러가 있는지 확인하고 다시 원래 form으로 보내면 에러 내용을 화면에 출력할 수 있다.
- 타임 리프를 이용한다면 `fields.hasErrors`를 이용한다.

## Hibernate5Module
- 객체에 LAZY 로딩을 적용하면 해당 객체는 프록시 객체로 변한다.
- json 생성 라이브러리는 프록시 객체를 다룰 수 없다.
- 이럴 때 json 생성 라이브러리에 프록시 객체는 무시하라는 것을 알려주기 위해 `Hibernate5Module`을 이용한다.
- main에 등록해주면 된다.
- 그러면 LAZY 로딩 객체를 null로 표시한다.

## 자동, 수동의 올바른 실무 운영 기준
- 편리한 자동 기능을 기본으로 사용하자.
- 수동 빈 등록은 언제?
- 업무 로직 빈(ex. 컨트롤러, 서비스 등등)
  - 자동 기능을 적극 사용하는 게 좋다.
  - 문제가 발생했을 때 명확하게 파악하기 쉽다.
- 기술 지원 빈(ex. AOP, 공통 로그 처리 등등)
  - 수동 빈 등록을 사용하는 게 좋다.
  - 수가 매우 적지만 애플리케이션 전반에 걸쳐서 광범위하게 영향을 미친다.
  - 문제가 발생했을 때 파악이 어렵다.
  - 단, 스프링과 스프링 부트가 자동으로 등록하는 수 많은 빈들을 예외이다.
- 비즈니스 로직 중에서 다형성을 적극 활용할 때
  - 같은 인터페이스를 구현한 여러 타입의 클래스를 이용해야할 때
  - 수동 빈 등록 (`@Configuration`)
  - 특정 패키지에 같이 묶어둔다.

## 스프링 빈의 이벤트 라이프사이클
- 스프링 컨테이너 생성 -> 스프링 빈 생성 -> 의존관계 주입 -> 초기화 콜백 -> 사용 -> 소멸전 콜백 -> 스프링 종료

## 빈 스코프
- 싱글톤(default): 스프링 컨테이너의 시작과 종료까지 유지되는 가장 넓은 범위의 스코프이다.
- 프로토타입: 스프링 컨테이너는 빈의 생성과 의존관계 주입까지만 관여하고 더는 관리하지 않는 매우 짧은 범위의 스코프이다.
- 웹 관련 스코프
  - request: 웹 요청이 들어오고 나갈때 까지 유지되는 스코프이다.
  - session: 웹 세션이 생성되고 종료될 때까지 유지되는 스코프이다.
  - application: 웹의 서블릿 컨텍스트와 같은 범위로 유지되는 스코프이다.

## Request Scope Bean
- `value = request`의 경우, `proxyMode`를 사용하면 obeject provider로 필요할 때 주입받는 효과를 낼 수 있다.
  - `ScopedProxyMode.TARGET_CLASS`: class
  - `ScopedProxyMode.INTERFACES`: interface
- 스프링 컨테이너는 CGLIB라는 바이트 코드 조작 라이브러리를 이용해 가짜 프록시 객체를 생성한다.
- DI시에 가짜 프록시 객체가 주입된다.
- 가짜 프록시 객체는 실제 요청이 오면 그때 내부에서 실제 빈을 요청하는 위임 로직이 있다.
- 가짜 프록시 객체는 싱글톤처럼 동작한다.
