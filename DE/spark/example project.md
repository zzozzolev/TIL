## Repo
- https://github.com/AlexIoannides/pyspark-example-project
- 'best practices' approach to writing ETL jobs using Apache Spark and its Python ('PySpark') APIs.

## Structure of an ETL Job
- 쉬운 디버깅 및 테스트를 용이하게 하기 위해 'Transformation' 단계를 'Extract' 및 'Load' 단계에서 자체 기능으로 분리하는 것이 좋다. 즉, `main()`에 모든 작업을 때려넣지 않는다.
- DataFrames 형식의 입력 데이터 인수를 취하고 변환된 데이터를 단일 DataFrame 반환한다.
- Transformation은 idempotent 하게 설계해야한다.

## Passing Configuration Parameters to the ETL Job
- Arg parser를 쓸 수 있지만 금방 복잡해진다.
- 이럴 때 별도의 파일을 만들어 `spark-submit`시에 `--files`로 파일을 지정해주는 게 좋다.

## Packaging ETL Job Dependencies
- 여러 ETL jobs에서 쓰일 수 있는 모듈을 `dependencies`라고 부른다.
  - 예를 들면, spark 사용에 필요한 정보를 주는 `start_spark` 
- 필요한 디펜던시(패키지)를 zip 파일로 만들어 `spark-submit`시에 `--py-files`로 제출할 수 있다.

## Managing Project Dependencies using Pipenv
- pipenv로 dependencies를 관리한다.
