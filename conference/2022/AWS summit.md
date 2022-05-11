## 일체형 데이터베이스, 목적에 맞게 MSA 구조로 전환하기
### 모던 애플리케이션과 마이크로 서비스 아키텍처
- 모던 애플리케이션
  - 여러 지역의 유저가 사용해 요청량이 많지만 밀리초 내에 빠르게 서빙될 수 있어야한다.
  - 정합성이 있으면서 빠른 개발과 배포를 요구한다.
- 마이크로 서비스 아키텍처
  - 모놀리틱 시스템을 서비스 단위로 분리
  - 더 빠르게 개발 및 배포하면서도 서비스 간 영향을 줄인다.
- 마이크로 서비스의 시작은 적절한 DB를 선택하는 것부터 시작된다.  
- 모놀리틱 RDB 한계
  - 성능 이슈
  - 확장성 한계
  - 개발자들의 유연성 저해
  - 통합할 수 없는 데이터 타입
- 각각의 DB 별로 효과적으로 처리할 수 있는 데이터가 있고 그렇지 않은 데이터가 있다.

### 목적별 데이터 베이스
- relational -> Aurora, RDS
  - 트랜잭션
  - Lift-and-shift(그대로 옮기기), ERP(Enterprise Resource Planning), CRM(Customer Relationship Management), finance
- key-value: DynamoDB
  - NoSQL이지만 보조 인덱스 및 ACID 트랜잭션 제공
  - 실시간 입찰/거래, 장바구니, SNS, 상품 카탈로그, 고객 선호도
- Document: DocumentDB
  - 스키마리스 DB
  - 초당 수백만 요청량 처리 가능
  - 밀리 세컨드 수준의 응답 시간 보장
  - 컨텐츠 관리, 개인화, 모바일
- In-Memory: Elastic Cache
  - 마이크로 세건드 수준의 응답 시간 보장
  - 리더보드(레디스 sorted set), 실시간 분석, 캐싱
- Graph: Neptune
  - 사기탐지, 소셜 네트워킹, 추천 엔진
- Time-series: TimeStream
  - IoT 응용프로그램, 이벤트 추적
- Ledger: QLDB
  - 변조 방지
  - 모든 변경 이력을 체이닝 방식으로 관리
  - 원장(거래 기록 장부) 기록, 공급망, 헬스 케어, 금융
- Wide Column: Keyspaces
  - 낮은 응답 시간 응용 프로그램, 클라우드에서 카산드라 사용

