# DateTimeField

## serialization

- [3.7.0의 릴리즈 노트](https://www.django-rest-framework.org/community/release-notes/#370)를 보면 다음과 같이 나와있다.
  > Timezone-aware DateTimeFields now respect active or default timezone during serialization, instead of always using UTC.
  - naive가 아닌 `DateTimeFields`는 UTC를 항상 사용하기보다는 active 혹은 default timezone을 serialization 동안 사용한다는 것이다.
