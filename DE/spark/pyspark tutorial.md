## 참고
- https://sparkbyexamples.com/pyspark

## StructType & StructField
- https://sparkbyexamples.com/pyspark/pyspark-structtype-and-structfield/

### Using SQL ArrayType and MapType
- `ArrayType`과 `MapType` 타입도 있다.

### Creating StructType object struct from JSON file
- 데이터 프레임의 스키마를 json으로 만들 수 있다.
  ```python
  df2.schema.json()
  ```
- 이렇게 한 번 json으로 저장한 스키마를 필요할 때마다 로드해서 사용할 수 있다.
  ```python
  with open("schema.json") as f:
    json_schema = json.load(f)

  schema_from_json = StructType.fromJson(json_schema)
  ```
- inferred 스키마는 이름이 지정되지 않은 채 저장된다.
  ```json
  "fields": [
    {
        "metadata": {},
        "name": "name",
        "nullable": true
    }
  ]

  "fields": [
    {
        "metadata": {},
        "name": "_1",
        "nullable": true,
    }
  ]
  ```

### Creating StructType object struct from DDL String
- DDL문으로도 만들 수 있다.
  ```python
  ddlSchemaStr = "`fullName` STRUCT<`first`: STRING, `last`: STRING, `middle`: STRING>,`age` INT,`gender` STRING"
  ddlSchema = StructType.fromDDL(ddlSchemaStr)
  ddlSchema.printTreeString()
  ```

### Checking if a Column Exists in a DataFrame
- 컬럼이 있는지 컬럼이 특정 스키마로 존재하는지도 확인할 수 있다.
  ```python
  print(df.schema.fieldNames.contains("firstname"))
  print(df.schema.contains(StructField("firstname",StringType,true)))
  ```

## PySpark UDF (User Defined Function)
### Special Handling
#### Execution order
- spark에서는 subexpression의 평가 순서를 보장하지 않는다. 즉, 왼쪽에 적은게 먼저 실행된다고 보장하지 않는다.

#### Handling null check
- `None`일 수 있는 컬럼은 UDF에서 확실하게 `None` 처리를 해줘야한다.

#### Performance concern using UDF
- UDF는 spark에게 블랙 박스이다. 그래서 최적화를 할 수 없다.
- 가능하다면 spark sql 빌트인 함수를 써야한다.
