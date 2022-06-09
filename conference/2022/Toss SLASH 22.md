## 지속 성장 가능한 코드를 만들어가는 방법
- https://toss.im/slash-22/sessions/1-6
- https://www.youtube.com/watch?v=RVO02Z1dLF8

### 생성자
- 의존하는 클래스를 확인할 수 있다.
- 해당 클래스가 무슨 일을 하는지 힌트를 줄 수 있다.

### 패키지 구성
- 역할보다는 개념으로 응집시켜야 불필요한 import를 줄일 수 있음.

### 레이어
- 토스 페이먼츠 표준 레이어
  - Presentation Layer
  - Business Layer
  - Implement Layer
  - Data Access Layer
- 레이어는 위에서 아래로 순방향으로만 참조돼야한다.
- 레이어의 참조 방향이 역류되지 않아야한다.
- 레이어를 건너뛰지 않는다. ex) Buisiness Layer -> Data Access Layer

### 모듈의 분리
- 라이브러리에 대한 부분을 격리해 사용한다면, 비즈니스 로직에서 특정 라이브러리에 대한 import를 할 수 없다.
- 비즈니스 로직이 더 뚜렷해진다.
- 라이브러리 교체시 비즈니스 로직에 영향이 없다.
