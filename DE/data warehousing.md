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

## Clarifying Data Warehouse Design with Historical Dimensions
### Introduction
- SCD Type 1은 간단한 오버라이트이고 SCD Type 3(컬럼에 오래된 값 기록)는 다소 특별한 목적을 가지고 제한돼있다.
- 따라서 디멘전 히스토리의 핵심은 SCD Type 2이다.
- 보통 Type 2 히스토리를 포함하는 디멘전들은 effective date와 expiration date가 있다. 그리고 current indicator가 있다. 그리고 이것들은 Type 2 SCD 로우들이 삽입될 때 관리돼야한다.

### Limitations of Type 2 SCD
- SCD Type 1에서 SCD Type 2로 가는 게 겉보기에는 변화가 크게 없는 것 같지만 그렇지 않다.
- 근본적으로 해당 디멘전이 무엇을 담고 있는지를 변화시키는 것이다.
- **팩트 테이블의 로우와 마찬가지로 디멘전 테이블의 로우도 비지니스 관점에서 무엇을 나타내는지 정확하게 알아야한다.**
- 예를 들어 고객 정보를 나타내는 디멘전 테이블이 있다고 해보자.
  - SCD Type 1에서는 각 로우가 고객의 최신 정보를 나타낸다. SCD Type 2는 특정 시점의 고객 정보를 나타낸다.
  - 그래서 비지니스 유저는 디멘전을 이해하기 전에 히스토리 테크닉을 완전히 이해해야만한다.
  - 얼마나 많은 고유한 유저수가 있는지 알기 위해 SCD Type 1은 단순한 `COUNT(*)`로 충분하지만, SCD Type2는 `DISTINCT` 또는 `WHERE current_indicator`를 사용해야한다.
- SCD Type 2는 동시에 현재 뷰와 히스토리컬 뷰를 나타내려고 하기 때문에 복잡성을 도입한다.
- **과거의 팩트와 현재의 디멘전을 이용하려고 할 때도 어려운 점이 있다. 과거의 팩트는 과거의 디멘전을 가리킬 수 있다.**
  - 예를 들어, 지난 쿼터에 특정 상품들을 구입한 모든 고객들에게 이메일을 보내려고 할 때
- 또 다른 문제는 스냅샷 팩트 테이블이 누적되면서 발생한다. 이런 종류의 팩트 테이블은 시간이 지남에 따라 달라지는 디멘전 엔티티의 통계를 추적한다.
- **SCD Type2를 사용하면 몇몇 디멘전 키가 같은 디멘전 엔티티를 가리켜 최신 디멘전 키만 가리키게 보장해야한다.**

### Historical Dimensions Add Clarity
- 간단하게 히스토리로부터 분리된 current 밸류의 카피를 유지하면 된다.
- 다음과 같이 정의를 따르면 된다.

| Table Type | Content | Table Prefix | Surrogate Key Suffix | History Type | SCD Type | Column Prefix |
| ---------- | ------- | ------------ | -------------------- | ------------ | -------- | ------------- |
| Dimension  | Current | Dim          | Key                  | Overwrite    | 1        |               |
| Historical Dimension | Past + Current | HDim | HKey | Insert | 2 | Hist_ |

- 히스토리컬 디멘전은 디멘전 테이블에 있는 모든 컬럼을 포함한다. 여기에 자신의 surrogate pk, effective date, expiration date, current indicator륻 더하면 된다.
- 테이블을 분리하면 동일한 테이블에서 현재와 히스토리 값을 가져와 디멘전에 대한 비지니스 유저의 이해를 흐리는 것을 방지할 수 있다.

### Historical Dimensions Add Flexibility
- 팩트 테이블들은 관련된 디멘전들의 Key와 HKey를 모두 포함할 수 있다.
- 유저가 'as was then' 값을 보고 싶다면 HDim과 조인하면 되고, 'as is now' 값을 보고 싶다면 Dim과 조인하면 된다.

### Historical Dimensions Ease the ETL Burden
- current dimension과 historical dimension을 분리하는 건 ETL 과정을 간단하게 만든다.
- 먼저 디멘전 로드 과정에의해 변경된 모든 로우들을 식별할 방법이 있어야한다.
- Kimball은 Audit Key를 권장한다. 만약 적절한 키가 없다면 날짜 변경 타임스탬프를 사용할 수 있다.
- 두번째는 각각의 디멘전 컬럼에 대해서 어떤 종류의 업데이트가 돼야하는지 메타데이터를 정의해라.

### Add Historical Dimensions at Your Own Pace
- 이미 존재하는 디멘전에 Type 2 히스토리를 더하는 건 브레이킹 체인지이다.
- 하지만, 히스토리컬 디멘전을 더하는 건 그렇지 않다. 기존 쿼리를 수정하지 않아도 된다.

### Historical Dimensions Compared to Kimball SCD 7 and Wikipedia SCD 4
- Kimball SCD 7에서 Type 1과 Type 2 디멘전을 섞으라고 했다.
- 하지만 두 디멘전을 분리하지 않은 결정적 결함을 가지고 있다.
- 일반적으로 중복되는 current 디멘전을 피하기 위해 뷰를 사용하는 건 권장하지 않는다.
- 자동화된 히스토리컬 디멘전 로딩이 있어서 더 이상 중복에 대해 고려하지 않아도 된다.
- 위키피디아에서는 히스토리 테이블을 SCD Type 4라고 했다. 하지만 구현상 부족한 부분이 있다.
- 주어진 예시에서 히스토리 테이블에 새로 추가된 로우의 surrogate 키는 current 디멘전의 키를 업데이트하는데 사용된다.
- 이건 current 디멘전에서 안정적인 키를 사용하지 못하도록 한다.
- current과 history 사이의 명백한 분리를 잃게한다.

### Put Historical Dimensions to Work
- star 스키마 디자인이 효과적이다. 명백하고 쿼리하기가 쉽기 때문이다.

### reference
- https://www.red-gate.com/simple-talk/databases/sql-server/bi-sql-server/clarifying-data-warehouse-design-with-historical-dimensions/

