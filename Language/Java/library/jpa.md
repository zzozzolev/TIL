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
  - 단, `CascadeType.ALL` 엔티티들은 persist를 직접하는 엔티티에서만 사용하거나 다른 엔티티에서 참조하지 않을 때만 사용한다. 만약 이렇다면 별도의 repository를 생성해서 관리한다.
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

## protected 기본 생성자
- setter가 필요한 엔티티에서 별도의 생성 메서드를 정의했다면 기본 생성자를 막아야한다.
- 기본 생성자를 이용하는 코드가 생겨나면 유지보수가 어렵기 때문이다.
- JPA에서는 `protected`이면 사용하지 말라는 의미이므로 `protected` 기본 생성자를 만들어준다.
- lazy 로딩에서 해당 클래스를 상속한 proxy 객체의 생성이 필요하기 때문에 `public` 혹은 `protected` 기본생성자가 필요하다.

## 변경감지와 머지
- 트랜잭션내에서 객치에 변화가 있으면 JPA가 알아서 변경을 감지하고 업데이트 쿼리를 날린다. 이를 dirty checking이라고 한다.

### 준영속 엔티티
- 영속성 컨텍스트가 더는 관리하지 않는 엔티티
- 이미 DB에 저장돼 식별자가 존재한다.
- 코드 상에서는 새로 생성한 객체이지만 기존 식별자를 가지고 있으면 준영속 엔티티이다.

### 변경 감지 (Dirty Checking)
- 영속성 컨텍스트에서 엔티티를 다시 조회한 후에 데이터를 수정한다.
- 트랜잭션 안에서 엔티티를 다시 조회하고 값을 변경하면 토랜잭션 커밋 시점에 dirty checking이 발생해 데이터 베이스에 UPDATE SQL을 실행한다.
```java
@Transactional
void update(Item param) {
    Item foundItem = em.find(Item.class, param.getId());
    foundItem.setPrice(param.getPrice());
}
```
- 실무에서 엔티티를 변경할 때는 항상 변경 감지를 사용한다.
- 컨트롤러에서 엔티티를 생성하지 않고 트랜잭션이 있는 서비스 계층에 식별자와 변경할 데이터를 명확하게 전달하는 게 좋다. (파라미터 or DTO)
- 트랜잭션에서 엔티티를 조회해야 영속 상태로 조회가 된다.

### 병합 (merge)
- 준영속 상태의 엔티티를 영속 상태로 변경할 때 사용하는 기능이다.
- `변경 감지`에서 하나씩 했던 코드를 한 줄로 표현한다.
```java
@Transactional
void update(Item param) {
    Item mergeItem = em.merge(item);
}
```
- 동작 방식
  1. 준영속 엔티티의 식별자 값으로 영속 엔티티를 조회한다.
  2. 영속 엔티티의 값을 준영속 엔티티 값으로 모두 교체한다. (병합)
  3. 트랜잭션 커밋 시점에 변경 감지 기능이 동작해서 데이터베이스에 UPDATE SQL이 실행
- 주의할 점은 변경 감지 기능을 사용하면 원하는 속성만 선택해서 변경할 수 있지만, 병합을 사용하면 모든 속성이 변경된다. 만약 병합시 값이 없으면 `null`로 업데이트 할 수 있다. 그래서 실무에서는 많이 쓰이지 않는다.

## 일급 컬렉션
- 컬렉션을 래핑하면서 그 외 다른 멤버 변수가 없는 상태를 일급 컬렉션이라고 한다.
- `@Embedded`로 감싸면 사용은 할 수 있지만 JPQL 작성, 개발시 객체를 한 번 더 거쳐야하는 불편함들이 있다.
- 그래서 실용적인 관점에서 일급 컬렉션을 잘 사용하지 않는다고 한다. (영한님)
- 하지만 사용하는 것이 나쁜 것은 아니므로 트레이드 오프를 고려해서 적절하게 사용하면 된다.
- 비즈니스 로직이 단순하면 일급 컬렉션이 큰 의미가 없고 비즈니스 로직이 매우 복잡하다면 사용하면 된다.

## 컬렉션 fetch join
- 1:N 관계에서 N에 fetch join을 하면 N만큼 결과가 중복된다. 예를 들면 주문에 주문 아이템 여러개가 있을 때, 똑같은 주문이 주문 아이템만큼 중복된다. 그래서 가져오는 데이터 양이 필요한 양보다 더 많아질 수 있다.
- 이때 JPQL로 `distinct`를 해주면 JPA에서 SQL에 `distinct`를 추가하고 같은 id인 엔티티의 중복을 제거하고 하나만 반환해준다.
- 하지만, 단점은 **페이징이 불가능**해진다. 하이버네이트는 경고 로그를 남기면서 모든 데이터를 DB에서 읽어와 메모리에서 페이징을 한다. (메모리 사망...)
- 또한 컬렉션 fetch join은 1개만 사용할 수 있다. 컬렉션 둘 이상에 페치 조인을 사용하면 안 된다. 데이터가 부정합하게 조회될 수 있다. (1:N:M)

## 페이징 + 컬렉션 엔티티 조회하기
- ToOne (OneToOne, ManyToOne) 관계는 모두 페치조인한다. 
  - ToOne 관계는 로우 수를 증가시키지 않으므로 페이징 쿼리에 영향을 주지 않는다.
- 컬렉션은 지연 로딩으로 조회한다.
- 지연 로딩 성능 최적화를 위해 `hibernate.default_batch_fetch_size`, `@BatchSize`를 적용한다. 컬렉션이나 프록시 객체를 한꺼번에 설정한 size 만큼 IN 쿼리로 조회한다.
  - `hibernate.default_batch_fetch_size`: 글로벌 설정
  - `@BatchSize`: 개별 최적화
    - ToMany(컬렉션)는 멤버 레벨에서, ToOne은 클래스 레벨에서 어노테이션을 사용한다.

### default_batch_fetch_size
- `default_batch_fetch_size`를 지정하면, 지정한만큼 N 관계에 있는 엔티티를 해당 값만큼 1번의 in 쿼리로 가져온다. 만약 엔티티 개수가 해당 값보다 크면 반복해서 가져온다.
  - 예를 들어, `default_batch_fetch_size`가 10이라면 10번의 쿼리가 나가는 것이 아니라 `in (id1 , id2, ...)` 이런 식으로 in 쿼리 하나가 나간다. 만약 엔티티 개수가 100개라면 10개의 엔티티를 10번의 in 쿼리로 가져온다.
- 장점
  - 쿼리 호출 수가 1 + N에서 1 + 1로 최적화된다. (단, batch fetch size 보다 크면 1보다 클 수 있음)
  - fetch join보다 DB 데이터 전송량이 줄어든다.
  - 페이징이 가능하다.
- 크기
  - 100 ~ 1000 사이를 선택하는 것을 권장한다. DB에 따라 다르지만 IN 절 파라미터를 1000으로 제한하기도 하기 때문이다.
  - 크기를 크게 잡으면 DB와 애플리케이션에 순간적으로 부하를 많이 일으킨다. 하지만 적게 가져오더라도 애플리케이션에는 전체 데이터를 로딩해야하므로 메모리 사용량이 같다.
  - 그래서 순간 부하를 어디까지 견딜 수 있는지로 결정하면 된다.

## 엔티티 조회하기
- ToOne 관계는 fetch join으로 쿼리 수를 줄이고 나머지는 `hibernate.default_batch_fetch_size`로 해결하면 된다.

## 권장 순서
1. 엔티티 조회 방식으로 우선 접근
  1. 페치조인으로 쿼리 수를 최적화
  2. 컬렉션 최적화
    1. 페이징 필요: `default_batch_fetch_size`, `@BatchSize`로 최적화
    2. 페이징 필요X -> fetch join 사용
2. DTO 조회 방식 사용
3. NativeSQL or 스프링 JDBC Template