# authtoken
- token으로 해도 request.user에 유저가 남는다.
- `urls.py`
    ```python
    from rest_framework.authtoken.views import obtain_auth_token

    urlpatterns = [
        url(r"^get-auth-token/", obtain_auth_token, name="get-auth-token"),
        url(r"^users/", ListUsersView.as_view())
    ]
    ```
- `views.py`
    ```python
    from rest_framework.permissions import AllowAny, IsAuthenticated

    class ListUsersView(ListAPIView):
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)
        serializer_class = RegisterSerializer

        def get(self, request, *args, **kwargs):
            print(request.user)
            return self.list(request, *args, **kwargs)
    ```

# simple jwt
- auth token과의 차이점은 다음과 같다.
  - [Django : DRF Token based Authentication VS JSON Web Token](https://stackoverflow.com/questions/31600497/django-drf-token-based-authentication-vs-json-web-token)

## authentication
- authentication은 `settings.AUTHENTICATION_BACKENDS`을 이용한다.

## setting
- [기본 setting](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)

## blacklist
- refresh token을 blacklist에 추가해 더 이상 사용하지 못하도록 한다.
- 유저 정보를 이용해 `access token`과 `refresh token`을 발급받을 때마다 `token_blacklist_outstandingtoken`라는 테이블에 `token`, `expires_at`, `user_id`, `jti`, `id`를 기록한다. 단, `refresh token`만 기록한다.
- blacklist api(직접 구현해야함)를 통해 `refresh token`을 blacklist에 등록할 때마다 `token_blacklist_blacklistedtoken`테이블에 `blacklisted_at`, `token_id`, `id`를 기록한다.
- `token_blacklist_blacklistedtoken`에 등록된 `refresh token`은 사용할 수 없다.
- 단, `access token`은 blacklist에 등록할 수 없다.
- blacklist에 등록된 `refresh token`을 이용해 발급받은 `access token`이라도 expiration까지는 사용할 수 있다.

### jti
- setting을 읽어보면 `jti`는 blacklist app에서 rovoked(취소된) token들을 알아보는데 사용한다고 나온다.
- 하지만 `token_blacklist_blacklistedtoken`에서 `token_id`를 foreign key로 사용하기 때문에 왜 `jti`가 필요한지 잘 몰랐다.
- `jti`는 `OutstandingToken`에서 unique한 필드로 등록돼있다.
  ```python
  class OutstandingToken(models.Model):
      jti = models.CharField(unique=True, max_length=255)
  ```
- 따라서 `OutstandingToken`을 얻을 때 lookup field로 사용하는 것이다. 아래는 `blacklist` 함수에서 `jti`로 `OutstandingToken`을 얻어서 `BlacklistedToken`을 생성하는 코드이다. 즉, blacklist에 등록할 때 해당 토큰을 찾기 위해 사용한다.
  ```python
  def blacklist(self):
        """
        Ensures this token is included in the outstanding token list and
        adds it to the blacklist.
        """
        jti = self.payload[api_settings.JTI_CLAIM]
        exp = self.payload['exp']

        # Ensure outstanding token exists with given jti
        token, _ = OutstandingToken.objects.get_or_create(
            jti=jti,
            defaults={
                'token': str(self),
                'expires_at': datetime_from_epoch(exp),
            },
        )

        return BlacklistedToken.objects.get_or_create(token=token)
  ```