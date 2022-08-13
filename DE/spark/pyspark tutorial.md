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
