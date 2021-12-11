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
- 하지만 도메인에 사용하는 걸 권장하지 않는다.

## @Getter @Setter 사용 시 주의점
- 실무에서 `@Getter`는 모두 사용하는 것이 편리하다.
- 하지만 `@Setter`는 무분별하게 사용하면 변경지점을 추적하기 힘들다.
- 따라서 엔티티 변경 시 `@Setter`를 이용하기보다는 별도의 메서드를 제공하는 게 좋다.

## @NoArgsConstructor
- argument가 없는 기본 생성자를 생성한다.
- `access`로 액세스 레벨을 설정할 수 있다.
- 아래는 `protected` 기본 생성자를 만드는 예시이다.
    ```java
    @NoArgsConstructor(access = AccessLevel.PROTECTED)
    ```
