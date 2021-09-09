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

# jwt
- auth token과의 차이점은 다음과 같다.
  - [Django : DRF Token based Authentication VS JSON Web Token](https://stackoverflow.com/questions/31600497/django-drf-token-based-authentication-vs-json-web-token)

## simple jwt
- [기본 setting](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html)