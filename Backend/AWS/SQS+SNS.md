## Amazon SQS - Standard Queue
- 속성들
  - 제한 없는 쓰루풋, 제한 없는 큐 내의 메세지 수.
  - 메세지들의 기본 리텐션: 4일, 최고 14일.
  - 낮은 레이턴시 (퍼블리쉬와 리시브에서 10ms 내외)
  - 보내지는 메세지 크기는 256KB로 제한됨.
  - 중복되는 메세지를 가질 수 있음. (at least once delivery)
  - 메세지 순서가 맞지 않을 수 있음. (best effort ordering)

## SQS - Producing Message
- SDK를 사용해 SQS로 생산됨.
- 컨수머가 삭제할 때까지 메세지는 SQS 내에서 퍼시스트됨.
- 메세지 리텐션: 기본 4일, 14일까지.
- SQS standard: 제한 없는 쓰루풋.

## SQS - Consuming Message
- 컨수머 (서버, 람다 등등...)
- 메세지를 얻기 위해 SQS를 폴링함. (한 번에 10개 정도의 메세지를 받음.)
- 메세지를 처리함. (예시: 메세지를 RDS DB에 넣음.)
- SDK를 이용해 메세지를 삭제함.
  - 다른 컨수머들이 이 메세지를 볼 수 없게 함.

## SQS - Multiple EC2 Instances Consumers
- 컨수머들은 병렬적으로 메세지를 받고 처리함.
- At least once delivery: 빨리 처리되지 못하면 다른 컨수머가 받음.
- Best-effort message ordering
- 컨수머들은 메세지를 처리한 후 삭제함.

## SQS Queue Access Policy
- Account 걸쳐서 접근: 계정을 넘어서 액세스할 수 있음.
- S3 이벤트 알림을 SQS 큐에 퍼블리쉬
