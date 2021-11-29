## @Enumerated
- enum은 기본적으로 ORDINAL이 된다.
- 하지만 새로운 값이 들어가면 기존 값이 밀리고 DB에 해당 값이 새로운 값으로 덮어씌어질 수 있다.
  - 예를 들어 a, b -> a, c, b로 되면 기존에 b로 저장돼있던 게 c로 바뀐다.
- 따라서 무조건 `EnumType.STRING`으로 해야한다.

## @ManyToMany
- 실무에서는 권장하지 않는다.
- associative table에 컬럼을 추가할 수 없고 세밀한 쿼리 실행이 어렵다.
- associative table을 직접 만들고 `@ManyToOne`, `@OneToMany`로 매칭해서 사용하는 게 낫다.
