# SlugField란?

- [공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#slugfield)
- letters, numbers, underscores, hyphens로만 이루어진 field.
- URL에 쓰일 수 있는 field. title 같은 것을 그대로 사용하면 보기에 좋지 않음.

  ```
  www.example.com/article/The%2046%20Year%20Old%20Virgin (x)

  www.example.com/article/the-46-year-old-virgin (o)
  ```

- [참고](https://itmining.tistory.com/119)

# CharField vs TextField

- [CharField 공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.CharField)
- [TextField 공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.TextField)
- `CharField`는 작은 사이즈의 스트링에 알맞은 필드이다. `max_length`를 필수로 지정해줘야한다.
- 반면 `TextField`는 큰 사이즈의 스트링에 알맞은 필드이다.
- 둘의 차이는 다음과 같다.
  1. DB 컬럼 타입: 물론 DMBS에 따라 차이가 없을 수 있다. 하지만 MySQL 같은 경우 `TextField`는 `longtext`로, `CharField`는 `varchar`로 된다.
  2. form에서 렌더링 되는 방식의 차이: `CharField`는 single line input이지만 `TextField`는 multi line으로 렌더링될 수 있다고 한다.

# CharField와 TextField에서 null=True? blank=True?

- string 기반의 필드인 CharField와 TextField를 쓸 때 빈 값을 허용할 때 `null=True`를 해야할지 `blank=True`를 해야할지 고민이 될 수 있다.
- 공식 문서에서는 특수한 케이스를 제외하고는 `blank=True`를 쓰라고 가이드하고 있다.
  - [null](https://docs.djangoproject.com/en/3.2/ref/models/fields/#null)
  - [blank](https://docs.djangoproject.com/en/3.2/ref/models/fields/#blank)
- 요약하면 string 기반 필드에 `null=True`를 하면 "no data"에 대해 두 가지 가능성이 있을 수 있기 때문에 `blank=True`를 쓰라는 것이다.
- `unique=True`이면서 `blank=True`이면 `null=True`가 필요할 수도 있다.
- 또한 두 필드의 중요한 차이점 중 하나는 `null`은 database-related이고 `blank`는 validation-related라고 한다.

# Field options

- [공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-options)

### unique

- If True, this field must be unique throughout the table.
- If you try to save a model with a duplicate value in a unique field, a django.db.IntegrityError will be raised by the model’s `save()` method.
- This option is valid on all field types except ManyToManyField and OneToOneField.
- Note that when unique is True, you don’t need to specify `db_index`, because unique implies the creation of an index.

# Custom relational fields

- [drf 문서](https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields)
- model instance로부터 output representation이 어떻게 보여져야하는지 직접 정의할 수 있음.
- 필요 조건
  - `serializers.RelatedField`를 상속해야함.
  - `.to_representation(self, value)`를 구현해야함. `value`는 모델 인스턴스임.
- `.to_internal_value(self, value)`를 구현해 real-write를 할 수 있도록 만들 수 있음.
- context에 따라 dynamic queryset을 제공하기 위해서는 `.get_queryset(self)`를 오버라이드하면 됨.
- 예시 (출처는 [여기](https://github.com/gothinkster/django-realworld-example-app/blob/master/conduit/apps/articles/relations.py#L6))

  ```python
  class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())

        return tag

    def to_representation(self, value):
        return value.tag
  ```

# DateField

## `auto_now`, `auto_now_add`의 time zone

- `auto_now`, `auto_now_add`를 `True`로 하면 해당 필드를 알아서 `now`로 설정한다.
- 이때 [문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.DateField.auto_now_add)를 보면 `DateTimeField`는 디폴트로 `django.utils.timezone.now()`를 사용한다.
- 코드를 정확하게 본 것이 맞나 싶지만 소스 코드를 보면 아래와 같이 나와있다.

```python
    def _check_fix_default_value(self):
        """
        Warn that using an actual date or datetime value is probably wrong;
        it's only evaluated on server startup.
        """
        if not self.has_default():
            return []

        now = timezone.now()
        if not timezone.is_naive(now):
            now = timezone.make_naive(now, timezone.utc)
```

- 또한 `django.utils.timezone.now()`의 [문서](https://docs.djangoproject.com/en/3.2/ref/utils/#django.utils.timezone.now)를 보면 다음과 같이 나와있다.

> If `USE_TZ` is True, this will be an aware datetime representing the current time in UTC. Note that `now()` will always return times in UTC regardless of the value of `TIME_ZONE`; you can use `localtime()` to get the time in the current time zone.

- 따라서 `auto_now`, `auto_now_add`를 `True`로 설정하면 항상 UTC로 저장된다는 것을 알 수 있다.
