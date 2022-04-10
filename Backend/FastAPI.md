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

- 물론 디폴트가 `None`이 아니고 값이 있는 경우도 있음.
