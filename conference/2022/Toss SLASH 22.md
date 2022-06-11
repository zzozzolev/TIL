## 지속 성장 가능한 코드를 만들어가는 방법
- https://toss.im/slash-22/sessions/1-6
- https://www.youtube.com/watch?v=RVO02Z1dLF8

### 생성자
- 의존하는 클래스를 확인할 수 있다.
- 해당 클래스가 무슨 일을 하는지 힌트를 줄 수 있다.

### 패키지 구성
- 역할보다는 개념으로 응집시켜야 불필요한 import를 줄일 수 있음.

### 레이어
- 토스 페이먼츠 표준 레이어
  - Presentation Layer
  - Business Layer
  - Implement Layer
  - Data Access Layer
- 레이어는 위에서 아래로 순방향으로만 참조돼야한다.
- 레이어의 참조 방향이 역류되지 않아야한다.
- 레이어를 건너뛰지 않는다. ex) Buisiness Layer -> Data Access Layer

### 모듈의 분리
- 라이브러리에 대한 부분을 격리해 사용한다면, 비즈니스 로직에서 특정 라이브러리에 대한 import를 할 수 없다.
- 비즈니스 로직이 더 뚜렷해진다.
- 라이브러리 교체시 비즈니스 로직에 영향이 없다.

## 토스에서는 테이블 정보를 어떻게 관리하나요?
- https://toss.im/slash-22/sessions/3-3
- https://www.youtube.com/watch?v=KUskYwqtPZM
- 토스 커뮤니티 고민
  1. 효율적인 검색
  2. 테이블 사용 방법
  3. 품질 관리
- 자체 서비스인 "테이블 센터"라는 것을 이용.

### 테이블 센터의 검색 기능
- 다양한 검색
  - 키워드 검색: 키워드 입력을 통해 원하는 테이블을 검색할 수 있는 검색
  - 드릴다운 검색: DB 타입 -> 서버 호스트 -> 테이블 스키마 -> 테이블 순으로 점진적으로 검색할 수 있는 검색
  - 태그 검색: SNS의 해시 태그와 같이 태그가 붙은 복수의 테이블을 볼 수 있는 태그 검색
- 테이블 정보 수집 아키텍처
  - LIVE 배치 수집: Live DB(서비스 DB) -> Batch Sync - Table Center Repo
  - DW 실시간 조회: Hadoop -> Hive Meta DB(MySql)
  - 두 정보 -> Table Center Backend Server
- LIVE 배치 수집
  - 라이브의 읽기 전용 슬레이브에서 네 시간마다 정보를 수집해 테이블 센터 리포에 저장
- DW 실시간 조회
  - 하이브 메타 스토어에 읽기 전용 슬레이브를 실시간 조회
  - 조회 시 성능에 문제가 되지 않을 수준의 단순한 쿼리로 조회

### 테이블 센터의 영향도 검색 기능
- 테이블이 어디에서 어떻게 만들어지고 사용되는지 정리
- 검색된 테이블이 어디에서 어떻게 쓰이고 있거나 만들어지고 있는지를 보여주는 기능
- 테이블이 사용되는 것에 대한 설명이나, 해당 링크로 이동할 수 있는 기능을 제공

### 영향도 검색 아키텍처
- 다양한 데이터 소스에서 테이블을 사용하고 있는 코드들을 수집하며 필요시 수동으로 수집.

### 테이블 센터의 Data Quality 관리 기능
- 테이터 품질 관리 구분
  - Completeness(완경성): NOT NULL or Check Constraint
  - Uniqueness(유일성): Unique Constraint
  - Validity(유효성): Check Constraint
  - Timeliness(시의적절성): 특정 시점의 데이터 유지
  - Accuracy(정확성): 현실 세계의 규칙을 정확히 반영
  - Consistency(일관성): 하나의 사실에 대해 같은 값을 유지
- 하둡 에코시스템에 데이터 웨어하우스를 구축하고 있는 특성상 RDB처럼 기본적으로 제공하고 있지 않음.
- 그래서 Data Quality 기능을 이용함.
  - 테이블 정보 페이지에서 DQ 등록 -> Spark를 이용해 정기적으로 DQ 실행 -> 이슈 발생 시 Slack 알림 발송 및 이슈 대응
