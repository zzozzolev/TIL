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
