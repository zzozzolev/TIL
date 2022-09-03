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

## Day 9: Kafka Streams
- Functional JAVA API.
- Filtering, grouping, aggregating, joining, and more.
- Scalable, fault-tolerant state management.
- Scalable computation based on Consumer Groups.
  - kafka streams 어플리케이션은 컨수머 그룹이다.
- Integrates within your services as a library.
  - infra가 아님.
- Runs in the context of your application.
- Does not require special infrastructure.

## Day 10: ksqlDB
- A database optimized for stream processing.
- Runs on its own scalable, fault-tolerant cluster adjacent to the Kafka cluster.
- Stream processing programs written in SQL.
- 단, RDB를 대체하는 용도로 사용하면 안 된다.

## Day 26 Schema Registry
- Server process external to Kafka brokers.
- Maintains a database of schemas.
- HA deployment option available.
- Consumer/Producer API component.
- Defined schema compatibility rules per topic.
- Producer API prevents incompatible messages from being produced.
- Consumer API prevents incompatible messages from being comsumed.
- 소규모 시스템이 아니면 schema registry는 필수이다.

### Supported Formats
- JSON Schema
- Avro
- Protocol Buffers

## Day 27 Why Avro?
- we have found Apache Avro to be one of the better choices for stream data.

### Why Use Avro with Kafka?
- Confluent Platform works with any data format you prefer, but we added some special facilities for Avro because of its popularity.
- 예시
  ```json
  {
    "time": 1424849130111,
    "customer_id": 1234,
    "product_id": 5678,
    "quantity":3,
    "payment_type": "mastercard"
  }

  {
    "type": "record",
    "doc":"This event records the sale of a product",
    "name": "ProductSaleEvent",
    "fields" : [
      {"name":"time", "type":"long", "doc":"The time of the purchase"},
      {"name":"customer_id", "type":"long", "doc":"The customer"},
      {"name":"product_id", "type":"long", "doc":"The product"},
      {"name":"quantity", "type":"int"},
      {"name":"payment",
       "type":{"type":"enum",
  	     "name":"payment_types",
               "symbols":["cash","mastercard","visa"]},
       "doc":"The method of payment"}
    ]
  }
  ```
- The schemas protect downstream data consumers from malformed data, as only valid data will be permitted in the topic.

### The Need For Schemas
- Schemas—when done right—can be a huge boon, keep your data clean, and make everyone more agile.
- Robustness: One of the primary advantages of this type of architecture where data is modeled as streams is that applications are decoupled.
- Clarity and Semantics: Keeping an up-to-date doc string for each field means there is always a canonical definition of what that value means.
- Compatibility: Schemas make it possible for systems with flexible data format like Hadoop or Cassandra to track upstream data changes and simply propagate these changes into their own storage without expensive reprocessing.
- Schemas are a Conversation: Unlike an application’s database, the writer of the data is, almost by definition, not the reader.
- Schemas Eliminate The Manual Labor of Data Science: they do give a tool by which you can enforce a standard like this.

### Back to Avro
- It has a pure JSON representation for readability but also a binary representation for efficient storage.
- Effective Avro
  - Use enumerated values whenever possible instead of magic strings.
  - Require documentation for all fields.
  - Avoid non-trivial union types and recursive types.
  - Enforce reasonable schema and field naming conventions.

## Day 34 Schema Compatibility Evolution
### Schema Evolution
- After the initial schema is defined, applications may need to evolve it over time.
- Without thinking through data management and schema evolution carefully, people often pay a much higher cost later on.
- When using Avro or other schema formats, one of the most important things is to manage the schemas and consider how these schemas should evolve.
- Schema compatibility checking is implemented in Schema Registry by versioning every single schema.

### Backward Compatibility
- `BACKWARD` compatibility means that consumers using the new schema can read data produced with the last schema.

### Forward Compatibility
- `FORWARD` compatibility means that data produced with a new schema can be read by consumers using the last schema, even though they may not be able to use the full capabilities of the new schema.

### Full Compatibility
- `FULL` compatibility means schemas are both backward and forward compatible. Schemas evolve in a fully compatible way.

### No Compatibility Checking
- `NONE` compatibility type means schema compatibility checks are disabled.
- Sometimes we make incompatible changes. For example, modifying a field type from `Number` to `String`.

### Transitive Property
- If compatibility is configured as transitive, then it checks compatibility of a new schema against all previously registered schemas; otherwise, it checks compatibility of a new schema only against the latest schema.

### Order of Upgrading Clients
- `BACKWARD` or` BACKWARD_TRANSITIVE`: Upgrade all consumers before you start producing new events.
- `FORWARD` or `FORWARD_TRANSITIVE`: First upgrade all producers to using the new schema and make sure the data already produced using the older schemas are not available to consumers, then upgrade the consumers.
- `FULL` or `FULL_TRANSITIVE`: You can upgrade the producers and consumers independently.

## Day 37 Basic Operations
### Event Streams
- 같은 키를 가져도 서로 다른 이벤트이다.
- Mapping으로 각각의 이벤트에 함수를 적용할 수 있다. map 보다는 mapvalues가 더 좋다.
- Filtering으로 원하는 값만 아웃풋으로 받을 수 있다.

## Day 38 KTable
- 같은 키를 가진 이벤트를 업데이트한다.
- KStream과 달리 한 번에 하나의 토픽만 구독할 수 있다.
- 최신 상태를 저장한다.
- KTable에서는 어떤 이벤트가 들어왔는지 보다는, 키의 최신 상태가 무엇인지를 신경쓴다.
- global KTable은 일반 KTable과는 달리 모든 파티션에 걸친 레코드들을 가지고 있는다.

## Day 39 Serialization
- Serdes: Serializer/Deserializer
- 미리 존재하는 serdes가 있다.

## Day 40 Joins
- Kafka Streams offers join operations.
- Stream-Stream joins.
  - Combine two event streams into a new event stream.
  - Join of events based on a common key.
  - Records arrive within a defined window of time.
  - Possible to compute a new value type.
  - Keys are available in read-only mode can be used in computing the new value.
- Stream-Table joins.
  - KStream-KTable.
  - KStream-GlobalKTable.
- Table-Table joins.
