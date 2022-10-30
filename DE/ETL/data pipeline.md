## What is Data Extraction? Everything You Need to Know
### What is Data Extraction Types
- **Full Extraction**
  - 소스 시스템으로부터 어떤 로직이나 조건없이 추출된다.
  - full extraction의 예시는 테이블을 덤프하는 것이다.
  - full extraction은 복잡한 로직을 필요로 하지 않는다.
  - 하지만 데이터가 클수록 시스템에 대한 로드가 높다.
  - 지난 추출 이후 변화를 추적하기 싫을 때 해야한다.
- **Incremental Extraction**
  - 데이터에 대한 변경이 추적된다.
  - 마지막 추출로부터 변경된 데이터만 추출되고 로드된다.
  - 로직이 복잡해진다.
  - 하지만 소스 시스템에 대한 로드가 감소한다.
  - 감소된 로드는 더 효율적인 프로세스를 이끌 수 있다.
  - incremental extraction의 몇몇 구현은 CDC를 쓰거나 데이터의 이전 버전을 비교하는 방법을 쓴다.

### reference
- https://hevodata.com/learn/what-is-data-extraction/
