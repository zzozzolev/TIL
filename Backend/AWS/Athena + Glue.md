## Athena
- S3에 저장된 데이터를 분석하기 위한 Serverless 쿼리 서비스
- Presto를 기반으로한 파일에 쿼리를 하기위해 standard SQL 언어를 사용함.
- TB 데이터 스캔당 고정 금액 사용함.

## Athena Performance Improvement
- columnar data를 사용함.
  - Apache parquet이나 ORC 권장함.
- 데이터를 압축함.
- 파티셔닝함.
- 오버헤드를 최소화하기 위해 128MB보다 큰 파일을 사용함.

## Athena Federated Query
- 어떤 데이터 소스에 저장돼있든 SQL 쿼리를 수행할 수 있음.
- AWS Lambda 위에서 돌아가는 데이터 소스 커넥터를 사용하면 됨.
- 결과는 S3에 저장됨.

## AWS Glue
- Managed ETL 서비스.
- 분석을 위해 데이터를 준비하고 변환하는데 유용함.
- serverless 서비스.
- use case
  - RDS -> Glue -> Red Shift
  - S3(csv) -> Glue -> S3(parquet) -> Athena

## Glue Data Catalog: catalog of datasets
- 글루 데이터 크롤러가 DB를 크롤해서 글루 데이터 카탈로그에 테이블, 컬럼, 데이터 타입의 메타데이터를 씀.
- 모든 DB, 테이블, 메타데이터를 갖게 됨.
- 글루 잡에서 활용됨.
- 아테나, EMR에서 데이터 디스커버리와 스키마 디스커버리로 글루 데이터 카탈로그를 사용함.
