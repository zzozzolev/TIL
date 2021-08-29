## wsgi 선택하기
- [wsgi benchmark](https://www.appdynamics.com/blog/engineering/a-performance-analysis-of-python-wsgi-servers-part-2/)
- 위의 사이트에서 유명한 wsgi를 벤치마크했다.

### 결론
```
- Bjoern: Appears to live up to its claim as a “screamingly fast, ultra-lightweight WSGI server.”
- CherryPy: Fast performance, lightweight, and low errors. Not bad for pure Python.
- Gunicorn: A good, consistent performer for medium loads.
- Meinheld: Performs well and requires minimal resources. However, struggles at higher loads.
- mod_wsgi: Integrates well into Apache and performs admirably.
```

### 참고
- `CherryPy`는 나온대로 퍼포먼스도 좋고 에러도 적었는데 동시에 연결된 커넥션이 증가할 수록 메모리 사용률도 비례해서 증가했다.
- `CherryPy`의 github star는 1.4k이고 `gunicorn`의 github star는 7.8k로 `gunicorn`이 더 유명하고 보편적으로 쓰이는 것 같다.
- `gunicorn`은 standalone 서버이기는하나 이런 저런 취약점 때문에 앞에 웹서버를 붙여서 쓴다고 한다.
