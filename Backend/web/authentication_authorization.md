# session, cookie 설명 및 차이점
- https://jeong-pro.tistory.com/80

# JWT
- 이미 존재하는 유저에 대해서 토큰을 발급해주고 이용하는 것이다.
- session은 서버에 유저 정보를 저장하기 때문에 동일한 클라이언트가 여러 서버에 접근해야할 때 불편하다. 하지만 JWT 같은 경우, 클라이언트가 정보를 갖고 있기 때문에 그렇지 않다.

## authentication vs authorization
- authorization에 쓰이는 거지 authentication에 쓰이는 게 아니다.
- authentication은 username과 password가 올바른지 확인하는 것이고 authorization은 request를 보내는 유저가 올바른 유저가 맞는지 확인하는 것이다.
- [비슷해보이지만 다른 두 친구를 소개합니다.](https://baek.dev/post/24/)

## session vs jwt
- [쉽게 알아보는 서버 인증 1편(세션/쿠키 , JWT)](https://tansfil.tistory.com/58)

## payload
- payload의 key, value 페어 하나 하나를 claim이라고 한다.
- claim은 다음과 같이 세 가지 종류가 있다.
  1. Registered claims
  2. Public claims
  3. Private claims
  - 위의 1,2번은 정의한 대로 써야하고 그 외에 나머지는 자유롭게 정의해도 된다.

## 인증 과정
- [jwt-security-nobody-talks-about](https://www.pingidentity.com/en/company/blog/posts/2019/jwt-security-nobody-talks-about.html)

### 대칭키
- 암호화와 복호화에 같은 키를 사용한다.
- 대칭키인 secret key를 이용해 서버가 인코딩된 header와 payload를 서명하고 클라이언트에게 `access token`으로 넘겨준다.
- 클라이언트는 authorization을 하고 싶을 때, 이 `access token`을 서버에게 넘겨준다.
- 서버는 클라이언트에게 받은 `access token`을 header, payload, signature로 분류한 뒤, 자신의 secret key로 signature를 생선한다. 그리고 새로 만든 signature와 클라이언트에게 받은 signature가 같은지 검증한다.
- 한계: 모든 서비스가 같은 secret key를 공유하고 있어야한다. secret key는 말 그대로 비밀스럽게 신뢰할 수 있는 곳에서만 가지고 있어야한다.

### 비대칭키
- 대칭키의 보안상 한계를 보완하기 위해 사용한다.
- secret key는 signature 생성에 public key는 signature 복호화에 사용한다.
- secret key는 안전한 장소에만 보관된다. public key는 검증이 필요한 모든 서버가 공유한다.
- 클라이언트에게 요청을 받은 public key를 가지고 있는 서버가 secret key를 들고 있는 서버에 jwt 생성을 요청한다. 해당 서버에서 header와 payload를 이용해 secret key로 signature를 생성한다. 클라이언트까지 `access token`을 넘겨준다.
- 클라이언트는 authorization을 하고 싶을 때, 이 `access token`을 public key를 가지고 있는 서버에게 넘겨준다.
- 서버는 클라이언트에게 받은 `access token`을 header, payload, signature로 분류한 뒤, 자신의 public key로 signature를 복호화한다. header + payload와 복호화한 signature가 같은지 검증한다.

## blacklist
- 클라이언트가 로그아웃을 해서 더 이상 `refresh token`을 사용하지 않더라도 expiration time까지는 토큰이 유효하다. `refresh token`은 expiration time을 길게 잡기 때문에 위험하다. 중간에 토큰이 탈취돼 악용될 수도 있다.
- 실제로 별도의 설정을 하지 않고 expiration만 설정해놓으면 expiration time이 지나기 전에는 이전에 발급한 `refresh token`을 재사용할 수 있다.
- 따라서 expiration과 상관없이 토큰이 더 이상 valid 하지 않도록 하는 방법이 필요하다. 이게 바로 blacklist이다.
- 로그아웃 혹은 토큰이 탈취돼 invalid 해야할 때 blacklist api에 요청을 해서 invalid 시킨다.
- 단, `access token`은 expiration이 비교적 짧기 때문에 프레임워크에 따라서 invalid에 포함하지 않는 것 같기도 하다. 일단 drf에서는 안 된다.

## 참고
- [What Is JWT and Why Should You Use JWT](https://www.youtube.com/watch?v=7Q17ubqLfaM)
- https://meetup.toast.com/posts/239
- [JWT 구조 & JWT 인증 과정](https://velog.io/@zz3n/HTTP-%EC%9D%B8%EC%A6%9D-JWT)

## 쿠키와 보안 문제
- 쿠키 값은 임의로 변경할 수 있다.
- 쿠키에 보관된 정보는 훔쳐갈 수 있다.
  - 이 정보가 브라우저에도 보관되고 네트워크 요청마나 계속 클라이언트에서 서버로 전달된다.
  - 로컬 PC 혹은 네트워크 전송 구간에서 패킷이 털릴 수도 있다.
- 해커가 쿠키를 훔쳐가면 계속 악용할 수 있다.

### 대안
- 쿠키에 중요한 값을 노출하지 않아야한다.
- 사용자별로 예측 불가능한 임의의 토큰을 노출해야한다.
- 서버에서 토큰과 사용자 id를 매핑해서 인식한다. 그리고 서버에서 토큰을 관리한다.
- 토큰을 털어가도 시간이 지나면 사용할 수 없도록 만료 시간을 짧게 유지해야한다.
- 또는 해킹이 의심되는 경우 서버에서 해당 토큰을 강제로 제거하면 된다.
