## 소개
- annotation을 통해 코드를 자동으로 완성해주는 라이브러리
- 자바의 annotation processor라는 기능을 이용해 컴파일 시점에 생성자 코드를 자동으로 생성해준다.

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

## @Data
- `@Getter`, `@Setter`, `@ToString`, `@EqualsAndHashCode`, `@RequiredArgsConstructor`를 자동으로 적용해준다.