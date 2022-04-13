## Data conversion
- 함수에 타입을 명시하면 해당 타입으로 파싱을 해준다.
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# /items/2
# {"item_id":2}
```
- 타입에 맞지 않으면 밸리데이션 에러가 난다.
```
/items/foo

{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

## Order matters
- path operations는 순서대로 처리된다.
- 그래서 더 먼저 처리되길 원하는 path를 상위에 써야한다.
- 예를 들어, 아래는 서로 다르게 처리해야하지만 패스가 겹치는 경우이다. `/users/me`가 별도로 처리되길 원한다면 더 상위에 정의한다.
```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

```

## Predefined values
- 미리 정의된 path 파라미터만 받고 싶은 경우 `Enum` class를 만든다.
  ```python
  from enum import Enum
  
  class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

  @app.get("/models/{model_name}")
  async def get_model(model_name: ModelName):
  ```

## Optional vs Required Parameters

|    | Optional | Required |
| --- | --- | --- |
| default | None | 없음 |
| 값이 없는 경우 | default 사용 | 오류 발생 |

- 물론 디폴트가 `None`이 아니고 값이 있는 경우도 있다.
- `Optional`은 에디터의 서포트를 받을 수 있지만 FastAPI에 해당 파라미터가 요구되지 않는다고 알려주는 건 아니다.

## Request body + path + query parameters
- 바디, 패스 파라미터, 쿼리 파라미터를 동시에 정의할 수 있다.
  ```python
  @app.put("/items/{item_id}")
  async def create_item(item_id: int, item: Item, q: Optional[str] = None):
  ```
- 함수 파라미터들을 다음과 같은 순서로 인식된다.
  - 만약 파라미터가 패스에 선언돼있다면 패스 파라미터로 쓰인다.
  - 만약 파라미터가 singular 타입이라면 (`int`, `float`, `str` 등등) 쿼리 파라미터로 해석된다.
  - 만약 파라미터가 Pydantic 모델로 정의됐다면, 리퀘스트 바디로 해석된다.

## Query Parameters and String Validations
- required 이므로 디폴트가 없지만 밸리데이션은 하고 싶다면 `...`인 `ellipsis`를 이용할 수 있다.
  ```python
  async def read_items(q: str = Query(..., min_length=3)):
  ```
- `Query`에 `title`, `description`을 선언해 OpenAPI에 포함되게 할 수 있다.
- `alias`를 이용하면 쿼리 파라미터와 파라미터 이름을 다르게 설정할 수 있다.
  ```python
  # ?item-query=foobaritems
  async def read_items(q: Optional[str] = Query(None, alias="item-query")):
  ```