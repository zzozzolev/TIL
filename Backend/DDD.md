## Reasons to Model Identity as a Value Object
- https://buildplease.com/pages/vo-ids/
- indentity의 타입을 바꿔야할 때, 엔티티를 참조하는 엔티티의 레퍼런스를 건드릴 필요가 없다.
  - 예를 들어, 처음에 `long` 으로 했다가 `int`로 바꿔야 한다고 했을 때 전혀 영향을 받지 않는다.
- invaild한 밸류가 설정되는 걸 막을 수 있다.
  - 예를 들어, 아이덴티티가 0보다 작게 설정되지 않아한다면 생성자에 이 조건을 넣으면 된다.
- 타입의 같은 다른 엔티티의 ID를 실수로 넣는 것을 방지한다.
  - 예를 들어, 오더의 ID도 `int`이고 프로덕트의 ID도 `int`일 때, 실수로 프로덕트의 ID에 오더의 ID를 넣는 일을 막을 수 있다.
