## 과정
- 1.table에서 전체 row 개수 혹은 split column이 있다면 이에 대한 min, max를 구한다.
- 2.1에서 구한 값으로 source를 몇 개의 파티션으로 나눌지 구한다. `max(1, 전체 row 개수 / 파티션당 레코드 개수)`
- 3-1.split column이 있다면 lower bound와 upper bound를 설정한다. 단 값에 `NULL`이 존재하면 min, max에 `NULL`이 될 수 있으므로 핸들링해야한다. lower bound는 적당한 최솟값으로, upper bound는 now로 설정한다. 보통 auto increment PK가 좋은 값이다.
- 3-2.split string column이 있다면 컬럼들을 concat하고 string을 number로 바꿀 수 있는 함수를 적용한다. (ex: CRC32) 그리고 해당 값에 mod 파티션 개수를 적용해 partition key로 지정한다. `FUNC(CONCAT(string columns)) % number_of_partitions AS partition_key`
- 4.지금까지 설정한 값들로 source에서 데이터를 읽어 DF로 만든다. 이때, partition key로 사용한 컬럼은 drop 한다. 필요에 따라 `repartition`을 이용해 파티션 개수를 줄인다.
- 5.string으로 바꿀 컬럼이 있다면 cast한다.
- 6.partition column이 있다면 `lit(partition column value)`를 이용해 partition column을 새로 만든다. 파티션 컬럼은 insert시에 마지막에 있어야하기 때문이다.
- 7-1.partition column이 있고 테이블이 존재하면 `insertInto`를 사용해 insert한다.
- 7-2.partition column이 있고 테이블이 존재하지 않으면 `partitionBy`와 `saveAsTable`을 이용해 테이블을 저장한다.
- 7-3.partition column이 없다면 `saveAsTable`로 테이블을 저장한다.

## Argument로 받으면 좋은 값들
- DB 종류
  - ex: mysql, postgresql, ...
- DB host
- DB user
- DB password
- DB database
- DB table
- DB where clause
  - 기본값을 `TRUE`로 하면 조건이 없을 때 모든 로우를 다 가져올 수 있음.
- DB database alias
  - 테스트, 용도의 분리 등 destination에 source와는 다르게 저장하고 싶을 수 있으므로
- Source split column
  - number or date type
  - source DB table이 너무 커서 executor 하나로 dump를 할 수 없을 때 필요함.
- Source split string column
  - ?
- String으로 변환하고 싶은 컬럼들
- partition column name
- partition column value
- jdbc properties

## 설정해놓으면 좋은 jdbc properties
- `zeroDateTimeBehavior=convertToNull`
  - MySQL의 datetime, timestamp의 값이 `0000-00-00 00:00:00`일 때, jdbc에서 에러를 레이즈하지 않고 null로 변환해주는 옵션

## 기타
- jdbc properties는 url에 쿼리 파라미터로 넘겨줌.
