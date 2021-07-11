# path vs path_info
- https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpRequest.path
- `path_info`의 설명을 보면 차이를 알 수 있다.
- 몇몇 웹 서버 설정들에서는 호스트 이름 이후의 URL 부분은 스크립트 프리픽스 부분과 패스 정보 부분으로 나뉜다.
- `path_info`는 항상 무슨 웹 서버가 쓰이든 항상 패스 정보만 담고 있다.
- `path` 대신 이걸 사용하면 코드를 테스트와 디플로이먼트 서버들 간에 바꾸는 게 더 쉬워진다.
- 예를 들면 만약 어플리케이션에 `WSGIScriptAlias`를 `"/minfo"`로 해놨다면 `path`는 `"/minfo/music/bands/the_beatles/"`가 되고 `path_info`는 `"/music/bands/the_beatles/"`가 된다.