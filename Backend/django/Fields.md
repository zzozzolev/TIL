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

# Field options
- [공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-options)

### unique
- If True, this field must be unique throughout the table.
- If you try to save a model with a duplicate value in a unique field, a django.db.IntegrityError will be raised by the model’s `save()` method.
- This option is valid on all field types except ManyToManyField and OneToOneField.
- Note that when unique is True, you don’t need to specify `db_index`, because unique implies the creation of an index.
