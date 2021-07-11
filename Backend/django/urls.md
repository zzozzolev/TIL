# Trailing Slash
- web 강의를 듣다가 갑자기 trailing slash를 붙이는 게 맞는지 아닌지 궁금해졌다.
- 찾아보니 Django는 trailing slash를 붙인다고 한다.
  ```
  Trailing slashes are conventional in Django, but are not used by default in some other frameworks such as Rails.
  - DRF
  ```

# 장고가 리퀘스트를 처리하는 방법
- https://docs.djangoproject.com/en/3.2/topics/http/urls/#how-django-processes-a-request 에 있는 내용을 번역했다.
- 유저가 장고로부터 페이지를 요청할 때 어떤 파이썬 코드를 실행할 지 결정한다.
1. 장고는 사용할 root URLconf 모듈을 결정한다. 일반적으로 이건 `ROOT_URLCONF` (`settings.py`에 있음)이지만, 만약 들어오는 `HttpRequest` 오브젝트가 `urlconf` 어트리뷰트를 가진다면 (미들웨어에 의해 셋팅) `ROOT_URLCONF` 대신 쓰인다.
2. 장고는 파이썬 모듈을 로드하고 `urlpatterns` 변수를 찾아본다. 이건 `django.urls.path()` 혹은 `django.urls.re_path()`의 인스턴스들의 시퀀스여야한다.
3. 장고는 `path_info`와 맞춰보면서 순서대로 각각의 URL 패턴을 돌리다가 요청된 URL과 매치하는 순간 멈춘다. (`path_info`에 대한 설명은 `request and response.md` 참고)
4. 만약 URL 패턴들 중 하나가 매치된다면, 장고는 주어진 뷰를 임포트하고 호출한다. 이때 뷰는 파이썬 함수이든 클래스일 것이다. 뷰는 다음과 같은 arguments를 넘겨 받는다.
  - `HttpRequest`의 인스턴스
  - 만약 URL 패턴이 named groups가 없다면 regex에서 매치된 게 positional arguments로 제공된다.
  - keyword argument들은 `django.urls.path()` 혹은 `django.urls.re_path()`에 optional kwargs로 지정된 아무 arguments에서 오버라이딩 된다. 그리고 제공되는 패스 표현에 의해 매치되는 named parts로 구성된다. (해석을 제대로 한 건지 모르겠음; path에 kwargs 지정하면 넘겨받는다는 의미인 것 같음) 
5. 만약 URL 패턴이 매치되지 않거나 예외가 발생한다면, 장고는 적절한 에러 핸들링 뷰를 호출한다.