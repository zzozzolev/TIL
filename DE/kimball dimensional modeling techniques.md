## Dimensional Design Process
1. 비지니스 프로세스 선택하기.
2. grain 정의하기.
3. 디멘전들 식별하기.
4. 팩트들을 식별하기.

### reference
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/four-4-step-design-process/


## 비지니스 프로세스
- 조직에의해 수행되는 oprational activity.
- 예를 들면, 주문, 학생 등록 등등.
- 비지니스 프로세스는 이벤트들은 팩트 테이블로 바뀌는 퍼포먼스 메트릭스를 생성하거나 캡처한다.
- 각각의 비지니스 프로세스는 데이터 웨어하우스의 로우에 해당한다.

### reference
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/business-process/

## Grain
- grain은 하나의 팩트 테이블 로우가 무엇을 나타내는지를 확립한다.
- grain은 모든 후보 디멘전과 팩트가 grain과 일관성이 있어야하기 때문에 디멘전과 팩트를 고르기 전에 선언돼야한다.
- atomic grain은 비지니스 프로세스에의해 캡처되는 데이터의 가장 낮은 수준이다.
- 유저 쿼리가 어떻게 될지 모르기 때문에 atomic grain부터 시작하는 게 좋다.

### reference
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/grain/