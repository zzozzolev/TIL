# session, cookie 설명 및 차이점
- https://jeong-pro.tistory.com/80

# JWT
- authorization에 쓰이는 거지 authentication에 쓰이는 게 아니다.
- 이미 존재하는 유저에 대해서 토큰을 발급해주고 이용하는 것이다.
- session은 서버에 유저 정보를 저장하기 때문에 동일한 클라이언트가 여러 서버에 접근해야할 때 불편하다. 하지만 JWT 같은 경우, 클라이언트가 정보를 갖고 있기 때문에 그렇지 않다.

## session vs jwt
- [세션은 뭐고 JWT는 무엇일까](https://m.blog.naver.com/shino1025/221568544633)

## payload
- payload의 key, value 페어 하나 하나를 claim이라고 한다.
- claim은 다음과 같이 세 가지 종류가 있다.
  1. Registered claims
  2. Public claims
  3. Private claims
  - 위의 1,2번은 정의한 대로 써야하고 그 외에 나머지는 자유롭게 정의해도 된다.

## 인증 과정
- 보통은 대칭키(암호화와 복호화에 같은 키 사용)인 secret key를 이용해 서버가 인코딩된 header와 payload를 서명하고 클라이언트에게 `access token`으로 넘겨준다.
- 클라이언트는 authorization을 하고 싶을 때, 이 `access token`을 서버에게 넘겨준다.
- 서버는 클라이언트에게 받은 `access token`을 header, payload, signature로 분류한 뒤, 자신의 secret key로 signature를 생선한다. 그리고 새로 만든 signature와 클라이언트에게 받은 signature가 같은지 비교한다.

## 참고
- [What Is JWT and Why Should You Use JWT](https://www.youtube.com/watch?v=7Q17ubqLfaM)
- https://meetup.toast.com/posts/239
- [JWT 구조 & JWT 인증 과정](https://velog.io/@zz3n/HTTP-%EC%9D%B8%EC%A6%9D-JWT)