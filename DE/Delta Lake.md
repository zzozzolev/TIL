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

### The Delta Lake Transaction Log at the File Level
- 유저가 델타 레이크 테이블을 생성할 때, 해당 테이블의 트랜잭션 로그는 자동으로 `_delta_log` 서브 디렉토리에 생성된다.
- 유저가 테이블에 변경을 만들면 해당 변경 사항이 트랜잭션 로그에 정렬된 원자성 커밋으로 기록된다.
- 각각의 커밋은 json 파일로 써진다.
- 커밋마다 번호가 1씩 증가한다.
- 델타 레이크는 이미 지워진 데이터일지라도 원자적 커밋을 유지한다. 테이블에 대한 감사나 time travel을 하기 위함이다.
- 또한 스파크는 디스크에서 파일들을 바로 지우지 않는다.

### Refrence
https://www.databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html
