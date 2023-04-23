## Kinesis Data Firehose란?
- 리얼 타임 스트리밍 데이터를 S3, Redshift, custom HTTP endpoint등에 전달하는 완전 관리형 서비스.
- Kinesis Firehose는 Kinesis Streaming 데이터 플랫폼의 구성 중 하나이다.
- 데이터 프로듀서들을 Kinesis Data Firehose에 보내도록 설정하면 알아서 데이터가 목적지에 전달된다.
- 또한 전달하기 전 데이터 처리 작업도 설정할 수 있다.

## Key Concepts
### Kinesis Data Firehose delivery stream
- Kinesis Data Firehose의 기본 엔티티.
- Kinesis Data Firehose delivery stream을 만들고 데이터를 여기에 보내서 사용할 수 있다.

### record
- 데이터 프로듀서가 Kinesis Data Firehose delivery stream에 보내는 데이터.
- 레코드는 최대 1000KB까지 가능하다.

### data producer
- 프로듀서는 Kinesis Data Firehose delivery stream으로 레코드들을 보낸다.
- 예를 들어, delivery stream에 로그 데이터를 보내는 웹 서버는 데이터 프로듀서이다.

### buffer size and buffer interval
- Kinesis Data Firehose는 목적지에 전달하기 전에 특정 사이즈 혹은 특정 기간 동안 인커밍 스트리밍 데이터를 버퍼한다.
- Buffer Size는 MB 단위이고 Buffer Interval은 초단위이다.

## 참고 자료
- https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html

## Transform by lambda
### Buffer Size
- 특정 람다를 선택할 수 있음.
- 람다는 호출 페이로드 쿼타가 6MB임.
- 람다로 처리한 후에 데이터가 커질 수 있음.
- 버퍼 사이즈를 작게 할 수록 처리 이후 데이터가 커질 공간이 더 있음.

### Buffer Interval
- 람다를 호출하기 전에 인커밍 데이터를 버퍼하는 간격임.
- 람다는 버퍼 사이즈나 버퍼 인터벌에 도달하면 호출됨.

## AWS S3 for Destination
### Dynamic Partitioning
- 데이터 내부의 키를 사용해 스트리밍 데이터를 지속적으로 파티셔닝해 대응되는 S3 프리픽스로 전달하게 해준다.
- 자세한 건 다른 섹션 참고!

### S3 bucket prefix
- 다이나믹 파티셔닝을 사용하면 S3 에러 버킷 프리픽스가 필수이다.
- 만약 파이어호스에서 동적으로 파티셔닝 하는 게 실패하면, 실패한 데이터 레코드들은 S3 에러 버킷 프리픽스로 전달된다.
- 버킷 프리픽스는 기본적으로 `YYYY/MM/dd/HH` 포맷의 UTC 타임 프리픽스를 더한다. `/`마다 하이어아키에서 레벨을 추가한다.
- 커스텀 프리픽스를 사용하면 다르게 지정할 수 있다.
- 커스텀 프리픽스는 `!{namespace:value}` 형식으로 지정할 수 있다.
- `namespace`는 다음과 같다.
  - `firehose`
    - `error-output-type`: 에러 타입.
    - `random-string`: 길이 11의 랜덤 스트링. 여러 번 쓰이면 다른 랜덤이 된다.
  - `timestamp`
    - Java DateTimeFormatter 스트링이다.
    - timestamp를 평가할 때 가장 오래된 레코드의 추정 도착 시간을 사용한다.
    - 항상 UTC이다.
    - 같은 프리픽스에서 `timestamp`를 두 번 이상 사용하면 모두 같은 시간으로 평가된다.
  - `partitionKeyFromQuery`: 인라인 파싱으로 생성된 키를 사용할 때
  - `partitionKeyFromLambda`: 람다로 생성된 키를 사용할 때
- Prefix와 ErrorOutputPrefix에 대한 [시멘틱 룰](https://docs.aws.amazon.com/firehose/latest/dev/s3-prefixes.html)이 있으니 참고해야한다.
  - 프리픽스가 timestamp 네임스페이스 표현이 없으면 Prefix에 `!{timestamp:yyyy/MM/dd/HH/}`를 append 한다.

### Multi record deaggregation
- 딜리버리 스트림의 레코드를 파싱하고 valid json 혹은 지정된 new line 구분자를 기반으로 레코드를 분리하는 과정이다.
- 여러 이벤트, 로그, 레코드를 어그리게이트 해도 다이나믹 파티셔닝을 할 수 있다.
- 어그리게이트된 데이터로 다이나믹 파티셔닝을 해도 파이어호스는 레코드를 파싱할 수 있다.
- 소스가 키네시스 데이터 스트림이면 빌트인 어그리게이션으로 KPL을 사용할 수 있다.
- 따라서 각각의 API 호출 내의 각각의 레코드를 서로 다른 S3 프리픽스로 전달될 수 있다.
- **데이터가 어그리게이트됐다면 deaggregation 이후에만 다이나믹 파티셔닝을 할 수 있다. 그래서 multi record deaggreagation을 enable 해야한다.**
- 타입은 json이나 delimited 두 가지가 있다.

### New line delimiter
- 다이나믹 파티셔닝을 활성화 했을 때, S3로 전달되는 오브젝트의 레코드 사이에 new line delimiter를 추가하도록 할 수 있다.
- new line 없을 때
  ```
  {...} {...}
  ```
- new line 있을 때
  ```
  {...}
  {...}
  ```

### Inline parsing
- 다이나믹 파티셔닝을 할 수 있는 메커니즘 중 하나이다.
- 파티셔닝 키로 쓰이는 데이터 레코드 파라미터를 지정하고 지정된 파니셔닝 키에 대한 값을 제공해야한다.
- 파티셔닝 키를 만들기 위해 람다 파티셔닝과 inline parsing을 동시에 사용할 수 있다.

### S3 buffer hints
- 파이어호스는 지정된 destination에 전달하기 전에 인커밍 데이터를 버퍼한다.

## Backup Settings
- 파이어호스는 S3를 모든 혹은 실패된 데이터를 백업하는데 사용한다.
- S3, Redshift를 destination으로 설정하고 lambda로 처리를 하거나 나머지로 destination을 설정하면 백업을 설정할 수 있다.

## Converting Your Input Record Format in Kinesis Data Firehose
- format conversion은 destination이 S3일 때만 사용가능하다.

### Record Format Conversion Requirements
- A deserializer to read the JSON of your input data
  - 같은 record에 여러 개의 JSON 문서가 합쳐져 있을 때, single-line string만 허용한다.
  - array of json이나 multi-line string 허용하지 않는다.
  - 문서에는 OpenXJsonSerDe랑 Apache Hive JSON SerDe 중에 고르라고 하는데 콘솔에는 선택할 수 있는 게 없고 무조건 OpenXJsonSerde로 돼있다.
- A schema to determine how to interpret that data
  - AWS Glue Catalog를 사용한다.
  - 키네시스 데이터 파이어호스는 스키마를 레퍼런스하고 인풋 데이터를 해석하는데 사용한다.
- A serializer to convert the data to the target columnar storage format
  - Parquet or ORC

### Record Format Conversion Error Handling
- 키네시스 데이터 파이어호스가 레코드를 parse하거나 deserialize를 하지 못할 때, S3 error prefix에 쓴다.
  - 예를 들면, 데이터가 스키마에 맞지 않을 때
- **error prefix에 쓰는 게 실패하면 키네시스 데이터 파이어호스는 영원히 재시도해 더 이상의 딜리버리를 블록킹한다.**

## Amazon Kinesis Data Firehose Data Delivery
### Data Delivery Format
- S3에 데이터를 전달할 때, 키네시스 데이터 파이어호스는 딜리버리 스트림의 버퍼링 설정에 따라 여러 개의 인커밋 레코드들은 concat한다.
- 그 다음에 S3에 S3 object로 전달한다.

### Data Delivery Frequency
- 각각의 destination마다 각자의 data delivery frequency를 가진다.

#### Amazon S3
- frequency는 Buffer size와 Buffer interval로 결정된다.
- 두 조건 중 먼저 만족하는 것이 data delivery를 트리거한다.
- destination으로의 data delivery가 딜리버리 스트림으로의 쓰기보다 뒤처지면, 파이어호스는 동적으로 버퍼 사이즈를 늘린다.
- 그러면 캐치업 할 수 있고 모든 데이터를 destination으로 보낼 수 있다.

### Data Delivery Failure Handling
- 각각의 destination마다 각자의 data delivery failure handling을 가진다.

#### Amazon S3
- 다양한 이유로 data delivery가 실패할 수 있다.
- 파이어호스는 딜리버리가 성공할 때까지 24시간동안 재시도를 한다.
- 파이어호스의 최대 데이터 저장 시간은 24시간이다.
- **만약 data delivery가 24시간보다 오래되면 데이터가 유실된다.**


## Kinesis Data Streams
- 실시간으로 큰 데이터 레코드 스트림을 수집하고 처리할 수 있다.
- 로그 데이터, 애플리케이션 로그, 소셜 미디어, 마켓 데이터 피드, 웹 클릭 스트림 데이터에 쓰일 수 있다.

### Benefits
- 키네시스 데이터 스트림에 들어가는 데이터는 durability와 elasticity를 보장한다.
- 레코드가 스트림에 들어가고 얻는데는 보통 1초도 걸리지 않는다.
- 매니지드 서비스이기 때문에 data intake pipeline을 만들고 운영하는 부담을 덜어준다.
- elasticity는 스트림을 스케일 업하고 다운할 수 있기 때문에 만료되기 전에는 절대 데이터 레코드를 유실하지 않는다.
- 여러 애플리케이션이 하나의 스트림으로부터 컨숨할 수 있다.

### Terminology
- Kinesis Data Stream
  - a set of shards
  - 각각의 샤드는 데이터 레코드들의 시퀀스를 가진다.
  - 각각의 데이터 레코드는 키네시스 데이터 스트림에의해 할당된 sequence number를 가진다.
- Data Record
  - Kinesis Data Stream에 저장되는 데이터 유닛.
  - sequence number, partition key, data blob으로 구성된다.
  - data blob is immutable sequence of bytes.
  - data blob은 1 MB까지 커질 수 있다.
- Capacity Mode
  - capacity가 어떻게 관리되고 데이터 스트림의 사용량에 대해 어떻게 비용을 지불할지 결정한다.
  - `on-demand`와 `provisioned`가 있다.
  - `on-demand`: 자동으로 샤드를 관리한다. 실제 throughput 만큼만 내면된다.
  - `provisioned`: 샤드 개수를 지정해야한다. 시간당 샤드 개수로 비용이 청구된다.
- Retention Period
  - 데이터 레코드가 스트림에 더해진 뒤 접근 가능한 시간이다.
  - 디폴트는 생성 이후 24시간이다.
  - 1년까지 늘릴 수 있다.
  - 24시간을 넘어가면 추가 비용이 청구된다.
- Amazon Kinesis Data Streams Application
  - consumer이다.
  - 두 가지 타입의 컨수머가 있다.
    - shared fan-out consumer: 샤드당 전체 2MB/sec로 고정된다. 여러 컨수머가 같은 샤드를 사용하면 throughput을 공유한다.
    - enhanced fan-out consumer: 컨수머당 독립적으로 2MB/sec을 사용한다.
- Shard
  - 스트림에서 고유하게 식별되는 데이터 레코드들의 시퀀스.
  - 스트림은 하나 이상의 샤드로 구성돼있다.
  - 각각은 고정된 단위의 capacity만 제공한다.
  - 스트림의 전체 capacity는 샤드들의 capacity의 합이다.
  - 샤드 개수는 resharding을 통해 증가시키거나 감소시킬 수 있다.
- Partition Key
  - 스트림 내의 샤드별로 데이터를 그룹화하는데 사용된다.
  - 스트림에 속한 데이터 레코드를 여러 샤드로 분리한다.
  - 각각의 데이터 레코드와 관련된 파티션 키를 주어진 데이터 레코드가 어떤 샤드에 속하지를 결정한다.
  - 어플리케이션이 스트림에 데이터를 넣을 때, 파티션 키를 지정해야한다.
  - MD5 해쉬 함수를 파티션 키를 128-bit 인티저 값에 매핑하고 샤드의 해시 키 범위를 사용해 연결된 데이터 레코드를 샤드에 매핑하는데 사용한다.
- Sequence Number
  - 각각의 데이터 레코드는 **샤드 내에서 파티션 키당** 고유한 시퀀스 넘버를 가진다.
  - 키네시스 데이터 스트림은 `putRecords` 혹은 `putRecord`로 스트림에 쓴 뒤 시퀀스 넘버를 할당한다.
  - 같은 파티션 키를 가지는 시퀀스 넘버는 시간이 지남에 따라 증가한다.

## Kinesis Data Stream Capacity Mode
### On-demand Mode
- no capacity planning
- automatically scale
- 큰 데이터를 받고 저장하는 것을 낮은 레이턴시로 간소화시킨다.
- **매우 변동적이고 예측불가능한** 어플리케이션 트래픽 패턴을 다루는데 적합하다.
- 데이터 스트림에 쓰이고 읽는 GB당 데이터로 비용을 지불한다.
- **지난 30일 동안 관측된 peak write throughput까지 수용한다.**
- **15분 동안 트래픽이 지난 peak의 두 배를 넘어가면 write throttling이 발생할 수 있다.**
- read capacity의 총량은 write throughput에 비례해 증가한다.
- **`GetRecord` API 당 하나의 컨수머 어플리케이션을 쓰는 걸 권장한다.**
- **두 개 이상의 컨수머 어플리케이션은 `SubscribeToShard`를 사용하는 Ehanced Fan-Out을 쓰는 걸 권장한다.**

### Handling Read and Write Throughput Exceptions
- 키네시스 데이터 스트림은 각각의 샤드에 대한 트래픽을 모니터링한다.
- **인커밍 트래픽이 샤드당 500 KB/s를 초과하면 15분 내로 샤드를 나눈다.**
- 부모의 샤드 해쉬 키 값이 자식 샤드들에 걸쳐 고르게 재분배된다.
- **만약 인커밍 트래픽이 이전 peak의 두 배를 초과하면 약 15분 동안 read 혹은 write exception을 경험할 수 있다.**
- **모든 레코드들이 적절하게 저장되기 위해 모든 그런 리퀘스트를 재시도하는 걸 권장한다.**
- 고르지 않은 데이터 분배를 만들어 레코드들이 특정 샤드에 할당돼 리밋을 초과하는 파티션 키를 사용하면 read와 write exception을 경험할 수 있다.
- **on-demand 모드에서는 데이터 스트림이 자동으로 고르지 않은 데이터 분배 패턴을 처리한다.** 물론 하나의 파티션 키가 샤드의 1MB/s throughput과 초당 1000 레코드 제한을 넘지 않는다면 말이다.
- **on-demand 모드에서는 키네시스 데이터 스트림이 트래픽 증가를 탐지했을 때 샤드를 고르게 나눈다.**
- 하지만 대량의 인커밍 트래픽을 특정 샤드에 넣는 해시 키를 감지하고 격리하지 않는다.
- 만약 highly uneven partition keys를 사용한다면 write exception을 계속 경험할 거다.
- 그런 유즈 케이스는 provisioned capacity mode를 사용하는 걸 권장한다.

### Provisioned Mode
- 동적으로 콘솔이나 UpdateShardCount API를 통해 샤드 capacity를 늘리거나 줄일 수 있다.
- 키네시스 데이터 스트림 프로듀서나 컨수머 어플리케이션이 스트림으로부터 읽기나 쓰기를 하는 동안 업데이트를 할 수 있다.
- **예측이 쉬운 capacity 요구 사항이 있는 예측 가능한 트래픽에 적합하다.**
- 데이터 스트림을 위한 샤드 개수를 지정해야한다. (공식은 문서 참고)
- 데이터 스트림을 peak throughput을 처리하도록 설정하지 않았으면 read and write throughput exceptions을 경험할 수 있다. 이런 경우 직접 스케일 업을 해야한다.
- 또한 uneven data distribution partition key를 사용해도 exeptions를 경험할 수 있다. 이런 경우 그런 샤드를 찾아서 직접 나눠줘야한다.

### Switching Between Capacity Modes
- 각각의 모드에서 서로의 모드로 바꿀 수 있다.
- 24시간 내에 두 번을 바꿀 수 있다. (Updating -> Active로 바뀐 후)
- capacity 모드를 바꾸는 건 어떤 장애도 유발하지 않는다.
- provisioned to on-demand
  - 처음에는 전환 전의 샤드 수를 그대로 유지한다.
  - 이 시점부터 키네시스 데이터 스트림은 데이터 트래픽을 모니터링하고 샤드를 스케일한다.
- on-demand to provisioned
  - 처음에는 전환 전의 샤드 수를 그대로 유지한다.
  - 이 시점부터 모니터링과 샤드 개수에 대한 조정에 대한 책임을 져야한다.
