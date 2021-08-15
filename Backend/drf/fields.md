# DateTimeField

## serialization

- [3.7.0의 릴리즈 노트](https://www.django-rest-framework.org/community/release-notes/#370)를 보면 다음과 같이 나와있다.
  > Timezone-aware DateTimeFields now respect active or default timezone during serialization, instead of always using UTC.
  - naive가 아닌 `DateTimeFields`는 UTC를 항상 사용하기보다는 active 혹은 default timezone을 serialization 동안 사용한다는 것이다.
- 단, 해당 필드를 `serializers.SerializerMethodField`를 이용하면 instance를 이용해야하므로 이러한 변환이 일어나지 않는다.
- 따라서 default time zone으로 변환도하면서 포맷을 변경하고 싶다면 `to_representation`을 오버라이딩할 때 부모의 메서드를 먼저 호출한 후 포맷을 변경해야한다.
  ```
  def to_representation(self, instance):
    data = super().to_representation(instance)
    data["created_at"] = # 원하는 포맷
    return data
  ```
