## Day 2: Events
- 카프카내의 이벤트는 key, value 페어로 모델링된다.
- 카프카는 내부적으로 losely typed, 하지만 외부인 프로그래밍 언어에서는 그렇지 않다.
  - serialized(json, pb...) <-> deserialized
- 카프카의 key는 DB pk 같은 역할을 하지 않는다. 오히려 시스템내의 엔티티를 구분하는 역할을 한다.
  - user, order

## Day 3: Topics
- Named container for similar events.
  - Systems contain lots of topics.
  - Can duplicate data between topics.
- Durable logs of events.
  - Append only.
  - Can only seek by offset, not indexed.
- Events are immutable.
- retention period is configurable.

## Day 4: Partitioning
- 토픽을 여러 토픽으로 쪼개서 카프카 클러스터 내의 별도의 노드에 저장할 수 있다.
- 메세지에 키가 없다면 라운드 로빈으로 파티션에 할당한다. 키가 있다면 해당 키를 이용해 어떤 파티션에 넣을지 결정한다.
- 같은 키를 가지는 메세지는 항상 같은 파티션에 있다. 따라서 항상 정렬된 순서로 들어간다.

## Day 5: Brokers
- Computer, instance, or container running the Kafka process.
- Manage partitions.
- Handle write and read requests.
- Manage replication of partitions.
- Intentionally very simple.

## Day 6: Producers
- Client application.
- Puts messages into topics.
- Connection pooling.
- Network buffering.
- Partitioning.
  - 메세지를 어떤 파티션에 보낼지 결정한다.

## Day 7: Consumers
- Client application.
- Reads messages from topics.
- Connection pooling.
- Network protocol.
- Horizontally and elastically scalable.
- Maintains ordering within partitions at scale.
- 서로 다른 컨수머 그룹이 하나의 토픽을 읽을 수 있다.
- 파티션 내에서의 순서는 보장하지만, 파티션 간의 순서는 보장하지 않는다.
- 같은 컨수머 그룹 내의 여러 컨수머 인스턴스는 서로 다른 파티션을 읽도록 만든다. (rebalancing process)
- rebalancing process는 컨수머 그룹 인스턴스를 추가하거나 제거할 때마다 반복한다.
- 이 과정은 기본적으로 일어난다. API 레벨에서 해줄 건 없다.
- 파티션 개수보다 더 많은 인스턴스가 추가되면 해당 인스턴스는 idle한 상태가 된다 왜냐하면 어떤 파티션도 할당되지 않기 때문이다.
- horizontal scale과 strongest ordering guarantee를 보장할 수 있다.

## Day 8: Kafka Connect
### Kafka Connect
- Data integration system and ecosystem.
- Because some other systems are not kafka.
- External client process; does not run on Brokers.
- Horizontally scalable.
- Fault tolerant.
- Declarative.
  - 카프카 커넥트를 통해 유저가 직접 코드를 작성하지 않고 config 파일만 작성하면 된다.

### Connectors
- Pluggable software component.
- Interfaces to external system and to Kafka.
- Also exist as runtime entities.
- Source connectors act as Producers.
- Sink connectors act as Consumers.
