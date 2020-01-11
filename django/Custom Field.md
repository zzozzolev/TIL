### 왜?
- list field를 쓰고 싶은데 MySQL에서 지원하지 않는다... 그렇다고 `TextField`로 그냥 json dumps 해버리면 대참사가 예상된다. 그리고 별도의 패키지를 깔자니 번거롭고 star도 많지 않다. (구글에 검색하면 나오는 거 https://django-mysql.readthedocs.io/en/latest/model_fields/list_fields.html)
- 그렇다면 그냥 custom field를 만들어서 db에는 text로 저장하고 python에서 쓸 때는 list로 쓰자!

### 기본
- `django.db.models.Field`를 상속받으면 `get_internal_type`을 선언해줘야 db에 저장된다.
- `value_from_object`는 instance에서 value를 얻는 건데 `obj`에서 `self.attname`으로 특정 값을 가져와야 한다. 근데 `django-rest-framework(drf)`에서 `django.db.models.Field`일 경우 `to_representation`에서 이 method를 호출하기 때문에 `django.db.models.Field`의 구현인 `getattr`로 호출하면 에러가 난다. `drf`는 `collections.OrderedDict`를 사용하기 때문이다. 그래서 `collections.OrderedDict`인 경우에 대해서는 따로 처리해줘야 한다. db에서 obj로 꺼내오면 null field를 처리해주지 않아도 되지만 이 경우에는 `None` 반환하도록 처리해줘야 한다.
- 그리고 `to_representation`에서 `value_to_string`을 호출하기 때문에 이것도 override 해줄 필요가 있다. 공식 문서에서는 `value_from_object`와 `get_prep_value`를 이용했다.
- `from_db_value`는 db에서 불러온 거를 적절한 python 자료형으로 바꿔줄 때 필요하다.
- `to_python`은 deserialization forms에서 쓰인다고 한다. 이것도 python 자료형으로 바꿔줄 때 필요하다.
- 대충 아래와 같은 형태로 작성하면 웬만한 거는 커버 가능 😎
```
import json
from collections import OrderedDict

from django.db import models

class ListField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        """Returns a string naming this field for backend specific purposes.
           models.Field isn't saved in databases if it is not defined.
        """
        return "TextField"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self._load_value(value)

    def value_from_object(self, obj):
        # django-rest-framework call this method in 
        # to_representation for models.Field
        if isinstance(obj, OrderedDict):
            if self.attname in obj:
                return obj[self.attname]
            else:
                return None
        else:
            return getattr(obj, self.attname)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def to_python(self, value):
        if isinstance(value, list) or value is None:
            return value
        return self._load_value(value)
    
    def get_prep_value(self, value):
        # To confirm JSON serializable (numpy type isn't)
        value = eval(str(value))
        return json.dumps(value)
        
    def _load_value(self, value):
        return json.loads(value)
```
- `models.py`에서 사용할 때는 제대로 값이 설정됐는지 validators argument를 넘겨줘서 확인하는 것을 추천한다.
```
def validate_list_type(value):
    if not isinstance(value, list):
        raise ValidationError(
            f"{value} type({type(value)}) != list"
        )
```
```
some = ListField(validators=validate_list)
```