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

## Path Parameter
- 패스 파라미터는 패스의 일부분이어야하기 때문에 항상 필요하다.
- 그래서 `...`으로 선언해야한다.
- 그럼에도 `None`으로 선언하거나 기본 값을 설정할 수 있지만 아무런 영향이 없다. 여전히 required 값이다.
```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
```

## Body
- body를 하나만 받을 때, json에 key도 포함되게 하고 싶다면 `embed=True`로 설정해주면 된다.
  ```python
  async def update_item(item_id: int, item: Item = Body(..., embed=True)):

  '''
  [embed=True]

  {
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
  }

  [embed=False]

  {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
  }
  '''
  ```
- Model 내에 다른 Model을 nested 시킬 수 있다. 입력시 모델을 json 형태로 입력하면 된다.
  ```json
  {
    "name": "string",
    "image": {
      "url": "string",
      "name": "string"
    }
  }
  ```
- 미리 알지 못하는 키를 받는 자료형을 선언하고 싶을 때, `dict`를 이용하면 유용하다.
  ```python
  @app.post("/index-weights/")
  async def create_index_weights(weights: Dict[int, float]):
  ```
- json은 키로 str만 지원한다. 하지만 `Pydantic`은 자동적인 데이터 변환을 한다. 즉, API 클라이언트는 스트링으로만 키를 사용할 수 있지만, 스트링이 순수한 인티저라면 Pydantic은 그것들을 변환하고 검증한다.
- Pydantic의 `.dict()`에서 `exclude_unset`을 `True`로 지정하면, 모델을 생성할 때 지정하지 않은 값들은 `dict` 결과에 나오지 않는다.
  ```python
  class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []
  
  # patch body: {"name": "test"}
  
  @app.patch("/items/{item_id}", response_model=Item)
  async def update_item(item_id: str, item: Item):
      item.dict(exclude_unset=True) # {'name': 'test'}
      item.dict() # {'name': 'test', 'description': None, 'price': None, 'tax': 10.5, 'tags': []}
  ```

## Response
- `response_model`의 중요한 점은 아웃풋 데이터를 모델로 제한한다.
- `response_model_exclude_unset`은 모델에 디폴트 값이 설정돼있어도 인풋으로 들어오지 않았다면 아웃풋으로 나가지 않게 한다. 하지만, OpenAPI에는 표시되니 여러 클래스들을 이용하는 걸 권장한다.
  ```python
  class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []
  
  
  # {"name": "Foo", "price": 50.2} -> {"name": "Foo", "price": 50.2}
  ```

## Handling Errors
- `HTTPException`은 일반적인 파이썬 예외이다. 그래서 `return`하면 안되고 `raise`를 해야한다.
- 레이즈되면 바로 리퀘스트를 멈추고 HTTP 에러를 클라이언트에게 보낸다.
- 커스텀 예외를 클래스로 만들고 `exeception_handler` 데코레이터를 이용하면 전역적으로 해당 에러를 처리할 수 있다.
  ```python
  class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
  
  @app.exception_handler(UnicornException)
  async def unicorn_exception_handler(request: Request, exc: UnicornException):
      return JSONResponse(
          status_code=418,
          content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
      )

  @app.get("/unicorns/{name}")
  async def read_unicorn(name: str):
      if name == "yolo":
          raise UnicornException(name=name)
  ```
- FastAPI의 `HTTPException`은 Starlette의 `HTTPException`을 상속했다. 유일한 차이점은 FastAPI의 예외가 헤더 추가를 허용한다는 것이다.
- 하지만 예외 핸들러를 등록할 때는 Starlette의 `HTTPException`을 등록해야한다. 이렇게 해야 내부 코드에서 Starlette의 `HTTPException`을 발생시켰을 때 잡을 수 있다.
  ```python
  from starlette.exceptions import HTTPException as StarletteHTTPException

  app = FastAPI()


  @app.exception_handler(StarletteHTTPException)
  async def http_exception_handler(request, exc):
      return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
  ```
