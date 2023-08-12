## Shuffle read and write
- Shuffle read
  - 스테이지가 시작될 때 익스큐터가 메모리에 로드하는 것.
  - 다른 익스큐터에 의해 이전 스테이지에서 준비된 셔플 파일들.
- Shuffle write
  - 다음 스테이지를 위해 준비하는 아웃풋 사이즈.
  - 해당 스테이제에서 만든 셔플 파일의 크기.

## Shuffle Spill이란?
- 메모리에 있던 RDD를 디스크로 옮기고 이후에 해당 RDD가 연산에서 필요할 때, 디스크에서 다시 메모리로 옮긴다.
- 메모리와 디스크를 왔다갔다 해야하기 때문에 비싼 연산이다.
- spill 문제와 실제로 관련된 것은 On-Heap 메모리이다.

## Shuffle Spill은 언제 발생할까?
- 파티션이 익스큐터의 메모리에 들어가기에 너무 클 때 spill이 발생한다.
- 익스큐터가 셔플 파일을 읽을 때 익스큐터의 사용가능한 Execution Memory 보다 클 때 발생한다.
- Execution Memory와 Storage Memory의 메모리 사용량의 총합이 설정한 값을 벗어날 때 일어난다.

## Shuffle Spill Memory and Spill Disk
- 일단 두 개가 같은 데이터이다.
- spill memory는 disc로 옮겨지기 전에 역질렬화된 형태의 shuffled 데이터가 메모리에서 차지하는 사이즈이다.
- spill disc는 disc로 쓰여졌을 때 직렬화된 형태의 데이터 사이즈이다.

## Reference
- https://selectfrom.dev/spark-performance-tuning-spill-7318363e18cb
- https://stackoverflow.com/questions/74824056/what-is-spark-spill-disk-and-memory-both
