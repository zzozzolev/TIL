## 예외 발생과 오류 페이지 요청 흐름
```
WAS <- 필터 <- 서블릿 <- 인터셉터 <- 컨트롤러(예외 발생)
WAS 에러 페이지 다시 요청 -> 필터 -> 서블릿 -> 인터셉터 -> 컨트롤러(에러 페이지) -> View
```
- 필터, 인터셉터를 한 번 더 거치므로 비효율적이다.
  - 필터는 디폴트로 클라이언트 요청이 있는 경우에만 적용된다.
  - 인터셉터는 오류 페이지 앤드포인트를 제외하면 된다.
- 이때, `DispatcherType`으로 클라이언트 요청인지 오류 핸들링 요청인지 구분할 수 있다.
  - `REQUEST`: 클라이언트 요청
  - `ERROR`: 오류 요청
  - `FORWARD`: 서블릿에서 다른 서블릿이나 JSP 요청
  - `INCLUDE`: 서블릿에서 다른 서블릿이나 JSP 결과를 포함할 때
  - `ASYNC`: 서블릿 비동기 호출

## ExceptionResolver
- `ExceptionResolver`를 사용하면 컨트롤러에서 예외가 발생해도 `ExceptionResolver`에서 예외를 처리한다.
- 예외가 발생해도 서블릿 컨테이너까지 예외가 전달되지 않고 스프링 MVC에서 예외 처리는 끝이 난다.
- 결과적으로 WAS 입장에서는 정상 처리가 된다. 예외를 이곳에서 모두 처리할 수 있다는 게 핵심이다.

## 스프링이 제공하는 ExceptionResolver
- `HandlerExceptionResolverComposite`에 다음 순서로 등록
1. `ExceptionHandlerExceptionResolver`
2. `ResponseStatusExceptionResolver`
  - 예외에 따라서 HTTP 상태 코드를 지정해주는 역할을 한다.
  - `@ResponseStatus`가 달려있는 예외, `ResponseStatusException` 예외
3. `DefaultHandlerExceptionResolver`

## 체크 예외 활용
### 기본 원칙
- 기본적으로 언체크(런타임) 예외를 사용하자.
- 체크 예외는 비즈니스 로직상 의도적으로 던지는 예외에만 사용하자.
  - 이 경우 해당 예외를 잡아서 반드시 처리해야 하는 문제일 때만 체크 예외를 사용해야 한다.
  - 체크 예외 예시
    - 계좌 이체 실패 예외
    - 결제시 포인트 부족 예외
    - 로그인 ID, PW 불일치 예외

### 체크 예외의 문제점
- 컨트롤러, 서비스에서는 DB, 네트워크 같은 시스템 레벨의 예외(`SQLException`, `ConnectException`)가 올라와도 처리할 방법이 없다.
- 서비스는 처리할 수 없어 밖으로 던지고, 컨트롤러 역시 처리할 수 없기 때문에 밖으로 던져야한다.
- 이런 문제들은 보통 사용자에게 에러 메세지로 설명을 남기기 어렵다. `서비스에 문제가 있습니다.` 정도가 최선이다.
