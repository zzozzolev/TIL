## MVC 패턴
- 모델, 뷰, 컨트롤러
- 비즈니스 로직과 뷰 로직을 분리한다.
- 컨트롤러가 리퀘스트 파라미터에 대한 검증을 끝내고 서비스나 리포지토리를 호출한다.
- 서비스에서 비즈니스 로직을 수행하고 리포지토리를 통해 데이터를 접근한다.
- 컨트롤러에서는 이 결과를 받아서 모델에 전달한다.

## 프론트 컨트롤러 패턴
- 클라이언트의 요청을 하나의 컨트롤러에서 받는다.
- 공통 로직을 프론트 컨트롤러에서 할 수 있다.
- 따라서 각각의 컨트롤러에서 중복된 로직을 줄일 수 있다.

## 뷰 리졸버
- 각각의 컨트롤러에서는 뷰의 논리적 이름만 반환한다.
- 그렇지 않다면 물리적 이름(전체 경로)이 변경됐을 때, 모든 컨트롤러를 변경해야하기 때문이다.
- 뷰 리졸버에서는 논리적 이름을 물리적 이름으로 바꾼다.

## 어댑터 패턴
- 클래스의 인터페이스를 사용자가 기대하는 다른 인터페이스로 변환하는 패턴이다.
- 호환성이 없는 인터페이스 때문에 함께 동작할 수 없는 클래스들이 함께 작동하도록 해준다.
- 서로 다른 컨트롤러를 어댑터 패턴을 이용해 프론트 컨트롤러에서 공통적으로 이용할 수 있다.
- 즉, 프론트 컨트롤러는 컨트롤러를 직접 사용하지 않고 어댑터를 통해서 사용한다.

## 도메인 모델 패턴 vs 트랜잭션 스크립트 패턴
- 엔티티가 비즈니스 로직을 가지고 있고 서비스 계층은 단순히 엔티티에 필요한 요청을 위임하는 역할을 하는 것을 말한다.
- 반대로 엔티티에 비즈니스 로직이 거의 없고 서비스 계층에서 비즈니스 로직을 처리하는 것을 트랜잭션 스크립트 패턴이라고 한다.
- 어느 하나가 좋은 것은 아니고 문맥에 따라 적절하게 사용해야한다. 두 가지가 양립할 수도 있다.

## 애플리케이션 서비스 vs 도메인 서비스
### 애플리케이션 서비스
- DB에서 데이터를 얻음.
- 도메인 모델을 업데이트 함.
- 변경된 내용을 영속화함.

### 도메인 서비스
- 도메인 모델에 속하지만 상태가 있는 엔티티나 value object에 속하지 않는 로직

## 이벤트 vs 커맨드
|   | 이벤트 | 커맨드 |
| --- | --- | --- |
| 이름 | 과거형 | 명령형 |
| 오류 처리 | (송신하는 쪽과) 독립적으로 실패하고 나머지 핸들러 계속 | (송신하는 쪽에 오류를 돌려주면서) 시끄럽게 실패함
| 받는 행위자 | 모든 리스너 | 정해진 수신자 |
| 핸들러 | 여러 핸들러 가능 | 핸들러 하나 |

- 커맨드는 한 애그리게이트를 변경. atomic 유지해야함.
- 커맨드가 성공하기 위해 이벤트가 성공하지 않아도 됨.
