## Singleton
- 스프링 컨테이너를 생성할 때 초기화 메서드가 실행된다.

## Prototype
- 스프링 컨테이너에서 bean을 얻을 때 생성 및 초기화 메서드가 실행된다.
- 스프링 DI 컨테이너가 요청시 생성과 DI만 하고 바로 클라이언트한테 리턴한다.
- 요청할 때 마다 다른 bean을 생성한다.
- 더 이상 스프링 DI 컨테이너가 관리하지 않는다.
- 따라서 `@PreDestroy` 같은 종료 메서드가 호출되지 않는다.

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
  3. `MappingJackson2HttpMessageConverter`
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
