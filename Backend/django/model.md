# Abstract base classes
- [문서](https://docs.djangoproject.com/en/3.2/topics/db/models/#abstract-base-classes)
- 여러 모델에 공통적으로 들어갈 필드를 넣을 때 인터페이스로 사용하기 좋다.
- `Meta` class에 `abstract=True`로 해서 만들게 되는데 이렇게 하면 DB에 table이 만들어지지 않는다.
- 예시 [여기](https://github.com/gothinkster/django-realworld-example-app/blob/29c9d42831fa0cfc5a4aa7561f674396eacf20a2/conduit/apps/core/models.py#L4)를 참고했다.
 ```python
 class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

 # 이제 Article은 `created_at`과 `updated_at`을 가진다.
 class Article(TimestampedModel):
 ```