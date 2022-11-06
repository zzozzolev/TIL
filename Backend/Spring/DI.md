## DI(Dependency Injection)란?
- 애플리케이션 실행 시점(런타임)에 외부에서 실제 구현 객체를 생성하고 클라이언트에 전달해 클라이언트와 서버의 실제 의존관계가 연결 되는 것.
- 의존관계는 정적인 클래스 의존 관계와, 실행 시점에 결정되는 동적인 객체(인스턴스) 의존 관계를 분리해서 생각해야한다.

## IoC(Inversion of Control)
- 프로그램의 제어 흐름을 직접 제어하는 게 아니라 외부에서 관리하는 것.

## 스프링 컨테이너
- 일반적으로 `ApplicationContext`를 지칭함.

## 동적으로 bean을 선택해야할 때
- 멤버 변수로 `Map<String, Type>` 혹은 `List<Type>`을 이용해 의존 관계를 주입할 수 있다.
- 스프링이 알아서 해당 타입의 빈을 등록해준다.

## third party 라이브러리를 Bean으로 추가하기
- third party 라이브러리를 DI로 주입하고 싶다면 `@Configuration`과 `@Bean`을 이용하면 된다.
- 아래와 같이 하면 라이브러리 인스턴스를 스프링 애플리케이션의 Bean으로 만들 수 있고 autowire를 할 수 있다.
```java
@Configuration
public class ThirdPartyLibConfig {

    @Bean
    public Slugify getSlugify() {
        return new Slugify();
    }
}
```

### 참고
- https://stackoverflow.com/questions/36010544/how-do-i-autowire-3rd-party-classes-with-annotations-in-spring
- https://programmer.help/blogs/there-are-three-ways-for-springboot-to-introduce-third-party-jar-beans.html