## Optimize - File Compaction
- https://www.youtube.com/watch?v=F9tc8EgIn3c
- 델타 레이크에서는 optimize를 통해 작은 파일을 큰 파일로 합친다.
- 하지만 time travel 때문에 이전 데이터 파일이 남아있을 수 있다.

## Unpacking The Transaction Log
### What Is the Delta Lake Transaction Log?
- `DeltaLog`로 알려져 있다.
- 처음부터 델타 레이크 테이블에서 수행된 모든 트랜잭션의 정렬된 레코드이다.

### What Is the Transaction Log Used For?
#### Single Source of Truth
- 델타 레이크는 테이블의 동시 읽기와 쓰기를 허용하기 위해 스파크 위에 지어졌다.
- 스파크는 트랜잭션 로그를 확인하여 테이블에 게시된 새 트랜잭션을 확인한 다음 새 변경 사항을 앤드 유저의 테이블에 업데이트한다.
- 이것을 통해 유저의 테이블 버전은 마스터 레코드와 동기화돼서 테이블과 컨플릭트가 나지 않도록 한다.

#### The Implementation of Atomicity on Delta Lake
- 원자성은 쓰기 연산이 완전히 수행되거나 전혀 수행되지 않도록 한다.
- 트랜잭션 로그는 델타 레이크가 원자성 보장을 제공할 수 있는 메카니즘이다.

### How Does the Transaction Log Work?
#### Breaking Down Transactions Into Atomic Commits
- 유저가 테이블을 변경하는 연산을 수행할 때마다, 델타 레이크는 연산을 일련의 개별 스텝으로 나눈다.
- 여러 액션이 있는데 세부 액션을 블로그 참고.
- 액션들은 트랜잭션 로그에 커밋이라고 하는 정렬된 원자 단위로 기록된다.

#### The Delta Lake Transaction Log at the File Level
- 유저가 델타 레이크 테이블을 생성할 때, 해당 테이블의 트랜잭션 로그는 자동으로 `_delta_log` 서브 디렉토리에 생성된다.
- 유저가 테이블에 변경을 만들면 해당 변경 사항이 트랜잭션 로그에 정렬된 원자성 커밋으로 기록된다.
- 각각의 커밋은 json 파일로 써진다.
- 커밋마다 번호가 1씩 증가한다.
- 델타 레이크는 이미 지워진 데이터일지라도 원자적 커밋을 유지한다. 테이블에 대한 감사나 time travel을 하기 위함이다.
- 또한 스파크는 디스크에서 파일들을 바로 지우지 않는다.

#### Quickly Recomputing State With Checkpoint Files
- 델타 레이크는 `_delta_log` 서브 디렉토리에 파켓 포맷의 체크포인트 파일을 저장한다.
- 체크포인트는 그 순간의 테이블의 전체 상태를 저장한다.
- 테이블의 최신 상태와 싱크를 맞출 때, 이후의 모든 트랜잭션을 읽지 않는다.
- 스피드를 높이기 위해 스파크는 `listFrom`로 현재 커밋 이후의 최신 체크포인트 파일을 읽고, 딱 그 이후의 json 커밋만 읽는다.

#### Dealing With Multiple Concurrent Reads and Writes
- 델타 레이크는 아파치 스파크를 이용하기 때문에 여러 유저가 동시에 테이블을 변경한다고 가정한다.
- 이 경우를 처리하기 위해 optimistic concurrency control을 사용한다.

#### What Is Optimistic Concurrency Control?
- 낙관적 동시성 제어는 서로 다른 사용자가 테이블에 수행한 트랜잭션(변경)이 서로 충돌하지 않고 완료될 수 있다고 가정하는 동시 트랜잭션을 처리하는 방법이다.

#### Solving Conflicts Optimistically
- 델타 레이크는 두 개 이상의 커밋이 동시에 이루어졌을 때, 이를 다루기 위한 방법으로 mutual exclusion을 따른다.
- 이 프로토콜은 ACID의 isolation을 가능하게 해준다.
- 여러 동시의 쓰기 이후에도 테이블의 결과 상태가 그런 쓰기가 순차적으로 일어났던 것과 동일하다.
- 델타 레이크는 변경 전에 읽은 테이블의 시작 테이블 버전을 기록한다.
- 동시에 변경이 이루어지면 mutual exclusion을 사용한다.
- 특정 유저의 커밋이 먼저 쓰여지고 다른 유저의 커밋은 에러가 나기보다는 낙관적으로 처리한다.
- 테이블에 새로운 커밋이 쓰였는지 확인하고 해당 변경을 반영하기 위해 테이블을 업데이트한다. 그래서 그 다음 커밋이 된다.
- 대부분의 경우에 핸들링은 조용히 성공적으로 된다. 하지만 조용히 해결하지 못한다면 에러가 발생한다.

### Other Use Cases
#### Time Travel
- 원래 테이블에서 시작하고 해당 시점 이전에 이루어진 커밋만 처리하여 언제든지 테이블 상태를 다시 만들 수 있다.

#### Data Lineage and Debugging
- 트랜잭션 로그는 유저에게 거버넌스, 어딧, 컴플라이언스 목적에 유용한 데이터 리니지를 제공한다.
- 또한 파이프라인의 변경 사항을 추적해 버그를 디버깅할 수도 있다.

### Refrence
https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html

## Schema Enforcement & Evolution
### Understanding Table Schemas
- 델타 레이크는 트랜잭션 로그 내에 json 포맷으로 테이블의 스키마를 저장한다.

### What Is Schema Enforcement?
- schema enforcement는 schema validation으로도 알려져있다.
- 테이블의 스키마와 매치되지 않는 쓰기를 거절해 데이터 퀄리티를 보장하는 것이다.

### How Does Schema Enforcement Work?
- 델타 레이크는 '쓰기'시점에 스키마 밸리데이션을 한다.
- 스키마가 호환 가능하지 않다면, 델타 레이크는 트랜잭션을 취소하고 에러를 레이즈한다.
- 테이블 쓰기가 호환 가능한지 결정하기 위해 다음 룰을 사용한다.
  - 타겟 테이블 스키마에 없는 컬럼을 포함하면 안 된다. 반대로, 타겟 테이블의 스키마에 없는 추가 컬럼은 괜찮다.
    - 단, merge를 all로 한다면 데이터 프레임과 타겟 테이블의 스키마가 일치해야한다.
  - 타겟 테이블의 컬럼 데이터 타입과 다른 컬럼 데이터 타입을 가지면 안 된다.
  - 영어 대소문자만 다른 컬럼을 사용하면 안 된다.

### How Is Schema Enforcement Useful?
- schema enforcement 덕분에 프로덕션 데이터를 깨끗하게 관리할 수 있다.
- 허들이 생기지 않기 위해, 브론즈-실버-골드의 레이어를 두는 `multi-hop` 아키텍처를 많이 이용한다.

### Preventing Data Dilution
- 컬럼을 테이블에 자유롭게 추가하지 못하는 게 불만족스러울 수 있다.
- 하지만 무작위로 컬럼이 추가돼 테이블이 의미를 잃는 것 보다 낫다.

### What Is Schema Evolution?
- 스키마 진화는 사용자가 시간이 지남에 따라 변경되는 데이터를 수용하기 위해 테이블의 현재 스키마를 쉽게 변경할 수 있는 기능이다.
- 흔하게 하나 이상의 새로운 컬럼을 포함하도록 스키마를 자동으로 조정하기 위해 append 또는 overwrite 작업을 수행할 때 사용된다.

### How Does Schema Evolution Work?
- 스키마 진화는 `.write`, `.writeStream` 스파크 커맨드에 `.option('mergeSchema', 'true')`을 추가해서 활성화된다.
- `mergeSchema` 옵션을 포함하면 DF에 있지만 타겟 테이블에 없는 어떤 컬럼이든 스키마의 끝에 자동으로 추가된다.
- nested field들도 추가될 수 있다.
- 다음 유형의 스키마 변경은 테이블 추가 또는 덮어쓰기 중에 스키마 진화에 적합하다.
  - 새로운 컬럼 추가.
  - 데이터 타입을 Null에서 다른 타입으로 변경 혹은 upcast.
- 스키마 진화에 적합하지 않은 다른 변경 사항은 `.option("overwriteSchema", "true")` 를 추가해 스키마와 데이터를 덮어써야함.

### Reference
- https://www.databricks.com/blog/2019/09/24/diving-into-delta-lake-schema-enforcement-evolution.html