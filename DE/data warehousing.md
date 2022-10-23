## SCD
- slowly changing dimension (SCD)
- 예시는 위키 문서 참고.

### Type 0: retain original
- 절대 바뀌지 않음.

### Type 1: overwrite
- 오래된 데이터를 최신 데이터로 오버라이트함.
- 데이터의 히스토리가 남지 않음.
- 대신 관리하기가 편함.
- 만약 시간에 따라 값이 변화할 수 있는 컬럼에 대한 어그리게이션 테이블을 생성한다면 재계산이 필요함.
  - 예를 들어, 고객의 주소에 대한 집계 테이블을 만들었다면 새로운 주소에 대한 집계가 필요함.

### Type 2: Add new row
- 디멘전 테이블에서 특정 네추럴 키에 대한 여러 개의 레코드를 만들어서 히스토리컬 데이터를 트랙킹함.
- version, effective date, effective date & current flag를 이용할 수 있음.
  - version: 업데이트가 있을 때마다 버전을 하나씩 증가시킴.
  - effective date: 레코드가 유효한 시작 날짜와 끝 날짜를 기록.
  - effective date & current flag: 업데이트 날짜를 기록하고 최신 레코드인지 표시함.

### Type 3: Add new attribute
- 별도의 컬럼을 이용해 제한된 히스토리를 트랙킹함.
- 제한된 히스토리는 히스토리를 기록할 컬럼 개수만큼만 기록됨.

### Type 4: Add history table
- 보통 history table이라고 불림.
- 하나의 테이블은 최신 데이터를 유지하고 추가적인 테이블은 레코드의 변경을 유지함.

### Type 5: 4 + 1
- 잘 이해못함; 예시가 없음 ㅠㅠ

### Type 6: Combined approach
- type (1 + 2 + 3)을 섞은 방법.
- 특정 컬럼은 최신을 유지하기 위해 overwrite함. (type 1)
- 업데이트가 될 때 새로운 레코드를 추가함. (type 2)
- 특정 컬럼에 이전 컬럼 값을 저장함. (type 3)

### Type 7: Hybrid
- 이것도 잘 모르겠음;

### reference
- https://en.wikipedia.org/wiki/Slowly_changing_dimension