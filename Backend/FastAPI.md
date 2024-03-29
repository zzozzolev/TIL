## Features
- automatic documentation
  - swagger
  - redoc
- standard python3
- security and authentication
- dependency injection
- testing - 100% coverage

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

## Dependencies
- `Depends`는 `Body`, `Query`와 비슷하게 사용되지만 약간 다르게 동작한다.
- 새로운 리퀘스트가 도착할 때마다, FastAPI는 다음과 같이 처리한다.
  - 올바른 파라미터들과 함께 dependency 함수를 호출한다.
  - 함수로부터 결과를 얻는다.
  - 해당 결과를 path operation 함수의 파라미터에 할당한다.
- 이렇게 하면 여러 함수들이 하나의 코드를 공유할 수 있다.
- OpenAPI에는 파라미터가 제대로 표시된다.
- FastAPI의 dependency는 callable이면 되기 때문에, 클래스도 넘겨줄 수 있다.

### Depends
- FastAPI는 type annotation이 아니라 `Depends`를 통해 디펜던시를 알 수 있다.
- 코드가 반복될 수 있는데 `Depends`에 파라미터를 넘겨주지 않아도 FastAPI가 처리할 수 있다.
  ```python
  commons: CommonQueryParams = Depends()
  ```
- `Depends`에 또 다른 `Depends`가 있을 수 있다.
  ```python
  def query_extractor(q: Optional[str] = None):
    return q


  def query_or_cookie_extractor(
      q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
  ):

  @app.get("/items/")
  async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
  ```
- 같은 path operation에 대해 같은 디펜던시를 여러번 사용한다면, FastAPI는 캐쉬를 사용해 리퀘스트당 한 번 만 호출되도록 한다.
- 만약 캐쉬된 결과를 사용하는 게 싫다면, `Depends`에 `use_cache=False`를 넘겨주면 된다.

### decorator
- 몇몇 케이스에서는 리턴된 값이 필요 없고 단지 실행만 필요할 수도 있다. 이때 데코레이터에 `dependencies`를 지정해주면 된다.
  ```python
  @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
  async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
  ```
- 애플리케이션 전체에 디펜던시를 추가하고 싶다면 `FastAPI` 인스턴스를 만들 때 `dependencies`를 넘겨주면 된다.
  ```python
  app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
  ```

### yield
- 응답을 전달한 후에 특정한 스텝들을 취하기 위해 `yield`를 이용할 수 있다. 대신, 한 번만 사용해야한다.
- 어떤 예외가 발생할 지 모르겠다면, `finally`로 exit 스텝을 정의할 수도 있다.
- `yield` 이후의 코드들은 응답이 전달된 뒤에 실행되는 것이다.
- 따라서, `yield` 이후에 `HTTPException`을 발생시켜도 소용이 없다.
- 대신, DB 롤백이라든지 응답과 상관없는 작업은 수행할 수 있다.

## Middleware
- FastAPI에 미들웨어를 추가할 수 있다.
- 미들웨어는 특정에 패스 operation에 의해 처리되기 전에 모든 리퀘스트마다 동작하는 함수이다. 리스폰스가 나가기 전에도 마찬가지이다.
- 단, 디펜던시에 `yield`를 썼다면, exit 코드는 미들웨어 이후에 수행될 것이다.
- `CORS` 미들웨어를 추가할 수도 있다.
  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app = FastAPI()

  origins = [
      "http://localhost.tiangolo.com",
      "https://localhost.tiangolo.com",
      "http://localhost",
      "http://localhost:8080",
  ]

  app.add_middleware(
      CORSMiddleware,
      allow_origins=origins,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

  ## Router
  - 공통의 `prefix`를 설정할 수 있다. 대신, `prefix`는 마지막에 `/`을 포함할 수 없다.
  - 해당 path operation 들에 공통적으로 적용되는 dependency를 선언할 수 있다.
  - 라우터 -> 데코레이터 -> 파라미터 순으로 디펜던시가 수행된다.

  ## Background Tasks
  - 리퀘스트 처리 이후에 수행돼야하지만 클라이언트가 기다릴 필요가 없는 작업에 적절하다.
  - 예를 들면 이메일 보내기, 데이터 처리 등등.
  - `BackgroundTasks` 인스턴스에 함수와 인자를 넘기면 된다.
  - `BackgroundTasks`를 함수 파라미터에 선언하면 FastAPI가 알아서 처리한다.
  - 만약, starlette의 `BackgroundTask`를 사용한다면 별도로 객체를 만들어서 처리해야한다.
  - 시간이 오래 걸리지 않는 간단한 작업이나 FastAPI와 컨텍스트를 공유해야한다면 `BackgroundTasks`를 사용하는게 좋고, 그렇지 않다면 Celery를 사용하는 게 좋다.
  
  ## FastAPI에서 SQLAlchemy 사용하기
- SQLAlchemy에서는 쓰레드당 세션을 보장하기 위해 `scoped_session`을 쓸 것을 권장한다.
- 하지만, FastAPI는 코루틴 기반으로 async 하게 동작하기 때문에 하나의 쓰레드가 하나 이상의 리퀘스트를 핸들링할 수 있다.
- 아래는 해당 문제에 대한 FastAPI 저자의 직접적인 코멘트이다.

> SQLAlchemy scoped_session is based on thread locals. As XXX points out, those are not mapped 1:1 to requests when using async stuff. In summary, **a single thread can handle more than one request, and at the same time, a single request could be handled by more than one thread** (so it's actually not 1:1 but many:many). The alternative would be ContextVars, those are made to solve these use cases. But they don't behave exactly the same as thread locals and there are some caveats.

- 실제로 어떤 사람은 파이썬의 코루틴이 쓰레드와 1:1 매핑이 안 되기 때문에, 동작하지 않는 걸 봤다고 한다. 여러 코루틴들이 같은 쓰레드 로컬 세션에 트랜잭션을 시작했다고 한다. 그래서 `scoped_session` 쓰는 걸 멈췄다고...
- `SQLAlchemy`에서 [asyncio scoped session](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-asyncio-scoped-session)을 지원해주기는 한다.
- [패스트 API 튜토리얼](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/)에서는 `Peewee`라는 쓰레드 로컬을 사용하는 라이브러리를 `contextvars`를 사용하도록 변경한다.
- 해당 [포스트](https://www.hides.kr/1103?category=666044)에서 `ContextVar`와 미들웨어를 다뤄서 처리한 방법을 공유한다. `AsyncSession`을 이용한 건 이 [포스트](https://www.hides.kr/1101)에 있다.