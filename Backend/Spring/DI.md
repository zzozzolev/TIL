## 동적으로 bean을 선택해야할 때
- 멤버 변수로 `Map<String, Type>` 혹은 `List<Type>`을 이용해 의존 관계를 주입할 수 있다.
- 스프링이 알아서 해당 타입의 빈을 등록해준다.