## Tracking Modes
- 서버가 처음에는 브라우저의 쿠키 지원 여부를 판단하지 못하므로 쿠키와 URL에 `jessionid`도 함께 전달한다.
- URL 전달 방식을 끄고 항상 쿠키를 통해서만 세션을 유지하고 싶다면 다음과 같이 하면 된다.
```yaml
server:
    servlet:
        session:
            tracking-modes: cookie
```

## 타임아웃
- 세션은 유저가 로그아웃을 직접 호출해서 `session.invalidate()`가 호출되는 경우에 삭제된다.
- 하지만 사용자는 보통 로그아웃을 하지 않고 웹 브라우저를 종료한다.
- HTTP는 비연결성이므로 서버 입장에서는 사용자가 웹 브라우저를 종료한 것인지 알 수 없다. 따라서  언제 삭제해야하는지 판단하기 어렵다.
- 이런 경우 남아있는 세션을 계속 보관하면 문제가 발생할 수 있다.
  - 세션과 관련된 쿠키를 해커가 얻은 경우 오랜 시간이 지나도 악용할 수 있다.
  - 세션은 기본적으로 메모리에 생성된다. 메모리의 크기는 제한적이므로 꼭 필요한 경우만 생성해서 사용해야한다.
### 세션의 종료 시점
- 생성 시점 기준으로 30분 뒤로 하면 유저가 서비스를 사용 중임에도 매 30분마다 로그인해야하는 번거로움이 생긴다.
- 따라서 유저가 최근에 요청한 시간을 기준으로 30분을 유지해주는 것이 좋다.
- 이렇게 하면 유저가 서버에 매번 요청해야하는 번거로움이 사라진다.

### 세션 타임아웃 설정
- 글로벌 설정
  - 분 단위로 설정해야한다.
  ```yaml
    server:
        servlet:
            session:
                timeout: 60
  ```
- 특정 세션 단위
  ```java
  session.setMaxInactiveInterval(1800);
  ```

### 세션 타임아웃 발생
- 세션과 관련된 `JSESSIONID`를 전달하는 HTTP 요청이 있으면 현재 시간으로 다시 초기회된다.
- 초기화되면 세션 타임아웃으로 설정한 시간동안 세션을 추가로 사용할 수 있다.
- `LastAccessedTime`이후로 timeout 시간이 지나면 WAS가 내부에서 해당 세션을 제거한다.

### 주의
- 실무에서 주의할 점은 세션에는 최소화의 데이터만 보관해야한다.
- `(보관한 데이터 용량) * (사용자 수)`로 메모리 사용량이 급격하게 늘어나서 장애로 이어질 수 있다.
- 세션 시간을 너무 길게 가져가면 메모리 사용이 계속 누적될 수 있으므로 적당한 시간을 선택하는 것이 필요하다.
- 기본이 30분이라는 것을 기준으로 고민하면 된다.

## Servlet Filter
- 인증은 여러 로직에서 공통으로 관심이 있는 공통 관심사이다.
- 이런 공통 관심사는 필터나 인터셉터를 이용해 처리하는 것이 좋다.
- 필터는 요청이 서블릿과 컨트롤러로 넘어가기 전에 적용된다.
- 따라서 필터에 걸리는 경우 서블릿까지 넘어가지 않는다.

### Filter 구현
- `Filter` 인터페이스의 `doFilter`를 구현하면 된다.
- 이때 중요한 것은 필터내에서 반드시 `chanin.doFilter()`를 호출해야 나머지 필터가 실행된다.
- `@Configuration`으로 `WebMvcConfigurer` 구현한 클래스를 컨피그로 만들고 `FilterRegistrationBean`을 통해 등록하면 된다.
  ```java
  @Configuration
  public class WebConfig implements WebMvcConfigurer {
  
  ...

  @Bean
  public FilterRegistrationBean loginCheckFilter() {
    FilterRegistrationBean<Filter> filterRegistrationBean = new FilterRegistrationBean<>();
    filterRegistrationBean.setFilter(new LoginCheckFilter());
    filterRegistrationBean.setOrder(2);
    filterRegistrationBean.addUrlPatterns("/*");

    return filterRegistrationBean;
  }
  
  ```
- 이때 `addUrlPatterns`에서 특정 패턴만 등록해도 된다. 하지만 이럴 경우 미래에 추가될 패스에 적용할 수 없으므로 필터내에서 화이트 리스트 처리를 해주는 것이 좋다.
- 필터는 재귀적으로 수행되므로 순서가 A -> B 라면 B가 끝났을 때 A의 `chain.doFilter()` 이후 부분이 수행된다.
- 미인증된 사용자는 `chain.doFilter()`로 진행하지 않고 로그인 필터 내에서 리턴해서 끝내버리면 된다.

## Interceptor
- 서블릿 필터와 같이 웹과 관련된 공통 관심 사항을 효과적으로 해결할 수 있는 기술이다.
- 서블릿 필터가 서블릿이 제공하는 기술이라면, 스프링 인터셉터는 스프링 MVC가 제공하는 기술이다. 서블릿 필터와는 적용 순서, 범위, 사용 방법이 다르다.
- 스프링 인터셉터는 서블릿과 컨트롤러 호출 직전에 호출 된다.
- 인터셉터에서 적절하지 않은 요청이라고 판단하면 컨트롤러 호출 전에 끝낼 수 있다.
- 서블릿 필터보다 편리하고 정교하고 다양한 기능을 지원한다.

### 인터페이스
- `HandlerInterceptor` 인터페이스를 구현하면 된다.
- `preHandle`: 컨트롤러 호출 전
- `postHandle`: 컨트롤러 호출 후
- `afterCompletion`: 요청 완료 이후
- `postHandle`은 컨트롤러에서 예외가 발생하면 호출되지 않는다. 하지만 `afterCompletion`은 항상 호출된다. 이 경우 예외를 파라미터로 받아서 어떤 예외가 발생했는지 로그로 출력할 수 있다. 정상 흐름에서는 예외가 null이다.

### Interceptor 구현
- `@Configuration`으로 `WebMvcConfigurer` 구현한 클래스를 컨피그로 만들고 `addInterceptors`를 오버라이드한다.
  ```java
  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(new LoginCheckInterceptor())
          .order(2)
          .addPathPatterns("/**")
          .excludePathPatterns("/", "/members/add", "/login", "/logout",
                  "/css/**", "/*.ico", "/error");
  }
  ```

### 핸들러간 변수 공유하기
- `request.setAttribute`를 통해 공유하면 된다.
- `LogInterceptor`는 싱글톤처럼 사용되기 때문에 멤버변수를 사용하면 위험하다.

### path pattern
- https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/util/pattern/PathPattern.html

## Argument Resolver
- 컨트롤러에서 argument에 애노테이션을 붙여 간단하게 처리할 수 있다.
  - before
    ```java
    public String homeLoginV3Spring(
            @SessionAttribute(name = SessionConst.LOGIN_MEMBER, required = false) Member loginMember, Model model) {
    ```
  - after
    ```java
    @GetMapping("/")
    public String homeLoginV3ArgumentResolver(@Login Member loginMember, Model model) {
    ```
- `@Login` 애노테이션을 구현한다.
- `HandlerMethodArgumentResolver`를 구현한 클래스를 구현한다.
- `supportsParameter`가 true를 반환하면 `resolveArgument`가 수행된다.
- `Webconfig`에서 argument resolver를 추가하면 된다.
  ```java
  @Override
  public void addArgumentResolvers(List<HandlerMethodArgumentResolver> resolvers) {
      resolvers.add(new LoginMemberArgumentResolver());
  }
  ```
