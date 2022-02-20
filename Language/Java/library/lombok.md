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

## @Data vs @Value
- `@Value`는 immutable objects를 만드는데 쓰인다.
- `@Value`는 `@Data`와 달리 `@Setter` 어노테이션을 포함하지 않는다.

## @Getter @Setter 사용 시 주의점
- 실무에서 `@Getter`는 모두 사용하는 것이 편리하다.
- 하지만 `@Setter`는 무분별하게 사용하면 변경지점을 추적하기 힘들다.
- 따라서 엔티티 변경 시 `@Setter`를 이용하기보다는 별도의 메서드를 제공하는 게 좋다.
- 단, 멤버 중 collections가 있을 때는 Getter를 이용해 수정을 할 수 있다. get 했을 때 컬렉션이 반환되는데 컬렉션 자체에서 변경 메서드를 제공하기 때문이다.
  ```java
  class Member {
      private List<Order> orders;
  }

  public void setMember(Member member) {
      this.member = member;
      member.getOrders().add(this); // add는 변경 메서드
  }
  ```
- 이는 Getter가 Setter처럼 쓰일 수 있으므로 변경 지점을 늘리는 것이다. 이는 JPA 사용시 한계점이다. 문제를 해결하기 위해서는 일급 컬렉션이라는 객체를 도입해야하는데 JPA에서는 어렵다고 한다. (갓영한님이 그러셨음... 자세한 건 [여기](https://www.inflearn.com/questions/359389) 참고) 

## @NoArgsConstructor
- argument가 없는 기본 생성자를 생성한다.
- `access`로 액세스 레벨을 설정할 수 있다.
- 아래는 `protected` 기본 생성자를 만드는 예시이다.
    ```java
    @NoArgsConstructor(access = AccessLevel.PROTECTED)
    ```

## @Builder
- 클래스에 builder 패턴을 적용할 수 있도록 해준다.
- 아래는 delombok으로 파악한 코드이다.
- `builder`라는 스태틱 메서드를 추가하고 호출하면 `<Class>Builder` 인스턴스를 생성한다.
  ```java
    public static ArticleBuilder builder() {
        return new ArticleBuilder();
    }
    ```
- `<Class>Builder`는 원래 클래스의 멤버를 그대로 가진다. 그리고 멤버 이름의 체이닝 메서드를 생성한다.
    ```java
    public static class ArticleBuilder {
        private Profile author;

        public ArticleBuilder author(Profile author) {
            this.author = author;
            return this;
        }
        ...
    ```
- `build` 메서드는 다시 원래 클래스의 생성자를 호출한다. 이때 원래 클래스의 생성자에서 인자로 받는 걸 체이닝 메서드에서 지정한 값 그대로 넘겨준다.
    ```java
    public class Article {
        public Article(Profile author, String title, String body, String description, Slugify slugify, int size, int maxSize) {
    }

    public static class ArticleBuilder {
        public Article build() {
            return new Article(author, title, body, description, slugify, size, maxSize);
        }
    }
    ```
