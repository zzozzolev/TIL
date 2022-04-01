## RDB에서 카산드라가 보고 배운 것
- consistency는 실용적이지 않으므로 버린다.
- 매뉴얼 샤딩과 리밸런싱은 힘드므로 빌트인으로 만들어 개발자가 별도의 코드를 작성하지 않도록 한다.
- 파티션을 옮기는 것은 시스템을 복잡하게 만든다. 그래서 master / slave 구조로 가지 않는다.
- 스케일 업은 비싸다. 대신 스케일 아웃을 사용하게 만든다.
- 스캐터 / 게더는 좋지 않다. 리얼 타임 쿼리 퍼포먼스를 위해 denormalize를 했다. 항상 하나의 머신만 hit 하도록 한다.

## Hash Ring
- master, slave, replica sets가 없다. 모든 노드가 동등하다.
- config server (zookeeper)가 없다.
- 데이터가 파티셔닝 돼있다.
- primary key가 partition key이다.
- 데이터가 여러 서버에 복제된다.
- 모든 노드들은 데이터를 가지고 있고 쿼리에 답할 수 있다. (r/w 모두 가능)

## CAP Tradeoffs
- 네트워크 단절 동안에 cosistency와 HA를 모두 만족할 수 없다.
- 데이터 센터 사이의 latency는 consistency를 실용적이지 않게 만든다.
- 그래서 카산드라는 consistency 보다 availablity와 partition tolerance를 선택했다.

## Replication
- 데이터는 자동으로 복제된다.
- 사용자가 서버들의 개수를 고를 수 있다. 이걸 replication factor 혹은 RF라고 부른다.
  - 실용적인 건 RF=3
  - Write 1 -> A:1, B:1, C:1, D: 
- 데이터는 항상 각각의 레플리카로 복제된다.
- 만약 머신이 다운된다면 잃어버린 데이터는 hinted handoff를 통해 리플레이된다.

## Consistency Levels
- 쿼리 consistency
- ALL, Quorum, One
  - 사람들이 쿼럼을 많이 사용함.
- 얼마나 많은 레플리카가 쿼리에 OK라고 응답해야하는지

## Multi DC
- 전형적인 사용법: 클라이언트들이 로컬 DC에 쓰고 async하게 다른 DC들에 복제한다.
- DC당 keyspace당 RF
- DC는 물리적일 수도 논리적일 수도 있다.

## 쓰기
### The Write Path
- 쓰기는 클러스터 내의 어떤 노드에도 쓰인다. 즉, 어떤 노드라도 coordinator가 될 수 있다.
- 쓰기는 commit log에 쓰이고 그 다음에 memtable에 쓰인다.
  - commit log: append only structure
  - memtable: in-memory
- 모든 쓰기는 타임 스탬프를 포함한다.
- memtable은 주기적으로 disk에 플러쉬된다. (sstable)
  - 백그라운드로 async 하게
- 새로운 memtable은 메모리에 생성된다.
- 삭제는 특별한 쓰기 케이스이다. tombstone이라고 불린다.
  - sstable과 commit log는 immutable 하다.

### What is an SSTable
- 로우 저장소를 위한 immutable 데이터 파일
- 모든 쓰기는 언제 쓰였는지에 대한 타임 스탬프를 포함한다.
- 파티션은 여러 개의 SSTable들에 걸쳐 퍼쳐있다.
- 같은 컬럼은 여러 개의 SSTable들에 있을 수 있다.
- 컴팩션을 통해 머지되고, 오직 최신 타임스탬프만 유지된다.
  - 컴팩션: 작은 SSTable들이 더 큰 것으로 합쳐진다.
  - 동일한 로우에 대해 t1, t2에 쓰인 게 있다면 t1을 무시하고 t2를 쓴다.
- 삭제는 tombstones로 쓰여진다.
- 백업이 쉽다.

## 읽기
### The Read Path
- 어느 서버라도 쿼리될 수 있다. coordinator로서 동작한다.
- 요청된 키와 함께 노드에 접근한다.
- 각각의 노드에서 데이터는 SSTable에서 꺼내지고 머지된다.
- Consistency가 ALL보다 적다면 백그라운드로 read repair을 수행한다.

## CQL
### Keyspaces
- top level namespace/container
- RDB 스키마와 비슷함.

### Use
- keyspace 사이를 바꿈.

### Tables
- keyspace들은 table들을 포함함.
- table들은 데이터를 포함함.

### UUID and TIMEUUID
- TIMEUUID: 타임스탬프 값을 내장함.
- 인티져 ID 대신 사용함.
- 카산드라는 분산 데이터 베이스이기 때문임.
- UUID는 내부 통신 없이 고유한 값을 만들어 낼 수 있음.
