## Amazon SQS - Standard Queue
- 속성들
  - 제한 없는 쓰루풋, 제한 없는 큐 내의 메세지 수.
  - 메세지들의 기본 리텐션: 4일, 최고 14일.
  - 낮은 레이턴시 (퍼블리쉬와 리시브에서 10ms 내외)
  - 보내지는 메세지 크기는 256KB로 제한됨.
  - 중복되는 메세지를 가질 수 있음. (at least once delivery)
  - 메세지 순서가 맞지 않을 수 있음. (best effort ordering)

## SQS - Producing Message
- 컨수머가 삭제할 때까지 메세지는 SQS 내에서 퍼시스트됨.
- 메세지 리텐션: 기본 4일, 14일까지.
- SQS standard: 제한 없는 쓰루풋.
