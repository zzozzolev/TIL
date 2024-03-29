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
- 각각의 노드에서 데이터는 SSTable에서 메모리로 꺼내지고 타임 스탬프를 이용해 머지된다.
  - latest timestamp always win
- Consistency가 ALL보다 적다면 백그라운드로 read repair을 수행한다.
  - eventually consistency
  - 어떤 노드는 아직 최신 데이터가 아닐 수도 있다.
  - 이때 read를 통해 모든 레플리카가 최신 데이터를 유지할 수 있도록 한다.

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

## Partitions
- 파티션 키는 데이터가 어떻게 분배될지 결정하는 것임.
- 파티션은 consistent 해싱 알고리즘을 씀.
- 데이터를 쿼리할 때마다 데이터는 같은 곳에 있음.
- 파티션을 찾는 데 O(1) 밖에 걸리지 않음.

## Clustering Columns
- 프라이머리 키를 통해 파티션을 정하고 정렬 방식을 정할 수 있음.
- 데이터 모델이 만들어지고 데이터가 삽입 됐다면 프라이머리 키를 바꿀 수 없음.
- 클러스터링 컬럼은 파티션 키 다음에 있는 컬럼임. 1개가 넘어가도 됨.
  ```
  PRIMARY KEY((state), city, name)
  ```
  - 파티션 키: state
  - 클러스터링 컬럼: city, name
  - 먼저 city로 정렬 후 name으로 정렬
- 하지만 이렇게만 프라이머리 키를 만들면 충돌이 발생할 수 있음.
- int ID를 이용하면 되는데, 카산드라에는 RDB 같은 sqeuntial이 없음.
- 프라이머리 키는 두 가지 문제를 해결함.
  - unique record
  - controlling the order

### Querying Clustering Columns
- select query일 때도 runtime에 order를 바꿀 수 있음.
- 모든 쿼리는 파티션 키를 포함해야함.
- 프라이머리 키에 명시한 클러스터링 컬럼 순서에 맞춰서 비교를 해야함.
  - 만약 `PRIMARY KEY((state), city, name)` 이렇게 프라이머리키를 지정했는데
  - `state == texas and name == a` 이런 식으로 하면 동작하지 않음.

### Changing Default Ordering
- 클러스터링 컬럼들은 기본적으로 asc 순서임.
- `WITH CLUSTRING ORDERY BY`로 순서를 바꿀 수 있음.
- desc로 하고 싶은 컬럼들까지 모든 컬럼을 포함해야함.
  - 예를들어 id를 제외하고 asc로 가정함.
  ```
  PRIMARY KEY((state), city, name, id))
  WITH CLUSTERING ORDER BY(city DESC, name ASC);
  ```

### Allow Filtering
- `ALLOW FILTERING`은 쿼리의 파티션 키 제약을 풀어줌.
- 클러스터링 컬럼에 쿼리를 할 수 있음.
- 테이블 내에 있는 모든 파티션들을 스캔하게 만듦.
- 진짜 필요한 게 아니면 쓰지말 것! 진짜 필요해 쓰지마라;

## Ring
- 싱글 노드를 로드가 증가했을 때, 망가지기 쉬움.
- 노드를 더 추가하면 됨.
- 데이터 관련 요청을 어느 노드에든 할 수 있음.
- 요청을 받은 노드를 `coordinator node` 라고 함.
- 코디네이터 노드는 데이터를 해당 파티션을 저장하고 있는 노드로 보냄.
- 각각의 노드는 특정 범위의 데이터를 책임져야 함. 이걸 `token range` 라고 함.
- 코디네이터 노드는 올바른 노드에 요청을 보내고 클라이언트에게 ack를 보냄.
- `2^63 ~ 2^63 - 1` 까지 가능함.
- partitioner는 데이터가 링에 어떻게 분배될지를 결정함.
- 파티셔닝을 잘못하면 특정 노드에만 데이터가 몰릴 수 있음.
- 필요할 때 노드를 추가했다가 제거할 수 있음.

### Joining the Cluster
- 다운타임 없이 조인 가능함.
- 노드들은 아무 노드와 커뮤니케이션을 해서 클러스터에 조인함.
- 카산드라는 `cassandra.yaml`에서 가능한 노드들의 `seed nodes`를 찾음.
- 조인한 노드는 가십을 시드 노드에 전달함.
- 시드 노드들은 조인 노드에 클러스터 토폴로지를 전달함.
- 새로운 노드가 클러스터에 조인하면, 모든 노드들은 peer임.

### Drivers
- 드라이버는 똑똑하게 어떤 노드가 코디네이트를 잘할지 선택함
- `TokenAwarePolicy`: 드라이버가 데이터를 포함하는 노드들 선택함.
- `RoundRobinPolicy`: 드라이버가 링을 라운드 로빈함.
- `DCAwareRoundRobinPolicy`: 드라이버가 타겟 데이터 센터를 라운드 로빈함.

## Peer to Peer
- 리더, 팔로워가 없고 모두 동등한 peer임.
- 그래서 코디네이터가 클라이언트로부터 요청을 받아서 비동기적으로 해당 데이터를 담당하는 각각의 레플리카 노드애 전달함.
- split brain이 발생해도 클라이언트가 요청을 보낼 수 있고 레플리카에 쓰기를 할 수 있다면 failover 이벤트가 아님.
- 카산드라는 뭔가 잘못돼도 여전히 online 상태를 유지하도록 설계됐음.

## Vnodes
- 노드에 token이 고르게 나눠지면 좋겠지만 항상 그럴 수는 없음.
- 특정 노드에만 token이 집중될 수 있음.
- 노드를 추가하면 기존 노드에 있었지만 새로운 노드에 할당돼야하는 데이터를 스트림으로 옮겨야 됨.
- 하지만 이건 기존 노드에 부담을 줌.
- `Vnode`를 이용해 이 문제를 완화함.
- physical node가 여러 개의 작은 virtual node 처럼 동작함.
- 각각의 vnode는 링의 큰 한 부분을 책임지기 보다는 작은 slice를 책임짐.
  - A -> 31 ~ 40, 61 ~ 70, 91 ~ 100
  - B -> 1 ~ 10, 41 ~ 50, 71 ~ 80
  - C -> 11 ~ 20, 51 ~ 60, 81 ~ 90
- 각각의 피지컬 노드는 대략적으로 같은 양의 데이터를 담당함.
- 새로운 노드는 한 노드의 전체 token range를 담당하기 보다는 각각의 노드의 각각의 token range를 담당함.
- 여러 노드에게 데이터를 받기 때문에 새로운 노드가 클러스터에 조인하는 시간이 줄어들고 스트리밍에 대한 부담을 여러 노드로 분산시킴.
- vnode를 통해 노드를 추가하거나 제거하는 것은 클러스터가 균형잡히도록 도와줌.
- 기본적으로 각각의 노드는 128개의 vnode를 가지고 있음.
- vnode는 token range 할당을 자동화함.
- `cassandra.yaml`의 `num_tokens`를 1보다 크게 하면 vnode를 사용하는 것임.

## Gossip
- 데이터를 전파하는 브로드캐스트 프로토콜
- 중앙화된 서버가 클러스터 정보를 담고있지 않고 대신 최신 정보만 유지하면서 피어가 이 정보를 퍼뜨림.

### Choosing a Gossip Node
- 각각의 노드는 매초마다 가십 라운드를 시작함.
- 가십을 퍼뜨릴 노드를 1 ~ 3개로 선택함.
- 노드는 클러스터내의 아무 다른 노드에 가십을 퍼뜨릴 수 있음.
- 확률적으로 seed, downed 노드임.
- 노드는 이전에 가십한 노드를 추적하지 않음.
- 신뢰할 수 있고 효과적으로 클러스터를 통해 노드 메타 데이터를 퍼뜨림.
- 노드가 실패했을 때도 퍼뜨리는 걸 계속할 수 있음.

### What to Gossip? - Cluster Metadata
- 가십은 노드 메타 데이터만 퍼뜨리고 클라이언트 데이터는 퍼뜨리지 않음.
- 각각의 노드는 대단히 중요한 자료 구조인 `Endpoint State`를 가지고 있음.
- 여기에 하나의 노드 혹은 앤드포인트에 대한 모든 가십 스테이트 정보를 저장하고 있음.
- `Endpoint State`는 `Heartbeat State`, `Application State`라고 하는 다른 자료 구조를 포함함.
- `Heartbeat State`는 두 가지 값을 트랙킹함.
  - `generation`: 노드가 언제 부트스트랩을 했는지에 대한 타임 스탬프
  - `version`: 각각의 노드는 버전을 매초마다 증가시킴
- Heartbeat 값은 증가되고 클러스터에 퍼져나감.
- 노드들이 다른 노드가 up 상태인지 아닌지를 알 수 있게함.
- `Application State`는 해당 노드에 대한 메타 데이터를 저장함.
  - `STATUS`: 노드 상태
  - `DC`: 데이터 센터
  - `RACK`: 랙
  - `SCHEMA`: 스키마 버전
  - `LOAD`: disk 사용 정도
- 노드 실패 디텍터가 피어가 up인지 down인지 결정하겠지만, 노드는 이 가정을 가지고 그런 노드들에게는 가십을 보내지 않음.

### Node Gossip Communication
- `Endpoint State`에 자신도 포함됨.
- 왼쪽 노드는 오른쪽 노드에 `SYC` 메세지를 통해 가십을 시작함.
- 해당 메세지는 간단한 digest 정보를 가지고 있음.
  - enpoint address
  - generation
  - version
- `SYC` 메세지를 받은 노드는 자신의 정보와 비교함.
- 받은 노드는 `ACK` 메세지를 보냄. `SYN`이랑 비슷함.
- 보낸 노드는 받은 노드가 더 오래된 버전을 들고 있다면 자신의 최신 버전을 `ACK2`로 보내고 자신이 더 오래된 버전을 들고 있다면 자신의 버전을 업데이트함.

### Network Traffic
- 네트워크 트래픽이 일정함.
- 데이터 스트리밍과 비교하면 더 적음.
- 네트워크 스파이크를 야기하지 않음.

## Snitch
- 각각 노드의 rack과 DC를 결정하는 것.
- 클러스터의 topology. 어떤 노드가 어디에 속하는지.
- 여러 가지 타입의 snitch가 있음.
- `cassandra.yaml`에서 설정할 수 있음.

### Simple Snitch
- 디폴트
- 모든 노드들을 같은 DC와 rack에 위치시킴.

### Property File Snitch
- 파일로부터 모든 노드들에 대한 DC와 rack 정보를 읽음.
- 운영자가 클러스터내의 모든 노드들에 대해 싱크를 맞춰야함.
- `cassandra-topology.properties` 파일에서 설정 가능함.

### Gossiping Property File Snitch
- property file snitch의 고통으로 부터 완화시킴.
- 파일에서 현재 노드의 DC/rack 정보를 선언함.
- 각각의 개별 노드의 셋팅들을 설정해야함.
- 하지만 property file snitch를 카피할 필요는 없음.
- 가십은 클러스터를 통해 셋팅을 퍼뜨림.
- `cassandra-rackdc.properties` 파일에서 설정 가능함.

### Rack Inferring Snitch
- rack과 DC를 IP 주소로부터 추론함.
  - 110.100(DC octet).200(rack octet).105(node octet)

### Dynamic Snitch
- 실제 snitch 위에 쌓임.
- 각 노드의 퍼포먼스에 대한 pulse를 유지함.
- 노드 상태에 따라 복제본을 쿼리할 노드를 결정함.
- 모든 snitch들에 대해 디폴트로 켜져있음.
- https://www.datastax.com/blog/dynamic-snitching-cassandra-past-present-and-future

### Cloud-Based Snitches
- AWS, Google Cloud, Cloudstack이 있음.

### Configuring Snitches
- 클러스터 내의 모든 노드들은 같은 snitch를 사용해야함.
- 클러스터 네트워크 토폴로지를 바꾸는 것은 모든 노드들을 재시작하는 것을 필요로 함.
- 순차적인 repair를 실행하고 각각의 노드에 대해 cleanup을 해야함.

## Replication 
- RF가 2 이상이면 이웃의 데이터도 가지고 있음.
- 데이터 쓰기 요청이 들어오면 해당 데이터를 담당하는 RF개의 노드에 데이터가 써짐.
- 보통 RF로 3을 많이 씀.
- 데이터는 코디네이터에 의해 찾을 수 있음.
- 왜냐하면 토폴로지가 링을 통해 공유되기 때문임.

### Multi DC Replication
- 예시
  - DC - West: 0, 25, 50, 75
  - DC - Ease: 13, 38, 63, 88
- DC 별로 RF를 각각 가질 수 있음.
  ```
  WITH REPLICATION = {
      'class':'NetworkTopologyStrategy',
      'dc-west': 2, 'dc-east': 3
  }
  ```
- 특정 DC에 데이터 쓰기 요청을 받았을 때, 코디네이터는 자신의 DC 뿐만 아니라 다른 DC에도 비동기적으로 데이터를 전달함.
- 다른 DC에서 해당 데이터를 받으면 로컬 데이터 센터에 복제함.

## Consistency
- 카산드라는 CAP 이론에서 Availability, Partition Tolerance를 선택하고 Consistency는 좀 포기함.
- 데이터를 쓸 때 CL(Consistency Level)을 지정할 수 있음.

### CL=ONE
- 노드 하나에서만 ACK해도 코디네이터가 클라이언트에 ACK를 보냄.
- 가장 빠른 consistency level.
- 단, 헷갈리지 말아야할 게 데이터를 노드 하나에 쓴다는 게 아니라 ACK를 하나에서만 받으면 바로 OK 하겠다는 거임.

### CL=QUORUM
- 51% 이상의 노드가 write를 ACK 하거나 read를 동의해야함.
- RF=3이라면 최소 2개의 노드가 ACK를 해야함.

### CL=ALL
- 모든 노드가 ACK 하거나 동의해야함.
- 이렇게 하면 Availability, Partition Tolerance를 희생해야하므로 추천하지 않음.
- 느림.

### Qurum
- WRITE_CL=QUORUM & READ_CL=QUORUM 로 하면 됨.
- WRITE_CL=ALL & READ_CL=ONE 보다 좋음.
- availability를 희생하지 않고 string consistency를 얻는 법임.

### One
- WRITE_CL=ONE & READ_CL=ONE
- 로그, TS 데이터 같이 강한 consistency가 요구되지 않을 때 유용하게 쓰일 수 있음.
- consistency 보다 strong availability가 더 좋을 때.

### Consistency Across Data Centers
- LOCAL_QUORUM 이면 노드가 위치한 DC의 쿼럼만 검사함.
- QUORUM은 전체 DC의 쿼럼을 검사함.

### Consistency Settings
- consistency가 높을 수록, stale data를 얻을 확률이 적어짐.
  - 대신 latency를 지불해야함.
  - 상황에 따라 다름.

## Hinted Handoff
- 코디네이터가 레플리카에 쓰기 데이터를 보내던 중 노드가 다운되면 데이터를 자신이 저장했다가 노드가 온라인 상태가 되면 다시 보냄.
- 힌트를 파일에 저장함.

### settings
- `cassandra.yaml`
- hinted handoff를 끌 수도 있음.
- hints 파일을 저장할 디렉토리를 고를 수 있음.
- 노드가 힌트를 저장할 시간을 지정할 수 있음.
- 디폴트는 세 시간임.

### Consistency Level ANY
- ANY는 hint만 저장하는 거임.
- ONE 이상은 적어도 하나의 레플리카가 쓰기를 성공해야함.
- hint만으로는 충분하지 않음.

## READ Repair
### Anti-Entropy Operations
- 네트워크 파티션은 노드들의 싱크가 맞지 않도록 만듦.
- availability와 CL 사이에서 선택해야함.
- CAP 이론
- availability를 선택하는 것은 네트워크 파티션 동안 실제 데이터에 대해 레플리카간에 동의하지 않는 부분이 있을 수 있다는 것임.

### Normal Read
- CL=ALL
- 코디네이터가 읽기 요청을 보냄.
- 가장 반응이 빠른 노드가 코디네이터에게 실제 데이터를 보냄.
- 최적화를 위해 다른 레플리카들에게는 실제 데이터가 아니라 데이터의 digest나 체크썸만 요구함.
- 코디네이터는 데이터의 체크썸을 구함.
- 모든 다른 노드들의 체크썸과 비교하고 클라이언트에 리턴함.

### Read Repair
- CL=ALL
- 레플리카들의 체크썸이 일치하지 않을 수 있음.
- 데이터는 타임 스탬프를 저장하고 있기 때문에, 코디네이터는 어떤 레플리카가 최신 데이터를 가지고 있는지 결정할 수 있음.
- 코디네이터는 데이터를 반환하지 않은 나머지 레플리카들에게 데이터를 요청함.
- 레플리카가 반환한 데이터 중 최신 데이터를 제외한 나머지는 버림.
- 클라이언트에게 데이터를 반환하는 동시에 최신 데이터를 가지고 있지 않은 레플리카들에 최신 데이터를 보냄.

### Read Repair Chance
- CL=ALL 미만인 상태에서 읽기를 할 때 수행됨.
- 항상 하는 건 아니고 read repair chance로 설정한 것에 따라 달라짐.
- 레플리카 서브셋에 대해서만 읽기를 요청함.
- 레플리카들이 싱크가 맞는지 확신할 수 없음.
- 보장은 못 하지만 안전하기 할 거임.
- read repair는 백그라운드로 비동기적으로 수행됨.
- 디폴트로 `dclocal_read_repair_chance`는 0.1로 설정돼있음.
  - 코디네이터 노드와 같은 DC로 제한돼있음.
- 디폴트로 `read_repair_chance`는 0으로 설정돼있음.
  - 모든 DC에 걸쳐있음.

### Nodetool Repair
- 클러스터내의 모든 데이터에 대해 싱크를 맞춤.
- 비용이 비쌈.
  - 클러스터의 데이터 양에 따라 증가함.
- 높은 쓰기/삭제를 수행하는 클러스터에 사용하면 됨.
- 실패한 노드가 online으로 돌아왔을 때 싱크를 맞추기 위해 사용할 수 있음.
- 자주 읽기 요청이 안 가는 노드에 대해 수행할 수 있음.

## Node Sync
### Full Repairs
- full repairs는 시스템을 마비시킴. (bog down)
- 클러스터와 데이터 셋이 클수록, 시간이 더 걸림.
- 과거에는 `gc_grace_seconds` 내에 full repair를 하는 것을 추천했음.

### Node Sync
- 백그라운드로 지속적으로 데이터를 복구함.
  - 조용히 하기 vs 모두가 멈추기
- full repair 보다는 작은 단위로 repair를 하는 게 나음.
- 데이터 스택 엔터프라이즈 버전에서는 자동으로 활성화돼있음.
  - 하지만 테이블 단위로 활성화해야함.

### Detail
- 각각의 노드는 NodeSync를 수행함.
- NodeSync는 지속적으로 데이터를 검증하고 복구함.
- 테이블 기반으로 활성화함. 디폴트는 비활성화.
```
CREATE TABLE myTable (...) WITH nodesync = {'enabled': 'true'};
```

### Save Points
- 각각의 노드는 로컬 레인지를 세그먼트들로 나눔.
  - 테이블의 작은 토큰 레인지
- 각각의 세그먼트는 세이브 포인트를 만듦.
  - 노드 싱크는 세그먼트를 리페어함.
  - 그 다음 노드 싱크는 자신의 진행률을 저장함.
  - 반복
- 노드 싱크는 데드라인 타켓을 만족하기 위해 세그먼트들에 우선 순위를 매김.
  - `gc_grace_seconds`는 디폴트로 10일.
  - 각각의 세그먼트는 해당 날짜 안에 리페어됨.

### Segments Size
- 주어진 세그먼트 내의 토큰 레인지를 결정하는 것은 간단한 리컬시브 스플릿임.
- 목표는 각각의 세그먼트가 200MB 보다 작게 하는 것임.
  - config로 `segment_size_target_bytes`를 조절할 수 있지만 디폴트가 좋음.
  - 파티션보다는 큼
  - 그래서 200MB 보다 큰 파티션들은 200MB보다 작은 세그먼트들에 win함.
- 알고리즘은 데이터 사이즈를 계산하지 않음. 대신, 클러스터 내에서 수용할 수 있는 데이터의 분산을 가정함.

### Segment Failures
- 노드들은 세그먼트들을 통째로 검증하거나 리페어함. (atomic unit)
- 만약 노드가 세그먼트 검증 동안 실패한다면, 노드는 해당 세그먼트에 대한 모든 작업을 버리고 다시 시작함.
- 노드는 `system_distributed.nodesync_status` 테이블에 성공적인 세그먼트 검증들을 기록함.

### Segment Validation
- 노드 싱크는 간단하게 세그먼트에 대해 리드 리페어를 수행함.
- 모든 레플리카들에 대해 데이터를 읽음.
- inconsistencies를 확인함.
- stale 노드들을 리페어함.

## Write Path
- 쓰기 요청이 왔을 때 `MemTable`(memory)와 `Commit Log`(disk)에 모두 기록함.
- `MemTable`은 항상 파티션 키와 클러스터링 컬럼들에 의해 정렬돼있음.
- 하지만 `CommitLog`는 순차적으로 저장돼서 모든 레코드가 단지 커밋 로그에 어펜드됨.
- 그 다음으로 클라이언트에 ACK를 보냄.
- 멤테이블을 데이터를 읽기 위해서, 커밋 로그는 재해로부터 복구하기 위해 사용함.
- 메모리에 얼마나 저장할지 지정할 수 있음.
- 멤테이블에 일정 수준 이상 저장하면 디스크로 플러쉬함.
- 커밋 로그에 있던 동일한 내용을 제거함.
- 디스크에 플러쉬된 걸 `SSTable(Sorted Stream Table)`이라고 함.
- 중요한 점은 이 자료구조는 immutable함.
- 커밋 로그와 SSTable은 다른 하드 디스크에 저장하는 게 좋음.
- 하드 디스크에 여러 가지 작업으로 부하가 가기 때문에 분리하는게 성능상 좋음. 특히 HDD를 쓴다면 더욱...

## Read Path
- 데이터는 메모리인 MemTable과 디스크인 여러 개의 SSTable에 나눠져있음.
- 그래서 여기 있는 데이터들을 합체시켜야됨.

### Reading a MemTable
- 메모리에서 파티션 토큰에 대해 바이너리 서치를 통해 데이터를 가져감.
- MemTable에서 읽는 건 굉장히 빠름.

### Reading an SSTable
- 각 파티션 별로 SSTable에 같은 길이를 가지지 않음. 어떤 건 적고, 어떤 건 더 많음.
  ```
  0   1,120 ...
  | 7 | 13  |
  ```
- partition index에 token에 대한 Byte Offset을 인덱싱함. 디스크에 저장함.
  ```
  | Token | Byte Offset |
  | ----- | ----------- |
  | 7     | 0           |
  | 13    | 1,120       |
  ```
- partition index가 커지는 것을 대비해 메모리에 별도의 자료구조를 저장함.
- `partition summary`라고 함. 각 토큰 범위가 몇 번째 바이트에 속하는지 나타냄. 해당 바이트부터 토큰을 찾음.
  ```
  | Token | Byte Offset |
  | ----- | ----------- |
  | 0-20  | 0           |
  | 21-55 | 32          |

  7 ~ 18: 0 byte ~ 32 bytes 전까지
  21 ~ 36: 32 bytes 부터 48 bytes 전까지
  ```
- 같은 토큰에 대해 다시 찾을 수 있기 때문에 메모리에 방금 읽었던 token과 byte offset을 `key cache`에 저장시켜놓음.
  ```
  | Token | Byte Offset |
  | ----- | ----------- |
  | 13    | 6,224       |
  ```

### Bloom Filter
- 데이터 존재 유무에 대해서 알려주는 필터.
- 메모리에 저장함.
- 요청한 파티션 키에 대해 있거나 알 수 없다면 파티션 써머리와 인덱스를 보고 없다면 보지 않음.
- 블륨 필터는 종종 false positive가 발생할 수 있음.
- 하지만 메모리를 좀 더 쓰면 이 확률을 줄일 수 있음.

## Compaction
- 기존에 존재하는 `SSTable`에 있는 오래된 데이터를 제거하는 과정
- 여러 개의 `SSTable`을 하나로 만듦.

### Compaction Partitions
- 위쪽 SSTable이 아래쪽 SSTable 보다 먼저 만들어짐. 괄호는 타임 스탬프.
```
1   Johnny (92)
2   Betsy (49)
3   Nicholi (85)
4   Sue (41)
5   Sam (96)

---

1   Johnny (181)
2   X (176) # tombstone greater than `gc_grace_seconds`
3   Norman(148)
5   (X) (184) # tombstone less than `gc_grace_seconds`
6   Henrie (134)
```
- 컴팩션할 때, 타임 스탬프가 더 큰걸 씀.
- tombstone이 `gc_grace_seconds`보다 오래됐다면 tombstone은 추방됨. 그렇지 않다면 데이터 복구를 위해 남겨둠.
- 업데이트되지 않은 레코드는 그대로 추가함.
- 컴팩션 결과는 아래와 같음.
```
1   Johnny (181)
3   Norman(148)
4   Sue (41)
5   (X) (184)
6   Henrie (134)
```
- 컴팩션에 사용한 오래된 SSTable은 제거함.

### Compacting SSTables
- SSTable 내에 파티션을 파티션 키 기준으로 정렬해놓음.
- 컴팩션을 하는 두 테이블에 stale 데이터(stale tombstone)가 많으면 컴팩션 이후 크기가 줄어듦.
```
| 7 | 13      | 18   | 21      | 58   |
| 3   | 7     | 18      | 36 | 58    | 84   |


| 3   | 7 | 13 | ...
```

### Compacting Strategies
- 모든 SSTable을 합칠 수 없으므로, 어떤 테이블끼리 합칠 건지 결정 해야됨.
- 컴팩션 전략은 configurable 함.
- 아래와 같은 걸 포함함.
  - `SizeTieredComapction`: 디폴트. 작은 사이즈의 여러 개의 SSTable들이 있을 때 트리커. write heavy workload에 적절함.
  - `LeveledCompaction`: SSTable들을 레벨로 그룹핑함. 각각의 레벨은 고정된 크기를 가지고 있음. read heavy workload에 적절함.
  - `TimeWindowCompaction`: SSTable의 time windowed 버켓들을 만듦. `SizeTieredComapction`를 이용해서 서로 컴팩션함. TS data에 적절함.
- `ALTER TABLE` 커맨드를 이용해서 전략을 바꿀 수 있음.

## Data Modeling
### What is Data Modeling?
- 도메인의 요구사항을 분석함.
- 엔티티들과 relationship들을 식별함 - Conceptual Data Model
- 쿼리를 식별함 - Workflow and Access Patterns
- 스키마를 구체화함 - Logical Data Model
- CQL로 작업을 함 - Physical Data Model
- 최적화하고 튜닝함

### Model for Queries
- 쿼리가 짱짱맨임.
- 가능하다면
  - 어플리케이션의 워크플로우를 이해해야함.
  - 어플리케이션이 지원해야하는 쿼리의 타입을 이해해야함.
  - 쿼리를 기반으로 해서 테이블을 빌드함.

## Relational vs Cassandra
### Relational
- data - model - application
- entity가 짱짱맨
- pk는 고유함을 위해 존재
- single point of failure를 가짐.
- ACID compliant
- 조인과 인덱스들
- referential integrity가 강요됨.

### Cassandra
- application - model - data
- 쿼리가 짱짱맨
- pk는 고유함 이상을 위헤 존재
  - 읽기와 쓰기 성능을 결정함.
- 분산 아키텍처
- CAP 이론
- Denormalization
- RI가 강요되지 않음.

### Transactions in Cassandra
- 카산드라는 ACID 트랜잭션을 지원하지 않음.
- ACID는 상당한 퍼포먼스 패널티를 일으킴.
- 여러 유즈 케이스들에서 필요하지 않음.
- 하지만, 싱글 카산드라 쓰기 연산은 ACID 프로퍼티를 증명함.
  - INSERT, UPDATE, DELETE들은 atomic, isolated, durable 함.
  - 데이터 레플리케이션에 대한 tunable consistency, 하지만 어플리케이션 인티그리티 제약을 다루지는 않음.
  - AP DB이기는 하지만 원한다면 availability를 희생하고 좀 더 높은 consistency를 가져갈 수도 있음.

### Denormalization
- 조인을 분산 시스템에서 구현할 때의 주요 문제 중 하나는 다른 테이블에서 레퍼런스하는 데이터가 또 다른 노드에 존재해야한다는 것임.
- 이로인해 레이턴시에 예측 불가능한 영향을 줄 수 있음.
- 그래서 카산드라는 조인을 지원하지 않음.
- 조인할만한 테이블을 위해 각각의 테이블을 생성하는 것을 추천함.
  - 예를 들어, 비디오, 댓글, 유저가 있다고 해보자.
  - 비디오에 대한 댓글과 유저가 남긴 댓글을 얻고 싶다면 `comments_by_video`와 `comments_by_user` 테이블을 별도로 생성한다.
    ```
    comments_by_video: video_title, comment_id, user_id, video_id, comment # PK ((video_title), comment_id)
    comments_by_user: user_login, comment_id, user_id, video_id, comment # PK ((user_login), comment_id)
    ```
- 테이블 이름에 `by`로 어떤 쿼리를 서포트하기 위해 만들어진 테이블인지 나타냄.

### Referential Integrity
- 카산드라는 referential integrity를 강요하지 않음.
- 퍼포먼스 때문에. 쓰기 전에 읽기를 요구함.
- 애플리케이션 레벨에서 강요할 수 있음.
- 아파치 스파크로 DSE 분석을 돌려서 검증할 수도 있음.

## Getting Started CQL
### Keyspaces
- top-level namespace/container
- RDB 스키마랑 유사함.
  ```
  CREATE KEYSPACE killrvideo
    WITH REPLICATION = {
      'class': 'SimpleStrategy',
      'replication_factor': 1
  };
  ```
- 레플리케이션 파라미터들이 요구됨.

### Tables
- keyspaces는 테이블을 저장하고 테이블은 데이터를 저장함.
- 모든 테이블은 PK를 포함함.

### TRUNCATE
- 즉시 그리고 돌이킬 수 없게 테이블의 모든 데이터를 제거함.
- 노드 중 하나라도 다운돼있다면 커맨드는 실패함.

### ALTER TABLE
- 컬럼의 데이터 타입을 바꾸거나, 컬럼을 추가하거나, 컬럼을 없애거나, 컬럼을 리네임하거나, 테이블 프로퍼티를 바꿀 수 있음.
- 하지만, PRIMARY KEY 컬럼들을 바꿀 수 없음.

### SOURCE
- CQL statements를 포함하는 파일을 실햄함.
- 각각의 staement에 대한 아웃풋이 차례로 보림.
```
SOURCE './myscript.cql';
```

## Fundamentals of cassandra table
### Terminology
- data model
  - 데이터를 조직화하기 위한 추상적인 모델
  - 쿼리의 기반이 됨.
- Keyspace
  - relational schema와 비슷함.
  - 모든 테이블들은 keyspace 내에 있음.
  - keyspace는 복제를 위한 컨테이너
- Table
  - keyspace에 그룹핑됨.
  - 컬럼들을 포함함.
- Partition
  - 파티셔닝 전략에 따라 특정한 노드에 저장된 로우들.

### Table Terminology
- Row
- Column
  - RDB에 있는 컬럼과 비슷함.
  - PK
    - 테이블 내에 있는 데이터에 접근하는데 사용되고 고유성을 보장함.
- Partition Key
  - 데이터가 저장될 노드를 결정함.
- Clustering column
  - 파티션 내에서 로우의 순서를 결정함.

### Data Types
- UUID vs TimeUUID
  - https://microeducate.tech/cassandra-uuid-vs-timeuuid-benefits-and-disadvantages/
  - sorting의 차이
- Blob: 어떤 건지 모를 때 걍 이걸로 하면 됨.
- Counter: 카운트 증가와 감소에 사용함.

## Partitioning & Storage Structure
### Storage Structure
- 컬럼은 `key`와 `value`를 묶어 `cell`이라고 불림.
- 파티션 키는 PK의 첫번째 값임.
- Non PK 컬럼에 where
  - 카산드라는 여러 노드에 걸쳐 파티션을 분산시킴.
  - 파티션 키를 제외한 아무 필드에 `WHERE`를 하는 것은 모든 노드의 모든 파티션을 스캔하는 것을 필요로 함.
  - 비효율적인 액세스 패턴.
  - 데이터를 찾기 원한다면 파티션 키를 제공해야됨.
- 파티션 키 값에 where
  - 클러스터링 컬럼들 뿐만 아니라 파티션 키 값에 WHERE를 할 수 있음.
  - 카산드라는 어떤 노드가 원하는 파티션을 포함하는지 빠르게 결정하기 위해 해싱 알고리즘을 사용함.
- 클러스터링 컬럼들과 함께 파티션 키를 적절하게 사용하면 리드 속도가 빨라짐.

### Primary Key
- Simple Primary Key
  - 파티션 키만 포함함.
  - 어떤 노드가 데이터를 저장하는지 결정함.

### Composite Partition Keys
- Multi-value primary key
  - multi value를 항상 알 수 있다면 스피드에 매우 좋음.
- 예시
  ```
  CREATE TABLE videos (
      name text,
      runtime int,
      year int,
      PRIMARY KEY ((name, year))
  );
  ```
- 단, 명심할 것은 where에 항상 여러 개의 파티션 키를 모두 적어줘야됨.

### Primary Key vs. Partition Key
- Partition key
  - 파티션이 어느 노드에 저장될지 결정하는 PK의 일부분.
  - placement where in the cluster is my data.
- Primary key
  - 파티션 키와 모든 클러스터링 컬럼들을 포함함.
  - everything inside of this primary key designation

## Clustering Columns
- 카산드라가 각각의 파티션 내에서 데이터를 정렬하는 방법
- `PRIMARY KEY` 구문 내에서 파티션 키 이후에 오는 부분
- optional 값
- `PRIMARY KEY`에 클러스터링 컬럼을 추가한다면, where에 추가하는 게 좋음.
- `PRIMARY KEY`가 아닌 컬럼만 사용하는 건 좋지 않음.

### Cluster Column Ordering
- ordering은 클러스터링 컬럼에서 제일 중요한 것임.
- 기본은 ascending, 하지만 descending으로도 할 수 있음.
  ```
  CREATE TABLE videos (
    ...
    PRIMARY KEY ((year), name)
  ) WITH CLUSTERING ORDER BY (name DESC);
  ```
- clustering column을 잘 지정해놓으면 런타임이 아닌 미리 정렬된 상태로 결과를 가져올 수 있음.

### Querying Clustering Columns
- lookup이 빠르기 때문에 클러스터링 컬럼들에 쿼리를 할 수 있음.
- 매우 효율적인 operation임.
- 파티션 키로 해당하는 파티션을 가고, 클러스터링 컬럼으로 해당 데이터가 파티션 내에 어디 있는지 찾음.
- 하나 이상의 SSTable일 수 있음.
- 클러스터링 컬럼들에 range query도 할 수 있음.

## Denormalization
- 비정규화를 하면 중복된 데이터를 가질 것임.
- 필요할 때 데이터를 얻는 것이므로 괜찮음.

### Denormalizing For Query Performance
- 카산드라는 조인 없이 동작함.
- 단, 각각의 테이블에 대해 PK를 다르게 구성함.
  - comments_by_video: ((title), comment_id)
  - comments_by_user: ((user_login), comment_id)
- 효율적이고 예측 가능한 쿼리 퍼포먼스를 줌.

## Collections
- 컬럼에 데이터를 같이 그룹핑하고 하고 저장함.
- 컬렉션 컬럼들은 multi-valued 컬럼들임.
- 작은 양의 데이터를 저장하도록 디자인돼있음.
- 전체를 얻음.
- 컬렉션 내에 다른 컬렉션을 내장할 수 없음.
  - `FROZEN`을 사용하면 가능함.

### SET Collection Type
- 고유한 값들의 컬렉션
- 정렬되지 않은 채 저장되지만, 정렬된 상태로 얻음.
- 예제
  ```
  CREATR TABLE users (
    ...
    emails set<text>
  );

  INSERT INTO ... VALUES (... , {'abc@email.com', '123@email.com'});
  ```

### LIST Collection Type
- SET과 비슷함. 같은 셀에 밸류들의 컬렉션이 있음.
- 고유할 필요가 없고 중복될 수 있음.
- 특정 순서로 저장됨.
- 예제
  ```
  ALTER TABLE users ADD freq_dest list<text>;

  UPDATE users SET freq_dest = ['Berlin', 'London', 'Paris']
    WHERE id = 'cass123';
  ```

### MAP Collection Type
- 키-밸류 페어의 typed collection.
- 고유한 키들로 정렬됨.
- 예제
  ```
  ALTER TABLE users ADD todo map<timestamp, text>;

  UPDATE users SET todo = {'2018-1-1': 'abc', '2018-1-2': 'fdf'}
    WHERE id = 'cass123';
  ```

### Using Frozen in a Collection
- 만약 nest 데이터 타입을 원한다면, `FROZEN`을 사용해야함.
- 컬렉션에서 `FROZEN`을 사용하는 것은 여러 컴포넌트들을 하나의 값으로 시리얼라이즈함.
- `FROZEN` 컬렉션에 있는 값들은 blobs처럼 여겨짐.
- Non-frozen 타입들은 개별 필드들을 업데이트하는 게 허용됨. 하지만 `FROZEN`은 허용되지 않음.
- 카산드라에서는 비정규화를 해야하기 때문에, 하나의 테이블로 만들어질 수 있는 자료를 `TYPE`으로 만들어서 특정 테이블의 컬럼 하나로 내장할 수 있음.

## UDTs
- collection으로도 해결 안 되는 복잡한 자료를 저장해야할 때 사용함.
- 관련된 필드들의 정보를 그룹핑함.
- 여러 데이터 필드들을 하나의 컬럼으로 attach 할 수 있음.
- 컬렉션과 다른 UDTs를 포함해 어떤 데이터 타입이든 될 수 있음.
- 더 복잡한 구조를 하나의 컬럼내에서 포함하는 게 가능해짐.

### Example
- 타입 생성
```
CREATE TYPE address (
  street text,
  city text,
  zip_code int,
  phones set<text>
);
```

### Using Created UDTs
- 테이블 정의에서 새로 생성된 타입을 사용함
```
CREATR TABLE users (
  id uuid,
  name frozen <full_name>,
  direct_reports set<frozen <full_name>>,
  address map<text, frozen <address>>,
  PRIMARY KEY ((id))
);
```

## Counters
### Counter Datatype
- 64-bit signed int를 저장하는데 사용되는 컬럼.
- 증가하거나 감소하는 방식으로 변경됨.
- 값들이 `UPDATE`를 사용해서 변경됨.
- pk와 카운터 컬럼만 가지는 특별하게 할당된 테이블이 필요함.
  - 하나 이상의 카운터 컬럼을 가질 수 있음.
 
### Counter Example
(해당 부분 안 들음)
- 태그당 있는 비디오 개수에 대한 쿼리를 허용함.
```
CREATE TABLE moo_counts (
  cow_name text,
  moo_count counter,
  PRIMARY KEY ((cow_name))
);

UPDATE moo_counts
SET moo_count = moo_count + 8
WHERE cow_name = 'Betsy';
```

### Counter Considerations
- 분산 시스템은 consistency 이슈를 발생시킬 수 있음.
- 밸류를 INSERT 하거나 할당할 수 없음. -> 디폴트가 0임.
- non PK 컬럼에 대해서만 가능함.
- 멱등성이 성립하지 않음.
- `UPDATE` 커맨드를 사용해야함.
- 카운터 컬럼은 인덱스 되거나 삭제될 수 없음.

## UDFs And UDAs
- Skip

## Conceptual Data Modeling
- 도메인을 모델링함.
- 도메인의 추상적인 뷰.
- 기술적으로 독립적임.
- 특정 DB 시스템에 종속되지 않음.
- Attribute Types: 엔티티 대해 데이터를 저장할 필드나 관계.
- Composite Attributes: 관련된 에트리뷰트들을 함께 그룹핑함.
- Multi-values Attributes: 엔티티당 여러 값들을 저장하는 에트리뷰트.

### Cardinality
- 엔티티들 간의 관계들.
- 엔티티가 관계에 참여해야하는 횟수.

### Weak Entity Types
- 스트롱 엔티티 타입에 대한 식별 관계 없이 존재하지 못함.

## Application Workflow & Access Patterns
- 카산드라는 query driven 임. 데이터 모델을 알기 전에 쿼리를 어떻게 사용할지를 먼저 알아야 됨.

### Application Workflow
- 각각의 어플리케이션 워크 플로우를 가짐.
- 액세스 패턴들은 어떻게 데이터가 접근되는지 결정하는데 도움을 줌.

## Mapping Conceptual To Logical Model
### Query-Driven Data Modeling
- Conceptual Data Model(ERD) + Access Patterns(Queries) -> Mapping Rules & Patterns - Chebotko Diagram -> Logical Data Model
- 파티션 키와 클러스터링 컬럼이 중요함.

### Data Modeling Principles
#### 데이터
- conceptual 데이터 모델에 의해 알게된 데이터
- DB에 무엇이 저장돼있는지 정의
- 데이터가 올바르게 정리되기 위해 프로퍼티들을 보존
- 엔티티와 관계 키는 테이블의 pk에 영향을 끼침
- pk는 고유하게 로우, 엔티티, 관계를 식별함

#### 쿼리
- 쿼리는 애플리케이션 워크플로우 모델을 통해 알 수 있음.
- 테이블 스키마 디자인은 쿼리가 바뀐다면 바뀜.
- 쿼리당 하나의 파티션이 가장 효율적인 접근 패턴
  - 쿼리는 결과를 얻기 위해 오직 하나의 파티션만 접근함.
  - 파티션은 하나의 로우나 여러 개의 로우가 될 수 있음.
- 쿼리가 여러 개의 파티션에 접근하는 것도 나쁘지는 않음.
- 안티 패턴은 쿼리가 모든 파티션들에 접근해야하는 것임.

#### 데이터 중첩(Nest)
- data nesting은 주요 데이터 모델링 기술.
- 네스팅은 여러 엔티티들을 하나의 파티션으로 정리함.
- 쿼리당 파티션 데이터 접근을 지원함.
- 세 가지 데이터 네스팅 메커니즘
  - 클러스터링 컬럼 -> multi-row 파티션
  - 컬렉션 컬럼
  - UDT 컬럼
- 클러스터링 컬럼
  - 주로 사용하는 메커니즘
  - 파티션 키는 다른 엔티티들이 중첩될 엔티티를 식별함.
  - 클러스터링 컬럼 내의 값들을 중첩되는 엔티티들을 식별함.
  - 여러 개의 클러스터링 컬럼들을 멀티-레벨 네스팅을 구현함.
- UDT 컬럼
  - 두번째 메커니즘
  - 1:1 관계를 나타내지만 컬렉션들과 함께 사용할 수 있음.
  - 여러 개의 컬렉션 컬럼들과 사용하는 것보다 쉬움.

#### 데이터 중복
- 조인하는 것보다 데이터 중복이 나음.
- 쿼리당 파티션과 데이터 네스팅은 데이터 중복을 가져올 것임.
- 쿼리 결과들은 미리 계산되고 구체화됨.
- 데이터는 테이블, 파티션, 혹은 로우를 걸쳐 중복될 수 있음.
- 물론 새로운 쓰기 요청이 들어올 때, 각각의 테이블에 써서 싱크를 맞춰야하기 때문에 고통스러울 수 있음.
- 하지만 이렇게 해서 constant 시간 접근을 가짐.
- 중복되는 데이터가 없다면 쓸 때는 편하겠지만, 여러 테이블에 쿼리해야하기 때문에 네트워크를 기다리는 시간이 늘어남.
  - (videos_by_actor, videos) vs (videos_by_actor)
  - 배우 정보 따로 비디오 정보 따로 vs 배우 정보와 비디오 정보 같이

## Mapping Rules
- 쿼리 드리븐 방법론을 위함.
- mapping rules는 로지컬 데이터 모델이 올바르도록 확신함.
- 각각의 쿼리는 대응하는 테이블을 가짐.
- 테이블들을 쿼리가 적절하게 수행되도록 디자인됐음.
- 테이블들은 올바른 순서로 데이터를 리턴함.
1. Entities and relationships
2. Equality search attributes: where. 파티션 키 혹은 클러스터링 컬럼.
3. Inequality search attributes: where. 클러스터링 컬럼. 레인지 쿼리.
4. Ordering attributes: order by. 클러스터링 컬럼.
5. Key attributes: uniqueness.

## Analysis And Validation
- 도메인에서의 요구사항이 바뀜.
- 데이터 모델이 더 이상 효과적이지 않음.
- 데이터가 불균형적이게 됨.
- 특정 노드에 대한 뜻밖의 로드는 핫스팟이 됨.

### 데이터 모델 변화 혹은 새로운 요구사항 처리
- 중요한 고민 사항들을 아래와 같음.
- natural 혹은 surrogate 키?
  - surrogate키는 특정 열을 PK로 하지 않고 시스템에 독립적으로 할당된 키. 예를 들면, serial 같은 거.
  - natural 키의 경우, 파티션 하나가 무한하게 커질 수 있음.
  - surrogate 키는 생성되는 키이기 때문에, 파티션당 하나의 로우를 가짐.
- 쓰기 충돌이 가능함?
  - race condition.
  - 예를 들면, 유저 등록시 동일한 유저 이름이 있는지 체크할 때.
- 어떤 데이터 타입이 사용돼야하는지.
  - signed 32 bits int를 썼을 때, 일정 년도가 지나면 다룰 수 있는 레인지에서 벗어남.
- 파티션이 얼마나 큰지.
- 얼마만큼의 데이터 중복이 요구되는지.
  - 비정규화로 인한 중복.
- 클라이언트 사이드 조인이 요구되는지와 코스트가 얼만큼인지.
  - 비정규화로 인한 중복이 너무 많아져서 선택한다면, 조인이 끝나기 전에 메모리는 얼마나 필요하고 데이터는 얼마나 옮겨져야하는지 등 많은 것을 고려해야함.
- 데이터 일관성의 비정상(anomaly)가 가능한지.
  - 비정규화로 데이터의 중복이 생기면 다른 테이블의 중복 데이터간에 일관성이 맞지 않을 수 있음.
- 어떻게 트랜잭션과 데이터 어그리게이션이 가능한지.

## Write Techniques
### Data Consistency with Batches
- 스키마 데이터 일관성은 데이터 카피의 올바른 것을 지칭함.
- 데이터 중복이 있다면, 사용자가 일광성에 대해 고민하고 처리해야함.
- 스키마 내의 같은 데이터의 모든 카피들을 같은 값을 가져야함.
- 데이터 추가, 업데이트, 삭제는 여러 번의 insert, update, delete를 요구할 수 있음.
- logged batches는 일관성을 유지하기 위해 만들어졌음.

### Batch
- 여러 데이터 수정 statement로 이루어져 있음.
- 쓰기 요청이 한 번에 코디네이터 노드에 감.
- batch가 받아들여지면 DB에 반영됨.
- 예제
  ```
  BEGIN BATCH
      UPDATE videos ...
      INSERT INTO videos_by_title ...
      DELETE FROM videos_by_title ...
  APPLY BATCH;
  ```
- 클라이언트가 코디네이터 노드에 배치를 보냈을 때 먼저 하는 것은 배치를 특별한 로그에 저장하는 것임.
- 실행 전에 코디네이터 노드와 레플리카 노드에 로그로 써짐.
  - 배치는 쓰기가 적용되거나 힌트될 때 성공함.
  - 레플리카들은 코디네이터 노드가 배치 중간에 실패하면 떠맡음.
- ACID 트랜잭션의 일부를 사용할 수 있는 방법.
  - 카산드라가 배치가 성공하는 것을 보장하기 때문에 롤백을 구현할 필요가 없음.
  - 하지만 배치 격리는 없음. 클라이언트가 부분적으로 업데이트된 로우들을 읽을 수 있음.

### Misconceptions about Batches
- 벌크 로딩을 위해 만들어진게 아님.
  - 데이터 로드에 대한 성능을 거의 증가시키지 않음.
  - 코디네이터가 과도하게 일을 해서 성능 보틀넥이나 다른 이슈를 만들 수 있음.
- 배치내의 연산들에 대해서 순서가 없음.
  - 모든 쓰기들을 같은 타임스태프로 수행됨.

## Read Techniques
### Secondary Indexes
- 보통 금지된 컬럼에 대해 쿼리하는 게 가능해지도록 하는 컬럼에 대한 인덱스
  - 테이블 구조는 영향받지 않음.
  - 테이블 파티션들은 파티션 키에 기반해 클러스터내의 노드들에 걸쳐 분산됨.
- 카운터와 스태틱 컬럼들을 제외한 컬렉션을 포함해 어떤 컬럼이든지 생성될 수 있음.
- 세컨드 인덱스는 파티션을 가지고 있는 노드들에 추가적인 자료 구조를 만듦.
  - 각각의 로컬 인덱스는 로컬하게 저장된 로우들을 인덱싱함.
  - 인덱스된 컬럼에 대한 쿼리는 모든 노드들에 대해 로컬 인덱스에 접근하는 것을 요구함. -> expensive
  - 파티션 키와 인덱스된 컬럼에 쿼리하는 것은 특정 노들들에 대해 접근하는 것을 요구함. -> efficient
- 세컨더리 인덱스가 동작하는 과정을 다음과 같음.
  - 클라이언트는 코디네이터에 쿼리 요청을 보냄.
  - 코디네이터는 모든 노드들에 요청을 보냄 - 파티션 키는 모름.
  - 각각의 노드는 자신의 로컬 인덱스를 찾음 - 결과를 코디네이터에 리턴함.
  - 코디네이터는 결과를 합치고 리턴함.

### When Secondary Indexes Are Used
- 사용해야할 때
  - 카디널리티가 낮은 컬럼들: 쿼리 한 번으로 많은 로우 리턴 가능함.
  - 프로토타입핑이나 작은 데이터 셋
  - 큰 파티션에 대해 파티션 키와 인덱스된 컬럼 모두를 검색
- 사용하지 말아야할 때
  - 카디널리티가 높은 컬럼들
  - 카운터 컬럼을 사용하는 테이블
  - 자주 업데이트 되거나 삭제되는 컬럼들

### Materialized Views
- 쿼리 결과들을 저장하는 DB 오브젝트
- 카산드라는 또 다른 테이블의 데이터로부터 테이블을 빌드함.
  - 새로운 PK와 새로운 프로퍼티들을 가짐.
- 세컨더리 인덱스들은 낮은 카디널리티 데이터에 적절함.
- materialized 뷰들은 높은 카디널리티 데이터에 적절함.
- 소스 테이블의 pk 컬럼들은 materialized 뷰의 pk의 일부분이여야함.
- materialized 뷰의 pk에 딱 하나의 새로운 컬럼만 추가 가능함.
  - 스태틱 컬럼들은 허용되지 않음.

### Creating Materialized Views
- `users` 테이블에서 `user_by_email`을 만든다고 가정함.
```
CREATE MATERIALIZED VIEW user_by_email
AS SELECT first_name, last_name, email
FROM users
WHERE email IS NOT NULL AND user_id IS NOT NULL
PRIMARY KEY (email, user_id);
```
- `AS SELECT`: 베이스 테이블에서 materialized 뷰로 카피될 컬럼들.
- `FROM`: 데이터가 카피될 소스 테이블.
- `WHERE`: 모든 PK 컬럼들을 `IS NOT NULL`로 명시해야함.
- PK 컬럼들을 명시하는 것은 중요함.
  - 소스 테이블 `users`는 `id`를 pk로 쓰므로 `id`는 materialized 뷰의 PK에 있어야함.

### Materialized Views Example
- 일반적인 테이블처럼 다루면 됨.
```
SELECT first_name, last_name, email
FROM user_by_email
WHERE email = 'test&email.com';
```

### Materialized Views Caveats
- 데이터는 소스 테이블에만 쓰일 수 있고 materialized 뷰에는 쓰일 수 없음.
- materialized 뷰는 소스 테이블에 데이터를 삽입한 후 비동기적으로 업데이트 되기 때문에, 업데이트에 딜레이가 있음.
- 카산드라는 소스 테이블이 업데이트 된 후에만 리드 리페어를 수행함.

### How To Do Data Aggregation
- 카산드라로 직접 하기
- 클라이언트에서 구현
- 아파치 스파크 사용
- 아파치 솔라 사용

## Table/Key Optimizations
### Apache Cassandra Key
- 카산드라의 PK는 uniqueness 외에 다른 목적도 있음.
- PK는 파티션 키와 클러스터링 컬럼으로 이루어짐.

### Natural Keys
- 이미 존재함.
- 직관적으로 얻을 수 있음.
- 의미가 있음.
- 쿼리하기 쉬움.
- 예시: 주민등록번호, 이메일 주소

### Surrogate Keys
- 인공적.
- 생성되는 것.
- 외부 세계에서 의미가 없음.
- 랜덤처럼 보임.
- 예시: auto incremented int, 시퀀스, UUID
- 특성
  - conflict-free 고유성
  - immutable: 시간이 지나도 바뀌지 않음.
  - uniformity
  - compactness
  - performance

### Table Optimizations
- 파티션 분리 -> size manageability
- 버티컬 파티셔닝 -> 스피드
- 파티션과 테이블 머지 -> 스피드와 중복 제거
- 컬럼 추가 -> 스피드

### 파티셔 분리
- 파티션이 너무 커질 수 있음.
- 예를 들어, 하루에 매우 액티브한 유저가 여러가지 동영상 인터렉션을 하는 것은 추천되는 파티션 값 리밋을 넘을 수 있음.
- 파티션 키에 또 다른 컬럼을 더하면 됨.
  - 존재하는 컬럼: user_id -> (user_id, video_id)
  - 인위적인 컬럼
    - user_id -> (user_id, event_date)
    - user_id -> (user_id, bucket): 각 버켓마다 개수를 조절함.
- 이론적 해석 (rationale)
  - 파티션 당 더 적은 로우 개수

### 버티컬 파티셔닝
- 테이블을 하나로 만들지 않고 컬럼 별로 테이블 나누기.
- 몇몇 쿼리들은 빠르게 수행 가능함.
- 테이블 파티션들은 더 작아짐.
- 얻기가 쉬워지고 대부분이 캐쉬 가능해짐.
- 하지만 스플릿한 테이블에서 하나가 누락되면 안 됨.
- 원래는 한 번의 쿼리로 얻을 수 있었지만 여러 번의 쿼리가 필요함.

### 파티션과 테이블 머지
- 버티컬 파티셔닝의 반대.
- 중복 제거에 효과적.
- 쿼리가 더 느려질 수 있음.
- 새로운 파티션 키를 도입하고 오브젝트를 새로운 파티션에 포함함.
- 파티션 키는 존재하거나 인위적인 컬럼들로 이루어질 수 있음.

### 컬럼 추가
- 별도의 테이블에서 관리하던 컬럼을 하나의 테이블에 넣음.

## Data Model Migration
### Primary Key Changes
- PK가 바껴야 한다면, 새로운 데이터 모델로 옮겨가야함.
- 하지만 데이터를 새로운 테이블로 옮겨야함.
- 일단 완료되면 두 테이블을 모두 유지하다가 오래된 테이블을 드롭함.
- 유즈 케이스에 따라 달라짐.

### Creating New Tables
- 현재의 스키마 파일을 CQL 스크립트에 유지하는 게 흔함.
- 스키마 체인지는 클러스터를 통해 전파해야함.
- 큰 클러스터에서는
  - 각각의 `CREATE TABLE`은 레이스 컨디션을 발생시킴.
  - 노드들은 스키마 체인지에 대해 싱크가 맞지 않을 수 있음.
- 클러스터 사이즈와 로드에 따라, 각각의 `CREATE TABLE`은 완료되는데 몇 초가 걸릴 수 있음.
- 스키마 싱크가 맞지 않으면 클러스터에 대환장이 일어날 수 있으니 조심...!
- 따르면 좋은 순서
  - 한번에 하나의 `CREATE/DROP` 테이블 커맨드만 수행
  - 클러스터를 통해 전파될 시간을 주기
  - `nodetool describecluster`를 통해 완료를 검증
  - 다음 `CREATE/DROP` 커맨드를 수행

### Application Considerations
- 왜 다른 PK가 필요한지?
  - 파티션이 너무 큰지?
  - 어플리케이션 요구사항이 바꼈는지?
  - 원래 테이블 또한 마찬가지로 필요한지?
- 기억해라, 우리는 쿼리를 충족시키기 위해 테이블을 만듦.
- 어플리케이션이 발전할 때마다, 테이블들을 추가하거나 없애야 할 수 있음.
  - 어플리케이션이 해당 테이블에 더 이상 의존하지 않을 때까지, 기존 테이블을 드롭하지 마라.
- 이상하게 디자인된 파티션으로 새로운 문제를 만들지 않도록 조심해라.

## Data Modeling Anti-Patterns
### Query Specific Anti-Patterns
- 전체 클러스터나 큰 테이블을 스캔하는 쿼리들은 비쌈.
  - 예를 들어, 전체 row 개수를 세기 위한 count를 구하는 쿼리
- 특정 결과를 얻기 위해 IN 구절을 레이어링 하는 것은 성능상 좋지 않음.
  - 특정 컬럼 값을 만족하는 로우를 구하는 쿼리.
- 쓰기 전에 읽기를 요구하는 쿼리도 비쌈.
  - 레이스 컨티션이 발생할 수도 있음.
- 필터링을 허용하는 것도 비쌈.
  - 특정 코너 케이스에 대해 과도하게 사용한다면 쿼리를 지원하는 테이블을 만드는 게 나음.
  - 쿼리가 하나의 파티션으로 제한된다는 것을 안다면 괜찮음.

### Table Specific Anti-Patterns
- 세컨더리 인덱스들이 과도하게 사용됨. (강의 자료에는 거의 사용되지 않는 걸로 적혀있는데 강사는 이렇게 말함;)
  - 이 정도로 필요하다면 별도로 테이블을 만드는 게 나음.
- non-frozen 컬렉션의 사용도 성능상 좋지 않음.
  - 컬렉션 데이터 타입이 제대로 만들어졌는지 확인하는 게 필요함.
- 날짜와 타임 스탬프를 나타내기 위해 스트링을 사용하는 것.
  - 원래의 자료형을 사용하는 게 더 좋음.

### Keyspace Level Anti-Patterns
- TTL을 사용하지 않거나 적절하게 지우지 않는 것은 tombstone들을 만들 수 있음.
  - 빈번하게 지우는 것은 컴팩션이나 이빅션보다 더 빠르게 tombstone을 만들 수 있음.
- 읽기 타임아웃을 증가시키는 걸 고려하고 있다면, 데이터 모델을 변경하는 게 어떻게 성능을 향상시키는지 봐야함.
