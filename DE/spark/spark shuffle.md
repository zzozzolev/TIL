# Spark Architecture: Shuffle
- https://0x0fff.com/spark-architecture-shuffle/

## Intro
- 셔플 연산에서 소스 익스큐터에서 아웃풋 데이터를 산출하는 태스크가 `mapper`이고, 타겟 익스큐터에서 데이터를 소비하는 태스크가 `reducer`임. 이 사이에서 일어나는 게 `shuffle`임.
- 2개의 중요한 압축(compression) 파라미터가 있음.
  - `spark.shuffle.compress`: 엔진이 셔플 아웃풋을 압축할지 말지 (default true)
  - `spark.shuffle.spill.compress`: 중간의 셔플 스필 파일을 압축할지 말지 (default true)
- 기본 코덱은 `snappy`를 사용함.
- 2.0 전까지는 `spark.shuffle.manager`에 의해 결정되는 다양한 셔플 구현이 있었음. `hash`, `sort`, `tungsten-sort`
- 근데 2.0 이후부터는 `SortShuffleManager`만 있음. 해당 매니저는 `tungsten-sort` (or `sort`)에 우선 순위를 두고 세 가지 방법을 모두 구현함. [참고](https://www.linkedin.com/pulse/apache-spark-shuffle-akhil-pathirippilly-mana/)

## Sort Shuffle
- reducer id로 정렬되고 인덱스된 하나의 파일을 아웃풋으로 함.
- 단지 파일에서 관련된 데이터 블록의 위치에 대한 정보를 얻는 것으로 reducer x와 관련된 데이터를 쉽게 꺼낼 수 있음.
- 하지만 reducer가 `spark.shuffle.sort.bypassMergeThreshold`보다 적으면 별개의 파일을 만들고 하나의 파일로 조인 하는게 빨라서 fallback 플랜으로 이렇게 함.
- map 사이드에서 데이터를 정렬하지만 reduct 사이드에서 머지하지 않음.
- 정렬된 데이터가 필요한 경우 다시 정렬함.
- 모든 map output을 저장할 메모리가 없으면 중간 데이터를 디스크에 spill함.
- 같은 executor에서 많은 스레드를 수행하면 map output을 저장할 공간이 줄어듦.
- 정렬된 output은 spilling이 발생하거나 더 이상 mapper output이 없을 때 디스크에 쓰여짐.
- 각각의 spill 파일은 디스크에 별도로 쓰여짐.
- 머지는 reducer에 의해 데이터가 요청될 때만 수행된다. 그리고 실시간으로 이루어진다.

![Sort Shuffle](./images/Sort%20Shuffle.png)

## Tungsten Sort
- deserialize 없이 serialized 바이너리 데이터에 직접 연산을 함.
- 압축된 레코드 포인터와 파티션 아이디의 어레이를 정렬하는 `ShuffleExternalSorter`를 사용함.
- 적은 메모리를 사용해서 캐쉬에 더 효율적임.
- 레코드는 deserialize 됐기 때문에 serialized 데이터에 바로 spilling을 함.
- 대신 아래의 모든 조건이 만족될 때만 쓰임.
  - 셔플이 aggregation을 사용하지 않는 경우.
  - 셔플이 16777216 보다 적은 파티션을 생산하는 경우.
  - 개별 레코드가 serialized 형태에서 128MB보다 크지 않음.

![Tungsten Shuffle](./images/Tungsten%20Sort.png)
