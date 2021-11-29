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
