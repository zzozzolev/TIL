## 소개
- annotation을 통해 코드를 자동으로 완성해주는 라이브러리

## @RequiredArgsConstructor
- `final`이 붙은 멤버 변수들을 파라미터로 받는 생성자를 만들어준다.
    ```java

    @RequiredArgsConstructor
    public class A {
        private final Member1 mem1;
        private final Member2 mem2;
    }
    ```
    - 위의 예제에 아래와 같은 코드 자동 생성
    ```
    public A(Member1 mem1, Member2 mem2) {
        this.mem1 = mem1;
        this.mem2 = mem2;
    }
    ```