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

## backref vs back_populates
- 객체간에 관계가 있을 때 사용하는 어트리뷰트.
- https://velog.io/@inourbubble2/SQLAlchemy%EC%9D%98-backref%EC%99%80-backpopulates%EC%9D%98-%EC%B0%A8%EC%9D%B4
