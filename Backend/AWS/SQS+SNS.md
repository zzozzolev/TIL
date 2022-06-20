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

## SQS - Message Visibility Timeout
- 메세지가 컨수머에 의해 폴링된 후에, 다른 컨수머들에게 invisible 한 상태가 됨.
- 기본적으로, "message visibility timeout"은 30초임.
- 즉, 메세지가 30초 내에 처리돼야함.
- message visibility timeout이 지난 후에는, 메세지가 SQS에서 visible 하게 됨.
- 즉, 다른 컨수머가 처리할 수 있음.

## SQS - Message Visibility Timeout
- 메세지가 visibility timeout 내에 처리되지 않는다면, 두 번 처리될 수 있음.
- 컨수머는 더 많은 시간을 얻기 위해, `ChangeMessageVisibility`를 호출 할 수 있음.
- 만약 visibility timeout이 많고 컨수머가 크래쉬 된다면, 재처리는 시간이 걸릴 수 있음.
- 만약 visibility timeout이 너무 적으면, 중복을 얻을 수 있음.

## Amazon SQS - Dead Letter Queue
- 이전에 봤던 것처럼 visibility timeout 내에 메세지가 처리되지 않으면 큐에 다시 들어감.
- 메세지가 몇 번 동안 큐에 다시 돌아갈지 쓰레스 홀드를 정할 수 있음.
- `MaximumReceives` 쓰레스홀드가 초과된 이후에, 메세지는 dead letter queue (DLQ)에 들어감.
- 디버깅에 도움이 됨.
- 만료되기 전에 DLQ에 있는 메세지를 확실히 처리해야함.
  - DLQ에 있는 리텐션을 14일로 설정하는 게 좋음.

## SQS DLQ - Redrive to Source
- 무엇이 문제인지 이해하기 위해 DLQ에 있는 메세지를 컨숨하는데 도움을 주는 기능.
- 코드가 고쳐졌을 때, 메세지를 DLQ에서 source queue 혹은 다른 큐로 다시 옮길 수 있다.

## SQS - Delay Queue
- 메세지를 15분까지 딜레이함. (컨수머들은 바로 못 봄)
- 기본은 0초임. (메세지를 바로 이용가능함)
- 큐 레벨에서 디폴트를 설정할 수 있음.
- `DelaySeconds` 파라미터를 이용해서 보낼 때 디폴트를 오버라이드할 수 있음.

## SQS - Long Polling
- 컨수머가 큐에서 메세지들을 요청할 때, 만약 큐에 아무것도 없다면 메세지가 도착하는 것을 기다릴 수도 있음.
- 이걸 `Long Polling`이라고 부름.
- Long Polling은 효율성을 높이고 레이턴시를 줄이면서 SQS에 대한 API 호출 횟수를 줄임.
- 웨잇 타임은 1초에서 20초 사이로 설정할 수 있음. (20초가 선호됨)
- Long Polling가 Short Polling 보다 선호됨.
- Long Polling은 `WaitTimeSeconds`를 통해 큐 레벨 혹은 API 레벨에서 활성화할 수 있음.

## SQS - FIFO Queue
- FIFO = First In First Out (ordering of messages in the queue)
- 제한된 쓰루풋: 300 msg/s without batching, 3000 msg/s with
- Exactly-once send capability (중복 제거)

## SNS
- 이벤트 프로듀서는 하나의 SNS 토픽에만 메세지를 보냄.
- SNS 토픽 알림을 듣기 원하는 만큼 많은 이벤트 리시버 (subscriptions)가 있을 수 있음.
- 토픽에 대한 각각의 구독자는 모든 메세지를 얻음. (메세지를 필터링하는 새로운 피처)
- 많은 AWS 서비스들이 알림을 위해 SAS에 바로 데이터를 보낼 수 있음.
- SDK를 이용해서 토픽 퍼블리쉬 가능.

## SNS + SQS: Fan Out
- SNS에 한 번 보내고, 구독자인 모든 SQS 큐들에서 받을 수 있음.
- 완전히 decoupled, 데이터 로스 없음.
- SQS는 data persistence, 지연된 프로세싱, 재시도를 할 수 있도로 해줌.
- 시간이 지남에 따라 더 많은 SQS 구독자들을 추가하는 능력도 있음.
- SQS access policy에 SNS가 쓸 수 있도록 해야함.
- 예를 들면, 다음과 같이 구성할 수 있음.
  ```
  (Buying Service) -> (SNS Topic) -> (SQS Queue1) -> (Fraud Service)
                                  -> (SQS Queue2) -> (Shipping Service)
  ```

## Amazon SNS - FIFO Topic
- FIFO = First In First Out (토픽 내 메세지의 순서)
- SQS FIFO와 비슷한 피처:
  - Message Group ID에 따른 순서 (같은 그룹내의 모든 메세지들은 정렬됨)
  - Deduplication ID 혹은 Content Based Deduplication을 사용해서 중복 제거
- SQS FIFO 큐만 구독자로 할 수 있음.
- 제한된 쓰루풋
- fan out + ordering + deduplication: SNS FIFO Topic + SQS FIFO Queue

## SNS - Message Filtering
- JSON 정책은 SNS 토픽의 구독자들에게 보내지는 메세지들을 거르기 위해 사용됨.
- 만약 구독자가 필터 정책이 없으면, 모든 메세지를 받음.
