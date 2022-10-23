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

### Type 4: Add Mini-Dimension.
```
위키피디아에는 history table이라고 나오지만 kimball group 글을 보면 아님.
```
- 자주 변화하는 컬럼들만 별도의 디멘전 테이블로 분리해서 관리함. (mini-dimension)
- 하나의 테이블은 최신 데이터를 유지하고 추가적인 테이블은 레코드의 변경을 유지함.

### Type 5: Add Mini-Dimension and Type 1 Outrigger
- currnet mini-dimension을 base dimension 테이블에서 레퍼런스함.
- view로 base dimension과 current mini-dimension을 합쳐서 보여줌.
- ETL 팀은 current mini-dimension이 바뀔 때마다 업데이트/오버라이트 해줘야됨.

### Type 6: Combined approach
- type (1 + 2 + 3)을 섞은 방법.
- 특정 컬럼은 최신을 유지하기 위해 overwrite함. (type 1)
- 업데이트가 될 때 새로운 레코드를 추가함. (type 2)
- 특정 컬럼에 이전 컬럼 값을 저장함. (type 3)

### Type 7: Hybrid
- 이전의 방법들은 surrogate key만 팩트 테이블에 넣었음.
- 하지만 Type 7은 surrogate key와 natural key 모두를 팩트 테이블에 넣는 방법임.

### reference
- https://en.wikipedia.org/wiki/Slowly_changing_dimension
- https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/

## Fact vs Dimension Tables
### Star schema
- 하나의 팩트 테이블과 여러 개의 디멘전 테이블들로 구성됨.
- 팩트 테이블이 모델 다이어그램의 중앙에 있고 디멘전 테이블이 둘러싸고 있어 star schema라고 이름 붙여짐.

### Fact and Dimension Tables
- Fact Table
  - 레퍼런스되는 디멘전 테이블들의 pk들을 갖고 있음.
  - 정량적 매트릭스를 가지고 있음.
  - 흔한 예시가 주문, 로그 이런 종류의 데이터임.
- Dimension Table
  - 팩트 테이블의 레코드들에 포함되는 모든 관련 필드들에 대한 설명 정보를 담고 있음.
  - 흔한 예시가 고객정보, 상품 정보임.
- 디멘전 테이블에서 팩트를 구분하는 방법은 명사로 표현되는지 동사로 표현되는지 생각해보는 것임. 즉, 이벤트이냐 이벤트가 아니냐임.
- 명사로 표현되는 것은 이벤트 없이도 존재할 수 있음. 예를 들면 고객, 상품은 특정 이벤트 없이도 존재할 수 있음.
- 동사로 표현되는, 즉 이벤트는 이벤트가 있어야만 존재할 수 있음. 예를 들면, 주문은 주문이 일어나야지만 존재할 수 있음.

### Benefits of Star Schema
- 모델의 비정규화적인 특성 때문에 start schema는 퍼포먼스 측면에서 더 빠름.
- 팩트 테이블은 하나의 레벨의 디멘전 테이블과 조인되기 때문임.

### When (not) to use Star Schema
- 비정규화때문에 테이블에서 값이 반복됨.
- 그래서 저장 비용이 더 많이 듦.
- 또한 데이터 중복 때문에 data integrity가 더 위험함.
- 데이터가 변경될 때마다 integrity에 영향을 줌.

### refrence
- https://towardsdatascience.com/star-schema-924b995a9bdf