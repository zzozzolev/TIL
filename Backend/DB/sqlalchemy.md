## Object Relational Tutorial
- [공식 문서](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) 내용 기록

### Building a Relationship
- 예를 들어 아래와 같은 클래스가 있다고 해보자.
    ```python
    >>> class Address(Base):
    ...     __tablename__ = 'addresses'
    ...     id = Column(Integer, primary_key=True)
    ...     email_address = Column(String, nullable=False)
    ...     user_id = Column(Integer, ForeignKey('users.id'))
    ...
    ...     user = relationship("User", back_populates="addresses")
    ...
    ...     def __repr__(self):
    ...         return "<Address(email_address='%s')>" % self.email_address

    >>> User.addresses = relationship(
    ...     "Address", order_by=Address.id, back_populates="user")
    ```
- 자식 테이블에 `ForeignKey`로 부모 테이블 PK를 명시한다.
- `relationship()`은 `Address.user` 속성을 사용하여 `Address` 클래스 자체가 `User` 클래스에 연결되어야 함을 ORM에 알려준다.
- `relationship()`은 두 테이블 간의 외래 키 관계를 사용하여 이 연결의 특성을 결정하고 `Address.user`가 다대일임을 결정한다.
- 추가 `relationship()` 지시문은 `User.addresses` 속성 아래의 사용자 매핑 클래스에 배치된다.
- 두 `relationship()` 지시문에서 파라미터 `relationship.back_populates`는 보완적인 속성 이름을 참조하기 위해 할당된다.
- `relationship.back_populates` 파라미터는 `relationship.backref`라는 매우 일반적인 SQLAlchemy 기능의 최신 버전이다.
- 두 가지 보완(complementing) 관계인 `Address.user`와 `User.addresses`는 양방향 관계라고 하며 SQLAlchemy ORM의 핵심 기능이다.
- 대부분 RDB에서 FK 제약은 PK 혹은 UNIQUE 제약 조건을 가지는 컬럼에만 연결할 수 있다.

## Eager Loading

## Relationship Configuration
- [공식 문서](https://docs.sqlalchemy.org/en/14/orm/relationships.html) 내용 기록
### Linking Relationships with Backref
- 다음과 같이 `User`와 `Address`가 선언돼있다고 하자.
    ```python
    class User(Base):
        __tablename__ = "user"
        id = Column(Integer, primary_key=True)
        name = Column(String)

        addresses = relationship("Address", backref="user")


    class Address(Base):
        __tablename__ = "address"
        id = Column(Integer, primary_key=True)
        email = Column(String)
        user_id = Column(Integer, ForeignKey("user.id"))
    ```
- 위의 설정은 `User.addresses`라는 `User`에 대한 `Address` 오브젝트 컬렉션을 설정한다.
- 또한 부모 `User` 객체를 참조하는 `Address`에 대한 `.user` 속성을 설정한다.
- 사실, `relationship.backref` 키워드는 `Address` 매팡에 두 번째 `relationship()`을 배치하기 위한 흔한 쇼트컷이다.
- 양쪽에 `back_populates`를 설정하는 것과 똑같다.
- 두 관계 모두에서 `relationship.back_populates` 지시문은 서로 간에 "bidirectional" 동작을 설정해야 함을 나타내는 다른 관계에 대해 각 관계에 알려준다.
- 이 구성의 주요 효과는 relationship이 "여기에서 추가 또는 설정 이벤트가 발생하면, 이 특정 속성 이름을 사용하는 인커밍 속성에 설정"하는 동작을 갖는 두 속성에 이벤트 핸들러를 추가한다는 것이다.
- 위의 예시로 보면, `u1` 이라는 `User` 인스턴스의 `addresses`에 `Address` 인스턴스가 추가되면 `u1`에 추가됨은 물론, 해당 `Address` 인스턴스의 `user`에도 `u1`이 추가된다.
- `.addresses` 컬렉션과 `.user` 속성의 조작은 SQL 데이터베이스와의 상호 작용 없이 전적으로 Python에서 발생한다.
- `relationship.backref/relationship.back_populates` 동작은 일반적인 bidirectional 연산이 데이터베이스 왕복 없이 올바른 상태를 반영할 수 있다는 이점이 있다.

## Relationship Loading Techniques
- relationship의 로딩은 세 가지 카테고리로 나뉜다.
    1. lazy loading
    2. eager loading
    3. no loading
- lazy loading은 관련 객체가 처음에 로드되지 않고 쿼리에서 객체가 반환됨을 나타낸다.
- 특정 객체에서 지정된 컬렉션 또는 참조에 처음 액세스하면 요청된 컬렉션이 로드되도록 추가 SELECT 문이 내보내진다.
- eager loading은 이미 로드된 관련 컬렉션 또는 스칼라 참조가 있는 쿼리에서 반환된 객체를 나타낸다.
- `Query`는 일반적으로 관련된 행에 동시에 로드하기 위해 JOIN과 함께 내보내는 SELECT 문을 확장하거나, 컬렉션 또는 스칼라 참조를 한 번에 로드하기 위해 기본 SELECT 문 다음에 추가 SELECT 문을 내보냄으로써 이를 달성한다.
- "No" loading은 원하지 않는 lazy load를 방지하기 위해 속성이 비어 있고 로드되지 않거나 액세스할 때 오류가 발생하는 주어진 관계에서 로드를 비활성화하는 것을 나타낸다.
- lazy loading
  - `lazy='select'` or `lazyload()`
  - 한 번에 단일 개체에 대한 관련 참조를 느리게 로드하기 위해 어트리뷰트 액세스 시간에 SELECT 문을 내보내는 로드 형식
  - 기본 설정.
- joined loading
  - `lazy='joined'` or `joinedload()`
  - 이 형식의 로드는 관련 행이 동일한 결과 집합에 로드되도록 지정된 SELECT 문에 JOIN을 적용한다.
- subquery loading
  - `lazy='subquery'` or `subqueryload()`
  - 이 형식의 로드는 서브 쿼리 내부에 포함된 원래 쿼리를 다시 설명하는 두 번째 SELECT 문을 내보낸다.
  - 그런 다음 관련 컬렉션/스칼라 참조의 모든 멤버를 한 번에 로드하기 위해 로드할 관련 테이블에 대한 하위 쿼리를 JOIN한다.
- select IN loading
  - `lazy='selectin'` or `selectinload()`
  - 이 형식의 로드는 부모 객체의 PK identifier를 IN 절로 조합하는 두 번째(또는 그 이상) SELECT 문을 내보낸다.
  - 관련 컬렉션/스칼라 참조의 모든 멤버가 PK로 한 번에 로드되도록 한다.
- raise loading
  - `lazy='raise'` or `lazy='raise_on_sql` or `raiseload()`
  - 이러한 형태의 로딩은 일반적으로 lazy load가 발생하는 동시에 트리거된다.
  - 애플리케이션이 원치 않는 lazy load를 만드는 것을 방지하기 위해 ORM 예외를 발생시키는 것을 제외한다.
- no loading
  - `lazy='noload'` or `noload()`
  - 이 로딩 스타일은 속성을 로드하지 않거나 로딩 효과가 없는 빈 속성(`None` 또는 `[]`)으로 바꾼다.
  - 거의 사용되지 않는 이 전략은 빈 속성이나 컬렉션이 배치된 상태에서 객체가 로드될 때 Eager Loader처럼 작동한다.
  - 그러나 만료된 객체의 경우 액세스 시 반환되는 속성의 기본값에 의존한다.
  - `noload`는 "write-only" 속성을 구현하는 데 유용할 수 있지만 이 사용법은 현재 테스트되거나 공식적으로 지원되지 않는다.

### Lazy Loading
- 기본적으로 모든 객체 간 관계는 지연 로드이다.
- `relationship()`과 관련된 스칼라 또는 컬렉션 속성에는 속성에 처음 액세스할 때 발생하는 트리거가 포함되어 있다.
- 이 트리거는 일반적으로 관련 객체를 로드하기 위해 액세스 지점에서 SQL 호출을 실행한다.
- SQL이 내보내지지 않는 한 가지 경우는 관련 객체가 기본 키로 식별될 수 있고 해당 객체가 이미 현재 세션에 있는 단순한 다대일 관계의 경우이다.
- 이러한 이유로 지연 로딩은 관련 컬렉션에 대해 비용이 많이 들 수 있지만, 상대적으로 작은 가능한 대상 객체 집합에 대해 간단한 다대일을 사용하여 많은 개체를 로드하는 경우,지연 로딩은 이러한 컬렉션을 참조할 수 있다. 상위 객체 수만큼 SELECT 문을 내보내지 않고 객체를 로컬로 가져온다.

#### Preventing unwanted lazy loads using raiseload
- `lazyload()` 전략은 ORM에서 언급되는 가장 일반적인 문제 중 하나인 효과를 생성한다.
- `N+1` 문제, 로드된 N 객체에 대해 지연 로드 속성에 액세스하면 N+1 SELECT 문이 방출됨을 의미한다.
- SQLAlchemy에서 N+1 문제에 대한 일반적인 완화는 매우 유능한 Eager 로드 시스템을 사용하는 것이다.
- 그러나 eager loading은 로드할 속성이 쿼리와 함께 미리 지정되어야 한다.
- lazy loading이 바람직하지 않은, 빠르게 로드되지 않은 다른 속성에 액세스할 수 있는 코드 문제는 `raiseload()` 전략을 사용하여 해결할 수 있다.
- 이 로더 전략은 lazy loading 동작을 레이즈되는 informative error로 대체한다.
- 아래 쿼리에서 로드된 `User` 객체에는 `.addresses` 컬렉션이 로드되지 않는다. 나중에 일부 코드가 이 속성에 액세스하려고 하면 ORM 예외가 발생한다.
  ```sql
  from sqlalchemy.orm import raiseload
  session.query(User).options(raiseload(User.addresses))
  ```
- 단, 1.4.0 부터는 UOW 플러시 과정내에서는 발생하지 않는다. 즉, UOW가 작업을 완료하기 위해 특정 속성을 로드해야 하는 경우 로드를 수행함을 의미한다.
- `lazy="raise"` 케이스는 애플리케이션 공간 내에서 명시적 속성 액세스를 위한 것이다.

### Joined Eager Loading
- ORM에서 가장 기본적인 Eager loading 스타입이다.
- JOIN(기본적으로 LEFT OUTER 조인)을 쿼리에서 내보낸 SELECT 문에 연결해 작동한다. 부모의 것과 동일한 결과 집합에서 대상 스칼라/컬렉션을 채운다.
- Joined Eager loading은 일반적으로 매핑의 기본 로딩 옵션이 아니라 쿼리에 대한 옵션으로 적용된다. 특히 many-to-one 참조가 아닌 컬렉션에 사용되는 경우에 적용된다.
- `joinedload()` 로더 옵션을 사용해서 달성된다.
- 기본적으로 내보낸 JOIN은 관련 행을 참조하지 않는 리드 객체를 허용하기 위해 LEFT OUTER JOIN이다.
- 참조하는 foreign key가 NULL이 아닌 관련 객체에 대한 many-to-one 참조와 같이 엘리먼트가 있다고 보장되는 속성의 경우, inner join을 사용해 쿼리를 보다 효율적으로 만들 수 있다.
- 매핑 레벨에서 아래와 같은 플래그로 가능하다.
    ```python
    class Address(Base):
      # ...

      user_id = Column(ForeignKey('users.id'), nullable=False)
      user = relationship(User, lazy="joined", innerjoin=True)
    ```

### Joined eager loading and result set batching
- 컬렉션에 적용할 때 결합된 즉시 로드의 중심 개념은 `Query` 객체가 쿼리되는 선행 엔터티에 대해 행 중복을 제거해야 한다는 것이다.
- 위와 같이 로드한 `User` 객체가 3개의 `Address` 객체를 참조한다면 SQL 문의 결과는 3개의 행을 가지게 된다. 하지만 `Query`는 하나의 `User` 객체만 반환한다.
- 이전 행에 방금 로드된 `User` 객체에 대한 추가 행이 수신되면, 새 `Address` 객체를 참조하는 추가 열이 해당 특정 객체의 `User.addresses` 컬렉션 내의 추가 결과로 전달된다.
- 이 프로세스는 매우 투명하지만 joined eager loading이 컬렉션 로드에 사용될 때, `Query.yield_per()` 메서드에서 제공하는 "일괄 처리된" 쿼리 결과와 호환되지 않음을 의미한다.
- 그러나 스칼라 참조에 사용되는 joined eager loading는 `Query.yield_per()`와 호환된다.
- `Query.yield_per()` 메서드는 컬렉션 기반 joined eager loader가 실행 중인 경우 예외가 발생한다.
- 컬렉션 기반 joined eager loading과의 ​​호환성을 유지하면서 임의의 큰 결과 데이터 세트로 쿼리를 "일괄 처리"하려면, 각각 `WHERE` 절을 사용하여 행의 하위 집합을 참조하는 여러 SELECT 문을 내보내라.
- 또는 `Query.yield_per()`와 잠재적으로 호환되는 "select IN" eager loading 사용을 고려해라.

### The Zen of Joined Eager Loading
- joined eager loading은 `Query.join()`의 사용과 많은 유사점을 가지고 있기 때문에, 언제, 어떻게 사용해야 하는지 혼동을 일으키는 경우가 많다.
- `Query.join()`은 쿼리 결과를 변경하는 데 사용되지만, `joinedload()`는 쿼리 결과를 변경하지 않고 대신 렌더링된 조인의 효과를 숨기기 위해 많은 시간을 거쳐야 한다는 차이점을 이해하는 것이 중요하다.
- 로더 전략의 기본 철학은 특정 쿼리에 모든 loading schemes를 적용할 수 있으며 결과는 변경되지 않는다는 것이다. 관련 객체와 컬렉션을 완전히 로드하는데 필요한 SQL 문의 수만 변경된다.
- 쿼리에 대한 다른 수정 없이 전략을 변경할 수 있으며 결과는 동일하게 유지되지만 더 적은 수의 SQL 문을 내보낸다.
- 특히 `joinedload()`가 어떤 식으로든 반환된 엔터티 행에 영향을 주지 않고 이러한 결과를 얻는 방법은 쿼리에 추가하는 조인의 익명 alias를 생성한다는 것이다.
- 그래서 `joinedload()`로 지정한 테이블은 다른 쿼리에서 접근할 수 없다.
- `Query.join()`을 사용하는 것은 뒤이은 쿼리 기준에 사용하려는 JOIN 절을 제공하는 것이지만, `joinedload()`는 컬렉션의 로드에만 관련이 있다.
- joined eager loading을 사용할 때, 쿼리에 DISTINCT, LIMIT, OFFSET 또는 이와 동등한 것을 사용할 때와 같이 조인에 대해 외부적으로 반환된 행에 영향을 주는 수정자가 포함되어 있으면 완료된 명령문이 먼저 서브 쿼리 내부에 래핑되고 조인이 특별히 사용된다. joined eager loading이 서브 쿼리에 적용된다.

## Session Basics
- [공식 문서](https://docs.sqlalchemy.org/en/14/orm/session_basics.html) 내용 기록

### 세션은 뭘 하는가?
- 세션은 ORM 매핑 객체를 반환하고 수정할 SELECT 및 기타 쿼리가 생성되는 인터페이스를 제공한다.
- ORM 오브젝트 자체는 `Session` 내에서 즉, `identity map`이라고 불리는 구조체 내에서 관리된다.
- `identity map`은 각각의 오브젝트의 "고유한" 복사본을 관리하는 자료 구조이다. 여기서 "고유한"은 "특정 PK를 가지는 단 하나의 객체"를 의미한다.
- 쿼리가 실행되거나 다른 객체들이 영속화되면 세션과 연결된 엔진에서 커넥션 자원을 요청한 다음 해당 커넥션에서 트랜잭션을 설정한다.
- 이 트랜잭션은 세션이 트랜잭션을 커밋하거나 롤백하도록 지시할 때까지 유효하다.
- 세션에의해 유지되는 ORM 객체들은 파이썬 프로그램에서 속성이나 컬렉션이 변경될때마다, 세션에 의해 기록되는 변경 이벤트가 생성되도록 인스트러멘티드된다.
*instrumented: 특정 클래스의 기능 및 속성 집합을 보강하는 프로세스 (뭔소리야 😢)
- 데이터베이스가 쿼리될 때마다 또는 트랜잭션이 커밋되려고 할 때마다 세션은 먼저 메모리에 저장된 모든 펜딩 중인 변경 사항을 데이터베이스로 플러시한다. 이것은 unit of work 패턴의 단위로 알려져 있다.
- ORM 매핑 객체는 세션이 보유하고 있는 트랜잭션에 로컬인 데이터베이스 행에 대한 프록시 객체로 유지 관리된다.
- 객체의 상태를 데이터베이스에 실제로 있는 것과 일치하도록 유지하기 위해, 즉 동기화를 유지하기 위해 객체가 데이터베이스에 다시 액세스하도록 하는 다양한 이벤트가 있다.
- 세션에서 개체를 "분리"하고 계속 사용하는 것이 가능하지만 이 방법에는 주의 사항이 있다.
- 일반적으로 분리된 개체를 다시 작업하고 싶을 때 다른 `Session`과 다시 연결하여 데이터베이스 상태를 나타내는 정상적인 작업을 재개할 수 있도록 하기 위한 것이다.

### 세션 열고 닫기
- 세션은 특정한 DB URL과 관련이 있는지 `Engine`을 이용해 인스턴스화된다.
- 파이썬의 컨텍스트 매니저(`with`)을 이용하면 자동으로 블록 끝에서 닫힌다. `Session.close()` 메서드를 호출하는 것과 같다.
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine('postgresql://scott:tiger@localhost/')

# create session and add objects
with Session(engine) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
```
- `commit()`은 새로운 데이터를 DB에 영속화할 때만 사용한다. 단순 읽기 쿼리에서는 불필요하다.
- `Session.commit()`이 호출된 후에는 세션과 연관된 모든 객체들은 만료된다. 즉, 내용이 모두 지워진다.
- 만약 객체들이 대신 detach 되면, `Session.expire_on_commit` 파라미터가 사용되지 않는 한 새로운 세션과 다시 연관될 때까지 non-functional 하게 된다.

### 시작 / 커밋 / 롤백 블록 구성
- 또한 데이터베이스에 데이터를 커밋할 경우 컨텍스트 관리자 내에서 `Session.commit()` 호출과 트랜잭션의 전체 "framing"을 묶을 수 있다.
- "framing"이란 모든 작업이 성공하면 `Session.commit()` 메서드가 호출되지만 예외가 발생하면 `Session.rollback()` 메서드가 호출되어 트랜잭션이 이전에 즉시 롤백됨을 의미한다. 예외를 외부로 전파한다.
    ```python
    # verbose version of what a context manager will do
    with Session(engine) as session:
        session.begin()
        try:
            session.add(some_object)
            session.add(some_other_object)
        except:
            session.rollback()
            raise
        else:
            session.commit()
    ```
- 위의 방식은 `Session.begin()`메서드에서 반환되는 `SessionTransaction` 객체를 이용하면 더 간결하게 처리할 수 있다.
    ```python
    # create session and add objects
    with Session(engine) as session:
        with session.begin():
        session.add(some_object)
        session.add(some_other_object)
        # inner context calls session.commit(), if there were no exceptions
    # outer context calls session.close()
    ```

### sessionmaker 사용하기
- `sessionmaker`의 목적은 고정 config로 세션 객체에 대한 팩토리를 제공하는 것이다.
    ```python
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # an Engine, which the Session will use for connection
    # resources, typically in module scope
    engine = create_engine('postgresql://scott:tiger@localhost/')

    # a sessionmaker(), also in the same scope as the engine
    Session = sessionmaker(engine)

    # we can now construct a Session() without needing to pass the
    # engine each time
    with Session() as session:
        session.add(some_object)
        session.add(some_other_object)
        session.commit()
    # closes the session
    ```
- `Engine.begin()`과 유사한 자체 `sessionmaker.begin()` 메서드도 있다. 이 메서드는 `Session` 객체를 반환하고 begin/commit/rollback 블록도 유지한다.
- 세션은 양 쪽 모두에서 `with` 블록이 끝날 때 닫힐 뿐만 아니라, 자신의 트랜잭션을 커밋시킬 것이다.
- 어플리케이션을 작성할 때, `sessionmaker` 팩토리는 `create_enging()`에 의해 생성되는 `Engine` 객체와 똑같은 스코프를 가져야한다. 보통 모듈 레벨 혹은 글로벌 스코프이다.
- 이 객체들은 둘 다 팩토리이기 때문에, 어떤 함수나 쓰레드들에서 동시에 사용될 수 있다.

### Querying(2.0 style)
- 2.0 부터는 `Session.execute()`를 사용할 수 있다.
- `Query` 메서드들은 하나의 완전한 엔티티가 요청되는 경우 바로 ORM 맵핑 객체들을 반환한다.
- 하지만 `Session.execute()`에 의해 반환되는 `Result` 객체는 항상 기본적으로 로우들을 (named tuples) 반환한다.

### 새롭거나 이미 존재하는 아이템 추가하기
- `Session.add()`는 세션에 인스턴스들을 위치시키는데 사용된다.
- `transient`(brand new) 인스턴스들에 대해서는 다음 플러시 때 그런 인스턴스들이 인서트되게 하는 효과가 있다.
- `persisten` 인스턴스들 즉, 세션에의해 로딩됐던 인스턴스들에 대해서는 이미 존재해 추가될 필요가 없다.
- `detached` 인스턴스들 즉, 세션에서 삭제된 인스턴스들에 대해서는 세션과 다시 연관을 맺게 한다.
    ```python
    user1 = User(name='user1')
    user2 = User(name='user2')
    session.add(user1)
    session.add(user2)

    session.commit()     # write changes to the database
    ```

### 삭제하기
- `Session.delete()` 메서드는 삭제될 거라고 마크되는 세션의 객체 리스트에 인스턴스를 추가한다.
    ```python
    # mark two objects to be deleted
    session.delete(obj1)
    session.delete(obj2)

    # commit (or flush)
    session.commit()
    ```
- `Session.delete()`는 삭제 대상을 표시하므로 영향을 받는 각 기본 키에 대해 DELETE 문이 생성된다.
- DELETE 후에는 세션에서 제거되며 트랜잭션이 커밋된 후 영구적이게 된다.
- `Session.delete()` 작업, 특히 다른 개체 및 컬렉션에 대한 관계가 처리되는 방식과 관련된 다양한 중요한 동작이 있다.
- `relationship()` 디렉티브를 통해 삭제된 개체와 관련된 매핑된 개체에 해당하는 행들은 **기본적으로 삭제되지 않는다.**
- 만약 그런 객체들이 삭제되는 로우에 대한 FK 제약조건이 있다면, 그러 컬럼들은 NULL로 설정된다. 이건 그 컬럼들이 non-nullable이면 제약 조건 위배를 일으킬 것이다.
- "SET NULL"로 설정되는 걸 관련 객체 로우의 삭제로 변경하려면, `relationship()`에서 삭제 cascade를 사용해라.
- `relationship.secondary` 파라미터를 통해 many-to-many 테이블로 연결된 테이블에 있는 로우들은 객체가 삭제될 때 모든 경우에 삭제된다.
- 관련 객체가 삭제되는 객체에 대한 FK 제약 조건을 포함하고 해당 객체가 속한 관련 컬렉션이 현재 메모리에 로드되지 않을 때, uow는 모든 관련 로우들을 가져오기 위해 SELECT를 내보내므로, PK 값을 사용하여 관련 행에서 UPDATE 또는 DELETE 문을 내보낼 수 있다.
- 이러한 방식으로 추가 지시가 없는 ORM은 이것이 핵심 `ForeignKeyConstraint` 객체에 구성되어 있더라도 ON DELETE CASCADE의 기능을 수행한다.
- `relationship.passive_deletes` 파라미터를 사용해 이 동작을 조정하고 "ON DELETE CASCADE"에 보다 자연스럽게 의존할 수 있다.
- 해당 파라미터를 True로 설정하면, SELECT 작업이 더 이상 발생하지 않지만 로컬에 있는 로우들은 여전히 ​​명시적 SET NULL 또는 DELETE의 적용을 받는다.
- `relationship.passive_deletes`를 "all" 문자열로 설정하면 관련된 모든 객체의 업데이트/삭제가 비활성화된다.
- 삭제 표시가 된 객체에 대한 DELETE가 발생하면, 객체는 참조하는 컬렉션이나 이것을 참조하는 객체 참조로부터 자동으로 제거되지 않는다.
- 세션이 만료되면 이러한 컬렉션이 다시 로드되어 객체가 더 이상 존재하지 않을 수 있다. (`session.flush()` 이후에도 여전히 삭제된 객체가 보이고, `session.commit()`을 해야 보이지 않음.)
- 그러나 이런 객체에 대해 `Session.delete()`를 사용하는 대신, 컬렉션에서 객체를 제거한 다음 해당 컬렉션 제거의 부차적인 효과로 삭제되도록 `delete-orphan`을 사용해야한다.

### 플러싱
- `flush`는 펜딩 중인 모든 객체 생성, 삭제 및 수정을 INSERT, DELETE, UPDATE 등으로 데이터베이스에 기록하는 것이다.
- 세션이 기본 설정으로 사용될 때 플러시 단계는 거의 항상 투명하게 수행된다. (암시적으로?)
- 특히, 플러시는 `Query` 또는 2.0 스타일 `Session.execute()` 호출의 결과로 개별 SQL 문이 실행되기 전에 발생하고 트랜잭션이 커밋되기 전에 `Session.commit()` 호출 내에서 발생한다.
- `Session.flush()` 메서드를 호출하여 언제든지 세션 플러시를 강제할 수 있다.
- 특정 메서드 범위 내에서 자동으로 발생하는 플러시를 `autoflush`라고 한다.
- `Autoflush`는 다음을 포함한 메소드의 시작 부분에서 발생하는 구성 가능한 자동 플러시 호출로 정의된다.
    - `Session.execute()` and other SQL-executing methods.
    - When a `Query` is invoked to send SQL to the database.
    - Within the `Session.merge()` method before querying the database.
    - When objects are `refreshed`.
    - When ORM `lazy load` operations occur against unloaded object attributes.
- 플러시가 무조건 발생하는 지점도 있다. 이러한 지점은 다음을 포함하는 주요 거래 경계 내에 있다.
    - `Session.commit()` 메서드의 프로세스 내에서
- 이전 항목 목록에 적용된 `autoflush` 동작은 `Session.autoflush` 매개변수를 `False`로 전달하는 `Session` 또는 `Sessionmaker`를 구성하여 비활성화할 수 있다.
- 플러시 프로세스는 DBAPI가 드라이버 수준 `autocommit`모드가 아닌 경우 항상 트랜잭션 내에서 발생한다. (데이터베이스 트랜잭션의 격리 수준에 따라 다름)
- 여기에는 더 이상 사용되지 않는 `Session.autocommit` 설정으로 세션이 구성된 경우에도 포함된다.
- 트랜잭션이 없으면 `Session.flush()`는 자체 트랜잭션을 만들고 커밋한다. 즉, 데이터베이스 연결이 트랜잭션 설정 내에서 원자성을 제공한다고 가정하면 플러시 내부의 개별 DML 문이 실패하면 전체 작업이 롤백된다.
- `Session.autocommit`을 사용하는 것 외에, 플러시 내에서 오류가 발생하면 동일한 세션을 계속 사용하기 위해 기반 트랜잭션이 이미 롤백되었더라도 플러시가 실패한 후 `Session.rollback()`에 대한 명시적 호출이 필요하다.
    - 자세한 건 [해당 링크](https://docs.sqlalchemy.org/en/14/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar) 참고!


### 익스파이어링 / 리프레싱
- 세션을 사용할 때 자주 제기되는 중요한 고려 사항은 트랜잭션의 현재 상태와 동기화된 상태를 유지한다는 점에서 데이터베이스에서 로드된 객체에 있는 상태를 처리하는 것이다.
- SQLAlchemy ORM은 객체가 SQL 쿼리에서 "로드될" 때 특정 데이터베이스 아이덴티디에 해당하는 고유한 Python 객체 인스턴스가 유지되는 것과 같은 `identity map`의 개념을 기반으로 한다.
- 즉, 각각 동일한 행에 대해 두 개의 개별 쿼리를 내보내고 매핑된 객체를 다시 가져오면 두 쿼리가 동일한 Python 객체를 반환한다.
    ```python
    u1 = session.query(User).filter(id=5).first()
    u2 = session.query(User).filter(id=5).first()
    u1 is u2
    ```
- 이에 따라 ORM이 쿼리에서 행을 다시 가져올 때 이미 로드된 **객체의 속성을 채우는 것을 건너뛴다.**
- 여기에서 설계 가정은 완벽하게 격리된 트랜잭션을 가정한 다음, 트랜잭션이 격리되지 않은 정도까지 어플리케이션이 데이터베이스 트랜잭션에서 객체를 새로 고치기 위해, 필요에 따라 조치를 취할 수 있다는 것아다.
- ORM 매핑된 개체가 메모리에 로드될 때 현재 트랜잭션의 새 데이터로 내용을 새로 고치는 세 가지 일반적인 방법이 있습니다.
    - `expire()`: 객체의 선택된 또는 모든 속성의 내용을 지울 것이므로 다음에 접근할 때 데이터베이스에서 로드된다. 예를 들면 지연 로딩 패턴을 사용한다.
        ```python
        session.expire(u1)
        u1.some_attribute  # <-- lazy loads from the transaction
        ```
    - `refresh()`: `expire()` 메서드가 수행하는 모든 작업을 수행하지만 하나 이상의 SQL 쿼리를 즉시 내보내 객체의 내용을 실제로 새로 고친다.
        ```python
        session.refresh(u1)  # <-- emits a SQL query
        u1.some_attribute  # <-- is refreshed from the transaction
        ```
    - `populate_existing()`: 실제로 `Query` 객체에 `Query.populate_existing()`으로 표시되며 데이터베이스의 내용에서 무조건 다시 채워지는 객체를 반환해야 함을 나타낸다.
        ```python
        u2 = session.query(User).populate_existing().filter(id=5).first()
        ```

### 임의의 WHERE 절이 있는 UPDATE 및 DELETE
- 반환된 결과 객체는 `CursorResult`의 인스턴스이다. UPDATE 또는 DELETE 문과 일치하는 로우수를 검색하려면 `CursorResult.rowcount`를 사용하면 된다.

#### 동기화 전략 선택
- ORM 지원 업데이트 및 삭제의 1.x 및 2.0 형식 모두에서 다음과 같은 동기화 세션 값이 지원된다.
    - `False`
        - 세션을 동기화하지 않는다.
        - 이 옵션은 가장 효율적이며 세션이 만료됐을 때도 신뢰할 수 있다. 일반적으로 만료는 `commit()` 후에 발생하거나 명시적으로 `expire_all()`을 사용했을 때 발생한다.
        - 만료되기 전에 데이터베이스에서 업데이트되거나 삭제된 객체가 오래된 값으로 세션에 남아 있을 수 있으며, 이로 인해 혼란스러운 결과가 발생할 수 있다.
    - `'fetch'`
        - UPDATE 또는 DELETE 전에 SELECT를 수행하거나 데이터베이스가 지원하는 경우 RETURNING을 사용하여 영향을 받는 로우들의 PK 아이덴티티를 검색한다.
        - 작업의 영향을 받는 메모리 내 객체를 새 값으로 새로 고치거나(업데이트) 세션에서 제거(삭제)할 수 있다.
    - `'evaluate'`
        - 세션 내에서 일치하는 객체를 찾기 위해 Python의 UPDATE 또는 DELETE 문에 제공된 WHERE 기준을 평가한다.
        - 이 접근 방식은 어떤 라운드 트립도 추가하지 않으며 RETURNING 지원이 없는 경우 더 효율적이다.
        - 기준이 복잡한 UPDATE 또는 DELETE 문의 경우 `'evaluate'` 전략이 Python에서 표현식을 평가하지 못할 수 있으며 오류가 발생한다.
        - 만약 그렇다면, `'fetch'`를 사용해라.
        - UPDATE 작업이, 만료된 많은 개체가 있는 세션에서 실행되는 경우 이 전략을 피해야한다.
        - 각 객체에 대해 SELECT를 내보내는 위치에 따라 해당 객체를 새로 고쳐야 하기 때문이다.
        - 세션이 여러 `Session.commit()` 호출에서 사용되고 있고 `Session.expire_on_commit` 플래그가 기본값인 `True`인 경우 세션에 만료된 개체가 있을 수 있다.
- ORM 지원 UPDATE 및 DELETE 기능은 ORM 작업 단위 자동화를 우회하여 복잡성 없이 한 번에 여러 행과 일치하는 단일 UPDATE 또는 DELETE 문을 내보낼 수 있다.
- 해당 작업들은 in-Python 릴레이션쉽 캐스케이딩을 제공하지 않는다.
- ON UPDATE CASCADE 및/또는 ON DELETE CASCADE가 이를 필요로 하는 모든 외래 키 참조에 대해 구성되어 있다고 가정한다.
- 그렇지 않으면 외래 키 참조가 실행 중인 경우 데이터베이스가 무결성 위반을 내보낼 수 있다.
- UPDATE 또는 DELETE 후에 관련 테이블에서 ON UPDATE CASCADE 또는 ON DELETE CASCADE에 의해 영향을 받은 세션의 종속 객체는 현재 상태를 포함하지 않을 수 있다. 이 이슈는 세션이 만료되면 해결된다.
- MySQL이나 SQLite는 RETURNING을 지원하지 않는다. 그래서 추가적인 SELECT문이 나가기 때문에 퍼포먼스를 감소시킨다.
- ORM 사용 UPDATE 및 DELETE는 조인된 테이블 상속을 자동으로 처리하지 않는다.
- 여러 테이블에 대한 작업인 경우 일반적으로 개별 테이블에 대한 개별 UPDATE/DELETE 문을 사용해야 한다.

### Auto Begin
```
이 섹션은 1.4 버전의 행동을 묘사한다. 이전 버전에는 적용되지 않는다.
```
- 세션 객체는 `autobegin`이라는 동작을 제공한다.
- 이것은 세션으로 작업이 수행되자마자 세션이 내부적으로 "트랜잭션" 상태에 있는 것으로 간주한다는 걸 나타낸다.
- 객체 상태 변경과 관련하여 세션의 내부 상태를 수정하거나 데이터베이스 연결이 필요한 작업을 포함한다.
- 세션이 처음 생성될 때 트랜잭션 상태가 존재하지 않는다.
- 트랜잭션 상태는 `Session.add()` 또는 `Session.execute()`와 같은 메서드가 호출될 때 자동으로 시작된다. 혹은 `Session.execute()`로 `Query`가 수행되거나 persistent 객체에서 속성이 변경될 때도 포함한다.
- 트랜잭션 상태는 "autobegin" 단계가 진행되었는지 여부를 나타내는 `True` 또는 `False`를 반환하는 `Session.in_transaction()` 메서드에 액세스하여 확인할 수 있다.
- 세션의 트랜잭션 상태는 `Session.begin()` 메서드를 호출하여 명시적으로 시작할 수도 있다. 이 메서드가 호출되면 세션은 무조건 "트랜잭션" 상태가 된다.

### Committing
- `Session.commit()`은 현재 트랜잭션을 커밋하는 데 사용된다.
- 핵심적으로 이것은 트랜잭션이 진행 중인 모든 현재 데이터베이스 연결에 대해 COMMIT를 내보낸다는 것을 나타낸다.
- 세션에 대한 트랜잭션이 없을 때 `Session.commit()`에 대한 이전 호출 이후 이 세션에서 호출된 작업이 없음을 나타낸다.
- 메서드는 내부 전용 "논리적" 트랜잭션을 시작하고 커밋한다.
- 보류 중인 플러시 변경 사항이 감지되지 않는 한 일반적으로 데이터베이스에 영향을 미치지 않는다. 그러나 여전히 이벤트 핸들러와 객체 만료 규칙을 호출한다.
- `Session.commit()` 작업은 관련 데이터베이스 연결에서 `COMMIT`를 내보내기 전에 무조건 `Session.flush()`를 실행한다.
- 보류 중인 변경 사항이 감지되지 않으면 데이터베이스에 SQL이 내보내지지 않는다.
- 이 동작은 config로 설정할 수 없으며 `Session.autoflush` 매개변수의 영향을 받지 않는다.
- 그 후 `Session.commit()`은 실제 데이터베이스 트랜잭션(있는 경우)을 커밋한다.
- 마지막으로 트랜잭션이 종료되면 세션 내의 모든 객체가 만료된다.
- 이는 속성 액세스를 통해 또는 `SELECT` 결과에 존재함으로써 인스턴스가 다음에 액세스될 때 가장 최근 상태를 수신하도록 하기 위한 것이다.
- 이 동작은 `Session.expire_on_commit` 플래그에 의해 제어될 수 있으며, 이 동작이 바람직하지 않을 때 `False`로 설정될 수 있다.

### Rolling Back
- `Session.rollback()`은 현재 트랜잭션이 있는 경우 롤백한다. 트랜잭션이 없으면 메서드가 조용히 패스한다.
- 기본 구성된 세션에서 `autobegin`을 통해 또는 `Session.begin()` 메서드를 명시적으로 호출하여 트랜잭션이 시작된 뒤, 세션의 롤백 후 상태는 다음과 같다.
    - 세션이 커넥션에 직접 바인딩된 경우(이 경우 커넥션은 계속 유지되지만 여전히 롤백됨) 되지 않는 한 모든 트랜잭션이 롤백되고 모든 커넥션이 커넥션 풀로 반환된다.
    - 트랜잭션 라이프스팬 내에서 세션에 추가될 때, 처음에 `pending` 상태에 있었던 객체는 롤백되는 `INSERT` 문에 따라 삭제된다. 속성의 상태는 변경되지 않은 상태로 유지된다. <br>
    *pending: 데이터베이스 아이덴티티가 없지만 최근에 세션과 연결된 새 객체입니다. 세션이 플러시를 내보내고 로우가 삽입되면 객체가 퍼시스턴트 상태로 이동합니다.
    - 트랜잭션 라이프스팬 내에서 삭제된 것으로 표시된 객체는 롤백되는 `DELETE` 문에 해당하는 퍼시스턴트 상태로 다시 승격된다.
    - 해당 객체가 트랜잭션 내에서 먼저 `pending` 중인 경우 해당 작업이 대신 우선한다.
    - 삭제되지 않은 모든 객체는 완전히 만료된다. 이는 `Session.expire_on_commit` 설정과 관계가 없다.
- 일반적으로 기본 키, 외래 키 또는 "not nullable" 제약 조건 위반과 같은 이유로 `Session.flush()`가 실패하면 롤백이 자동으로 실행된다. (현재 부분 실패 후 플러시를 계속할 수 없음)
- 그러나 이 시점에서 세션은 "inactive"으로 알려진 상태가 된다. 그리고 호출하는 어플리케이션은 항상 `Session.rollback()` 메서드를 명시적으로 호출하여 세션이 사용 가능한 상태로 돌아갈 수 있도록 해야한다.

### Closing
- `Session.close()` 메서드는 세션에서 모든 ORM 매핑 객체를 제거하고 바인딩된 엔진 객체에서 트랜잭션/커넥션 리소스를 해제하는 `Session.expunge_all()`을 실행한다. 커넥션이 커넥션 풀로 반환되면 트랜잭션 상태도 롤백된다.
- `Session`이 닫히면 기본적으로 처음 생성될 때와 같은 원래 상태가 되며 **다시 사용할 수 있다.**
- 이런 의미에서 `Session.close()` 메서드는 "데이터베이스 닫기" 메서드가 아니라 깨끗한 상태로 다시 "재설정"하는 것과 비슷하다.
- 세션의 범위는 특히 `Session.commit()` 또는 `Session.rollback()` 메서드가 사용되지 않는 경우 마지막에 `Session.close()`를 호출하여 제한하는 것이 좋다.

## Session Frequently Asked Questions
### Is the Session a cache?
- 네...니오.
- 아이덴티티 냅 패턴을 구현하고 기본 키에 키가 지정된 개체를 저장한다는 점에서 캐시로 다소 사용된다.
- 하지만 어떤 종류의 쿼리 캐싱도 수행하지 않는다.
- 세션은 모두가 객체의 레지스트리로 참조하는 글로벌 객체로 설계되지 않았다.

### Is the session thread-safe?
- 세션은 일반적으로 한 번에 하나의 스레드만 의미하는 non-concurrent 방식으로 사용하기 위한 것이다.
- 세션은 단일 트랜잭션 내에서 단일 일련의 작업에 대해 하나의 인스턴스가 존재하는 방식으로 사용해야 한다.
- 더 큰 요점은 여러 concurrent 스레드가 있는 세션을 사용하지 않아야 한다는 것이다.

## backref 궁금한 점
- 모델 양쪽에 선언이 가능한가?
  - 불가능하다. 다음과 같이 선언하고, `DBUser`를 생성하려고 하면 에러가 난다.
  ```python
  class DBUser(Base):
    id = Column(Integer, primary_key=True, index=True)
    items = relationship("DBArticle", backref="user")


  class DBArticle(Base):
    id = Column(Integer, primary_key=True, index=True)
    user = relationship("DBUser", backref="items")
  ```
  ```
  sqlalchemy.exc.ArgumentError: Error creating backref 'user' on relationship 'DBUser.items': property of that name exists on mapper 'mapped class DBArticle->articles'
  ```
- `relationship`을 선언한쪽에서 변경했을 때와 상대 쪽에서 변경했을 때 자동 반영에 차이가 있는가?
  - 없다.
    |     | 새로운 객체 | 존재하는 객체 |
    | --- | -------- | ---------- |
    | child 관계 사용 | 변경 | 변경 | 
    | parent 관계 사용 | 변경 | 변경 |
  - `backref`나 `back_populates`나 똑같다.
