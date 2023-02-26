# Spark Memory Management
- https://0x0fff.com/spark-memory-management/
## UnifiedMemoryManager
- ![spark memory menagement](./images/spark%20memory%20management.png)

### Reserved Memory
- 스파크 내부 객체를 생성하기 위해 리저브된 영역임.
- 스파크 익스큐터에 1.5 * Reserved Memory의 JVM heap 영역을 주지 않으면 에러가 발생함.
- 해당 영역의 사이즈 바꾸는 것 권장하지 않음.

### User Memory
- Spark Memory 할당 이후 남은 영역임.
- RDD 트랜스포메이션에 사용되는 사용자의 데이터 구조를 저장할 수 있음.
- 이 바운더리를 고려하지 않으면 OOM 에러가 발생할 수 있음.

### Spark Memory
- Storage Memory와 Execution Memory 두 리전으로 나뉨.
- 바운더리는 `spark.memory.storageFraction` 파라미터로 설정됨. (디폴트 0.5)
- 바운더리는 고정돼있지 않음.
- memory pressure에 따라서 바뀔 수 있음.
- Storage Memory
  - 스파크의 캐쉬된 데이터와 serialized 데이터를 unroll 하는데 사용하는 임시 공간으로 사용됨.
  - 모든 broadcast 변수들이 캐쉬된 블록으로 저장됨.
  - unroll 할 공간이 충분하지 않으면 persistence 레벨이 허용하는 한 디스크에 저장함.
- Execution Memory
  - 스파크 태스크들의 실행동안 필요로 하는 객체들을 저장하는데 사용됨.
  - 예를 들면, map side에서 셔플 중간 버퍼를 저장하는데 사용됨.
  - 메모리가 충분하지 않다면 디스크에 스필링 할 수 있음.
  - 하지만 이 pool에 있는 블록들은 다른 스레들에 의해 강제로 쫓겨나지 않음.
- Execution Memory는 중간 연산의 데이터를 저장하기 때문에 강제로 디스크로 블록을 내쫓을 수 없음.
- 하지만 Storage Memory는 RAM에 블록을 캐쉬한 것이어서 괜찮음.
- 그냥 블록 메타데이터 업데이트하고 디스크에서 가져오면 된다.
- Execution Memory가 Storage Memory로 부터 빌릴 때
  - Storage Memory에 free 공간이 있는 경우
  - Storage Memory 풀 사이즈가 처음의 사이즈를 초과한 경우 eviction이 발생함.
- Storage Memory가 Execution Memory로부터 빌릴 수 있는 건 free 공간이 있는 경우만 가능함.
- 4GB 힙을 사용하더라도 결국 실제로 각 메모리 영역에서 사용하는 건 1423MB 밖에 안 됨.
- 스파크 캐시를 사용할 때 executor에 캐시된 데이터 양이 처음 Storage Memory 리전과 크기가 동일한 경우, eviction으로 데이터를 제거해 더 작게 만들 수 없음.
- 하지만 Execution Memory 리전이 Storage Memory를 채우기 전에 처음 크기보다 커지면, Execution Memory는 강제로 내쫓을 수 없어서 더 작은 Storage Memory를 가지게 된다.
