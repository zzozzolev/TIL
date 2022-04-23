## 상위 디렉토리 모듈을 import 하기
- `PYTHONPATH`에 루트 디렉토리를 추가한다.
- 예를 들어 아래와 같은 구조라면 `PYTHONPATH`에 `/app`을 추가한다. (단, 절대 경로가 들어가야됨)
  ```
  app
    L dir1
        L a.py # from app.dir2 import b
    L dir2
        L b.py
  ```
