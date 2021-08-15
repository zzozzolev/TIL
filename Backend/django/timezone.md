# Time zones documentation

## Overview

- When support for time zones is enabled, Django stores datetime information in UTC in the database, uses time-zone-aware datetime objects internally, and translates them to the end user’s time zone in templates and forms. (물론 django의 템플릿과 폼을 쓰는 일이 없어서 이건 해당 안 됨ㅠ)
- 이 기능은 사용자가 둘 이상의 표준 시간대에 살고 있고 각 사용자의 wall clock에 따라 날짜 시간 정보를 표시하려는 경우에 유용하다.
- 웹 사이트가 하나의 표준 시간대에서만 사용 가능하더라도 UTC로 데이터를 데이터베이스에 저장하는 것이 좋다. 주된 이유는 일광 절약 시간제(DST)때문이다. 많은 나라들은 봄이 되면 시계가 전진하고 가을이 되면 후진하는 DST 시스템을 가지고 있다.
- Time zone support는 기본적으로 지원이 되지 않아서 `USE_TZ = True`로 하라고 나와있지만 바로 다음에 이렇게 나와있다
  > The default settings.py file created by django-admin startproject includes USE_TZ = True for convenience.

## Concepts

### Naive and aware datetime objects

- Python의 datetime.datetime 개체에는 datetime.tzinfo 하위 클래스의 인스턴스로 표시되는 표준 시간대 정보를 저장하는 데 사용할 수 있는 tzinfo attribute가 있다. 이 attribute가 설정되고 오프셋을 설명하면 datetime object가 aware이고 그렇지 않으면 naive이다.
- `USE_TZ=True`이면 장고는 time-zone-aware datetime objects를 사용한다. 이렇게하면 코드에서 naive datetime objects를 만들었을 때, Django는 필요할 때 aware하게 만든다.

### Interpretation of naive datetime objects

- `USE_TZ`가 `True`인 경우에도 Django는 이전 버전과의 호환성을 유지하기 위해 naive datetime objects 계속 허용한다. 데이터베이스 계층이 수신하면 default time zone에서 해석하여 인식하려고 시도하고 경고가 발생한다.

### Default time zone and current time zone

- default time zone은 `TIME_ZONE` setting에 의해 정의되는 time zone이고 current time zone은 렌더링에 사용되는 time zone이다.
- `activate()`를 사용해 current time zone을 앤드 유저의 actual time zone으로 설정해야한다. 그렇지 않다면 default time zone이 사용된다.
- `TIME_ZONE`의 문서에서 설명된 대로 Django는 프로세스가 default time zone에서 실행되도록 환경 변수를 설정한다. 이 문제는 `USE_TZ` 값과 current time zone에 관계없이 발생한다.
- `USE_TZ`가 `True`인 경우, 여전히 local time에 의존하는 어플리케이션과의 backwards-compatibility를 유지하는 데 유용하다. 그러나 위에서 설명한 것처럼, 이것은 전적으로 신뢰할 수 있는 것은 아니며, 항상 UTC의 aware datetimes을 코드에서 사용해야한다. 예를 들어 `fromtimestamp()`를 사용하고 `tz` 매개 변수를 `utc`로 설정한다.

### Fixtures

- aware datetime을 시리얼라이징할 때는 다음과 같이 UTC offset이 포함된다.
  ```
  "2011-09-01T13:20:30+03:00"
  ```
- naive datetime일 때는 그렇지 않다.
  ```
  "2011-09-01T13:20:30"
  ```

### Selecting the current time zone

- current time zone은 current locale과 동일하다.
- 하지만 locale처럼 헤더에서 `Accept-Language`같은 정보는 얻지 못한다.
- Django는 time zone을 선택하는 함수들을 제공한다. time zone을 선택할 때 이걸 사용해라.
- time zone을 신경쓰는 대부분의 웹 사이트들은 유저들에게 어떤 time zone에서 사는지 물어보고 이 정보를 유저의 프로필에 저장한다.
- 구체적인 구현은 제외하고 대략적인 것만 보면 다음과 같이 time zone을 activate한다.
  ```
  import pytz
  from django.utils import timezone
  ...
  timezone.activate(pytz.timezone(tzname))
  ```
