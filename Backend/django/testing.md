# 특정 클래스의 테스트만 수행하기
- `$ python3 manage.py tests <root_dir>/<app>/<test file name>/<class name>`
- 예를 들어 디렉토리 구조가 아래와 같이 생겼다면 다음과 같이 한다.
    ```
    medium_clone
      L apps
        L posts
          L test.py (class PostSerializerTests)    
    ```
    ```
    $ python3 manage.py test apps.posts.tests.PostSerializerTests
    ```