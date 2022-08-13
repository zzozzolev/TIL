## Reasons to Model Identity as a Value Object
- https://buildplease.com/pages/vo-ids/
- indentity의 타입을 바꿔야할 때, 엔티티를 참조하는 엔티티의 레퍼런스를 건드릴 필요가 없다.
  - 예를 들어, 처음에 `long` 으로 했다가 `int`로 바꿔야 한다고 했을 때 전혀 영향을 받지 않는다.
- invaild한 밸류가 설정되는 걸 막을 수 있다.
  - 예를 들어, 아이덴티티가 0보다 작게 설정되지 않아한다면 생성자에 이 조건을 넣으면 된다.
- 타입의 같은 다른 엔티티의 ID를 실수로 넣는 것을 방지한다.
  - 예를 들어, 오더의 ID도 `int`이고 프로덕트의 ID도 `int`일 때, 실수로 프로덕트의 ID에 오더의 ID를 넣는 일을 막을 수 있다.

## Domain services vs Application services
- 이들 사이의 주요 차이점은 **도메인 서비스는 도메인 로직을 보유**하지만 애플리케이션 서비스는 보유하지 않는다는 것이다.
- 도메인 서비스는 엔터티 및 VO와 동일한 방식으로 의사 결정 프로세스에 참여한다.
- 애플리케이션 서비스는 엔터티 및 VO가 내린 결정을 오케스트레이션하는 것과 같은 방식으로 이러한 결정을 오케스트레이션한다.

### 참고
- [Domain services vs Application services](https://enterprisecraftsmanship.com/posts/domain-vs-application-services/)
