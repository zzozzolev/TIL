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
- computer, instance, or container running the Kafka process.
- manage partitions.
- handle write and read requests.
- manage replication of partitions.
- intentionally very simple.
