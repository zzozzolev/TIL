## @PersistenceContext
- 해당 annotation이 있으면 스프링이 JPA 엔티티 매니저를 주입해준다.
- `EntityManager`를 인젝션하기 위해 필요하다. 단, 스프링 부트가 `@Autowired`로 인젝션되도록 지원을 해준다.

## EntityManager
- `flush`를 호출하면 영속성 컨텐스트에 있던 쿼리를 DB에 날린다.

## @Enumerated
- enum은 기본적으로 ORDINAL이 된다.
- 하지만 새로운 값이 들어가면 기존 값이 밀리고 DB에 해당 값이 새로운 값으로 덮어씌어질 수 있다.
  - 예를 들어 a, b -> a, c, b로 되면 기존에 b로 저장돼있던 게 c로 바뀐다.
- 따라서 무조건 `EnumType.STRING`으로 해야한다.

## @ManyToMany
- 실무에서는 권장하지 않는다.
- associative table에 컬럼을 추가할 수 없고 세밀한 쿼리 실행이 어렵다.
- associative table을 직접 만들고 `@ManyToOne`, `@OneToMany`로 매칭해서 사용하는 게 낫다.

## 값 타입
- 값 타입은 변경 불가능하게 설계해야한다.
- `@Setter`를 만들지 않고 생성자에서 값을 모두 초기화해서 변경 불가능한 클래스를 만들면 된다.
- JPA 스펙상 `@Entity`나 `@Embeddable`은 자바 기본 생성자를 `public` 또는 `protected`로 설정해야한다. `protected`가 그나마 낫다.
- 이런 제약이 있는 이유는 JPA 구현 라이브러리가 객체를 생성할 때 reflection 같은 기술을 사용할 수 있어야하기 때문이다.

## 엔티티 설계시 주의점
- 인티티에는 되도록 Setter를 사용하지 말자.
- 모든 연관관계는 지연 로딩(`LAZY`)으로 설정하자.
  - 어떤 SQL이 실행될지 추적하기 어렵다. 특히 JPQL을 실행할 때 N + 1 문제가 자주 발생한다.
  - 연관된 엔티티를 함께 DB에서 조회해야하면 fetch join 또는 엔티티 그래프 기능을 사용한다.
  - `@OneToOne`, `@ManyToOne` 관계는 기본이 즉시 로딩(`EAGET`)이므로 직접 지연 로딩으로 설정해야한다.
  - 예를 들어 `Order`에 `@ManyToOne`으로 `Member`가 있다고 해보자. 그러면 `select * from order`를 날려서 100개의 `Order`를 가져왔다면, 단 건으로 `Member`를 조회하는 100개의 쿼리가 수행된다.
- 컬렉션은 필드에서 초기화하자.
  - `null` 문제에서 안전하다.
  - 하이버네이트는 엔티티를 영속화할 때(`persist`), 컬렉션을 감사서 하이버네이트가 제공하는 내장 컬렉션으로 변경한다. 따라서 중간에 변경해버리면 원하는 대로 동작하지 않을 수 있다.
- 특정 패턴의 이름을 적용해야되면 테이블, 컬럼명 생성 전략을 이용하자.
  - `SpringPhysicalNamingStrategy`
  - 논리명 생성(`implicit-strategy`): 명시적으로 적지 않았을 때 `ImplicitNamingStrategy`을 사용한다.
  - 물리명 적용(`physical-strategy`): 모든 논리명에 적용된다.
- 엔티티 하나를 저장할 때 many 엔티티를 한 번에 저장하고 싶다면 `cascade = CascadeType.ALL`을 이용한다.
  - 예를 들어 `Order`와 `OrderItem`이 있을 때 `Order`를 한 번 `persist`할 때 `OrderItem`도 같이 `persist`하길 원한다면 사용한다.
    ```java
    // before
    persist(orderItem1);
    persist(orderItem2);
    persist(orderItem3);
    persist(order);

    // after
    persist(order);
    ```
- 양방향 관계일 때 원자적으로 필드를 셋팅하는 연관 관계 메서드를 지정해주면 좋다.
  - 예를 들면 `Order`와 `Member`가 있고 `Member`가 one `Order`가 many라고 해보자.
  - `Order`에 `Member`를 지정할 때 `Member`에 있는 `Order` list에도 추가해주는 것이 좋다. (DB 저장이 아님)
  - 하지만 별개로 처리한다면 어느 하나만 할 가능성이 있을 것이다.
  - 이럴 때 핵심적인 컨트롤을 담당하는 객체에 `연관 관계 메서드`를 지정해주면 실수를 줄일 수 있다.
    ```java
    class Order {
        ...
        public void setMember(Member member) {
            this.member = member;
            member.getOrders().add(this);
        }
    }
    ```
