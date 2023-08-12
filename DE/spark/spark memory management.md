## Executor Memory
![Executor Memory](./images/Spark%20Executor%20Memory.png)
https://selectfrom.dev/spark-performance-tuning-spill-7318363e18cb

## Memory inside JVM
### Reserved Memory
- 스파크 내부 객체를 생성하기 위해 리저브된 영역임.
- 스파크 익스큐터에 1.5 * Reserved Memory의 JVM heap 영역을 주지 않으면 에러가 발생함.
- 해당 영역의 사이즈 바꾸는 것 권장하지 않음.
- memory size: 300MB로 고정됨.

### User Memory
- 사용자가 정의한 데이터 구조, UDF가 저장되는 공간임.
- Spark Memory 할당 이후 남은 영역임.
- Spark에 의해 관리되지 않음.
- 이 바운더리를 고려하지 않으면 OOM 에러가 발생할 수 있음.
- memory size: (Java Heap Memory - Reserved Memory) * (1 - `spark.memory.fraction`)

### Spark Memory
- memory size: (Java Heap Memory - Reserved Memory) * `spark.memory.fraction`
- Storage Memory와 Execution Memory 두 리전으로 나뉨.
- 바운더리는 `spark.memory.storageFraction` 파라미터로 설정됨. (디폴트 0.5)
- 바운더리는 고정돼있지 않음.
- memory pressure에 따라서 바뀔 수 있음.
- Storage Memory
  - 스파크의 캐쉬된 데이터와 serialized 데이터를 unroll 하는데 사용하는 임시 공간으로 사용됨.
  - 모든 broadcast 변수들이 캐쉬된 블록으로 저장됨.
  - unroll 할 공간이 충분하지 않으면 persistence 레벨이 허용하는 한 디스크에 저장함.
  - memory size: (Java Heap Memory - Reserved Memory) * `spark.memory.fraction` * `spark.memory.storageFraction`
- Execution Memory
  - 스파크 태스크들의 실행동안 필요로 하는 객체들을 저장하는데 사용됨.
  - 예를 들면, map side에서 셔플 중간 버퍼를 저장하는데 사용됨.
  - 메모리가 충분하지 않다면 디스크에 스필링 할 수 있음.
  - 하지만 이 pool에 있는 블록들은 다른 스레들에 의해 강제로 쫓겨나지 않음.
  - memory size: (Java Heap Memory - Reserved Memory) * `spark.memory.fraction` * (1 - `spark.memory.storageFraction`)
- Execution Memory는 중간 연산의 데이터를 저장하기 때문에 강제로 디스크로 블록을 내쫓을 수 없음.
- 하지만 Storage Memory는 RAM에 블록을 캐쉬한 것이어서 괜찮음.
- 그냥 블록 메타데이터 업데이트하고 디스크에서 가져오면 된다.
- Memory Eviction
  - Storage Memoery와 Execution Memory 모두 각 영역을 사용하지 않는 경우에만 서로 영역으로부터 빌릴 수 있음.
  - Storage Memory가 점유한 Execution Memory 블록은 Execution이 요청할 경우, 강제로 추방될 수 있음.
  - Execution Memory가 점유한 Storage Memory 블록은 Storage가 요청하더라도, 강제로 추방될 수 없음. (Spark가 Execution의 블록을 release할 때까지 기다려야 함.)
- 4GB 힙을 사용하더라도 결국 실제로 각 메모리 영역에서 사용하는 건 1423MB 밖에 안 됨.
- 스파크 캐시를 사용할 때 executor에 캐시된 데이터 양이 처음 Storage Memory 리전과 크기가 동일한 경우, eviction으로 데이터를 제거해 더 작게 만들 수 없음.
- 하지만 Execution Memory 리전이 Storage Memory를 채우기 전에 처음 크기보다 커지면, Execution Memory는 강제로 내쫓을 수 없어서 더 작은 Storage Memory를 가지게 된다.

### 메모리 설정 값에 따른 각 영역의 메모리
- `spark.executor.memory`: 4G
- `spark.memory.fraction`: 0.75
- `spark.memory.storageFraction`: 0.5
- Reserved Memory : 300MB
- User Memory : (4096MB - 300MB) * (1 - 0.75) = 949MB
- Spark Memory : (4096MB - 300MB) * 0.75 = 2847MB
- Storage Memory : (4096MB - 300MB) * 0.75 * 0.5 = 1423MB
- Execution Memory : (4096MB - 300MB) * 0.75 * (1 - 0.5) = 1423MB

## Memory outside JVM
- OffHeap memory: JVM 밖의 메모리이지만 JVM 목적으로 쓰이거나 프로젝트 텅스텐을 위해 사용되는 메모리
- External process memory: R 혹은 Python을 위한 메모리. JVM 밖에 존재하는 프로세스에 의해 사용되는 메모리.

### OffHeap
- `spark.executor.memoryOverhead`: 익스큐터당 추가적인 non-heap 메모리.

### Python
- `spark.executor.pyspark.memory`
  - external process 메모리의 일부임.
  - 각 익스큐터에서 pyspark에 할당되는 메모리.
  - default는 지정돼있지 않음.
  - 지정되면 pyspark의 메모리는 해당 설정값만큼으로 제한됨.
  - 지정돼있지 않으면 파이썬의 메모리 사용을 제한하지 않음.
  - 다른 non-JVM 프로세스와 공유하는 overhead 메모리 공간을 초과하지 않도록 알아서 잘 해야됨.
- `spark.python.worker.memory`
  - JVM 프로세스와 Python 프로세스는 py4J 브릿지를 통해 커뮤니케이션함.
  - py4J는 JVM과 파이썬 사이의 오브젝트들을 노추함.
  - 해당 설정값은 디스크에 스필링을 하기 전에 객체 생성에 py4J가 얼마만큼의 메모리를 사용할 수 있는지 컨트롤함.

## Reference
- https://0x0fff.com/spark-memory-management/
- https://dhkdn9192.github.io/apache-spark/spark_executor_memory_structure/
- https://stackoverflow.com/questions/68249294/in-spark-what-is-the-meaning-of-spark-executor-pyspark-memory-configuration-opti