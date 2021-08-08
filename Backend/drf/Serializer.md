### model에 없는 key 값을 넘겨주면 어떻게 될까?
- serializer에 model에 없는 key가 있어도 `is_valid`를 거친 `data`에는 해당 key가 존재하지 않는다. 즉 이상한 key 넘겨줘도 알아서 걸러줌

### read_only, write_only
- 해당 옵션들을 이용해 인스턴스를 업데이트 하거나 생성할 때 (deserialization) 사용할 것인지, representation에 내보낼 것인지 (serialization)를 결정할 수 있다.

### Saving instances
- https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
- 밸리데이션한 데이터를 저장하기 위해서는 `.create()`와 `.update()`를 오버라이드하면 된다.
- `.create()`는 데이터에서 모델 인스턴스를 새롭게 만드는 것이고 `.update()`는 기존 인스턴스의 내용을 업데이트하는 것이다.
- 데이터를 deserializing할 때 인스턴스를 리턴하기 위해 `.save()`를 호출할 수 있다.
- `.save()`를 호출하는 것은 새로운 인스턴스를 만들거나 이미 존재하는 인스턴스를 업데이트할 수도 있다. 이건 시리얼라이저 클래스를 인스턴스화할 때 이미 존재하는 인스턴스를 넘겨줬냐에 따라 다르다.
    ```python
    # .save() will create a new instance.
    serializer = CommentSerializer(data=data)

    # .save() will update the existing `comment` instance.
    serializer = CommentSerializer(comment, data=data)
    ```
- 단, 주의해야할 게 `.save()`에서 모델을 저장하지 않는 것이다. `BaseSerializer`의 `.save()`에서 밸리데이션하는 부분을 걷어내면 다음과 같다. 위에서 나온 것처럼 `self.instance`가 지정돼있으면 `.update()`를 호출하고 그렇지 않으면 `.create()`를 호출한다.
  ```
    ...
    validated_data = {**self.validated_data, **kwargs}

    if self.instance is not None:
        self.instance = self.update(self.instance, validated_data)
        assert self.instance is not None, (
            '`update()` did not return an object instance.'
        )
    else:
        self.instance = self.create(validated_data)
        assert self.instance is not None, (
            '`create()` did not return an object instance.'
        )

    return self.instance
  ```

### Including extra context
- https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context
- serializer에 추가로 context를 제공해야할 수도 있다.
- 흔한 케이스 중 하나는 serializer가 다른 모델과 relation을 맺고 있을 때이다. (문서에서는 hyperlinked relation을 언급했음)
- 이때는 serializer가 현재 request에 접근해서 적절한 정보를 얻을 수 있어야한다.
- 딱 정해진 건 아니고 아무 정보나 넘겨줄 수 있다.
```
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': 'denvercoder9', 'created': datetime.datetime(2013, 2, 12, 09, 44, 56, 678870), 'details': 'http://example.com/accounts/6/details'}
```
