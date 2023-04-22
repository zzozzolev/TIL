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
