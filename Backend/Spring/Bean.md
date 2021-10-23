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